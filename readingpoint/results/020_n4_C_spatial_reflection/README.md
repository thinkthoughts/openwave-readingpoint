# Result 020 — N4 `C` actual spatial reflection

## Outcome

**DIRECT SPATIAL PARITY ODDNESS NOT SUPPORTED.**

**DIRECT SPATIAL PARITY EVENNESS SUPPORTED IN THE TESTED GEOMETRY.**

Results 018–019 established that the N4 chiral operator `C` changes sign
approximately under the tested mu-tau orientation mirror, while remaining
approximately invariant under `chi -> -chi`.

Result 020 applies a stronger control: an actual spatial reflection of the
M5 tensor fields.

The reflected operator is approximately equal to the original `C`, not to
`-C`.

## Spatial reflection

The tested physical-space transformation is:

`x -> -x`

with spatial reflection matrix:

`S = diag(-1, +1, +1)`.

For the rank-2 spatial tensor block, the reflected field is constructed as:

`M'_sp(x) = S M_sp(Sx) S^T`.

On the discrete grid this means:

1. reverse the x-coordinate axis;
2. conjugate the spatial `3 x 3` tensor block by `S`;
3. leave the time / `g` component unchanged apart from coordinate reversal.

This is an actual spatial reflection, distinct from the mu-tau flavour
relabeling used in Results 018–019.

## Tested geometry

The controlled point is:

`n = 40`

`dx = 1`

`alpha = 0.6`

`delta = 0.1`

`chi = 0.6`

`q = 0.5`

`R_loop = 9`

`core_vox = 2`

## Original operator

```text
[[ 0.        1.009874 -1.009884]
 [-1.009874  0.       -1.179775]
 [ 1.009884  1.179775  0.      ]]
```

## Reflected operator

```text
[[ 0.        1.009884 -1.009873]
 [-1.009884  0.       -1.179771]
 [ 1.009873  1.179771  0.      ]]
```

The two matrices are nearly identical.

## Direct parity diagnostics

The direct evenness error is:

`||C_ref - C|| / ||C|| = 8.371447e-06`

The direct oddness error is:

`||C_ref + C|| / ||C|| = 1.999999`

The normalized even-shape error is:

`8.246263e-06`

The normalized odd-shape error is:

`2.000000`.

Therefore:

**`C_ref ≈ C`**

rather than:

**`C_ref ≈ -C`.**

## Magnitude preservation

The lattice-normalized magnitude ratio is:

`||dx*C_ref|| / ||dx*C|| = 0.999998557649`

with relative magnitude difference:

`1.442351e-06`.

Therefore:

**Magnitude preservation under spatial reflection: SUPPORTED**

## Antisymmetry

The original antisymmetry error is:

`2.823e-15`

The reflected antisymmetry error is:

`6.023e-15`.

Therefore:

**Antisymmetry is preserved.**

## Basis-adjusted comparison

Let `P` swap the mu and tau flavour basis labels.

The reflected matrix is compared with:

`P C P^T`

and:

`-P C P^T`.

Measured errors are:

`error(C_ref, P C P^T) = 1.999999`

`error(C_ref, -P C P^T) = 1.999098e-06`.

Thus:

**`C_ref ≈ -P C P^T`.**

This composite relation is much more accurate than `C_ref ≈ P C P^T`.

## Result

The executable test establishes:

**Direct spatial parity sign reversal:** NOT SUPPORTED

**Direct spatial parity invariance:** SUPPORTED

**Magnitude preservation:** SUPPORTED

**Antisymmetry preservation:** PASS

**Basis-adjusted relation:** `C_ref ≈ -P C P^T`

**Physical spatial-reflection law in the fixed flavour basis:** `C_ref ≈ C`

## Interpretation

The robust sign reversal found in Results 018–019 is not simply the direct
action of physical-space parity on the N4 operator.

An actual `x -> -x` reflection leaves `C` approximately invariant in the
fixed flavour basis.

The sign-reversing behavior therefore belongs to a more structured
orientation/basis transformation.

At the same time, the reflected operator satisfies:

`C_ref ≈ -P C P^T`.

This suggests that the relevant symmetry should be classified as a
**combined spatial-reflection and flavour-basis action**, rather than calling
`C` directly parity odd.

Result 020 therefore prevents an overinterpretation of the N4 operator as a
simple pseudoscalar-like parity-odd object.

## Relation to Result 018

Result 018 found:

- `chi -> -chi` approximately leaves `C` invariant;
- the mu-tau orientation swap transforms `C` exactly as `P C P^T`;
- and that transformed matrix is approximately `-C`.

Result 020 shows that an independently applied spatial reflection behaves
differently:

`C_ref ≈ C`.

Thus screw reversal, orientation swapping, and actual spatial reflection are
three distinct transformations in the current effective construction.

## Relation to Result 019

Result 019 established that the orientation-mirror sign reversal is robust
across 27 tested geometry points.

Result 020 shows that this robust sign reversal should remain classified as
an **orientation/basis property**, rather than direct physical parity
oddness.

The direct spatial-reflection result at the tested geometry is instead
approximately even.

## Constraint

Result 020 uses only the reflection:

`x -> -x`.

It does not yet establish the transformation law for reflections across all
coordinate axes or arbitrary improper rotations.

It also uses one controlled geometry.

Therefore the exact physical handedness interpretation remains open.

The composite relation:

`C_ref ≈ -P C P^T`

also requires separate algebraic classification before it can be assigned a
physical meaning.

No Reading Point residue correspondence is introduced.

## Current bridge status

**N4 `C` normalized shape:** SUPPORTED

**N4 lattice normalization `dx*C`:** SUPPORTED

**N4 antisymmetry:** SUPPORTED

**`chi` sign as handedness selector:** REJECTED

**Orientation-mirror oddness:** ROBUST

**Direct spatial parity oddness:** NOT SUPPORTED

**Direct spatial parity evenness:** SUPPORTED IN TESTED GEOMETRY

**Composite relation:** `C_ref ≈ -P C P^T`

**Physical handedness identification:** NOT YET ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Result 021 should classify the combined transformation algebraically.

The next question is:

> What is the action of spatial reflection together with the mu-tau basis
> permutation on `C`, and does that composite action square to the expected
> identity?

The test should keep the ingredients explicit:

- spatial reflection `R`;
- flavour permutation `P`;
- matrix action on `C`.

It should determine whether the composite symmetry is stable across a small
geometry family and whether applying it twice returns the original operator.

Only after that should the audit ask whether this symmetry deserves a
physical handedness interpretation.

## Script

`readingpoint/tests/test_020_n4_C_spatial_reflection.py`
