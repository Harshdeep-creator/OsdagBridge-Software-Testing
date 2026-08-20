"""Off-screen CAD schematic + structural plot capture (no GitHub, local only)."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def dto_to_jsonable(dto) -> dict:
    if dto is None:
        return {}
    if is_dataclass(dto):
        return asdict(dto)
    return {"type": type(dto).__name__, "repr": repr(dto)}


def render_cad_schematic(dto, out_path: Path, title: str = "3D CAD schematic (from BridgeParametersDTO)") -> bool:
    """Draw a dimensionally consistent isometric of slab + girders from the CAD DTO."""
    if dto is None:
        return False
    try:
        span = float(dto.span_length_L) / 1000.0
        cw = float(dto.carriageway_width) / 1000.0
        deck_t = max(float(dto.deck_thickness) / 1000.0, 0.05)
        n_g = max(int(dto.num_girders), 1)
        spacing = float(dto.girder_spacing) / 1000.0 if getattr(dto, "girder_spacing", 0) else (cw / max(n_g - 1, 1))
        depth = float(dto.girder_section_d) / 1000.0
        bf = float(getattr(dto, "girder_section_bf", 500.0)) / 1000.0
        skew = float(getattr(dto, "skew_angle", 0.0) or 0.0)
    except Exception:
        return False

    fig = plt.figure(figsize=(11, 6.2), dpi=140, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")

    def box(x0, y0, z0, dx, dy, dz, color, alpha=0.85):
        verts = [
            [(x0, y0, z0), (x0 + dx, y0, z0), (x0 + dx, y0 + dy, z0), (x0, y0 + dy, z0)],
            [(x0, y0, z0 + dz), (x0 + dx, y0, z0 + dz), (x0 + dx, y0 + dy, z0 + dz), (x0, y0 + dy, z0 + dz)],
            [(x0, y0, z0), (x0 + dx, y0, z0), (x0 + dx, y0, z0 + dz), (x0, y0, z0 + dz)],
            [(x0, y0 + dy, z0), (x0 + dx, y0 + dy, z0), (x0 + dx, y0 + dy, z0 + dz), (x0, y0 + dy, z0 + dz)],
            [(x0, y0, z0), (x0, y0 + dy, z0), (x0, y0 + dy, z0 + dz), (x0, y0, z0 + dz)],
            [(x0 + dx, y0, z0), (x0 + dx, y0 + dy, z0), (x0 + dx, y0 + dy, z0 + dz), (x0 + dx, y0, z0 + dz)],
        ]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=color, edgecolors="#333333", linewidths=0.4, alpha=alpha))

    # Slab (deck)
    box(0, 0, depth, span, cw, deck_t, "#9ecae1", 0.55)
    # Girders under slab
    y0 = 0.15 if n_g == 1 else 0.0
    for i in range(n_g):
        y = y0 + i * spacing
        y = min(max(y, 0.0), max(cw - bf, 0.0))
        box(0, y, 0, span, max(bf, 0.08), depth, "#4d4d4d", 0.9)

    ax.set_xlabel("Span (m)")
    ax.set_ylabel("Width (m)")
    ax.set_zlabel("Depth (m)")
    ax.set_title("")
    ax.view_init(elev=18, azim=-60)
    try:
        ax.set_box_aspect((span, max(cw, 0.5), depth + deck_t))
    except Exception:
        pass
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out_path.exists()


def capture_structural_plots(bridge, out_dir: Path, prefix: str) -> dict:
    """Save grillage / BMD / SFD / deflection PNGs using the same generators as the GUI plots dock."""
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {"ok": False, "files": {}, "errors": []}
    try:
        from osdagbridge.core.bridge_types.plate_girder.plot_generator import (
            build_figure_grillage,
            capture_report_figures,
            figure_to_bytes,
        )

        ds = bridge.get_results_dataset()
        nodes, members = bridge.get_nodes_members()
        edge = 0.0
        try:
            edge = float(bridge.get_edge_dist() or 0.0)
        except Exception:
            pass
        if not nodes or not members:
            result["errors"].append("empty nodes/members — OpenSees model not live")
            return result

        try:
            fig = build_figure_grillage(nodes, members, edge_dist=edge)
            p = out_dir / f"{prefix}_plot_grillage.png"
            p.write_bytes(figure_to_bytes(fig, fmt="png", dpi=140))
            result["files"]["grillage"] = str(p)
        except Exception as e:
            result["errors"].append(f"grillage: {e}")

        try:
            figs = capture_report_figures(ds, nodes, members, edge_dist=edge, eng_scale=1.0) or {}
            names = {"bm_envelope": "plot_bmd", "sf_envelope": "plot_sfd", "defl_ll": "plot_defl"}
            for key, stem in names.items():
                blob = figs.get(key)
                if blob:
                    p = out_dir / f"{prefix}_{stem}.png"
                    p.write_bytes(blob)
                    result["files"][stem] = str(p)
        except Exception as e:
            result["errors"].append(f"report figures: {e}")

        result["ok"] = bool(result["files"])
        result["node_count"] = len(nodes)
        result["member_count"] = len(members)
    except Exception as e:
        result["errors"].append(str(e))
    return result


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
