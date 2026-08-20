"""
Local multi-scenario tester for OsdagBridge short-span plate girder module.

No GitHub / no commit / no push. Writes evidence under OsdagBridge-Testing/.

Covers task.md:
  1. Basic + additional inputs, custom steel (girder/CB/ED) and custom deck
  2. Consecutive multi-run (>=3) via backend.reset() — same call as GUI Unlock
  3. Output dict vs entered values, component coverage, CAD DTO, structural plots
  4. Pass and fail cases with exact parameter combinations
"""
from __future__ import annotations

import json
import sys
import traceback
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
DICT_DIR = ROOT / "dictionaries"
CASE_DIR = ROOT / "test_cases"
OSI_DIR = ROOT / "osi_files"
SHOT_DIR = ROOT / "screenshots"
CAD_DIR = ROOT / "cad"

for d in (LOG_DIR, DICT_DIR, CASE_DIR, OSI_DIR, SHOT_DIR, CAD_DIR):
    d.mkdir(parents=True, exist_ok=True)

SRC = Path(__file__).resolve().parents[2] / "OsdagBridge" / "src"
if not SRC.exists():
    SRC = Path(__file__).resolve().parents[1].parent / "OsdagBridge" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from graphics_evidence import (  # noqa: E402
    capture_structural_plots,
    dto_to_jsonable,
    render_cad_schematic,
    write_json,
)


COMPARE_KEYS = [
    "geometry.span",
    "geometry.carriageway_width",
    "geometry.skew_angle",
    "geometry.include_median",
    "geometry.footpath",
    "geometry.design_mode",
    "material.girder",
    "material.cross_bracing",
    "material.end_diaphragm",
    "material.deck",
    "material.girder.fy",
    "material.girder.fu",
    "material.girder.e",
    "material.girder.density",
    "material.girder.g",
    "material.cross_bracing.fy",
    "material.cross_bracing.density",
    "material.end_diaphragm.fy",
    "material.end_diaphragm.density",
    "material.deck.fck",
    "material.deck.density",
    "typical_section.deck_thickness",
    "typical_section.wearing_course.density",
    "typical_section.wearing_course.thickness",
    "design_options.deck.top_clear_cover",
    "design_options.shear_studs.diameter",
    "design_options_cont.partial_factor.yielding_and_buckling.gamma_m0",
    "loading.live_load.eccentricity",
]

UTIL_KEYS = [
    "util.flexure",
    "util.shear",
    "util.interaction",
    "util.ltb",
    "util.long_trans_shear",
    "util.fatigue",
    "util.stress_limitation",
    "util.deflection_crack",
]

STEEL_DOCK_KEYS = [
    "steeldesign.details.grade_of_material",
    "steeldesign.details.section_type",
    "steeldesign.details.section_designation",
    "steeldesign.details.section_class",
    "steeldesign.details.total_depth",
    "steeldesign.details.web_thickness",
    "steeldesign.details.top_flange_width",
    "steeldesign.details.top_flange_thickness",
    "steeldesign.details.bottom_flange_width",
    "steeldesign.details.bottom_flange_thickness",
    "steeldesign.details.shear.diameter",
    "steeldesign.details.shear.height",
    "steeldesign.details.stiffener_summary.method",
    "steeldesign.details.stiffener_summary.end_count",
    "steeldesign.details.moment.mu_applied",
    "steeldesign.details.moment.md_capacity",
]

DECK_REPORT_KEYS = [
    "deck.report.span",
    "deck.report.fy",
    "deck.report.w_dl",
    "deck.report.m_uls_sag",
    "deck.report.punch_ok",
    "deck.report.as_req_bot",
]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _safe_json(obj):
    def default(o):
        try:
            if hasattr(o, "items"):
                return dict(o)
        except Exception:
            pass
        return str(o)

    return json.loads(json.dumps(obj, default=default))


def dump_dict(path: Path, data) -> None:
    path.write_text(json.dumps(_safe_json(data), indent=2, default=str), encoding="utf-8")


def build_base_input() -> dict:
    from osdagbridge.core.bridge_types.plate_girder.defaults import (
        BASIC_INPUT_DICT,
        solve_extend_basic_input_dict,
    )
    from osdagbridge.core.utils.common import (
        KEY_SPAN,
        KEY_CARRIAGEWAY_WIDTH,
        KEY_SKEW_ANGLE,
        KEY_INCLUDE_MEDIAN,
        KEY_FOOTPATH,
        KEY_DESIGN_MODE,
        KEY_PROJECT_LOCATION,
    )

    inp = dict(BASIC_INPUT_DICT)
    inp.update(
        {
            KEY_PROJECT_LOCATION: {
                "display_text": "Mumbai, Maharashtra, India",
                "city": "Mumbai",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 19.0760,
                "longitude": 72.8777,
            },
            KEY_SPAN: 30.0,
            KEY_CARRIAGEWAY_WIDTH: 7.5,
            KEY_SKEW_ANGLE: 0.0,
            KEY_INCLUDE_MEDIAN: "No",
            KEY_FOOTPATH: "None",
            KEY_DESIGN_MODE: "Optimized",
        }
    )
    solve_extend_basic_input_dict(inp)
    return inp


def _steel_subkeys(inp, prefix_fy, fy, fu, e, density, poisson=0.3):
    g = round(e / (2 * (1 + poisson)), 3)
    inp[prefix_fy] = fy
    # derive sibling keys from fy key stem
    stem = prefix_fy.rsplit(".fy", 1)[0]
    inp[f"{stem}.fu"] = fu
    inp[f"{stem}.e"] = e
    inp[f"{stem}.poisson"] = poisson
    inp[f"{stem}.density"] = density
    inp[f"{stem}.g"] = g
    inp[f"{stem}.thermal"] = 1.2e-5
    return g


def apply_custom_materials(
    inp: dict,
    steel_fy=350.0,
    steel_fu=490.0,
    steel_e=200.0,
    steel_density=78.5,
    deck_fck=40.0,
    deck_fctm=3.5,
    deck_ecm=33.0,
    deck_density=25.0,
    same_for_cb_ed=True,
) -> dict:
    from osdagbridge.core.utils.common import (
        KEY_GIRDER,
        KEY_CROSS_BRACING,
        KEY_END_DIAPHRAGM,
        KEY_DECK_CONCRETE_GRADE_BASIC,
        KEY_MATERIAL_GIRDER_FY,
        KEY_MATERIAL_DECK_FCK,
        KEY_MATERIAL_DECK_FCTM,
        KEY_MATERIAL_DECK_ECM,
        KEY_MATERIAL_DECK_DENSITY,
        KEY_MATERIAL_DECK_THERMAL,
        KEY_MATERIAL_CROSS_BRACING_FY,
        KEY_MATERIAL_END_DIAPHRAGM_FY,
    )

    steel_name = f"custom_steel_{int(steel_fy)}_{int(steel_fu)}"
    deck_name = f"custom_concrete_{int(deck_fck)}_{str(deck_fctm).replace('.', '_')}"
    inp[KEY_GIRDER] = steel_name
    inp[KEY_DECK_CONCRETE_GRADE_BASIC] = deck_name
    _steel_subkeys(inp, KEY_MATERIAL_GIRDER_FY, steel_fy, steel_fu, steel_e, steel_density)
    if same_for_cb_ed:
        inp[KEY_CROSS_BRACING] = steel_name
        inp[KEY_END_DIAPHRAGM] = steel_name
        _steel_subkeys(inp, KEY_MATERIAL_CROSS_BRACING_FY, steel_fy, steel_fu, steel_e, steel_density)
        _steel_subkeys(inp, KEY_MATERIAL_END_DIAPHRAGM_FY, steel_fy, steel_fu, steel_e, steel_density)
    inp[KEY_MATERIAL_DECK_FCK] = deck_fck
    inp[KEY_MATERIAL_DECK_FCTM] = deck_fctm
    inp[KEY_MATERIAL_DECK_ECM] = deck_ecm
    inp[KEY_MATERIAL_DECK_DENSITY] = deck_density
    inp[KEY_MATERIAL_DECK_THERMAL] = 1.0e-5
    return inp


def flatten_output(out: dict, prefix: str = "") -> dict:
    """Flatten nested bags such as deck_report_values so deck.report.* is visible."""
    flat = {}
    for k, v in (out or {}).items():
        sk = str(k)
        path = f"{prefix}.{sk}" if prefix else sk
        if isinstance(v, dict) and (
            sk in ("deck_report_values", "deck_design")
            or any(str(ik).startswith("deck.report.") for ik in v.keys())
        ):
            flat.update(flatten_output(v, ""))
            continue
        flat[path if prefix else sk] = v
    return flat


def slim_output(out: dict) -> dict:
    flat = flatten_output(out)
    keep = set(COMPARE_KEYS + UTIL_KEYS + STEEL_DOCK_KEYS + DECK_REPORT_KEYS)
    extra_prefixes = (
        "util.",
        "deck.report.",
        "deck_design_check",
        "steeldesign.details.",
        "geometry.",
        "material.",
        "typical_section.",
        "design_options.",
        "design_options_cont.",
        "loading.live_load.eccentricity",
    )
    slim = {}
    for k, v in flat.items():
        sk = str(k)
        if sk in keep or sk.startswith(extra_prefixes):
            if isinstance(v, (dict, list)) and sk.startswith("analysis"):
                continue
            slim[sk] = v
    if "deck_report_values" in out and isinstance(out["deck_report_values"], dict):
        slim["deck_report_values"] = out["deck_report_values"]
    return slim


def component_coverage(out: dict) -> dict:
    flat = flatten_output(out)
    keys = [str(k) for k in list(out.keys()) + list(flat.keys())]
    groups = {
        "girder_steel_design": [k for k in keys if k.startswith("steeldesign.")],
        "stiffeners": [k for k in keys if "stiffener" in k.lower()],
        "shear_connectors": [k for k in keys if "shear" in k.lower() and "steeldesign" in k],
        "deck": [k for k in keys if k.startswith("deck.")],
        "utilization": [k for k in keys if k.startswith("util.")],
        "cross_bracing_input_echo": [k for k in keys if "cross_bracing" in k],
        "end_diaphragm_input_echo": [k for k in keys if "end_diaphragm" in k],
        "typical_section": [k for k in keys if k.startswith("typical_section.")],
    }
    present = {name: sorted(vals)[:40] for name, vals in groups.items()}
    counts = {name: len(vals) for name, vals in groups.items()}
    missing_util = [k for k in UTIL_KEYS if k not in out]
    missing_steel = [k for k in STEEL_DOCK_KEYS if k not in out]
    missing_deck = [k for k in DECK_REPORT_KEYS if k not in out]
    util_vals = {}
    over_100 = []
    for k in UTIL_KEYS:
        if k in out:
            try:
                util_vals[k] = float(out[k])
                if float(out[k]) > 100.0:
                    over_100.append({k: float(out[k])})
            except Exception:
                util_vals[k] = out[k]
    return {
        "counts": counts,
        "sample_keys": present,
        "missing_util": missing_util,
        "missing_steel_dock": missing_steel,
        "missing_deck_report": missing_deck,
        "util_values": util_vals,
        "util_over_100": over_100,
    }


def dict_side_by_side(planned: dict, input_after: dict, output: dict) -> list[dict]:
    rows = []
    for k in COMPARE_KEYS:
        if k not in planned and k not in input_after and k not in output:
            continue
        pv, iv, ov = planned.get(k), input_after.get(k), output.get(k)
        match_in = pv == iv
        try:
            if pv is not None and iv is not None:
                match_in = abs(float(pv) - float(iv)) < 1e-6 or pv == iv
        except Exception:
            match_in = pv == iv
        match_out = ov == pv if ov is not None else None
        try:
            if pv is not None and ov is not None:
                match_out = abs(float(pv) - float(ov)) < 1e-6 or ov == pv
        except Exception:
            match_out = ov == pv
        rows.append(
            {
                "key": k,
                "planned_ui": pv,
                "input_dict": iv,
                "output_dict": ov,
                "input_matches_ui": match_in,
                "output_matches_ui": match_out,
            }
        )
    return rows


def _finalize_status(result: dict) -> None:
    if result.get("errors"):
        result["status"] = "FAIL"
    elif result.get("warnings"):
        result["status"] = "PASS_WITH_WARNINGS"
    else:
        result["status"] = "PASS"


def _merge_deck_report(out: dict, case_id: str) -> dict:
    bag = out.get("deck_report_values")
    if isinstance(bag, dict) and bag:
        dump_dict(DICT_DIR / f"{case_id}_deck_report_values.json", bag)
        for k, v in bag.items():
            if str(k).startswith("deck.report.") and k not in out:
                out[k] = v
    return bag if isinstance(bag, dict) else {}


def run_case(case_id: str, mutate_fn, notes: str = "", capture_graphics: bool = False) -> dict:
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.utils.common import (
        KEY_MATERIAL_GIRDER_DENSITY,
        KEY_MATERIAL_GIRDER_FY,
        KEY_GIRDER,
        KEY_SPAN,
        KEY_CARRIAGEWAY_WIDTH,
        KEY_MATERIAL_CROSS_BRACING_DENSITY,
        KEY_MATERIAL_END_DIAPHRAGM_DENSITY,
        KEY_DS_STUD_DIAMETER,
        KEY_DS_TOP_CLEAR_COVER,
        KEY_DO_GAMMA_M0,
        KEY_TS_DECK_THICKNESS,
        KEY_WC_DENSITY,
        KEY_WC_THICKNESS,
    )

    result = {
        "case_id": case_id,
        "notes": notes,
        "status": "UNKNOWN",
        "errors": [],
        "warnings": [],
        "checks": {},
        "started_at": _now(),
    }
    try:
        inp = mutate_fn(build_base_input())
        dump_dict(DICT_DIR / f"{case_id}_input_before.json", inp)
        try:
            import yaml

            osi_path = OSI_DIR / f"{case_id}.osi"
            with open(osi_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(inp, f, sort_keys=False)
            result["osi_file"] = str(osi_path)
        except Exception as e:
            result["errors"].append(f"OSI save failed: {e}")

        bridge = PlateGirderBridge()
        bridge.set_input(deepcopy(inp))
        after = dict(bridge.input_dict)
        dump_dict(DICT_DIR / f"{case_id}_input_after_set.json", after)
        rows = dict_side_by_side(inp, after, {})
        dump_dict(DICT_DIR / f"{case_id}_comparison.json", rows)
        result["checks"]["input_dict_mismatches"] = [r for r in rows if r["input_matches_ui"] is False]

        bridge.design()

        out = dict(bridge.get_results() or {})
        _merge_deck_report(out, case_id)
        dump_dict(DICT_DIR / f"{case_id}_output_slim.json", slim_output(out))
        rows = dict_side_by_side(inp, after, out)
        dump_dict(DICT_DIR / f"{case_id}_comparison.json", rows)

        custom_density = inp.get(KEY_MATERIAL_GIRDER_DENSITY)
        try:
            from osdagbridge.core.utils.common import (
                KEY_MATERIAL_DECK_DENSITY as _KEY_DECK_DENSITY,
                DEFAULT_CONCRETE_DENSITY,
            )

            mats = bridge._build_material_props()
            result["checks"]["custom_steel_density"] = {
                "ui_input_density": custom_density,
                "backend_rho": mats.steel_prop.rho,
                "steel_grade": inp.get(KEY_GIRDER),
                "fy_ui": inp.get(KEY_MATERIAL_GIRDER_FY),
                "fy_backend": mats.steel_prop.Fy,
                "cb_ui_density": inp.get(KEY_MATERIAL_CROSS_BRACING_DENSITY),
                "ed_ui_density": inp.get(KEY_MATERIAL_END_DIAPHRAGM_DENSITY),
                "cb_ui_fy": inp.get("material.cross_bracing.fy"),
                "ed_ui_fy": inp.get("material.end_diaphragm.fy"),
                "deck_ui_density": inp.get(_KEY_DECK_DENSITY),
                "concrete_prop_fields": list(getattr(mats.concrete_prop, "__dataclass_fields__", {})),
            }
            if custom_density not in (None, "") and str(inp.get(KEY_GIRDER, "")).startswith("custom_"):
                ui = float(custom_density)
                rho = float(mats.steel_prop.rho)
                expected_n = ui * 1000.0
                if abs(rho - expected_n) > 1.0 and abs(rho - ui) > 1.0:
                    result["warnings"].append(
                        f"Custom girder density ignored: UI={ui} vs backend rho={rho} (expected ~{expected_n} N/m3)"
                    )
                    result["checks"]["density_bug_confirmed"] = True
            deck_ui = inp.get(_KEY_DECK_DENSITY)
            if deck_ui not in (None, "") and str(inp.get("material.deck", "")).startswith("custom_"):
                try:
                    deck_ui_f = float(deck_ui)
                    has_rho = hasattr(mats.concrete_prop, "rho") or hasattr(mats.concrete_prop, "density")
                    result["checks"]["custom_deck_density"] = {
                        "ui_density": deck_ui_f,
                        "concrete_prop_has_density": bool(has_rho),
                        "dead_load_uses_default": DEFAULT_CONCRETE_DENSITY,
                        "add_dead_loads_passes_density": False,
                    }
                    if abs(deck_ui_f - float(DEFAULT_CONCRETE_DENSITY)) > 0.05 and not has_rho:
                        result["warnings"].append(
                            f"Custom deck density ignored: UI={deck_ui_f} kN/m3; "
                            f"ConcreteProperties has no density field; add_dead_loads() calls "
                            f"create_deck_load() without density (default {DEFAULT_CONCRETE_DENSITY} kN/m3)"
                        )
                        result["checks"]["deck_density_bug_confirmed"] = True
                except (TypeError, ValueError):
                    pass
            cb_fy = inp.get("material.cross_bracing.fy")
            ed_fy = inp.get("material.end_diaphragm.fy")
            g_fy = inp.get(KEY_MATERIAL_GIRDER_FY)
            if cb_fy not in (None, "") and g_fy not in (None, "") and float(cb_fy) != float(g_fy):
                result["warnings"].append(
                    f"Distinct CB fy={cb_fy} stored but _build_material_props uses girder fy={g_fy} only"
                )
            if ed_fy not in (None, "") and g_fy not in (None, "") and float(ed_fy) != float(g_fy):
                result["warnings"].append(
                    f"Distinct ED fy={ed_fy} stored but _build_material_props uses girder fy={g_fy} only"
                )
        except Exception as e:
            result["errors"].append(f"material props check failed: {e}")

        cad_ok = False
        try:
            cad = bridge.get_3d_cad_parameters()
            cad_ok = cad is not None
            result["checks"]["cad_params_generated"] = cad_ok
            result["checks"]["cad_type"] = type(cad).__name__
            cad_j = dto_to_jsonable(cad)
            dump_dict(CAD_DIR / f"{case_id}_cad_dto.json", cad_j)
            if cad_ok:
                render_cad_schematic(cad, SHOT_DIR / f"{case_id}_cad_schematic.png", title=f"{case_id} CAD")
                result["checks"]["cad_span_mm"] = cad_j.get("span_length_L")
                result["checks"]["cad_num_girders"] = cad_j.get("num_girders")
                result["checks"]["cad_deck_thickness"] = cad_j.get("deck_thickness")
                result["checks"]["cad_skew"] = cad_j.get("skew_angle")
        except Exception as e:
            result["checks"]["cad_params_generated"] = False
            result["errors"].append(f"CAD params failed: {e}")

        if capture_graphics:
            plots = capture_structural_plots(bridge, SHOT_DIR, case_id)
            result["checks"]["plots"] = plots
            if not plots.get("ok"):
                result["warnings"].append(f"plot capture incomplete: {plots.get('errors')}")

        cov = component_coverage(out)
        result["checks"]["coverage"] = {
            "counts": cov["counts"],
            "missing_util": cov["missing_util"],
            "missing_steel_dock": cov["missing_steel_dock"],
            "missing_deck_report": cov["missing_deck_report"],
            "util_values": cov["util_values"],
            "util_over_100": cov["util_over_100"],
        }
        if cov["util_over_100"]:
            result["warnings"].append(f"Utilization > 100%: {cov['util_over_100']}")
        if cov["missing_deck_report"]:
            result["warnings"].append(
                f"Deck report keys missing from output dictionary: {cov['missing_deck_report']}"
            )
        uv = cov.get("util_values") or {}
        try:
            flex = float(uv.get("util.flexure") or 0)
            shear = float(uv.get("util.shear") or 0)
            fat = float(uv.get("util.fatigue") or 0)
            ltb = float(uv.get("util.ltb") or 0)
            if flex == 0.0 and shear == 0.0 and fat == 0.0 and ltb > 0:
                result["warnings"].append(
                    "util.flexure/shear/fatigue are 0.0 while util.ltb is non-zero — "
                    "store_design_results() writes missing category_urs as 0.0, so the dock "
                    "cannot distinguish a genuine 0% check from a skipped check"
                )
        except (TypeError, ValueError):
            pass
        result["checks"]["span_in_output"] = out.get(KEY_SPAN)
        result["checks"]["cw_in_output"] = out.get(KEY_CARRIAGEWAY_WIDTH)
        result["checks"]["output_key_count"] = len(out)
        result["checks"]["additional_echo"] = {
            "deck_thickness_out": out.get(KEY_TS_DECK_THICKNESS, after.get(KEY_TS_DECK_THICKNESS)),
            "wc_density_out": out.get(KEY_WC_DENSITY, after.get(KEY_WC_DENSITY)),
            "wc_thickness_out": out.get(KEY_WC_THICKNESS, after.get(KEY_WC_THICKNESS)),
            "stud_dia_out": out.get("steeldesign.details.shear.diameter"),
            "stud_dia_in": inp.get(KEY_DS_STUD_DIAMETER),
            "cover_in": inp.get(KEY_DS_TOP_CLEAR_COVER),
            "gamma_m0_in": inp.get(KEY_DO_GAMMA_M0),
        }

        mismatches = [r for r in rows if r["input_matches_ui"] is False]
        result["checks"]["input_dict_mismatches"] = mismatches
        if mismatches:
            result["warnings"].append(f"{len(mismatches)} input_dict key(s) differ from planned UI values")

        _finalize_status(result)
    except Exception as e:
        result["status"] = "FAIL"
        result["errors"].append(str(e))
        result["traceback"] = traceback.format_exc()

    result["finished_at"] = _now()
    dump_dict(LOG_DIR / f"{case_id}_result.json", result)
    print(f"[{result['status']}] {case_id}  errors={result['errors'][:1]}", flush=True)
    return result


def run_multi_run(case_id: str = "TC_MULTI_01") -> dict:
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.utils.common import KEY_SPAN, KEY_CARRIAGEWAY_WIDTH, KEY_SKEW_ANGLE

    summary = {"case_id": case_id, "runs": [], "status": "UNKNOWN", "started_at": _now(), "notes": "GUI Unlock == backend.reset()"}
    spans = [25.0, 30.0, 35.0]
    cws = [7.5, 8.5, 9.5]
    skews = [0.0, 5.0, 10.0]
    try:
        bridge = PlateGirderBridge()
        prev_span = None
        prev_cad_span = None
        for i, (span, cw, skew) in enumerate(zip(spans, cws, skews), start=1):
            run_id = f"{case_id}_run{i}"
            entry = {"run": i, "span": span, "cw": cw, "skew": skew}

            inp = build_base_input()
            inp[KEY_SPAN] = span
            inp[KEY_CARRIAGEWAY_WIDTH] = cw
            inp[KEY_SKEW_ANGLE] = skew
            solve_extend_basic_input_dict(inp)
            apply_custom_materials(inp)

            if i > 1:
                bridge.reset()
                entry["after_reset_output_empty"] = (
                    bridge.output_dict is None or len(dict(bridge.output_dict or {})) == 0
                )

            bridge.set_input(deepcopy(inp))
            bridge.design()
            out = dict(bridge.get_results() or {})
            dump_dict(DICT_DIR / f"{run_id}_output_slim.json", slim_output(out))

            entry["output_span"] = out.get(KEY_SPAN)
            entry["output_cw"] = out.get(KEY_CARRIAGEWAY_WIDTH)
            entry["output_skew"] = out.get(KEY_SKEW_ANGLE)
            entry["stale_span_detected"] = (
                prev_span is not None and out.get(KEY_SPAN) == prev_span and span != prev_span
            )
            entry["span_matches"] = out.get(KEY_SPAN) == span
            entry["cw_matches"] = out.get(KEY_CARRIAGEWAY_WIDTH) == cw
            try:
                cad = bridge.get_3d_cad_parameters()
                entry["cad_ok"] = cad is not None
                cad_span = getattr(cad, "span_length_L", None)
                entry["cad_span_mm"] = cad_span
                entry["cad_stale"] = (
                    prev_cad_span is not None and cad_span == prev_cad_span and abs(span * 1000 - float(cad_span or 0)) > 1
                )
                prev_cad_span = cad_span
                render_cad_schematic(cad, SHOT_DIR / f"{run_id}_cad_schematic.png", title=f"Multi-run {i} CAD")
            except Exception as e:
                entry["cad_ok"] = False
                entry["cad_error"] = str(e)

            if i == 3:
                plots = capture_structural_plots(bridge, SHOT_DIR, run_id)
                entry["plots"] = {"ok": plots.get("ok"), "files": plots.get("files"), "errors": plots.get("errors")}

            prev_span = span
            summary["runs"].append(entry)
            print(f"[MULTI] run {i} span={span} out={entry.get('output_span')} cad={entry.get('cad_ok')}", flush=True)

        stale = any(r.get("stale_span_detected") or r.get("cad_stale") for r in summary["runs"])
        mismatches = [r for r in summary["runs"] if not (r.get("span_matches") and r.get("cw_matches"))]
        summary["status"] = "FAIL" if (stale or mismatches) else "PASS"
        summary["stale_data_found"] = stale
        summary["mismatch_runs"] = mismatches
    except Exception as e:
        summary["status"] = "FAIL"
        summary["error"] = str(e)
        summary["traceback"] = traceback.format_exc()

    summary["finished_at"] = _now()
    dump_dict(LOG_DIR / f"{case_id}_result.json", summary)
    return summary


def _mut_geo_skew(inp):
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict
    from osdagbridge.core.utils.common import (
        KEY_SKEW_ANGLE,
        KEY_FOOTPATH,
        KEY_INCLUDE_MEDIAN,
        KEY_SPAN,
        KEY_CARRIAGEWAY_WIDTH,
    )

    inp[KEY_SPAN] = 28.0
    inp[KEY_CARRIAGEWAY_WIDTH] = 10.0
    inp[KEY_SKEW_ANGLE] = 12.0
    inp[KEY_FOOTPATH] = "Both"
    inp[KEY_INCLUDE_MEDIAN] = "Yes"
    solve_extend_basic_input_dict(inp)
    return apply_custom_materials(inp, steel_fy=300, steel_fu=440, steel_density=78.5)


def _mut_short(inp):
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict
    from osdagbridge.core.utils.common import KEY_SPAN, KEY_CARRIAGEWAY_WIDTH

    inp[KEY_SPAN] = 20.0
    inp[KEY_CARRIAGEWAY_WIDTH] = 6.0
    solve_extend_basic_input_dict(inp)
    return inp


def _mut_long(inp):
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict
    from osdagbridge.core.utils.common import KEY_SPAN, KEY_CARRIAGEWAY_WIDTH

    inp[KEY_SPAN] = 45.0
    inp[KEY_CARRIAGEWAY_WIDTH] = 12.0
    solve_extend_basic_input_dict(inp)
    return apply_custom_materials(inp)


def _mut_additional(inp):
    """Non-default additional geometry, wearing course, design options, loading."""
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict
    from osdagbridge.core.utils.common import (
        KEY_TS_DECK_THICKNESS,
        KEY_WC_DENSITY,
        KEY_WC_THICKNESS,
        KEY_WC_MATERIAL,
        KEY_DS_TOP_CLEAR_COVER,
        KEY_DS_BOTTOM_CLEAR_COVER,
        KEY_DS_STUD_DIAMETER,
        KEY_DS_STUD_HEIGHT,
        KEY_DO_GAMMA_M0,
        KEY_DO_GAMMA_M1,
        KEY_LL_ECCENTRICITY,
        KEY_CB_DENSITY,
    )

    apply_custom_materials(inp, steel_fy=350, steel_fu=490, steel_density=78.5, deck_density=26.0)
    solve_extend_basic_input_dict(inp)
    inp[KEY_TS_DECK_THICKNESS] = 280.0
    inp[KEY_WC_MATERIAL] = "Concrete"
    inp[KEY_WC_DENSITY] = 22.0
    inp[KEY_WC_THICKNESS] = 80.0
    inp[KEY_DS_TOP_CLEAR_COVER] = "40"
    inp[KEY_DS_BOTTOM_CLEAR_COVER] = "45"
    inp[KEY_DS_STUD_DIAMETER] = "22"
    inp[KEY_DS_STUD_HEIGHT] = "125"
    inp[KEY_DO_GAMMA_M0] = "1.15"
    inp[KEY_DO_GAMMA_M1] = "1.30"
    inp[KEY_LL_ECCENTRICITY] = 1.5
    if KEY_CB_DENSITY in inp:
        inp[KEY_CB_DENSITY] = 26.0
    return inp


def _mut_cb_ed_distinct(inp):
    from osdagbridge.core.utils.common import (
        KEY_CROSS_BRACING,
        KEY_END_DIAPHRAGM,
        KEY_MATERIAL_CROSS_BRACING_FY,
        KEY_MATERIAL_END_DIAPHRAGM_FY,
    )

    apply_custom_materials(inp, steel_fy=350, steel_fu=490, steel_density=80.0, same_for_cb_ed=False)
    inp[KEY_CROSS_BRACING] = "custom_steel_250_410"
    inp[KEY_END_DIAPHRAGM] = "custom_steel_280_440"
    _steel_subkeys(inp, KEY_MATERIAL_CROSS_BRACING_FY, 250, 410, 200, 70.0)
    _steel_subkeys(inp, KEY_MATERIAL_END_DIAPHRAGM_FY, 280, 440, 200, 75.0)
    return inp


def _prime_db_material_subkeys(inp: dict) -> dict:
    """Write the material sub-keys the GUI dialog would prime for a DB grade.

    designer.py reads Gs and deck fck/fctm/Ecm from input_dict, not from SQLite.
    BASIC_INPUT_DICT does not include those keys (TC01/TC04). This helper fills
    them from the same DB lookup the backend already uses for fy/E.
    """
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.utils.common import (
        KEY_GIRDER,
        KEY_DECK_CONCRETE_GRADE_BASIC,
        KEY_MATERIAL_GIRDER_E,
        KEY_MATERIAL_GIRDER_POISSON,
        KEY_MATERIAL_GIRDER_G,
        KEY_MATERIAL_DECK_FCK,
        KEY_MATERIAL_DECK_FCTM,
        KEY_MATERIAL_DECK_ECM,
    )

    probe = PlateGirderBridge()
    steel = str(inp.get(KEY_GIRDER) or "E 350A").strip()
    deck = str(inp.get(KEY_DECK_CONCRETE_GRADE_BASIC) or "M40").strip()
    e_pa = probe._lookup_material(steel, "Modulus of Elasticity")
    nu = probe._lookup_material(steel, "Poisson's Ratio")
    e_gpa = (float(e_pa) / 1e9) if e_pa not in (None, "") else 200.0
    nu = float(nu) if nu not in (None, "") else 0.3
    inp[KEY_MATERIAL_GIRDER_E] = e_gpa
    inp[KEY_MATERIAL_GIRDER_POISSON] = nu
    inp[KEY_MATERIAL_GIRDER_G] = round(e_gpa / (2.0 * (1.0 + nu)), 3)
    fck = probe._lookup_material(deck, "fck")
    fctm = probe._lookup_material(deck, "fctm")
    ecm = probe._lookup_material(deck, "Ecm")
    if fck is not None:
        inp[KEY_MATERIAL_DECK_FCK] = fck
    if fctm is not None:
        inp[KEY_MATERIAL_DECK_FCTM] = fctm
    if ecm is not None:
        inp[KEY_MATERIAL_DECK_ECM] = ecm
    return inp


def _mut_db_grade_with_gs(inp):
    """Same geometry as TC01, with GUI-equivalent DB material sub-keys (Gs + deck fck)."""
    return _prime_db_material_subkeys(inp)


def _mut_custom_section_stiffeners(inp):
    """Custom design type: explicit girder plate sizes and non-default stiffeners."""
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict
    from osdagbridge.core.utils.common import (
        KEY_DESIGN_MODE,
        KEY_MP_GIRDER_DEPTH,
        KEY_MP_GIRDER_WEB_DEPTH,
        KEY_MP_GIRDER_TOP_FLANGE_WIDTH,
        KEY_MP_GIRDER_TOP_FLANGE_THICKNESS,
        KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH,
        KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS,
        KEY_MP_GIRDER_WEB_THICKNESS,
        KEY_MP_STIFFENER_NO_BEARING_STIFFENERS,
        KEY_MP_STIFFENER_INTERMEDIATE,
        KEY_MP_STIFFENER_BEARING_THICKNESS,
        KEY_TS_NO_OF_GIRDERS,
    )

    apply_custom_materials(inp, steel_fy=350, steel_fu=490, steel_density=78.5, deck_density=26.0)
    inp[KEY_DESIGN_MODE] = "Custom"
    solve_extend_basic_input_dict(inp)
    dims = {
        KEY_MP_GIRDER_DEPTH: 1400.0,
        KEY_MP_GIRDER_WEB_DEPTH: 1350.0,
        KEY_MP_GIRDER_TOP_FLANGE_WIDTH: 450.0,
        KEY_MP_GIRDER_TOP_FLANGE_THICKNESS: 20.0,
        KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH: 520.0,
        KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS: 25.0,
        KEY_MP_GIRDER_WEB_THICKNESS: 12.0,
    }
    try:
        count = int(float(inp.get(KEY_TS_NO_OF_GIRDERS) or 4))
    except (TypeError, ValueError):
        count = 4
    for base, val in dims.items():
        inp[base] = val
        for gi in range(1, count + 1):
            inp[f"{base}.G{gi}.M1"] = val
    stiff = {
        KEY_MP_STIFFENER_NO_BEARING_STIFFENERS: "2",
        KEY_MP_STIFFENER_INTERMEDIATE: "Yes",
        KEY_MP_STIFFENER_BEARING_THICKNESS: "16",
    }
    for base, val in stiff.items():
        inp[base] = val
        for gi in range(1, count + 1):
            inp[f"{base}.G{gi}.M1"] = val
    return inp


def run_osi_roundtrip(case_id: str = "TC10_osi_roundtrip") -> dict:
    """Save OSI, load into a new backend, confirm custom keys survive set_input + design."""
    import yaml
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.utils.common import (
        KEY_MATERIAL_GIRDER_DENSITY,
        KEY_MATERIAL_GIRDER_FY,
        KEY_GIRDER,
        KEY_SPAN,
    )

    summary = {
        "case_id": case_id,
        "notes": "API OSI round-trip: yaml dump → new PlateGirderBridge.set_input → design",
        "status": "UNKNOWN",
        "errors": [],
        "warnings": [],
        "checks": {},
        "started_at": _now(),
    }
    try:
        inp = apply_custom_materials(
            build_base_input(), steel_fy=350, steel_fu=490, steel_density=80.0, deck_density=26.0
        )
        osi_path = OSI_DIR / f"{case_id}.osi"
        with open(osi_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(inp, f, sort_keys=False)
        loaded = yaml.safe_load(osi_path.read_text(encoding="utf-8"))
        dump_dict(DICT_DIR / f"{case_id}_input_before.json", loaded)

        bridge = PlateGirderBridge()
        bridge.set_input(deepcopy(loaded))
        after = dict(bridge.input_dict)
        dump_dict(DICT_DIR / f"{case_id}_input_after_set.json", after)
        rows = dict_side_by_side(inp, after, {})
        dump_dict(DICT_DIR / f"{case_id}_comparison.json", rows)

        summary["checks"]["osi_file"] = str(osi_path)
        summary["checks"]["grade_after_load"] = after.get(KEY_GIRDER)
        summary["checks"]["fy_after_load"] = after.get(KEY_MATERIAL_GIRDER_FY)
        summary["checks"]["density_after_load"] = after.get(KEY_MATERIAL_GIRDER_DENSITY)
        summary["checks"]["span_after_load"] = after.get(KEY_SPAN)
        lost = []
        for k in ("material.girder.fy", "material.girder.density", "material.deck.density", KEY_GIRDER):
            if inp.get(k) != after.get(k):
                lost.append({"key": k, "saved": inp.get(k), "loaded": after.get(k)})
        summary["checks"]["keys_lost_on_load"] = lost
        if lost:
            summary["warnings"].append(f"OSI round-trip lost {len(lost)} custom key(s) at API set_input")

        bridge.design()
        out = dict(bridge.get_results() or {})
        _merge_deck_report(out, case_id)
        dump_dict(DICT_DIR / f"{case_id}_output_slim.json", slim_output(out))
        rows = dict_side_by_side(inp, after, out)
        dump_dict(DICT_DIR / f"{case_id}_comparison.json", rows)
        summary["checks"]["output_span"] = out.get(KEY_SPAN)
        summary["checks"]["output_key_count"] = len(out)
        summary["checks"]["cad_ok"] = False
        try:
            cad = bridge.get_3d_cad_parameters()
            summary["checks"]["cad_ok"] = cad is not None
            if cad is not None:
                render_cad_schematic(cad, SHOT_DIR / f"{case_id}_cad_schematic.png", title=f"{case_id} CAD")
        except Exception as e:
            summary["warnings"].append(f"CAD after OSI load: {e}")
        summary["warnings"].append(
            "GUI-only: populate_from_dict() does not rebuild InputDock._material_custom_fields; "
            "see issues/BUG_osi_custom_material_map_not_restored.md"
        )
        _finalize_status(summary)
    except Exception as e:
        summary["status"] = "FAIL"
        summary["errors"].append(str(e))
        summary["traceback"] = traceback.format_exc()

    summary["finished_at"] = _now()
    dump_dict(LOG_DIR / f"{case_id}_result.json", summary)
    print(f"[{summary['status']}] {case_id}  errors={summary['errors'][:1]}", flush=True)
    return summary


def write_markdown(cases: list[dict], overview: dict) -> None:
    lines = [
        "# Test Case Log — OsdagBridge Short-Span Steel Girder Module",
        "",
        "**Tester:** Harshdeep Singh  ",
        "**Module:** Plate Girder / Short-span steel girder bridge  ",
        "**Source under test:** OsdagBridge clone (`dev` branch)  ",
        "**Method:** Programmatic API `PlateGirderBridge.set_input()` → `design()`, plus off-screen plot/CAD capture and live GUI screencast.  ",
        "**GUI Unlock analogue:** `input_dock` Unlock calls `backend.reset()` — exercised in TC_MULTI_01.  ",
        "**Issue drafts:** `issues/*.md` (search upstream issues before filing).",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total cases | {overview.get('total')} |",
        f"| Passed | {overview.get('passed')} |",
        f"| Failed | {overview.get('failed')} |",
        f"| Generated | {overview.get('generated_at')} |",
        "",
    ]
    for c in cases:
        cid = c.get("case_id")
        lines += [f"## {cid} — {c.get('status')}", "", f"{c.get('notes') or c.get('error') or ''}", ""]
        if c.get("errors"):
            lines += [f"**Errors:** `{c.get('errors')}`", ""]
        if c.get("warnings"):
            lines += ["**Warnings / defects observed:**"] + [f"- {w}" for w in c["warnings"]] + [""]
        ch = c.get("checks") or {}
        dens = ch.get("custom_steel_density")
        if dens:
            lines += [
                "| Check | Value |",
                "|-------|-------|",
                f"| UI girder density | {dens.get('ui_input_density')} |",
                f"| Backend rho | {dens.get('backend_rho')} |",
                f"| CAD generated | {ch.get('cad_params_generated')} |",
                f"| Output keys | {ch.get('output_key_count')} |",
                "",
            ]
        cov = ch.get("coverage") or {}
        if cov.get("util_values"):
            lines.append("Utilization (output dock):")
            lines.append("")
            lines.append("| Key | Value |")
            lines.append("|-----|-------|")
            for k, v in cov["util_values"].items():
                lines.append(f"| `{k}` | {v} |")
            lines.append("")
        if c.get("runs"):
            lines += [
                "| Run | Span | CW | Skew | Output span | CAD span mm | Stale? |",
                "|-----|------|----|------|-------------|-------------|--------|",
            ]
            for r in c["runs"]:
                lines.append(
                    f"| {r.get('run')} | {r.get('span')} | {r.get('cw')} | {r.get('skew')} | "
                    f"{r.get('output_span')} | {r.get('cad_span_mm')} | {r.get('stale_span_detected')} |"
                )
            lines.append("")
        tb = c.get("traceback")
        if tb:
            snippet = "\n".join(tb.strip().splitlines()[-8:])
            lines += ["**Traceback (last lines):**", "", "```", snippet, "```", ""]
        lines.append("---")
        lines.append("")

    lines += [
        "## Defects discovered (drafts in `issues/` — file on the upstream repo at submission)",
        "",
        "1. Custom steel density ignored — `issues/BUG_custom_steel_density_ignored.md`",
        "2. Custom deck density ignored — `issues/BUG_custom_deck_density_ignored.md`",
        "3. OSI custom material map not restored (GUI) — `issues/BUG_osi_custom_material_map_not_restored.md`",
        "4. DB grade E 350A missing Gs — `issues/BUG_e350a_missing_gs.md`",
        "5. CB/ED custom materials collapse to girder props — `issues/BUG_cross_bracing_end_diaphragm_custom_density_same.md`",
        "6. Fatigue utilization can exceed 100% while design() still completes — `issues/BUG_fatigue_util_exceeds_100.md`",
        "7. Missing DCR categories written as 0.0 on the output dock — `issues/BUG_missing_dcr_written_as_zero.md`",
        "",
    ]
    (CASE_DIR / "TEST_CASE_LOG.md").write_text("\n".join(lines), encoding="utf-8")

    # Dictionary comparison markdown
    md = [
        "# Side-by-side: Planned UI inputs vs Input/Output dictionaries",
        "",
        "Generated from `dictionaries/*_comparison.json` after local design runs.",
        "",
    ]
    for path in sorted(DICT_DIR.glob("*_comparison.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        md += [f"## {path.stem}", "", "| Key | Planned / UI | input_dict | output_dict | In match | Out match |",
               "|-----|---------------|------------|-------------|----------|-----------|"]
        for r in rows:
            md.append(
                f"| `{r['key']}` | {r['planned_ui']} | {r['input_dict']} | {r['output_dict']} | "
                f"{r['input_matches_ui']} | {r['output_matches_ui']} |"
            )
        md.append("")
    for path in sorted(DICT_DIR.glob("*_deck_report_values.json")):
        bag = json.loads(path.read_text(encoding="utf-8"))
        md += [
            f"## {path.stem} — nested `deck_report_values` vs design-report chapter",
            "",
            "| Key | Value |",
            "|-----|-------|",
        ]
        for k in (
            "deck.report.span",
            "deck.report.fy",
            "deck.report.w_dl",
            "deck.report.m_uls_sag",
            "deck.report.as_req_bot",
            "deck.report.punch_ok",
            "deck.report.shear_ok",
        ):
            if k in bag:
                md.append(f"| `{k}` | {bag.get(k)} |")
        md.append("")
    (CASE_DIR / "DICTIONARY_COMPARISON.md").write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    cases = []
    cases.append(
        run_case(
            "TC01_basic_optimized",
            lambda inp: inp,
            "Basic optimized geometry span=30 m, CW=7.5 m, DB default materials (E 350A / M40)",
        )
    )
    cases.append(
        run_case(
            "TC02_custom_materials",
            lambda inp: apply_custom_materials(
                inp, steel_fy=350, steel_fu=490, steel_density=80.0, deck_fck=40, deck_density=26.0
            ),
            "Custom steel fy=350 fu=490 density=80 and custom M40-like deck density=26",
            capture_graphics=True,
        )
    )
    cases.append(run_case("TC03_skew_footpath_median", _mut_geo_skew, "Skew 12°, footpath both, median yes, custom steel fy=300"))
    cases.append(run_case("TC04_span_min_boundary", _mut_short, "Minimum span 20 m, CW=6 m, DB defaults"))
    cases.append(run_case("TC05_span_max_boundary", _mut_long, "Maximum span 45 m, CW=12 m, custom materials"))
    cases.append(
        run_case(
            "TC06_additional_inputs",
            _mut_additional,
            "Additional inputs: deck t=280 mm, wearing 22 kN/m3 / 80 mm, covers 40/45, stud 22x125, gamma_m0=1.15, ecc=1.5",
            capture_graphics=True,
        )
    )
    cases.append(
        run_case(
            "TC07_distinct_cb_ed_materials",
            _mut_cb_ed_distinct,
            "Distinct custom grades: girder 350/490 d=80, CB 250/410 d=70, ED 280/440 d=75",
        )
    )
    cases.append(
        run_case(
            "TC08_db_grade_with_gs",
            _mut_db_grade_with_gs,
            "DB E 350A / M40 with GUI-equivalent Gs + deck fck/fctm/Ecm primed from SQLite",
            capture_graphics=True,
        )
    )
    cases.append(
        run_case(
            "TC09_custom_section_stiffeners",
            _mut_custom_section_stiffeners,
            "Design Type=Custom; girder 1400×450×20 / 520×25 / tw=12; bearing stiffeners=2; intermediate=Yes",
            capture_graphics=True,
        )
    )
    cases.append(run_osi_roundtrip("TC10_osi_roundtrip"))
    multi = run_multi_run("TC_MULTI_01")
    cases.append(multi)

    overview = {
        "generated_at": _now(),
        "total": len(cases),
        "passed": sum(1 for c in cases if str(c.get("status", "")).startswith("PASS")),
        "failed": sum(1 for c in cases if c.get("status") == "FAIL"),
        "cases": [
            {
                "case_id": c.get("case_id"),
                "status": c.get("status"),
                "errors": c.get("errors") or c.get("error"),
                "warnings": c.get("warnings"),
            }
            for c in cases
        ],
    }
    dump_dict(LOG_DIR / "test_overview.json", overview)
    dump_dict(CASE_DIR / "executed_cases.json", overview)
    write_markdown(cases, overview)
    print(json.dumps(overview, indent=2, default=str), flush=True)
    print("SUITE_COMPLETE", flush=True)
    return 0 if overview["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
