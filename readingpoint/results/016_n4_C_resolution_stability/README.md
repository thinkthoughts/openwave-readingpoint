# Result 016 — N4 `C` resolution stability

## Outcome

**NORMALIZED N4 CHIRAL-OPERATOR SHAPE SUPPORTED AS CONVERGING UNDER THE TESTED REFINEMENT.**

The existing N4 chiral-overlap matrix `C` was evaluated across a controlled
resolution sweep while the loop radius and core size were held fixed relative
to the lattice size.

The result separates two questions:

1. whether the **dimensionless operator shape** `C_hat = C / ||C||_F` stabilizes;
2. whether the **raw magnitude** `||C||_F` is already resolution independent.

The normalized operator shape shows clear monotonic stabilization. The raw
magnitude does not.

## Controlled refinement

The tested resolutions were:

`n = 24, 32, 40, 48`

with fixed dimensionless geometry:

`R_loop / n = 0.225`

`core_vox / n = 0.050`

and fixed model parameters:

`alpha = 0.6`, `delta = 0.1`, `chi = 0.6`, `q = 0.5`.

## Resolution sweep

| `n` | `R_loop` | `core_vox` | `||C||_F` | antisymmetry error | distance to normalized `n=48` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 24 | 5.4 | 1.2 | 1.698142 | `4.441e-15` | `3.018033e-02` |
| 32 | 7.2 | 1.6 | 2.145233 | `2.220e-15` | `1.264968e-02` |
| 40 | 9.0 | 2.0 | 2.619763 | `2.823e-15` | `4.549089e-03` |
| 48 | 10.8 | 2.4 | 3.104983 | `1.263e-15` | `0` |

Antisymmetry remains at machine precision throughout the refinement.

## Pairwise operator convergence

The Frobenius distance between successive normalized matrices is:

`n=24 -> 32 : 1.753148e-02`

`n=32 -> 40 : 8.100647e-03`

`n=40 -> 48 : 4.549089e-03`

The refinement changes decrease monotonically.

Relative to the finest tested matrix, the normalized distances are:

`n=24 : 3.018033e-02`

`n=32 : 1.264968e-02`

`n=40 : 4.549089e-03`

`n=48 : 0`

This supports convergence of the **shape** of `C` in the tested family.

## Raw normalization

The raw Frobenius norm increases from `1.698142` at `n=24` to `3.104983`
at `n=48`.

A diagnostic log-log fit gives:

`||C||_F ~ n^0.8702`

This exponent should not be treated as an established law. The supported
conclusion is simply:

**Raw `C` magnitude is resolution dependent in the tested implementation.**

## Result

The executable test supports:

**`C` finite across refinement:** YES

**`C` nonzero across refinement:** YES

**`C` antisymmetric across refinement:** PASS

**Normalized `C` operator shape:** CONVERGING IN TESTED FAMILY

**Raw `C` normalization:** RESOLUTION DEPENDENT

**Physical normalization:** NOT ESTABLISHED

This strengthens the status of N4 `C`: its relative three-flavour structure
is not merely a single-grid artifact in the tested refinement family.

## Relation to Results 013–015

Result 013 found that N4 `C` differs from the P2 Lifshitz operator in
differential order, tensor contraction, and explicit normalization.

Result 014 established that N4 `C` is a nonzero antisymmetric operator and
cannot be generated through the ordinary N3 scalar-energy Hessian route.

Result 015 left `C` as a separately defined effective N4 operator whose
microscopic M5 provenance remains unestablished.

Result 016 now supplies the first direct robustness result:

**N4 `C` has a converging normalized operator shape under controlled lattice
refinement.**

## Constraint

Result 016 applies only to the tested refinement family with fixed
`R_loop/n`, `core_vox/n`, `alpha`, `delta`, `chi`, and `q`.

It does not establish convergence for arbitrary loop geometries or parameter
choices.

It also does not establish a physical normalization for raw `C`.

The fitted exponent `0.8702` is diagnostic only.

No Reading Point residue correspondence is introduced.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**N4 `C` antisymmetry:** SUPPORTED

**N4 normalized operator shape under refinement:** SUPPORTED AS CONVERGING

**N4 raw magnitude:** RESOLUTION DEPENDENT

**N4 physical normalization:** NOT ESTABLISHED

**N4 microscopic M5 provenance:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Result 017 should address normalization directly:

> What explicit lattice-spacing or volume normalization makes the raw N4
> chiral-overlap magnitude converge, if such a normalization exists?

The normalization should be measured rather than assumed.

## Script

`readingpoint/tests/test_016_n4_C_resolution_stability.py`
