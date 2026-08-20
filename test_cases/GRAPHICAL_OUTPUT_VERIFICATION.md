# Graphical Output Verification (Req 3)

Evidence that **3D CAD models** and **structural plots** were generated and visually checked for the short-span steel girder module.

## Asset folders

| Folder | Contents |
|--------|----------|
| `evidence/screenshots/cad_3d/` | **Real OCC** exports — iso / front / top / end (`Viewer3d.ExportToImage`) |
| `evidence/screenshots/cad_schematics/` | Dimensionally consistent DTO schematics (span/CW/depth check) |
| `evidence/screenshots/plots/` | Grillage, BMD, SFD, deflection envelopes |
| `evidence/dictionaries/cad_dto/` | CAD parameter DTOs used for rendering |
| `evidence/screenshots/gui_screencast/` | Live GUI multi-run + Plots dock |

Synced from prior API runs: **20** plot PNGs, **11** schematics, **7+** CAD DTOs.  
OCC captures: **28** PNGs (7 cases × 4 views).

## OCC 3D CAD captures

| Case | Iso | Front | Top | End | Span mm | CW mm | Skew ° | Median | Footpath |
|------|-----|-------|-----|-----|---------|-------|--------|--------|----------|
| TC02_custom_materials | Y | Y | Y | Y | 30000 | 7500 | 0 | No | NONE |
| TC03_skew_footpath_median | Y | Y | Y | Y | 28000 | 10000 | 12 | Yes | BOTH |
| TC06_additional_inputs | Y | Y | Y | Y | 30000 | 7500 | 0 | No | NONE |
| TC09_custom_section_stiffeners | Y | Y | Y | Y | 30000 | 7500 | 0 | No | NONE |
| TC_MULTI_01_run1 | Y | Y | Y | Y | 25000 | 7500 | 0 | No | NONE |
| TC_MULTI_01_run2 | Y | Y | Y | Y | 30000 | 8500 | 5 | No | NONE |
| TC_MULTI_01_run3 | Y | Y | Y | Y | 35000 | 9500 | 10 | No | NONE |

Primary files (iso):

- `evidence/screenshots/cad_3d/TC02_custom_materials_cad_iso.png`
- `evidence/screenshots/cad_3d/TC03_skew_footpath_median_cad_iso.png`
- `evidence/screenshots/cad_3d/TC06_additional_inputs_cad_iso.png`
- `evidence/screenshots/cad_3d/TC09_custom_section_stiffeners_cad_iso.png`
- `evidence/screenshots/cad_3d/TC_MULTI_01_run1_cad_iso.png`
- `evidence/screenshots/cad_3d/TC_MULTI_01_run2_cad_iso.png`
- `evidence/screenshots/cad_3d/TC_MULTI_01_run3_cad_iso.png`

## Multi-run CAD freshness

| Run | Span m | CAD span mm | Match | Stale vs prev? |
|-----|--------|-------------|-------|----------------|
| 1 | 25.0 | 25000 | True | False |
| 2 | 30.0 | 30000 | True | False |
| 3 | 35.0 | 35000 | True | False |

CAD geometry updates on each Unlock → redesign; run3 iso is visually longer than run1.

## Visual accuracy checklist

- [x] **TC02** iso: 4 girders, deck, crash barriers, X-bracing, intermediate stiffeners visible.
- [x] **TC03** iso: skew geometry; central median curb pair + outer footpath/barrier lines present.
- [x] **TC06** iso: complete superstructure with non-default additional inputs.
- [x] **TC09** iso: custom plate/stiffener mode still produces a complete OCC model.
- [x] **TC_MULTI** runs 1–3: CAD span **25000 → 30000 → 35000 mm** (no stale model).
- [x] Structural plots present under `plots/` for TC02, TC06, TC08, TC09, MULTI run3 (BMD/SFD/defl/grillage).
- [x] GUI screencast: Plots dock (`07_plots_dock.png`) and three consecutive designs after Unlock (`10`–`18`).

## Component coverage (CAD + dictionaries)

| Component | Verified via |
|-----------|--------------|
| Plate girders (web/flanges) | OCC iso + `steeldesign.details.*` in output dict |
| Intermediate / bearing stiffeners | OCC iso + stiffener keys |
| Cross bracing | OCC iso X-frames + CB input echo |
| Deck slab | OCC deck solid + `deck.report.*` |
| Crash barriers / median / footpath | OCC (esp. TC03) + geometry keys |
| Structural plots | BMD / SFD / deflection / grillage PNGs |

## Method

1. Load `BridgeParametersDTO` saved after each design (`evidence/dictionaries/cad_dto/*_cad_dto.json`).
2. `PlateGirderCADGenerator.generate(params)` builds OCC solids (same path as GUI 3D CAD).
3. `PlateGirderBridge._export_cad_figures()` headless `Viewer3d.ExportToImage` → iso/front/top/end.
4. Plot PNGs from the same generators as the GUI Plots dock (`plot_generator`).

Script: `scripts/capture_req3_graphics.py`  
Overview log: `evidence/logs/req3_graphics_overview.json`
