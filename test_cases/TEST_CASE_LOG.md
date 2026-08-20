# Test Case Log — OsdagBridge Short-Span Steel Girder Module

**Tester:** Harshdeep Singh  
**Module:** Plate Girder / Short-span steel girder bridge  
**Source under test:** OsdagBridge clone (`dev` branch)  
**Method:** Programmatic API `PlateGirderBridge.set_input()` → `design()`, plus off-screen plot/CAD capture and live GUI screencast.  
**GUI Unlock analogue:** `input_dock` Unlock calls `backend.reset()` — exercised in TC_MULTI_01.  
**Issue drafts:** `issues/*.md` (search upstream issues before filing).

---

## Summary

| Metric | Value |
|--------|-------|
| Total cases | 11 |
| Passed | 9 |
| Failed | 2 |
| Generated | 20260819T131449Z |

## TC01_basic_optimized — FAIL

Basic optimized geometry span=30 m, CW=7.5 m, DB default materials (E 350A / M40)

**Errors:** `["Gs (shear modulus) is not set for grade 'E 350A'. Populate it in the material database before running the design check."]`

**Traceback (last lines):**

```
    _, engine, design_results = run_design_check(
                                ^^^^^^^^^^^^^^^^^
  File "osdagbridge/src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 3235, in run_design_check
    config = BridgeConfig.from_plate_girder_bridge(plate_girder_bridge)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "osdagbridge/src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 311, in from_plate_girder_bridge
    raise ValueError(
ValueError: Gs (shear modulus) is not set for grade 'E 350A'. Populate it in the material database before running the design check.
```

---

## TC02_custom_materials — PASS_WITH_WARNINGS

Custom steel fy=350 fu=490 density=80 and custom M40-like deck density=26

**Warnings / defects observed:**
- Custom girder density ignored: UI=80.0 vs backend rho=78500.0 (expected ~80000.0 N/m3)
- Custom deck density ignored: UI=26.0 kN/m3; ConcreteProperties has no density field; add_dead_loads() calls create_deck_load() without density (default 25.0 kN/m3)
- Utilization > 100%: [{'util.fatigue': 157.26}]

| Check | Value |
|-------|-------|
| UI girder density | 80.0 |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1118 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 19.509999999999998 |
| `util.shear` | 39.910000000000004 |
| `util.interaction` | 19.66 |
| `util.ltb` | 22.81 |
| `util.long_trans_shear` | 19.82 |
| `util.fatigue` | 157.26 |
| `util.stress_limitation` | 24.87 |
| `util.deflection_crack` | 45.78 |

---

## TC03_skew_footpath_median — PASS_WITH_WARNINGS

Skew 12°, footpath both, median yes, custom steel fy=300

**Warnings / defects observed:**
- util.flexure/shear/fatigue are 0.0 while util.ltb is non-zero — store_design_results() writes missing category_urs as 0.0, so the dock cannot distinguish a genuine 0% check from a skipped check

| Check | Value |
|-------|-------|
| UI girder density | 78.5 |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1065 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 0.0 |
| `util.shear` | 0.0 |
| `util.interaction` | 0.0 |
| `util.ltb` | 20.44 |
| `util.long_trans_shear` | 23.89 |
| `util.fatigue` | 0.0 |
| `util.stress_limitation` | 0.0 |
| `util.deflection_crack` | 0.0 |

---

## TC04_span_min_boundary — FAIL

Minimum span 20 m, CW=6 m, DB defaults

**Errors:** `["Gs (shear modulus) is not set for grade 'E 350A'. Populate it in the material database before running the design check."]`

**Traceback (last lines):**

```
    _, engine, design_results = run_design_check(
                                ^^^^^^^^^^^^^^^^^
  File "osdagbridge/src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 3235, in run_design_check
    config = BridgeConfig.from_plate_girder_bridge(plate_girder_bridge)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "osdagbridge/src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 311, in from_plate_girder_bridge
    raise ValueError(
ValueError: Gs (shear modulus) is not set for grade 'E 350A'. Populate it in the material database before running the design check.
```

---

## TC05_span_max_boundary — PASS_WITH_WARNINGS

Maximum span 45 m, CW=12 m, custom materials

**Warnings / defects observed:**
- Utilization > 100%: [{'util.fatigue': 160.14}]

| Check | Value |
|-------|-------|
| UI girder density | 78.5 |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1118 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 19.040000000000003 |
| `util.shear` | 57.379999999999995 |
| `util.interaction` | 19.35 |
| `util.ltb` | 36.71 |
| `util.long_trans_shear` | 20.29 |
| `util.fatigue` | 160.14 |
| `util.stress_limitation` | 26.810000000000002 |
| `util.deflection_crack` | 47.92 |

---

## TC06_additional_inputs — PASS_WITH_WARNINGS

Additional inputs: deck t=280 mm, wearing 22 kN/m3 / 80 mm, covers 40/45, stud 22x125, gamma_m0=1.15, ecc=1.5

**Warnings / defects observed:**
- Custom deck density ignored: UI=26.0 kN/m3; ConcreteProperties has no density field; add_dead_loads() calls create_deck_load() without density (default 25.0 kN/m3)
- Utilization > 100%: [{'util.fatigue': 169.52}]

| Check | Value |
|-------|-------|
| UI girder density | 78.5 |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1118 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 21.61 |
| `util.shear` | 43.65 |
| `util.interaction` | 21.78 |
| `util.ltb` | 23.849999999999998 |
| `util.long_trans_shear` | 18.35 |
| `util.fatigue` | 169.52 |
| `util.stress_limitation` | 26.88 |
| `util.deflection_crack` | 46.63 |

---

## TC07_distinct_cb_ed_materials — PASS_WITH_WARNINGS

Distinct custom grades: girder 350/490 d=80, CB 250/410 d=70, ED 280/440 d=75

**Warnings / defects observed:**
- Custom girder density ignored: UI=80.0 vs backend rho=78500.0 (expected ~80000.0 N/m3)
- Distinct CB fy=250 stored but _build_material_props uses girder fy=350 only
- Distinct ED fy=280 stored but _build_material_props uses girder fy=350 only
- Utilization > 100%: [{'util.fatigue': 157.26}]

| Check | Value |
|-------|-------|
| UI girder density | 80.0 |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1118 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 19.509999999999998 |
| `util.shear` | 39.910000000000004 |
| `util.interaction` | 19.66 |
| `util.ltb` | 22.81 |
| `util.long_trans_shear` | 19.82 |
| `util.fatigue` | 157.26 |
| `util.stress_limitation` | 24.87 |
| `util.deflection_crack` | 45.78 |

---

## TC08_db_grade_with_gs — PASS_WITH_WARNINGS

DB E 350A / M40 with GUI-equivalent Gs + deck fck/fctm/Ecm primed from SQLite

**Warnings / defects observed:**
- Utilization > 100%: [{'util.fatigue': 157.26}]

| Check | Value |
|-------|-------|
| UI girder density | None |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1098 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 19.509999999999998 |
| `util.shear` | 39.910000000000004 |
| `util.interaction` | 19.66 |
| `util.ltb` | 22.81 |
| `util.long_trans_shear` | 19.82 |
| `util.fatigue` | 157.26 |
| `util.stress_limitation` | 24.87 |
| `util.deflection_crack` | 45.78 |

---

## TC09_custom_section_stiffeners — PASS_WITH_WARNINGS

Design Type=Custom; girder 1400×450×20 / 520×25 / tw=12; bearing stiffeners=2; intermediate=Yes

**Warnings / defects observed:**
- Custom deck density ignored: UI=26.0 kN/m3; ConcreteProperties has no density field; add_dead_loads() calls create_deck_load() without density (default 25.0 kN/m3)
- Utilization > 100%: [{'util.fatigue': 175.82}]

| Check | Value |
|-------|-------|
| UI girder density | 78.5 |
| Backend rho | 78500.0 |
| CAD generated | True |
| Output keys | 1118 |

Utilization (output dock):

| Key | Value |
|-----|-------|
| `util.flexure` | 22.3 |
| `util.shear` | 23.9 |
| `util.interaction` | 22.52 |
| `util.ltb` | 28.08 |
| `util.long_trans_shear` | 19.82 |
| `util.fatigue` | 175.82 |
| `util.stress_limitation` | 27.91 |
| `util.deflection_crack` | 37.91 |

---

## TC10_osi_roundtrip — PASS_WITH_WARNINGS

API OSI round-trip: yaml dump → new PlateGirderBridge.set_input → design

**Warnings / defects observed:**
- GUI-only: populate_from_dict() does not rebuild InputDock._material_custom_fields; see issues/BUG_osi_custom_material_map_not_restored.md

---

## TC_MULTI_01 — PASS

GUI Unlock == backend.reset()

| Run | Span | CW | Skew | Output span | CAD span mm | Stale? |
|-----|------|----|------|-------------|-------------|--------|
| 1 | 25.0 | 7.5 | 0.0 | 25.0 | 25000.0 | False |
| 2 | 30.0 | 8.5 | 5.0 | 30.0 | 30000.0 | False |
| 3 | 35.0 | 9.5 | 10.0 | 35.0 | 35000.0 | False |

---

## Graphical outputs (Req 3)

Full checklist: [`GRAPHICAL_OUTPUT_VERIFICATION.md`](GRAPHICAL_OUTPUT_VERIFICATION.md)

| Evidence | Location |
|----------|----------|
| Real OCC 3D CAD (iso/front/top/end) | `evidence/screenshots/cad_3d/` — TC02, TC03, TC06, TC09, MULTI×3 |
| CAD DTO schematics | `evidence/screenshots/cad_schematics/` |
| Structural plots (BMD/SFD/defl/grillage) | `evidence/screenshots/plots/` |
| Live GUI Plots + Unlock multi-run | `evidence/screenshots/gui_screencast/` |
| CAD parameter DTOs | `evidence/dictionaries/cad_dto/` |

**Visual checks:** TC02/TC09 show 4-girder + deck + X-bracing; TC03 shows median + footpath/barrier layout on skewed span; MULTI run1→run3 CAD span 25→30→35 m with no stale geometry.

---

## Defects discovered (drafts in `issues/` — file on the upstream repo at submission)

1. Custom steel density ignored — `issues/BUG_custom_steel_density_ignored.md`
2. Custom deck density ignored — `issues/BUG_custom_deck_density_ignored.md`
3. OSI custom material map not restored (GUI) — `issues/BUG_osi_custom_material_map_not_restored.md`
4. DB grade E 350A missing Gs — `issues/BUG_e350a_missing_gs.md`
5. CB/ED custom materials collapse to girder props — `issues/BUG_cross_bracing_end_diaphragm_custom_density_same.md`
6. Fatigue utilization can exceed 100% while design() still completes — `issues/BUG_fatigue_util_exceeds_100.md`
7. Missing DCR categories written as 0.0 on the output dock — `issues/BUG_missing_dcr_written_as_zero.md`
