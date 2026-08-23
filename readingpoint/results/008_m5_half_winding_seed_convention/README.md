# Result 008 --- M5 half-winding seed-convention control

## Outcome

**SEED-CONVENTION DEPENDENCE SUPPORTED.**

Result 005 found that the current M5 implementation returns the same
measured winding for synthetic positive and negative half-winding
inputs:

`+0.5 → +0.5`

`-0.5 → +0.5`

Result 008 controls for the asymmetric seed construction used by the
current OpenWave `winding_director()` implementation.

When positive and negative half-windings are constructed using matched
seed conventions, the existing M5 winding instrument distinguishes their
signs.

## Tested conventions

Three half-winding seed conventions were passed through the same
`winding_measure_biax` observable.

  Convention           `q = +0.5`   `q = -0.5` Behavior
  ------------------ ------------ ------------ --------------------
  current OpenWave         `+0.5`       `+0.5` SIGN_IDENTIFIED
  generic                  `-0.5`       `+0.5` SIGN_DISTINGUISHED
  symmetric                `+0.5`       `-0.5` SIGN_DISTINGUISHED

Each result was reproduced at read radii:

`r = 3, 4, 5, 6`

The out-of-plane mixing monitor remained zero throughout the test.

## Current OpenWave convention

The current M5 seed contains a special branch for positive half-winding:

``` python
if abs(q - 0.5) < 1e-12:
    n1, n3 = np.cos(0.5 * chi), np.sin(0.5 * chi)
else:
    n1, n3 = np.sin(q * chi), np.cos(q * chi)
```

Therefore:

`q = +0.5`

uses the special `cos/sin` construction, while:

`q = -0.5`

uses the generic `sin/cos` construction.

Under this current convention the instrument returns:

`+0.5 → +0.5`

`-0.5 → +0.5`

and therefore identifies the two input signs.

## Generic control

The generic control uses:

``` text
n = (sin(qχ), cos(qχ))
```

for both signs.

The measured response is:

`+0.5 → -0.5`

`-0.5 → +0.5`

The signs are distinguished.

## Symmetric control

The symmetric control uses:

``` text
n = (cos(qχ), sin(qχ))
```

for both signs.

The measured response is:

`+0.5 → +0.5`

`-0.5 → -0.5`

Again, the signs are distinguished.

The difference in overall orientation between the generic and symmetric
controls is convention-dependent. The important result here is that both
matched conventions preserve a distinction between the two input signs.

## Relation to Result 007

Result 007 established that both positive and negative half-winding
seeds satisfy apolar closure:

`n → -n`

after one complete circuit.

Thus all half-winding constructions tested here satisfy the same basic
closed-field condition.

Apolar closure alone therefore does not force the current numerical
identification:

`q ~ -q`

The sign response depends on how the half-winding seed is constructed.

## Qualification of Result 005

Result 005 remains a valid reproduction of the current OpenWave
implementation.

However, Result 008 changes its interpretation.

The Result 005 observation:

`+0.5 → +0.5`

`-0.5 → +0.5`

should be treated as **current seed-convention behavior**, rather than
evidence that the M5 winding observable generally identifies positive
and negative half-windings.

Under matched seed conventions, the same observable distinguishes the
two signs.

## Relation to Result 003

Result 003 established the mathematical quotient:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

That mathematical result remains unchanged.

Result 008 removes the proposed numerical shortcut from the current M5
half-winding measurement to a physical `q ~ -q` identification.

Therefore the common quotient remains a mathematical structural result.

A physical realization of the `Q8/{1,-1}` reduction in M5 has not been
established by the winding measurement.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**M5 half-winding apolar closure:** SUPPORTED

**Current OpenWave half-winding sign identification:** REPRODUCED

**Seed-convention dependence:** SUPPORTED

**General M5 `q ~ -q` identification:** NOT SUPPORTED

**Physical `Q8/{1,-1}` reduction:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Constraint

This test is a numerical control of the current M5 seed and winding
instrument.

It does not select which seed convention is physically preferred.

It does not assign Reading Point residues to M5 states.

It does not establish that either half-winding sign corresponds to a
particular quaternion element.

## Next reading point

Determine which half-winding convention follows from the intended M5
biaxial order-parameter topology rather than from a numerical seed
choice.

The next test should inspect the existing M5 theoretical and numerical
construction for an independently specified orientation, frame,
composition, or transport rule that determines the meaning of the
positive and negative half-winding classes.

Only after that convention is fixed should the physical relationship to
the `Q8/{1,-1}` quotient be reconsidered.

## Script

`readingpoint/tests/test_008_m5_half_winding_seed_convention.py`
