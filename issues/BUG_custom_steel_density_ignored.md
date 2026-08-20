# [Bug] Custom girder steel density is ignored in `_build_material_props`

## Description
When the girder grade is **custom** (name not in SQLite), `PlateGirderBridge._build_material_props()` reads custom `fy`, `fu`, `E` and Poisson from `input_dict`, but **does not read** `material.girder.density` (`KEY_MATERIAL_GIRDER_DENSITY`). Density falls back to `_DEFAULT_DENSITY = 78500` N/m³.

The value **is stored** in the input and output dictionaries, so the UI looks correct. Analysis self-weight still uses 7850 kg/m³.

**Works:** database grades (density looked up from SQLite).  
**Fails:** any `custom_steel_*` grade with a non-default density.

## Trigger
1. Short-span plate girder module.
2. Material Inputs → Girder → Custom. Set fy/fu/E and density **80** kN/m³ (not 78.5).
3. Span 30 m, carriageway 7.5 m. Design.
4. Dictionaries show `material.girder.density = 80`. Backend `steel_prop.rho` remains `78500`.

Local cases: **TC02**, **TC07**, **TC10**.

## Evidence
| Source | Result |
|--------|--------|
| `dictionaries/TC02_custom_materials_comparison.json` | UI / input_dict / output_dict all `80.0` |
| `logs/TC02_custom_materials_result.json` | `backend_rho: 78500.0` |
| `screenshots/gui_screencast/01b_custom_materials_fields.png` | Custom density entered in the dock |

File: `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` — `_build_material_props` (~1192):

```python
rho = self._lookup_material(steel_grade, "Density")
if rho is None:
    rho = _DEFAULT_DENSITY  # ignores KEY_MATERIAL_GIRDER_DENSITY
```

Related keys: `KEY_MATERIAL_GIRDER_DENSITY` in `core/utils/common.py`; density is exported by `desktop/ui/dialogs/material_properties.py` and validated in `validator.py`.

Not the same as wearing-course density validation.

## Suggested fix
Mirror the custom fy/fu/E path. Confirm SQLite Density units (N/m³ vs kN/m³) before merge; the UI stores kN/m³.

```python
rho = self._lookup_material(steel_grade, "Density")
if rho is None:
    raw_rho = self.input_dict.get(KEY_MATERIAL_GIRDER_DENSITY)
    if raw_rho not in (None, ""):
        rho = float(raw_rho) * 1000.0  # kN/m³ → N/m³
    else:
        rho = _DEFAULT_DENSITY
```
