# [Bug] Default steel grade `E 350A` cannot complete design — Gs not set

## Description
Default optimized designs using SQLite grade **E 350A** fail at design-check with:

```text
ValueError: Gs (shear modulus) is not set for grade 'E 350A'.
Populate it in the material database before running the design check.
```

`BridgeConfig.from_plate_girder_bridge` requires `KEY_MATERIAL_GIRDER_G` on `input_dict`. The database grade does not populate that key. Custom grades succeed because the material dialog writes `G = E / (2(1+ν))`.

**Works:** custom steel with sub-keys (TC02, TC05, TC06).  
**Works if GUI-equivalent keys are primed:** same E 350A + M40 geometry as TC01 with Gs and deck fck/fctm/Ecm written onto `input_dict` (TC08).  
**Fails:** untouched default path (TC01 span 30 m; TC04 span 20 m). After Gs is supplied, the next missing key is `material.deck.fck` (then fctm, Ecm). The GUI material dialog primes these; `BASIC_INPUT_DICT` does not.

## Trigger
1. New plate-girder session, leave steel as **E 350A**.
2. Set location, span 30 m, carriageway 7.5 m.
3. Design → failure at Stage 5 (`run_design_check` → `BridgeConfig.from_plate_girder_bridge`).

## Evidence
- Logs: `logs/TC01_basic_optimized_result.json`, `logs/TC04_span_min_boundary_result.json` (full traceback).
- Isolation: `TC08_db_grade_with_gs` uses the same DB grade and only adds `Gs = E/(2(1+ν))`; design completes.
- File: `src/osdagbridge/core/bridge_types/plate_girder/designer.py` (~308–314):

```python
raw_g = bridge.input_dict.get(KEY_MATERIAL_GIRDER_G)
if raw_g in (None, ""):
    raise ValueError(
        f"Gs (shear modulus) is not set for grade "
        f"{bridge.basic_inputs.get(KEY_GIRDER)!r}. ..."
    )
```

Also: `Intg_osdag.sqlite` Steel_Grade_Properties for `E 350A`.

## Suggested fix
Do **one** of:

1. Store Gs for `E 350A` (and audit other grades) in the material seed / SQLite.
2. Derive G when missing but E and Poisson exist:

```python
raw_g = bridge.input_dict.get(KEY_MATERIAL_GIRDER_G)
if raw_g in (None, ""):
    Es_GPa = steel_prop.E / 1e9
    nu = float(steel_prop.v)
    raw_g = Es_GPa / (2.0 * (1.0 + nu))
Gs_MPa = float(raw_g) * 1000.0
```
