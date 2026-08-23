# Result 011 — M5 chiral-origin baseline

## Outcome

**SUPPORTED as a conditional M5 orientation mechanism.**

The existing OpenWave M5 chiral-origin program was reproduced from the
Reading Point fork.

The upstream artifact is:

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4b_chiral_origin.py`

The reproduced scan separates three distinct pieces of the M5 construction:

- a nonzero geometric chiral overlap `C`;
- exact achiral handedness degeneracy, `E(+chi) = E(-chi)`;
- a chiral coupling `g_chiral` that activates CP and selects handedness sign.

The result therefore supplies an M5-native orientation mechanism only
conditionally: the orientation selector appears when a chiral substrate
term is present.

## Test domain

The reproduced scan uses:

- `delta = 0.1`
- `chi = 1.2`
- `g_chiral = 0.00, 0.30, 0.60, 0.94, 1.50`

The reported observables are:

- geometric chiral overlap `|C|`
- `delta_CP`
- `theta13`
- handedness-energy splitting `|E(+chi) - E(-chi)|`

## Reproduced scan

| `g_chiral` | `|C|` | `delta_CP` | `theta13` | `|E(+chi)-E(-chi)|` |
| ---: | ---: | ---: | ---: | ---: |
| `0.00` | `0.9447` | `0.0` | `0.000` | `0.000e+00` |
| `0.30` | `0.9447` | `-90.0` | `2.858` | `0.000e+00` |
| `0.60` | `0.9447` | `-90.0` | `5.631` | `0.000e+00` |
| `0.94` | `0.9447` | `-90.0` | `8.581` | `0.000e+00` |
| `1.50` | `0.9447` | `-90.0` | `12.841` | `0.000e+00` |

## Result

The executable Reading Point test confirms:

- geometric chiral overlap: **SUPPORTED**
- `|C|` independent of `g_chiral`: **SUPPORTED**
- achiral handedness degeneracy: **SUPPORTED**
- `g_chiral = 0` CP-conserving baseline: **SUPPORTED**
- nonzero `g_chiral` activates CP in the tested scan: **SUPPORTED**
- achiral physical orientation selector: **ABSENT IN TESTED MODEL**
- chiral orientation selector: **CONDITIONAL ON `g_chiral`**
- Reading Point → M5 physical mapping: **NOT ESTABLISHED**

## Geometric chiral structure

The reproduced overlap remains:

`|C| = 0.9447`

throughout the full `g_chiral` scan.

Thus the loop arrangement already contains a nonzero geometric chiral
overlap before the coupling strength is varied.

The coupling does not create the geometric overlap; it scales the chiral
term acting on that structure.

## Achiral handedness degeneracy

For every tested `g_chiral` value, the underlying achiral loop energies
satisfy:

`E(+chi) = E(-chi)`

to the reported numerical precision.

Equivalently:

`|E(+chi) - E(-chi)| = 0`

throughout the reproduced scan.

The tested achiral M5 Landau-de Gennes energy therefore does not
energetically prefer either handedness.

## CP activation

At:

`g_chiral = 0`

the reproduced result is:

`delta_CP = 0`

`theta13 = 0`

which is the CP-conserving baseline of the tested construction.

At:

`g_chiral = 0.94`

the reproduced result is:

`delta_CP = -90`

`theta13 = 8.581`

so the chiral coupling activates the CP sector in the existing M5
construction.

## Orientation interpretation

Result 009 established that the scalar half-winding sign from
`winding_measure_biax` is basis-orientation dependent.

Result 010 then tested the M5 self-linking candidate `N`, but the naive
`N*s` framing failed to preserve the clean baseline for nonzero `N`.

Result 011 identifies a different M5-native route:

the chiral coupling `g_chiral` can select a handedness sign while acting
on an already nonzero geometric chiral overlap.

However, the achiral theory itself remains handedness-degenerate.

Therefore:

**geometric handed structure:** PRESENT

**achiral energetic handedness preference:** ABSENT

**handedness selection through chiral coupling:** CONDITIONAL

The missing step is the physical origin of the chiral substrate term.

## Relation to Result 003

Result 003 established the mathematical quotient:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

Result 011 does not establish a physical realization of that quotient.

It does not identify:

- a Reading Point residue pair with a handedness state;
- a quaternion coset with the sign of `g_chiral`;
- a winding sign with a mod-30 residue;
- or `g_chiral` with any Reading Point quantity.

The common quotient remains a mathematical structural correspondence.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**M5 geometric chiral overlap:** SUPPORTED

**M5 achiral handedness degeneracy:** SUPPORTED

**M5 achiral physical orientation selector:** ABSENT IN TESTED MODEL

**M5 chiral orientation selector:** CONDITIONAL ON `g_chiral`

**Physical origin of `g_chiral`:** NOT ESTABLISHED HERE

**Physical `Q8/{1,-1}` reduction:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Constraint

Result 011 reproduces the existing M5 chiral-origin construction.

It does not establish that the M5 substrate physically contains the
required chiral or Lifshitz invariant.

It does not derive the sign or magnitude of `g_chiral` from a deeper M5
object.

It does not assign Reading Point structure to the chiral coupling.

The existing M5 program itself leaves the substrate origin of
`g_chiral` as an open question.

## Repository side effects

The upstream script writes:

`openwave/xperiments/m5_liquid_crystal/research/data/m5_11_n4b_chiral_origin_summary.json`

Reading Point Test 011 preserves and restores the original contents of
that upstream file after the baseline run.

Therefore the test leaves no persistent modification to the upstream
OpenWave data artifact.

## Next reading point

Determine whether the current M5 repository already derives or specifies
a chiral / Lifshitz / cholesteric substrate term that can supply
`g_chiral` independently.

The next test should distinguish between:

1. `g_chiral` as a free phenomenological input;
2. `g_chiral` as an explicitly specified M5 substrate term;
3. `g_chiral` as a quantity derived from another M5 invariant.

Only if the coupling is independently grounded should it be reconsidered
as a physical orientation selector for the Reading Point → M5 bridge.

## Script

`readingpoint/tests/test_011_m5_chiral_origin_baseline.py`
