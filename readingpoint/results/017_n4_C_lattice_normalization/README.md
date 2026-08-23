# Result 017 — N4 `C` lattice normalization

## Outcome

**`dx * C` SUPPORTED AS THE LATTICE NORMALIZATION AMONG THE TESTED INTEGER POWERS.**

Result 016 showed that the normalized N4 chiral operator

`C_hat = C / ||C||_F`

converges in shape under controlled lattice refinement, while the raw
magnitude `||C||_F` grows with resolution.

Result 017 tests whether that raw scaling is explained by the lattice
normalization implicit in the current implementation of
`chiral_overlap()`.

The result supports:

`C_continuum ~ dx * C_raw`

for the tested refinement family.

## Why `dx * C` is the candidate normalization

The current N4 `chiral_overlap()` uses two central-difference gradients
with the helper `_grads()` evaluated at its default:

`dx = 1`.

It then directly sums the resulting lattice-cell contributions.

For a fixed physical field sampled with physical lattice spacing `dx`:

- each coded finite difference contributes one factor of `dx` relative to
  the physical derivative;
- the product of two coded gradients therefore contributes `dx^2`;
- the number of lattice cells in a fixed physical volume scales as
  `dx^-3`.

Thus continuum counting predicts:

`C_raw ~ dx^-1`

and therefore suggests:

`dx * C_raw`

as the candidate lattice-normalized operator.

Result 017 measures this instead of assuming it.

## Fixed physical geometry

The refinement holds:

`R_loop = 9.0`

`core = 2.0`

with:

`alpha = 0.6`

`delta = 0.1`

`chi = 0.6`

`q = 0.5`

The reference grid is:

`n = 40`, `dx = 1`.

For each refinement,

`dx = 40 / n`.

## Resolution sweep

| `n` | `dx` | `||C_raw||_F` | `||dx*C||_F` |
| ---: | ---: | ---: | ---: |
| 24 | 1.666667 | 1.698142 | 2.830236 |
| 32 | 1.250000 | 2.145233 | 2.681542 |
| 40 | 1.000000 | 2.619763 | 2.619763 |
| 48 | 0.833333 | 3.104983 | 2.587486 |

The raw norm grows strongly with refinement.

The `dx`-normalized norm is much flatter and approaches a stable value.

## Raw scaling fit

A log-log fit gives:

`||C_raw||_F ~ dx^-0.8702`

The continuum-counting prediction is:

`C_raw ~ dx^-1`.

The measured exponent is reasonably close over this finite refinement
range, but `-0.8702` is retained only as a diagnostic.

It is not promoted to an asymptotic scaling law.

## Candidate normalization comparison

The test compares integer powers:

`dx^p * C`

for:

`p = 0, 1, 2, 3`.

Measured relative spreads of the Frobenius norm are:

| normalization | relative spread |
| --- | ---: |
| `C` | `5.881368e-01` |
| `dx*C` | `9.058688e-02` |
| `dx^2*C` | `7.974542e-01` |
| `dx^3*C` | `1.473109e+00` |

The best tested power is:

`p = 1`.

Therefore:

**`dx * C` is strongly preferred among the tested integer powers.**

## Convergence of the normalized magnitude

The measured values are:

`2.830236`

`2.681542`

`2.619763`

`2.587486`.

Successive relative changes are:

`n=24 -> 32 : 5.545128e-02`

`n=32 -> 40 : 2.358165e-02`

`n=40 -> 48 : 1.247449e-02`.

The changes decrease monotonically.

Thus the `dx*C` magnitude is not merely flatter than the raw norm; it is
also showing convergence under the tested refinement.

## Antisymmetry

The N4 matrix remains antisymmetric throughout the refinement.

Therefore the lattice normalization does not alter the defining symmetry
class of the effective operator.

## Result

The executable test supports:

**Raw `C` resolution independent:** NO

**Continuum-counting prediction:** `C_raw ~ dx^-1`

**Best tested integer normalization:** `dx * C`

**`dx*C` magnitude convergence:** SUPPORTED IN TESTED REFINEMENT

**N4 lattice normalization:** SUPPORTED

**Deeper microscopic provenance:** NOT ESTABLISHED

This significantly strengthens the effective-operator status of N4 `C`.

Result 016 established a stable normalized operator shape.

Result 017 now establishes a natural lattice normalization for its
magnitude.

## Relation to Result 016

Result 016 found:

- antisymmetry stable under refinement;
- normalized operator shape converging;
- raw magnitude resolution dependent.

Result 017 explains the raw resolution dependence consistently with the
derivative-and-sum structure of the implementation.

Multiplication by `dx` removes most of the refinement dependence and
produces a converging magnitude.

Thus the two results together support a continuum-like effective operator:

`C_eff = dx * C_raw`

within the tested family.

## What this does not establish

Result 017 does not establish the microscopic origin of N4 `C`.

It does not connect `C` to the P2 Lifshitz term, to the P1/Faber
connection, or to another underlying M5 interaction.

It also does not determine an absolute physical unit or coupling scale for
`g_chiral`.

The result is a numerical lattice-normalization statement about the
effective operator already implemented in N4.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**N4 `C` antisymmetry:** SUPPORTED

**N4 `C` normalized shape:** SUPPORTED AS CONVERGING

**N4 lattice normalization:** `dx * C` SUPPORTED

**N4 effective-operator status:** STRENGTHENED

**N4 microscopic provenance:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Result 018 should test the defining physical interpretation of the operator:

> Does `C` transform with the expected handedness/reflection behavior?

The next control should compare the relevant mirror or

`chi -> -chi`

transformation and test whether:

- `C` reverses sign as expected;
- `||dx*C||` is preserved;
- antisymmetry is preserved;
- and the normalized operator changes by the expected sign rather than
  changing shape arbitrarily.

That is the next requirement before treating `C` as a robust chiral
effective observable.

## Script

`readingpoint/tests/test_017_n4_C_lattice_normalization.py`
