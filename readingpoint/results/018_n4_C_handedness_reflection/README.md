# Result 018 — N4 `C` handedness / reflection behavior

## Outcome

**SCREW-SIGN ODDNESS NOT SUPPORTED; MIRROR BASIS COVARIANCE SUPPORTED.**

Result 018 tests how the existing N4 chiral-overlap matrix `C` transforms
under two distinct operations:

1. screw reversal: `chi -> -chi`;
2. swapping the `+alpha` and `-alpha` flavour-loop orientations.

The two operations are not treated as physically equivalent.

## Tested geometry

The controlled run used:

`n = 40`

`dx = 1`

`alpha = 0.6`

`delta = 0.1`

`|chi| = 0.6`

`q = 0.5`

`R_loop = 9`

`core_vox = 2`

Four cases were evaluated:

- A: standard alpha ordering, `chi = +0.6`
- B: standard alpha ordering, `chi = -0.6`
- C: mirrored alpha ordering, `chi = +0.6`
- D: mirrored alpha ordering, `chi = -0.6`

## Screw reversal

The test compares:

`C(-chi)` with `-C(+chi)`

and separately with:

`C(+chi)`.

Measured oddness error:

`1.999999`

Measured evenness error:

`8.371447e-06`

Thus `C(-chi)` is approximately equal to `C(+chi)`, not to `-C(+chi)`.

The normalized even-shape error is:

`8.246263e-06`

while the normalized odd-shape error is:

`2.000000`.

The lattice-normalized magnitudes are also preserved:

`||dx*C(-chi)|| / ||dx*C(+chi)|| = 0.999998557649`

with relative magnitude difference:

`1.442351e-06`.

Therefore:

**Screw-sign reversal `chi -> -chi` does not reverse `C` in the tested geometry.**

**Approximate chi-evenness is supported.**

## Mirror orientation swap

The mirror-order control swaps:

`mu: +alpha -> -alpha`

`tau: -alpha -> +alpha`.

Let `P` be the permutation matrix that swaps the mu and tau flavour basis
labels.

The exact covariance relation is:

`C_mirror = P C P^T`.

Measured basis-covariance errors are:

`0.000000e+00`

for both signs of `chi`.

Therefore:

**Mirror basis covariance is exactly supported in the tested implementation.**

## Mirror sign reversal

The test separately asks whether the basis-transformed matrix is also
approximately equal to `-C`.

Measured relative errors are:

`8.129252e-06` for `chi = +0.6`

`8.129264e-06` for `chi = -0.6`.

The mirror operation also preserves the matrix norm exactly in the tested
run.

Therefore:

**Mirror-induced `C -> -C` is supported approximately in the tested geometry.**

This approximate sign reversal is distinct from the exact basis-covariance
statement.

## Result

The executable test supports:

**Antisymmetry:** PASS

**`chi -> -chi` gives `C -> -C`:** NOT SUPPORTED

**`chi -> -chi` leaves `C` approximately invariant:** SUPPORTED

**Screw-reversal magnitude preservation:** SUPPORTED

**Mirror basis covariance `P C P^T`:** SUPPORTED

**Mirror-induced approximate sign reversal:** SUPPORTED IN TESTED GEOMETRY

**Physical handedness identification:** NOT YET ESTABLISHED

## Interpretation

The result changes the interpretation of the screw parameter.

Although the N4 source describes `chi` as a screw parameter associated with
handedness, the effective operator `C` is approximately even under
`chi -> -chi` in this tested geometry.

The sign of `chi` therefore does not, by itself, define the operation that
reverses the N4 chiral matrix.

By contrast, swapping the `+alpha` and `-alpha` flavour-loop orientations
transforms `C` exactly by the expected mu-tau basis permutation.

In this geometry that mirror transformation is also approximately equivalent
to:

`C -> -C`.

Thus Result 018 distinguishes:

- screw-sign reversal;
- flavour-basis mirror transformation;
- and approximate sign reversal of the effective chiral operator.

## Relation to Results 016–017

Result 016 supported convergence of the normalized N4 `C` operator shape.

Result 017 supported:

`C_eff = dx * C_raw`

as the lattice normalization among the tested integer powers.

Result 018 now tests transformation behavior of that effective operator.

The operator remains antisymmetric and magnitude-stable, but its sign is not
controlled by `chi -> -chi` in the tested geometry.

## Constraint

The approximate chi-evenness and mirror sign reversal are established only
for the tested geometry.

The exact statement from this result is the basis covariance:

`C_mirror = P C P^T`.

The further relation:

`P C P^T ≈ -C`

is a numerical property of this tested configuration and must be checked
across a broader geometry family before it can be interpreted as robust
mirror oddness.

No physical handedness observable is yet established.

No Reading Point residue correspondence is introduced.

## Current bridge status

**N4 `C` normalized shape:** SUPPORTED

**N4 lattice normalization `dx*C`:** SUPPORTED

**N4 antisymmetry:** SUPPORTED

**`chi` sign as `C` handedness selector:** NOT SUPPORTED

**Mirror basis covariance:** SUPPORTED

**Approximate mirror sign reversal:** SUPPORTED IN TESTED GEOMETRY

**Physical handedness identification:** NOT YET ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Result 019 should test whether the approximate mirror relation

`P C P^T ≈ -C`

persists across controlled changes in:

- `alpha`;
- `delta`;
- `chi`;
- loop radius;
- core size;
- and resolution.

Two diagnostics must remain separate:

1. exact basis covariance:
   `C_mirror = P C P^T`;

2. mirror oddness:
   `P C P^T ≈ -C`.

If the second relation remains stable across geometry changes, then the N4
effective operator may support a robust mirror-odd interpretation.

If it does not, the sign reversal should remain classified as a special
property of the tested geometry.

## Script

`readingpoint/tests/test_018_n4_C_handedness_reflection.py`
