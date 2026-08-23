# Result 008 — M5 half-winding seed-convention control

## Outcome

**SEED-CONVENTION DEPENDENCE SUPPORTED.**

Result 005 found that the current M5 implementation returns the same
measured winding for synthetic positive and negative half-winding inputs:

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

| Convention | `q = +0.5` | `q = -0.5` | Behavior |
| --- | ---: | ---: | --- |
| current OpenWave | `+0.5` | `+0.5` | SIGN_IDENTIFIED |
| generic | `-0.5` | `+0.5` | SIGN_DISTINGUISHED |
| symmetric | `+0.5` | `-0.5` | SIGN_DISTINGUISHED |

Each result was reproduced at read radii:

`r = 3, 4, 5, 6`

The out-of-plane mixing monitor remained zero throughout the test.

## Current OpenWave convention

The current M5 seed contains a special branch for positive half-winding:

```python
if abs(q - 0.5) < 1e-12:
    n1, n3 = np.cos(0.5 * chi), np.sin(0.5 * chi)
else:
    n1, n3 = np.sin(q * chi), np.cos(q * chi)
