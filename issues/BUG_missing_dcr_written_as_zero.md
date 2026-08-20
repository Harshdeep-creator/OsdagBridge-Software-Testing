# [Bug] Missing DCR categories are written as 0.0 on the output dock

## Description
`store_design_results()` maps eight utilization keys from `design_results["category_urs"]`. If a category is **absent**, it writes **0.0**, not `None` / `"N/A"`.

The dock then shows 0% flexure/shear/fatigue, which looks like a safe check. A genuine 0% and a skipped check cannot be told apart.

**Works:** typical orthogonal span without footpath/median (TC02) — all eight util keys are populated with non-zero values where expected.  
**Fails:** TC03 (span 28 m, CW 10 m, skew 12°, footpath Both, median Yes): `util.flexure`, `util.shear`, `util.interaction`, `util.fatigue`, `util.stress_limitation`, `util.deflection_crack` are **0.0** while `util.ltb` is 20.44% and `util.long_trans_shear` is 23.89%. Deck report keys are present once nested `deck_report_values` is read.

## Trigger
Skew + both footpaths + median, custom steel fy=300 (TC03). Design completes (PASS) with CAD.

## Evidence
- `logs/TC03_skew_footpath_median_result.json` — `util_values` as above; `missing_deck_report` for `deck.report.*`.
- `plategirderbridge.py` `store_design_results` (~4100–4109):

```python
out[KEY_UTIL_FLEXURE] = cat_urs.get(1, {}).get("max_dcr", 0.0) * 100
out[KEY_UTIL_SHEAR]   = cat_urs.get(2, {}).get("max_dcr", 0.0) * 100
# ...
out[KEY_UTIL_FATIGUE] = cat_urs.get(6, {}).get("max_dcr", 0.0) * 100
```

`.get(..., 0.0)` is the silent default.

## Suggested fix
Use `None` when the category is missing, and show "—" on the dock:

```python
def _ur(cat):
    block = cat_urs.get(cat)
    if not block or block.get("max_dcr") is None:
        return None
    return float(block["max_dcr"]) * 100.0

out[KEY_UTIL_FLEXURE] = _ur(1)
```

Separately, investigate why categories 1, 2, 3, 6, 7, 8 are empty for the TC03 geometry (possible analysis/check coverage gap for skew + divided carriageway).
