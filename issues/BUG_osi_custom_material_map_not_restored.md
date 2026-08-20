# [Bug] OSI load does not restore `_material_custom_fields`; Design can overwrite custom properties

## Description
Custom material maps live only in memory: `InputDock._material_custom_fields`. Saving OSI writes the grade **name** (`custom_steel_350_490`) and exported property keys. `populate_from_dict()` after OSI load **does not rebuild** that map.

Before every Design, `common_design_func` calls `_prime_material_inputs()`, which builds `MaterialPropertiesDialog(..., custom_fields=_material_custom_fields.get(selected))`. After a cold OSI load the map is empty, so the dialog can fall back to name-parse / defaults and **overwrite** restored `material.girder.fy/e/density`.

**Works:** custom materials created in the same GUI session (map is filled).  
**Fails:** restart (or new session) → File → Load OSI → Design without reopening the custom-material dialog.

API round-trip (yaml → `PlateGirderBridge.set_input`) **keeps** the keys (TC10). This defect is **desktop-only**.

## Trigger
1. Create custom steel + custom concrete; Design once.
2. File → Save Input (`.osi`).
3. Restart the app → Load the OSI.
4. Design **without** reopening the custom material dialog.
5. Watch material sub-keys move back toward dialog defaults.

## Evidence
- `desktop/ui/docks/input_dock.py`
  - `__init__`: `_material_custom_fields = {}` (~78)
  - `_prime_material_inputs` (~324–340)
  - `populate_from_dict` (~1048–1084): copies keys into widgets, **never** rebuilds `_material_custom_fields`
- `desktop/ui/template_page.py` `common_design_func` (~636): `_prime_material_inputs()`
- OSI files: `osi_files/TC02_custom_materials.osi`, `osi_files/TC10_osi_roundtrip.osi`

## Suggested fix
On OSI load, rebuild the map from loaded sub-keys for names starting with `custom_steel_` / `custom_concrete_`. Or skip priming when those prefixes exist **and** sub-keys are already on `input_dict`:

```python
# in _prime_material_inputs
if selected.startswith(("custom_steel_", "custom_concrete_")):
    custom_flds = self._material_custom_fields.get(selected)
    if custom_flds is None and self._has_material_subkeys(key):
        self._update_input_dict(key, selected)
        continue
```

Optional: persist a `custom_materials` block in OSI YAML for a true round-trip.
