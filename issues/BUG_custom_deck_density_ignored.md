# [Bug] Custom deck concrete density never reaches dead-load analysis

## Description
The UI and OSI store `material.deck.density` (`KEY_MATERIAL_DECK_DENSITY`). That value is **not** part of `ConcreteProperties` and is **not** passed into `create_deck_load()`.

Deck self-weight always uses `WET_CONCRETE_DENSITY_kN_m3` / `DEFAULT_CONCRETE_DENSITY` (**25.0 kN/m³**).

**Works:** default M40-like deck at 25 kN/m³ (accidental match).  
**Fails:** custom deck density 26 kN/m³ (TC02, TC06, TC09) — dictionaries keep 26; analysis uses 25.

## Trigger
1. Custom concrete grade, density **26** kN/m³.
2. Design.
3. `input_dict["material.deck.density"] == 26`.
4. `ConcreteProperties` has only `grade, fck, fctm, Ecm` — no density field.
5. `add_dead_loads()` calls `create_deck_load(slab_thickness_m=deck_t_m)` with no density argument.

## Evidence
- `dto.py` `ConcreteProperties` (~133–151): no `rho` / `density`.
- `plategirderbridge.py` `_build_material_props` (~1217–1239): reads fck/fctm/Ecm for custom deck, never `KEY_MATERIAL_DECK_DENSITY`.
- `plategirderbridge.py` `add_dead_loads` (~1333):

```python
model.create_deck_load(slab_thickness_m=deck_t_m)
```

- `analyser.py` `create_deck_load` (~466):

```python
rho_c = WET_CONCRETE_DENSITY_kN_m3 if concrete_density_kN_m3 is None else concrete_density_kN_m3
```

Local cases: **TC02** (ρ=26), **TC06** (ρ=26). Comparison tables show the dictionary value is retained.

## Suggested fix
1. Add `density_kN_m3` to `ConcreteProperties` and populate it from DB or `KEY_MATERIAL_DECK_DENSITY`.
2. Pass it through:

```python
rho_deck = float(self.input_dict.get(KEY_MATERIAL_DECK_DENSITY) or DEFAULT_CONCRETE_DENSITY)
model.create_deck_load(slab_thickness_m=deck_t_m, concrete_density_kN_m3=rho_deck)
```
