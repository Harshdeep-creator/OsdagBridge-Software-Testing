# [Bug] Cross-bracing and end-diaphragm custom grades are stored but not used in design

## Description
The UI lets Girder, Cross bracing and End diaphragm each have a **different** custom steel grade. `_build_material_props()` builds **one** `SteelProperties` from the **girder** grade only. CB/ED fy, fu, E and density stay on `input_dict` and are echoed in the output dictionary, but global design steel follows the girder.

**Works:** same custom grade on all three members (matches girder — coincidental).  
**Fails:** distinct grades (TC07): girder 350/490 ρ=80, CB 250/410 ρ=70, ED 280/440 ρ=75. Analysis `steel_prop.Fy` / `rho` follow girder only.

## Trigger
1. Custom girder 350 MPa, density 80.
2. Custom cross bracing 250 MPa, density 70.
3. Custom end diaphragm 280 MPa, density 75.
4. Design.
5. Input/output dictionaries keep the three names and sub-keys. `steel_prop` matches girder.

## Evidence
- `dictionaries/TC07_distinct_cb_ed_materials_comparison.json` — three distinct grade names stored.
- `logs/TC07_distinct_cb_ed_materials_result.json` — `backend_rho` 78500 (girder fallback), not 70/75.
- `plategirderbridge.py` `_build_material_props` (~1179–1215): `steel_grade = self.input_dict.get(KEY_GIRDER)` only.

Companion of the girder-density bug; this issue is about **member class**, not only density.

## Suggested fix
Short term: document in the UI that only girder steel drives global `MaterialProperties`.  
Correct behaviour: pass CB/ED properties into transverse / end-diaphragm design (`_design_cross_bracing_members`, `_design_end_diaphragm_members`) instead of reusing girder `steel_prop`.
