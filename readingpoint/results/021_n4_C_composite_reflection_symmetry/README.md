# Result 021 — N4 `C` composite spatial-reflection + mu-tau symmetry

## Outcome

**COMPOSITE SIGN ODDNESS: SUPPORTED ACROSS 9/9 TESTED POINTS.**

**COMPOSITE SQUARE: IDENTITY.**

**ALGEBRAIC CLASSIFICATION: Z2-LIKE SIGN REPRESENTATION ON `C` SUPPORTED.**

Result 021 combines the two operations separated in Result 020:

- the actual spatial reflection `R_x`;
- the mu-tau flavour-basis permutation `P`.

The composite is

`T = P o R_x`.

Across the tested geometry family,

`T(C) ≈ -C`

and applying the composite twice gives exactly

`T^2(C) = C`

in the implemented test.

This provides a precise order-2 transformation law for the effective N4
antisymmetric operator without yet identifying that transformation with
physical handedness.

## Operations

### Spatial reflection

`R_x` acts by

`x -> -x`

with

`S = diag(-1, +1, +1)`

and the spatial tensor transformation

`M'_sp(x) = S M_sp(Sx) S^T`.

### Flavour permutation

`P` exchanges the mu and tau flavour labels:

`[e, mu, tau] -> [e, tau, mu]`.

### Composite

The tested operation is

`T = P o R_x`.

The target sign action is

`T(C) ≈ -C`.

The target order-2 law is

`T^2 = identity`.

## Tested geometry family

The test uses:

- `n = 40`
- `dx = 1`
- `alpha = {0.40, 0.60, 0.80}`
- `delta = {0.05, 0.10, 0.20}`
- `chi = 0.6`
- `q = 0.5`
- `R_loop = 9.0`
- `core_vox = 2.0`

This gives nine tested `(alpha, delta)` points.

## Composite sign action

All nine points support

`T(C) ≈ -C`.

The relative oddness errors are:

- minimum: `7.039153e-07`
- median: `1.698129e-06`
- maximum: `2.535024e-06`

The competing evenness relation `T(C) ≈ C` has errors essentially equal to
`2`:

- minimum: `1.999998`
- median: `1.999999`
- maximum: `2.000000`

Therefore the sign-odd relation is cleanly selected by the test.

**Supported points: 9/9.**

## Composite involution

At the field level:

`T^2 = identity`

with minimum, median, and maximum measured errors all exactly:

`0.000000e+00`.

At the effective-matrix level:

`T^2(C) = C`

with minimum, median, and maximum errors also:

`0.000000e+00`.

Thus the implemented composite is an exact involution in this test.

## Magnitude preservation

The relative difference in the `dx*C` magnitude after one application of
`T` ranges from

`3.298796e-07`

to

`1.635667e-06`

with median

`9.036876e-07`.

**Magnitude preservation: SUPPORTED AT 9/9 POINTS.**

## Antisymmetry

The maximum antisymmetry error across the tested original, transformed, and
twice-transformed matrices is:

`6.328271e-15`.

**Antisymmetry: PASS.**

## Algebraic result

The observed action is

`T(C) ≈ -C`

together with

`T^2(C) = C`.

Therefore the tested effective operator carries the nontrivial sign action
of an order-2 transformation.

The appropriate current classification is:

**Z2-LIKE SIGN REPRESENTATION ON `C` SUPPORTED.**

This wording is intentionally narrower than claiming a larger discrete group.

One tested involution establishes one order-2 action. It does not by itself
establish `V4`, `Q8`, or a quotient relation.

## Relation to Result 018

Result 018 separated screw-sign reversal from the orientation/basis mirror.

It found that:

- `chi -> -chi` leaves `C` approximately invariant;
- the mu-tau orientation swap transforms `C` by the corresponding basis
  permutation;
- at the tested geometry, that mirror action is also approximately a sign
  reversal.

Thus the sign of `chi` was not established as the sign selector for `C`.

## Relation to Result 019

Result 019 extended the Result 018 controls over 27 geometry points.

It established that:

- mirror/orientation oddness is robust across the tested family;
- `chi -> -chi` approximate invariance is robust;
- magnitude is preserved;
- antisymmetry remains at machine precision.

This showed that the observed orientation sign behavior was not an isolated
parameter-point accident.

## Relation to Result 020

Result 020 then applied an actual spatial reflection rather than a
flavour-loop orientation swap.

For `x -> -x`, it found:

`C_ref ≈ C`.

So direct spatial reflection is approximately even in the fixed flavour
basis at the tested geometry.

It also found:

`C_ref ≈ -P C P^T`.

That relation motivated the present composite test.

## What Result 021 adds

Result 021 applies the composite operation directly:

`T = P o R_x`.

Across all nine tested geometries,

`T(C) ≈ -C`.

Applying the same operation twice returns both the fields and effective
matrix exactly to their original tested representations.

The sequence from Results 018–021 is therefore:

`chi -> -chi`  
approximately even;

orientation / mu-tau mirror  
approximately sign reversing across the tested family;

actual `x` spatial reflection  
approximately even in the fixed flavour basis at the Result 020 point;

`P o R_x`  
sign odd across the Result 021 family and exactly order two in the
implemented transformation.

## Interpretation

The N4 operator now has a well-characterized discrete transformation law.

The result supports an effective order-2 sign sector:

`C -> -C`.

The generator tested here is specifically the composite

`T = P o R_x`.

This is more precise than labeling `C` generically as "handed" or
"parity odd."

Physical handedness remains a separate interpretive question because the
test establishes the algebraic action of a constructed composite operation,
not its unique physical identification.

## Constraints

Result 021 does **not** establish:

- that `T` is the physical handedness operation;
- that every spatial reflection gives the same induced action;
- that `C` furnishes a larger discrete group representation;
- that the tested `Z2` is a subgroup or quotient of a previously discussed
  `Q8` or `V4` structure;
- a Reading Point residue correspondence.

Those require additional explicit operations and composition tests.

## Current bridge status

**N4 `C` normalized shape:** SUPPORTED

**N4 lattice normalization `dx*C`:** SUPPORTED

**N4 antisymmetry:** SUPPORTED

**`chi` sign oddness:** NOT SUPPORTED

**Mirror/orientation oddness:** ROBUST ACROSS RESULT 019 FAMILY

**Direct spatial parity oddness:** NOT SUPPORTED

**Composite `T = P o R_x` sign oddness:** SUPPORTED ACROSS 9/9 POINTS

**Composite `T^2`:** IDENTITY

**Algebraic classification:** Z2-LIKE SIGN REPRESENTATION ON `C` SUPPORTED

**Physical handedness identification:** NOT YET ESTABLISHED

**Larger discrete-group identification:** OPEN

**Reading Point -> M5 physical mapping:** NOT ESTABLISHED

## Next reading point

Result 022 should determine whether this tested order-2 action is merely one
binary symmetry of `C` or belongs to a larger explicitly implemented
discrete structure.

The safe next question is:

> Can a second independent involution be constructed from existing M5/N4
> operations, and what composition law does it obey with `T`?

That test should require explicit generators and explicit composition laws
before assigning names such as `V4`.

In particular, one `Z2` generator is insufficient evidence for a
`Q8/{+1,-1} ≅ V4` identification.

The Reading Point -> M5 physical mapping remains held until such a bridge is
established independently.

## Script

`readingpoint/tests/test_021_n4_C_composite_reflection_symmetry.py`
