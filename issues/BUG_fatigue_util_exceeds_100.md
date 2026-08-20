# [Bug] `design()` completes and builds CAD when fatigue utilization exceeds 100%

## Description
Optimized plate-girder runs can finish with a full output dictionary, CAD DTO and plots while `util.fatigue` is **greater than 100%**. `PlateGirderBridge.design()` does not raise and Stage 8 still prepares CAD.

**Works (API):** design returns; GUI may colour the util cell.  
**Fails (reliability):** a completed design with fatigue UR > 1.0 is treated as success.

## Trigger
Custom-material optimized runs, for example:
- TC02: `util.fatigue = 157.26%`
- TC05: `160.14%`
- TC06: `169.52%`

Other util keys (flexure, shear, LTB) stay below 100.

## Evidence
- `logs/TC02_custom_materials_result.json` → `checks.coverage.util_over_100`
- Util keys written in `store_design_results` (`plategirderbridge.py` ~4100–4109) from `category_urs`.
- CAD Stage 8 (`_stage_cad_generation` ~646) runs whenever Stage 5–7 did not throw.

## Suggested fix
After `store_design_results`, if any `util.* > 100`, set a failed-design flag, show it on the output dock, and skip or confirm CAD:

```python
self.store_design_results(design_results)
over = [k for k in (KEY_UTIL_FLEXURE, KEY_UTIL_SHEAR, KEY_UTIL_FATIGUE, ...)
        if float(self.output_dict.get(k) or 0) > 100.0]
if over:
    self.output_dict["design_status"] = "FAIL"
    # optionally: raise or skip _stage_cad_generation until the user accepts
```
