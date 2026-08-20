# Side-by-side: Planned UI inputs vs Input/Output dictionaries

Generated from `dictionaries/*_comparison.json` after local design runs.

## TC01_basic_optimized_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | None | True | None |
| `geometry.carriageway_width` | 7.5 | 7.5 | None | True | None |
| `geometry.skew_angle` | 0.0 | 0.0 | None | True | None |
| `geometry.include_median` | No | No | None | True | None |
| `geometry.footpath` | None | None | None | True | None |
| `geometry.design_mode` | Optimized | Optimized | None | True | None |
| `material.girder` | E 350A | E 350A | None | True | None |
| `material.cross_bracing` | E 350A | E 350A | None | True | None |
| `material.end_diaphragm` | E 350A | E 350A | None | True | None |
| `material.deck` | M40 | M40 | None | True | None |
| `typical_section.deck_thickness` | 250.0 | 250.0 | None | True | None |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | None | True | None |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | None | True | None |
| `design_options.deck.top_clear_cover` | 50 | 50 | None | True | None |
| `design_options.shear_studs.diameter` | 20 | 20 | None | True | None |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | None | True | None |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | None | True | None |

## TC02_custom_materials_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | 30.0 | True | True |
| `geometry.carriageway_width` | 7.5 | 7.5 | 7.5 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.cross_bracing` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.end_diaphragm` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 350 | 350 | 350 | True | True |
| `material.girder.fu` | 490 | 490 | 490 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 350 | 350 | 350 | True | True |
| `material.cross_bracing.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.end_diaphragm.fy` | 350 | 350 | 350 | True | True |
| `material.end_diaphragm.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.deck.fck` | 40 | 40 | 40 | True | True |
| `material.deck.density` | 26.0 | 26.0 | 26.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC03_skew_footpath_median_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 28.0 | 28.0 | 28.0 | True | True |
| `geometry.carriageway_width` | 10.0 | 10.0 | 10.0 | True | True |
| `geometry.skew_angle` | 12.0 | 12.0 | 12.0 | True | True |
| `geometry.include_median` | Yes | Yes | Yes | True | True |
| `geometry.footpath` | Both | Both | Both | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | custom_steel_300_440 | custom_steel_300_440 | custom_steel_300_440 | True | True |
| `material.cross_bracing` | custom_steel_300_440 | custom_steel_300_440 | custom_steel_300_440 | True | True |
| `material.end_diaphragm` | custom_steel_300_440 | custom_steel_300_440 | custom_steel_300_440 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 300 | 300 | 300 | True | True |
| `material.girder.fu` | 440 | 440 | 440 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 300 | 300 | 300 | True | True |
| `material.cross_bracing.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.end_diaphragm.fy` | 300 | 300 | 300 | True | True |
| `material.end_diaphragm.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `material.deck.density` | 25.0 | 25.0 | 25.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC04_span_min_boundary_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 20.0 | 20.0 | None | True | None |
| `geometry.carriageway_width` | 6.0 | 6.0 | None | True | None |
| `geometry.skew_angle` | 0.0 | 0.0 | None | True | None |
| `geometry.include_median` | No | No | None | True | None |
| `geometry.footpath` | None | None | None | True | None |
| `geometry.design_mode` | Optimized | Optimized | None | True | None |
| `material.girder` | E 350A | E 350A | None | True | None |
| `material.cross_bracing` | E 350A | E 350A | None | True | None |
| `material.end_diaphragm` | E 350A | E 350A | None | True | None |
| `material.deck` | M40 | M40 | None | True | None |
| `typical_section.deck_thickness` | 250.0 | 250.0 | None | True | None |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | None | True | None |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | None | True | None |
| `design_options.deck.top_clear_cover` | 50 | 50 | None | True | None |
| `design_options.shear_studs.diameter` | 20 | 20 | None | True | None |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | None | True | None |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | None | True | None |

## TC05_span_max_boundary_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 45.0 | 45.0 | 45.0 | True | True |
| `geometry.carriageway_width` | 12.0 | 12.0 | 12.0 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.cross_bracing` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.end_diaphragm` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 350.0 | 350.0 | 350.0 | True | True |
| `material.girder.fu` | 490.0 | 490.0 | 490.0 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 350.0 | 350.0 | 350.0 | True | True |
| `material.cross_bracing.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.end_diaphragm.fy` | 350.0 | 350.0 | 350.0 | True | True |
| `material.end_diaphragm.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `material.deck.density` | 25.0 | 25.0 | 25.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC06_additional_inputs_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | 30.0 | True | True |
| `geometry.carriageway_width` | 7.5 | 7.5 | 7.5 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.cross_bracing` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.end_diaphragm` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 350 | 350 | 350 | True | True |
| `material.girder.fu` | 490 | 490 | 490 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 350 | 350 | 350 | True | True |
| `material.cross_bracing.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.end_diaphragm.fy` | 350 | 350 | 350 | True | True |
| `material.end_diaphragm.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `material.deck.density` | 26.0 | 26.0 | 26.0 | True | True |
| `typical_section.deck_thickness` | 280.0 | 280.0 | 280.0 | True | True |
| `typical_section.wearing_course.density` | 22.0 | 22.0 | 22.0 | True | True |
| `typical_section.wearing_course.thickness` | 80.0 | 80.0 | 80.0 | True | True |
| `design_options.deck.top_clear_cover` | 40 | 40 | 40 | True | True |
| `design_options.shear_studs.diameter` | 22 | 22 | 22 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.15 | 1.15 | 1.15 | True | True |
| `loading.live_load.eccentricity` | 1.5 | 1.5 | 1.5 | True | True |

## TC07_distinct_cb_ed_materials_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | 30.0 | True | True |
| `geometry.carriageway_width` | 7.5 | 7.5 | 7.5 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.cross_bracing` | custom_steel_250_410 | custom_steel_250_410 | custom_steel_250_410 | True | True |
| `material.end_diaphragm` | custom_steel_280_440 | custom_steel_280_440 | custom_steel_280_440 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 350 | 350 | 350 | True | True |
| `material.girder.fu` | 490 | 490 | 490 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 250 | 250 | 250 | True | True |
| `material.cross_bracing.density` | 70.0 | 70.0 | 70.0 | True | True |
| `material.end_diaphragm.fy` | 280 | 280 | 280 | True | True |
| `material.end_diaphragm.density` | 75.0 | 75.0 | 75.0 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `material.deck.density` | 25.0 | 25.0 | 25.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC08_db_grade_with_gs_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | 30.0 | True | True |
| `geometry.carriageway_width` | 7.5 | 7.5 | 7.5 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | E 350A | E 350A | E 350A | True | True |
| `material.cross_bracing` | E 350A | E 350A | E 350A | True | True |
| `material.end_diaphragm` | E 350A | E 350A | E 350A | True | True |
| `material.deck` | M40 | M40 | M40 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC09_custom_section_stiffeners_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | 30.0 | True | True |
| `geometry.carriageway_width` | 7.5 | 7.5 | 7.5 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Custom | Custom | Custom | True | True |
| `material.girder` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.cross_bracing` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.end_diaphragm` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 350 | 350 | 350 | True | True |
| `material.girder.fu` | 490 | 490 | 490 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 350 | 350 | 350 | True | True |
| `material.cross_bracing.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.end_diaphragm.fy` | 350 | 350 | 350 | True | True |
| `material.end_diaphragm.density` | 78.5 | 78.5 | 78.5 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `material.deck.density` | 26.0 | 26.0 | 26.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC10_osi_roundtrip_comparison

| Key | Planned / UI | input_dict | output_dict | In match | Out match |
|-----|---------------|------------|-------------|----------|-----------|
| `geometry.span` | 30.0 | 30.0 | 30.0 | True | True |
| `geometry.carriageway_width` | 7.5 | 7.5 | 7.5 | True | True |
| `geometry.skew_angle` | 0.0 | 0.0 | 0.0 | True | True |
| `geometry.include_median` | No | No | No | True | True |
| `geometry.footpath` | None | None | None | True | True |
| `geometry.design_mode` | Optimized | Optimized | Optimized | True | True |
| `material.girder` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.cross_bracing` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.end_diaphragm` | custom_steel_350_490 | custom_steel_350_490 | custom_steel_350_490 | True | True |
| `material.deck` | custom_concrete_40_3_5 | custom_concrete_40_3_5 | custom_concrete_40_3_5 | True | True |
| `material.girder.fy` | 350 | 350 | 350 | True | True |
| `material.girder.fu` | 490 | 490 | 490 | True | True |
| `material.girder.e` | 200.0 | 200.0 | 200.0 | True | True |
| `material.girder.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.girder.g` | 76.923 | 76.923 | 76.923 | True | True |
| `material.cross_bracing.fy` | 350 | 350 | 350 | True | True |
| `material.cross_bracing.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.end_diaphragm.fy` | 350 | 350 | 350 | True | True |
| `material.end_diaphragm.density` | 80.0 | 80.0 | 80.0 | True | True |
| `material.deck.fck` | 40.0 | 40.0 | 40.0 | True | True |
| `material.deck.density` | 26.0 | 26.0 | 26.0 | True | True |
| `typical_section.deck_thickness` | 250.0 | 250.0 | 250.0 | True | True |
| `typical_section.wearing_course.density` | 24.0 | 24.0 | 24.0 | True | True |
| `typical_section.wearing_course.thickness` | 50.0 | 50.0 | 50.0 | True | True |
| `design_options.deck.top_clear_cover` | 50 | 50 | 50 | True | True |
| `design_options.shear_studs.diameter` | 20 | 20 | 20 | True | True |
| `design_options_cont.partial_factor.yielding_and_buckling.gamma_m0` | 1.10 | 1.1 | 1.1 | True | True |
| `loading.live_load.eccentricity` | 1.2 | 1.2 | 1.2 | True | True |

## TC02_custom_materials_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 45.9407878432377 |
| `deck.report.as_req_bot` | 596.2922946746502 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC02_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 45.9407878432377 |
| `deck.report.as_req_bot` | 596.2922946746502 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC03_skew_footpath_median_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 6.4625 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 109.27425291130254 |
| `deck.report.as_req_bot` | 1512.6679944738235 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC05_span_max_boundary_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 3.225 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 59.940633051891126 |
| `deck.report.as_req_bot` | 788.3053491132634 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC06_additional_inputs_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.867000000000001 |
| `deck.report.m_uls_sag` | 44.94361700769232 |
| `deck.report.as_req_bot` | 488.1197328420369 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC07_distinct_cb_ed_materials_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 45.9407878432377 |
| `deck.report.as_req_bot` | 596.2922946746502 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC08_db_grade_with_gs_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 45.9407878432377 |
| `deck.report.as_req_bot` | 596.2922946746502 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC09_custom_section_stiffeners_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 45.9407878432377 |
| `deck.report.as_req_bot` | 596.2922946746502 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |

## TC10_osi_roundtrip_deck_report_values — nested `deck_report_values` vs design-report chapter

| Key | Value |
|-----|-------|
| `deck.report.span` | 2.1 |
| `deck.report.fy` | 500.0 |
| `deck.report.w_dl` | 6.1312500000000005 |
| `deck.report.m_uls_sag` | 45.9407878432377 |
| `deck.report.as_req_bot` | 596.2922946746502 |
| `deck.report.punch_ok` | True |
| `deck.report.shear_ok` | True |
