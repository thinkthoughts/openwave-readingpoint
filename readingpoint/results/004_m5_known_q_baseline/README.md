# Result 004 --- M5 known-q baseline

## Outcome

**SUPPORTED as an M5 numerical baseline.**

The existing OpenWave M5 synthetic known-q validation was executed from
the Reading Point fork.

The upstream artifact is:

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_20_1_b_seeds.py`

## Reproduced gates

The run reports:

`B0  PASS`\
`B0b PASS`\
`B1  PASS`\
`B2  PASS`

The target for this Reading Point result is **B1**, the synthetic
known-q validation of the M5 biaxial eigenframe-winding measurement.

## Result

The executable Reading Point test confirms:

-   upstream M5 artifact runnable: **PASS**
-   B1 synthetic known-q gate: **PASS**
-   all reported upstream gates: **PASS**
-   M5 known-q winding baseline: **SUPPORTED**

This establishes that the existing M5 measurement baseline can be
reproduced from the Reading Point fork.

## Scope

Result 004 does not assign mod-30 residues to quaternion states.

It does not establish:

`{7,13} ↔ {i,-i}`

or any other particular assignment.

It also does not establish a physical correspondence between the Reading
Point quotient and M5.

The result establishes only that an existing M5 numerical instrument is
available and passes its own synthetic known-q validation.

## Relation to Result 003

Result 003 established the mathematical quotient relation:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

Result 004 supplies an independently runnable M5 measurement baseline.

These results remain separate:

**Result 003:** shared mathematical structure --- SUPPORTED\
**Result 004:** M5 numerical baseline --- SUPPORTED\
**Reading Point → M5 physical mapping:** NOT ESTABLISHED

## Next reading point

Test whether the common `C2 × C2` quotient from Result 003 can be
related to an output of the M5 measurement machinery without choosing an
arbitrary residue-to-quaternion pairing.

A successful next test must obtain its M5 side from the existing
measurement machinery rather than assigning quaternion labels by hand.

## Script

`readingpoint/tests/test_004_m5_known_q_baseline.py`
