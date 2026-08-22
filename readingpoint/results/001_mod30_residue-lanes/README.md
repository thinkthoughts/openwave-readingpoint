# Result 001 — Mod-30 units vs Q8

## Outcome

**REJECTED as a group isomorphism.**

Both structures have eight elements, but their group structures differ.

- `(Z/30Z)* ≅ C4 × C2`
- `Q8` is non-abelian

The executable test confirms:

- cardinality match: PASS
- group isomorphism: REJECTED

## Interpretation

The shared cardinality `8` is insufficient to define a structural correspondence.

Any future Reading Point ↔ M5 mapping must therefore be based on a more specific object such as:

- a quotient,
- an action,
- conjugacy classes,
- an observable,
- a symmetry representation,
- or another independently specified structure.

## Script

`readingpoint/tests/test_001_mod30_vs_q8.py`
