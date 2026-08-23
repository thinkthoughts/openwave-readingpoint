# Result 007 — M5 winding-seed closure

## Outcome

**SUPPORTED.**

The M5 winding seed was tested for closure after one complete circuit
around the loop.

Because the M5 tensor field is apolar, closure does not require the
director itself to return with the same orientation.

Both

`n → n`

and

`n → -n`

produce the same quadratic apolar tensor field.

## Tested winding values

The synthetic probes were:

`q = -1, -0.5, -0.25, +0.25, +0.5, +1`

The measured endpoint behavior was:

| `q` | Director after one circuit | Apolar field |
| ---: | --- | --- |
| `-1.0` | `n → n` | CLOSED |
| `-0.5` | `n → -n` | CLOSED |
| `-0.25` | no `±n` return | NOT CLOSED |
| `+0.25` | no `±n` return | NOT CLOSED |
| `+0.5` | `n → -n` | CLOSED |
| `+1.0` | `n → n` | CLOSED |

The numerical tensor closure errors for the closed cases were at
approximately machine precision.

The quarter-winding cases produced tensor closure error `1.0`.

## Result

The test establishes two forms of closure in the synthetic M5 seed:

### Integer winding

For `q = ±1` the director returns to its original orientation:

`n → n`

The corresponding apolar tensor field therefore closes.

### Half-integer winding

For `q = ±0.5` the director returns with reversed orientation:

`n → -n`

Because the tensor representation identifies `n` and `-n`, the apolar
field still closes after one circuit.

### Quarter winding

For `q = ±0.25` the director returns to neither `n` nor `-n`.

The resulting apolar tensor therefore does not close after one circuit.

## Relation to Result 006

Result 006 used `|q| = 0.25`, `0.5`, and `1.0` as synthetic instrument
probes.

It found:

`|q| = 0.25 → approximately 0`

`|q| = 0.5 → sign identified`

`|q| = 1.0 → sign distinguished`

Result 007 now adds an important qualification.

The `q = ±0.25` seeds do not define closed apolar fields after one
circuit.

Their zero readout in Result 006 should therefore be interpreted as
instrument behavior on **non-closing synthetic probes**, rather than
evidence for a quarter-winding topological sector.

The `q = ±0.5` and `q = ±1` probes satisfy the basic apolar closure
condition and remain appropriate for further instrument analysis.

## Relation to Result 005

Result 005 found:

`q_input = +0.5 → q_meas = +0.5`

`q_input = -0.5 → q_meas = +0.5`

Result 007 confirms that both half-winding inputs correspond to closed
apolar fields.

This strengthens the reason to investigate the half-winding
sign-identification result.

It does not yet establish that the identification represents the full
M5 `Q8/{1,-1}` quotient.

## Seed implementation

The current OpenWave `winding_director()` contains an asymmetric code
path:

```python
if abs(q - 0.5) < 1e-12:
    n1, n3 = np.cos(0.5 * chi), np.sin(0.5 * chi)
else:
    n1, n3 = np.sin(q * chi), np.cos(q * chi)
