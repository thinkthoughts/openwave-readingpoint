# Result 022 — N4 `C` second independent involution

## Outcome

**SECOND INDEPENDENT INVOLUTION: SUPPORTED.**

**FIELD-LEVEL V4-LIKE STRUCTURE: SUPPORTED FOR BOTH TESTED CANDIDATE PAIRS.**

**REPRESENTATION ON `C`: NON-FAITHFUL.**

Result 021 established one explicit order-2 transformation,

`T_x = P o R_x`,

with

`T_x(C) ≈ -C`

and

`T_x^2 = identity`.

Result 022 preregisters the two remaining coordinate-reflection candidates:

`T_y = P o R_y`

`T_z = P o R_z`

and tests whether either supplies a second independent involution.

Both do.

## Tested geometry

The reference geometry is:

- `n = 40`
- `dx = 1`
- `alpha = 0.6`
- `delta = 0.1`
- `chi = 0.6`
- `q = 0.5`
- `R_loop = 9.0`
- `core_vox = 2.0`

## Candidate `T_y`

The candidate is

`T_y = P o R_y`.

### Involution

`T_x^2` field error:

`0.000000e+00`

`T_y^2` field error:

`0.000000e+00`

Both operations are exact involutions in the implemented test.

### Independence

The field distance between the two generators is:

`distance(T_x, T_y) = 1.012946e+00`.

Thus `T_y` is clearly distinct from `T_x`.

### Commutation

The field-level commutation error is:

`||T_x T_y - T_y T_x|| = 0.000000e+00`.

Therefore the tested generators commute exactly.

### Product involution

The product also squares to identity:

`(T_x T_y)^2` field error:

`0.000000e+00`.

### Four distinct field states

The tested set is:

`{I, T_x, T_y, T_x T_y}`.

All four field transformations are distinct.

Selected pairwise distances are:

- `I - T_x = 1.012493e+00`
- `I - T_y = 9.525433e-02`
- `I - T_x T_y = 1.012946e+00`
- `T_x - T_y = 1.012946e+00`
- `T_x - T_x T_y = 9.525433e-02`
- `T_y - T_x T_y = 1.012493e+00`

Therefore the field-level composition pattern is:

**FOUR DISTINCT COMMUTING INVOLUTIONS: V4-LIKE**

## Action of `T_y` on `C`

The induced actions are:

`T_x(C) ≈ -C`

`T_y(C) ≈ +C`

`(T_x T_y)(C) ≈ -C`.

For `T_y` itself:

- evenness error: `8.371e-06`
- oddness error: approximately `2`.

Thus `T_y` acts trivially on the sign of this single effective operator,
while remaining a distinct nontrivial field transformation.

This makes the representation on `C` non-faithful.

## Candidate `T_z`

The second preregistered candidate is

`T_z = P o R_z`.

### Involution

`T_z^2` field error:

`0.000000e+00`.

### Independence

The field distance from `T_x` is:

`distance(T_x, T_z) = 1.263628e+00`.

Thus `T_z` is also distinct from `T_x`.

### Commutation

`||T_x T_z - T_z T_x|| = 0.000000e+00`.

### Product involution

`(T_x T_z)^2` field error:

`0.000000e+00`.

### Four distinct field states

The set

`{I, T_x, T_z, T_x T_z}`

again contains four distinct field transformations.

Selected pairwise distances are:

- `I - T_x = 1.012493e+00`
- `I - T_z = 1.074153e+00`
- `I - T_x T_z = 1.263628e+00`
- `T_x - T_z = 1.263628e+00`
- `T_x - T_x T_z = 1.074153e+00`
- `T_z - T_x T_z = 1.012493e+00`

Therefore this pair also supports:

**FOUR DISTINCT COMMUTING INVOLUTIONS: V4-LIKE**

## Action of `T_z` on `C`

The induced actions are:

`T_x(C) ≈ -C`

`T_z(C) ≈ +C`

`(T_x T_z)(C) ≈ -C`.

For `T_z`:

- evenness error: `3.682e-15`
- oddness error: approximately `2`.

So `T_z` acts essentially exactly as `+1` on `C`.

Again, the representation is non-faithful.

## Antisymmetry

For both candidate analyses, the maximum antisymmetry error is:

`6.022717e-15`.

**Antisymmetry: PASS.**

## Result

The executable test establishes two valid second-involution candidates:

**`T_y`: SUPPORTED**

**`T_z`: SUPPORTED**

For each pair,

`{I, T_x, T_a, T_x T_a}`

contains four distinct commuting involutions.

Thus:

**FIELD-LEVEL V4-LIKE STRUCTURE: SUPPORTED FOR BOTH TESTED PAIRS**

This is the first point in the N4 effective-operator audit where a genuine
four-element transformation pattern has been produced operationally from
explicit field transformations rather than inferred from cardinality alone.

## Non-faithful action on `C`

The four field transformations do not remain four distinct actions on `C`.

For the tested pairs:

`T_x -> -1`

`T_y -> +1`

`T_z -> +1`

`T_x T_y -> -1`

`T_x T_z -> -1`.

Thus different field transformations collapse to the same sign action on
the single effective matrix `C`.

In particular, `C` cannot distinguish:

`I` from `T_y`

or

`I` from `T_z`

through its sign alone.

Likewise, it cannot distinguish:

`T_x`

from

`T_x T_y`

or

`T_x T_z`

through its sign alone.

Therefore:

**THE REPRESENTATION ON `C` IS NON-FAITHFUL.**

## Why this matters for the bridge

Result 003 established the abstract mathematical quotient

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 x C2`.

Result 022 now finds V4-like field-level transformation patterns on the M5/N4
side.

However, this is not yet the Reading Point -> M5 bridge.

The reasons are important:

1. two different V4-like candidate pairs exist;
2. `C` does not distinguish all four field transformations;
3. it is not yet known whether `T_y` and `T_z` belong to the same
   four-element transformation set;
4. no explicit derivation connects these field transformations to
   `Q8/{+1,-1}`;
5. no residue classes have been assigned to any of the transformations.

Therefore Result 022 does **not** establish:

`Q8/{+1,-1}`

as the physical classification of these transformations.

It establishes only the explicit V4-like composition patterns tested here.

## Relation to Result 021

Result 021 established one order-2 sign generator:

`T_x(C) ≈ -C`

with

`T_x^2 = identity`.

Result 022 adds independent commuting involutions.

This is exactly the additional algebraic evidence required before even
considering a four-element transformation structure.

## Constraint

The phrase **V4-like** refers to the field-level composition pattern:

- identity;
- two independent order-2 generators;
- their product;
- all four distinct;
- commuting composition.

It does not identify those transformations with particle states, quaternion
defects, or Reading Point residue classes.

The action on `C` is non-faithful and therefore cannot itself provide a
four-way state readout.

## Current bridge status

**N4 `C` normalized shape:** SUPPORTED

**N4 lattice normalization `dx*C`:** SUPPORTED

**N4 antisymmetry:** SUPPORTED

**`T_x`:** SUPPORTED

**Second independent involution:** SUPPORTED

**`T_y`:** SUPPORTED

**`T_z`:** SUPPORTED

**Field-level V4-like pairs:** SUPPORTED

**Representation on `C`:** NON-FAITHFUL

**Four-way operational classification from `C`:** NOT ESTABLISHED

**`Q8/{+1,-1}` identification:** NOT ESTABLISHED

**Physical handedness identification:** NOT YET ESTABLISHED

**Reading Point -> M5 physical mapping:** NOT ESTABLISHED

## Next reading point

Result 023 should determine the full closure generated by:

`T_x`, `T_y`, `T_z`.

The key question is:

> Do the three generators produce only four distinct transformations, or
> eight?

The next test should explicitly generate:

`I`

`T_x`

`T_y`

`T_z`

`T_x T_y`

`T_x T_z`

`T_y T_z`

`T_x T_y T_z`

and compare them at field level.

If only four are distinct, then the repository has supplied a naturally
selected V4-like transformation set.

If all eight are distinct, then the field-level structure is instead
`C2^3`-like, with multiple embedded V4 subgroups.

In that case selecting one V4 subgroup for the Reading Point bridge would
still require an independent reason.

The representation on `C` must remain separate from the field-level group
classification.

## Script

`readingpoint/tests/test_022_n4_C_second_involution.py`
