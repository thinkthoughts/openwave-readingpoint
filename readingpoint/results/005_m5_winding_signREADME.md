# Result 005 --- M5 winding sign identification

## Outcome

**SUPPORTED IN THE TESTED SECTOR.**

The current M5 biaxial eigenframe-winding observable was evaluated on
synthetic inputs with opposite winding signs.

For every tested case:

`q_input = +0.5 → q_meas = +0.5`

`q_input = -0.5 → q_meas = +0.5`

The tested observable therefore does not distinguish the sign of the
input winding in this configuration family.

## Test domain

The comparison covered:

-   `delta = 0.1, 0.3, 0.5`
-   `pair_1d`
-   `pair_d0`
-   read radii `3, 4, 5, 6`
-   input windings `+0.5` and `-0.5`

All tested cases passed the sign-identification criterion.

The out-of-plane mixing monitor remained zero in the reported runs.

## Result

The executable test confirms:

-   positive winding measurable: **PASS**
-   negative winding measurable: **PASS**
-   winding magnitude preserved: **PASS**
-   input sign distinguished: **NO**
-   input sign identified by this observable: **SUPPORTED**

## Relation to Result 003

Result 003 established the mathematical quotient:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

Result 005 adds an operational M5 observation:

the current eigenframe-winding read identifies `+q` and `-q` for the
tested half-winding configurations.

This is consistent with a sign-quotiented reading of the observable.

## Constraint

This result does **not** establish that the full M5 quaternion topology
is physically reduced to:

`Q8 / {1,-1}`

The test covers one numerical observable, one winding magnitude, and a
specified family of synthetic configurations.

It also does not assign any Reading Point residue pair to a particular
quaternion coset.

## Current bridge status

**Shared mathematical quotient:** SUPPORTED

**M5 sign identification for tested winding observable:** SUPPORTED

**Full physical Q8/{1,-1} reduction:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Test whether the observed sign identification persists beyond
`|q| = 0.5` and whether another independently defined M5 observable
exposes the same four-way quotient structure.

The next bridge must remain non-arbitrary: no residue-to-quaternion
labels should be assigned by hand.

## Script

`readingpoint/tests/test_005_m5_winding_sign.py`
