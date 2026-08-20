# OsdagBridge — short-span steel girder testing

**Harshdeep Singh** · screening package for functional testing of the plate-girder module.

Start with **`report/OsdagBridge_Testing_Report.pdf`**.

| Folder | Contents |
|--------|-------------------|
| `report/` | Formal PDF (all cases, dictionaries, CAD/plots, defects) |
| `video/` | Silent demo: custom materials, Design, 3D CAD, Plots, Unlock, three runs |
| `test_cases/` | Pass/fail log; UI vs dictionary tables; **CAD / plot verification** |
| `osi_files/` | `.osi` snapshot for each case |
| `issues/` | Bug write-ups + `ISSUE_LINKS.md` with live URLs (#19, #20, #41–#45 on Nidhikhare12/OsdagBridge) |
| `evidence/logs/` | Per-case JSON (errors, warnings, checks) |
| `evidence/dictionaries/` | Side-by-side UI vs input/output dict; CAD DTOs |
| `evidence/screenshots/cad_3d/` | **Real OCC 3D CAD** (iso/front/top/end) for TC02/03/06/09 + multi-run |
| `evidence/screenshots/plots/` | Grillage / BMD / SFD / deflection envelopes |
| `evidence/screenshots/cad_schematics/` | DTO-based dimensional schematics |
| `evidence/screenshots/gui_screencast/` | Live GUI Unlock → 3 consecutive designs + Plots dock |
| `scripts/` | Test runner + `capture_req3_graphics.py` (OCC export) |

**11 cases:** 9 passed (warnings = product defects), 2 failed on default E 350A (missing Gs). Three designs after Unlock keep CAD in sync. See `test_cases/GRAPHICAL_OUTPUT_VERIFICATION.md` for CAD and plot evidence.
