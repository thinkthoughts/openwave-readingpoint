# Result 010 --- M5 self-linking baseline

## Outcome

**REPRODUCED NEGATIVE BASELINE.**

The existing OpenWave M5 self-linking program was executed from the
Reading Point fork.

The upstream artifact is:

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4_topo.py`

The program defines an integer self-linking candidate `N` by adding
`N*s` azimuthal twists to the secondary director framing of a biaxial
loop.

In the upstream construction, integer `N` is required for
single-valuedness and changes sign under reflection. It therefore
provides an explicitly defined, reflection-odd handedness candidate.

The numerical scan reproduces the upstream conclusion that the current
naive `N*s` framing does **not** provide clean topological quantization
while preserving the M5 baseline structure.

## Test domain

The reproduced scan uses:

-   `N = -2, -1, 0, 1, 2`
-   `delta = 0.1`
-   `chi = 0.6`
-   `g_chiral = 1.0`

The reported observables are `theta12`, `theta23`, `theta13`,
`delta_CP`, `J`, and `C_norm`.

## Reproduced scan

     `N`   `theta12`   `theta23`   `theta13`   `delta_CP`
  ------ ----------- ----------- ----------- ------------
    `-2`    `32.958`    `44.543`     `0.374`     `-18.03`
    `-1`    `32.829`    `44.696`     `0.265`     `-18.26`
     `0`    `35.264`    `45.000`     `0.136`     `-90.00`
    `+1`    `32.790`    `45.361`     `0.371`     `-12.97`
    `+2`    `33.326`    `46.204`     `1.259`      `-3.91`

## Result

The executable Reading Point test confirms:

-   M5 self-linking handedness candidate defined: **YES**
-   integer `N` scan reproduced: **PASS**
-   `N = 0` clean TBM/maximal-CP structure: **PASS**
-   tested nonzero `N` preserves the TBM baseline: **NO**
-   `delta_CP` cleanly antisymmetric under `N -> -N`: **NO**
-   clean topological quantization from naive `N*s`: **NOT SUPPORTED**
-   orientation bridge for Result 009: **NOT ESTABLISHED**

The reproduced upstream verdict is:

**INCONCLUSIVE / NEGATIVE for clean topological quantization.**

## Self-linking candidate

The M5 construction supplies more than an arbitrary sign label.

Its proposed framing uses an integer self-linking number `N`, with the
secondary director receiving `N` full twists around the loop azimuth.

Within the construction:

-   `N` must be integer for single-valuedness;
-   reflection reverses the handedness label, `N -> -N`;
-   `N` is therefore an independently specified orientation-sensitive
    candidate rather than a Reading Point label assigned after the fact.

This makes the self-linking program directly relevant to the open
orientation question left by Result 009.

## Failure of the naive framing

The existence of the candidate does not make the current construction
successful.

At `N = 0`, the scan reproduces:

`theta12 = 35.264`

`theta23 = 45.000`

`delta_CP = -90.00`

This is the clean TBM/maximal-CP baseline identified by the upstream
program.

For every tested nonzero `N`, the TBM criterion fails.

The upstream program interprets the naive azimuthal `N*s` twist as
breaking the mu-tau structure rather than cleanly stepping the desired
observables.

The `delta_CP` values also fail the proposed antisymmetry test under
`N -> -N`.

For example:

`N = -1 -> delta_CP = -18.26`

`N = +1 -> delta_CP = -12.97`

These values are neither opposite in sign nor maximal.

## Relation to Result 009

Result 009 established that the opposite winding-sign readouts obtained
from the generic and symmetric half-winding constructions are related by
a fixed global basis transformation.

The sign reported by `winding_measure_biax` therefore cannot by itself
select a physically distinct orientation.

Result 010 asks whether an existing M5 construction already supplies the
missing orientation-sensitive object.

The answer is qualified:

**M5 self-linking handedness candidate:** DEFINED

**Current naive self-linking implementation as a clean physical
orientation selector:** NOT SUPPORTED

Thus Result 010 identifies a genuine M5-native candidate but does not
complete the orientation bridge sought after Result 009.

## Relation to Result 003

Result 003 established:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

That remains a supported mathematical quotient correspondence.

Result 010 does not promote that quotient to a physical Reading Point →
M5 mapping.

In particular, it does not establish that self-linking values, winding
signs, quaternion cosets, or mod-30 residue pairs should be identified
with one another.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**M5 self-linking integer candidate:** DEFINED

**M5 reflection-odd handedness candidate:** DEFINED

**Naive `N*s` topological quantization:** NOT SUPPORTED

**Basis-independent physical orientation selector:** NOT YET ESTABLISHED

**Full physical `Q8/{1,-1}` reduction:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Constraint

Result 010 reproduces the behavior of the existing `m5_11_n4_topo.py`
construction.

It does not claim that the failure of the naive `N*s` framing rules out
self-linking as a useful M5 topological observable.

The upstream program itself identifies a more specific open requirement:
a self-linking definition applied consistently with the loop
orientations while respecting the mu-tau structure.

No new self-linking construction is introduced by this Reading Point
test.

No Reading Point residue is assigned to `N`.

No quaternion element or coset is assigned to `N`.

## Repository side effects

The upstream M5 script writes:

`openwave/xperiments/m5_liquid_crystal/research/data/m5_11_n4_topo_summary.json`

The Reading Point Test 010 wrapper preserves and restores the original
contents of that upstream artifact after the baseline run.

Therefore the reproduced test leaves no persistent modification to the
upstream OpenWave data file.

## Next reading point

Inspect the existing M5 chiral-overlap and handedness-energy machinery
for an orientation-sensitive observable that does not rely on the failed
naive `N*s` framing.

The next candidate should remain M5-native and should be evaluated on
its own existing criteria before any Reading Point correspondence is
introduced.

A useful next question is:

Does the existing M5 chiral-overlap or handedness-energy machinery
provide a basis-invariant orientation observable that preserves the
clean baseline better than the naive self-linking construction?

## Script

`readingpoint/tests/test_010_m5_self_linking_baseline.py`
