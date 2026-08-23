# Result 019 — N4 `C` mirror-oddness robustness

## Outcome

**MIRROR ODDNESS ROBUST ACROSS THE TESTED GEOMETRY FAMILY.**

Result 018 found, at one controlled geometry, that:

- `C` is approximately invariant under `chi -> -chi`;
- the mu-tau mirror/order swap transforms `C` exactly by the basis permutation
  `P C P^T`;
- and that transformed matrix is also approximately equal to `-C`.

Result 019 tests whether those behaviors persist across a broader family of
N4 geometries.

They do.

## Tested family

The test holds fixed:

`n = 40`

`dx = 1`

`R_loop = 9`

`core_vox = 2`

`q = 0.5`

and varies:

`alpha = 0.4, 0.6, 0.8`

`delta = 0.05, 0.10, 0.20`

`chi = 0.30, 0.60, 1.00`

for a total of:

`27`

geometry points.

For each point the test evaluates standard and mirrored alpha ordering for
both signs of `chi`.

## Basis covariance

The exact structural control is:

`C_mirror = P C P^T`

where `P` swaps the mu and tau flavour basis labels.

Across all 27 tested geometry points:

**maximum basis-covariance error:** `0.000000e+00`

Therefore:

**Basis covariance across geometry: SUPPORTED**

This remains separate from the approximate mirror-oddness question.

## Mirror oddness

The mirror-oddness diagnostic is:

`||P C P^T + C|| / ||C||`

with threshold:

`1.0e-03`.

All tested points satisfy the criterion:

`27 / 27`.

Measured error range:

- minimum: `1.018361e-06`
- median: `5.841212e-06`
- maximum: `2.159673e-05`

Therefore:

**Mirror oddness across geometry: ROBUST ACROSS TESTED FAMILY**

The sign reversal observed in Result 018 is therefore not a single-point
numerical accident.

## Screw-sign reversal

The same geometry family tests:

`chi -> -chi`.

The approximate-invariance diagnostic is:

`||C(-chi) - C(+chi)|| / ||C(+chi)||`.

All 27 tested points satisfy the `1.0e-03` threshold.

Measured errors are:

- minimum: `1.077438e-06`
- median: `5.902615e-06`
- maximum: `2.184209e-05`

Therefore:

**`chi -> -chi` approximate invariance: ROBUST ACROSS TESTED FAMILY**

## Screw-sign oddness

The competing hypothesis,

`C(-chi) ≈ -C(+chi)`,

is decisively unsupported.

The oddness diagnostic remains essentially:

`2`

throughout the family:

- minimum: `1.999997`
- median: `1.999999`
- maximum: `2.000000`

Therefore:

**`chi`-sign oddness: REJECTED IN THE TESTED FAMILY**

This strengthens Result 018's conclusion that the sign of `chi` is not the
operation that reverses the N4 effective chiral matrix.

## Magnitude preservation

The lattice-normalized magnitude from Result 017 is preserved under
`chi -> -chi`.

All 27 points satisfy the `1.0e-03` threshold.

Relative differences are:

- minimum: `1.647260e-07`
- median: `8.178009e-07`
- maximum: `2.726370e-06`

Therefore:

**Screw-reversal magnitude preservation: ROBUST ACROSS TESTED FAMILY**

## Antisymmetry

The maximum antisymmetry error across all tested cases is:

`8.992806e-15`

Therefore:

**N4 `C` antisymmetry: PASS**

## Result

The executable test establishes:

**Basis covariance:** SUPPORTED

**Mirror oddness:** ROBUST ACROSS TESTED FAMILY

**`chi -> -chi` approximate invariance:** ROBUST ACROSS TESTED FAMILY

**`chi -> -chi` oddness:** REJECTED

**Magnitude preservation under `chi` reversal:** ROBUST

**Antisymmetry:** PASS

The tested sign-reversing transformation is therefore associated with the
mu-tau mirror/orientation operation rather than with the sign of the screw
parameter `chi`.

## Relation to Result 018

Result 018 distinguished two operations:

1. screw-sign reversal;
2. mirror/orientation swap.

At the original point, `chi -> -chi` left `C` approximately unchanged, while
the mirror transformation sent `C` approximately to `-C`.

Result 019 shows that both observations persist throughout the tested
alpha-delta-chi family.

This substantially strengthens the effective transformation law of `C`.

## Relation to Results 016–017

Result 016 established that the normalized shape of `C` converges under
lattice refinement.

Result 017 supported:

`C_eff = dx * C_raw`

as the lattice normalization among the tested integer powers.

Result 019 now adds a robust transformation property to that effective
operator:

`P C_eff P^T ≈ -C_eff`

throughout the tested geometry family.

Thus the effective-operator characterization now includes:

- converging shape;
- lattice-normalized magnitude;
- antisymmetry;
- and robust mirror oddness under the tested orientation transformation.

## Constraint

The tested mirror operation is still implemented through the mu-tau
orientation swap and the corresponding flavour-basis permutation.

It is not yet an independently applied spatial reflection of the complete M5
tensor field.

Therefore Result 019 does **not** yet establish that `C` is reflection-odd
under a physical spatial parity operation.

It establishes robust oddness under the tested mirror/orientation
transformation.

Likewise, the result does not establish a microscopic M5 provenance for `C`.

No Reading Point residue correspondence is introduced.

## Current bridge status

**N4 `C` normalized shape:** SUPPORTED

**N4 lattice normalization `dx*C`:** SUPPORTED

**N4 antisymmetry:** SUPPORTED

**`chi` sign as `C` handedness selector:** REJECTED IN TESTED FAMILY

**Mirror basis covariance:** SUPPORTED

**Mirror oddness under tested orientation swap:** ROBUST

**Physical spatial-reflection oddness:** NOT YET TESTED

**Physical handedness identification:** NOT YET ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Result 020 should apply an actual spatial reflection to the M5 loop fields.

For example, a reflection such as:

`x -> -x`

must transform both spatial coordinates and tensor components consistently.

The test should then ask whether the reflected, lattice-normalized chiral
operator obeys:

`C_reflected ≈ -C`

after accounting for any independently required flavour-basis
transformation.

This is stronger than the current mu-tau orientation swap.

If it passes, the N4 effective operator would have direct evidence of genuine
spatial reflection oddness.

If it fails, the robust sign reversal established by Results 018–019 should
remain classified specifically as an orientation/basis property rather than
physical parity.

## Script

`readingpoint/tests/test_019_n4_C_mirror_oddness_robustness.py`
