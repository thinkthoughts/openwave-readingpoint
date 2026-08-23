# Result 007 --- M5 winding-seed closure

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

        `q` Director after one circuit   Apolar field
  --------- ---------------------------- --------------
     `-1.0` `n → n`                      CLOSED
     `-0.5` `n → -n`                     CLOSED
    `-0.25` no `±n` return               NOT CLOSED
    `+0.25` no `±n` return               NOT CLOSED
     `+0.5` `n → -n`                     CLOSED
     `+1.0` `n → n`                      CLOSED

The numerical tensor closure errors for the closed cases were at
approximately machine precision.

The quarter-winding cases produced tensor closure error `1.0`.

## Result

The test establishes two forms of closure in the synthetic M5 seed.

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

Result 007 adds an important qualification.

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

It does not establish that the identification represents the full M5
`Q8/{1,-1}` quotient.

## Seed implementation

The current OpenWave `winding_director()` contains an asymmetric code
path:

``` python
if abs(q - 0.5) < 1e-12:
    n1, n3 = np.cos(0.5 * chi), np.sin(0.5 * chi)
else:
    n1, n3 = np.sin(q * chi), np.cos(q * chi)
```

Therefore `q = +0.5` uses the special branch, while `q = -0.5` uses the
generic branch.

Both seeds close as apolar fields, but Result 007 does not determine
whether this implementation asymmetry affects the winding measurement.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**M5 half-winding apolar closure:** SUPPORTED

**M5 half-winding sign identification:** SUPPORTED IN TESTED SECTOR

**Universal M5 `q ~ -q` identification:** NOT SUPPORTED

**Full physical `Q8/{1,-1}` reduction:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Constraint

The winding values in this test are synthetic probes of the M5 seed
construction.

Result 007 establishes the closure behavior of those probes. It does not
by itself establish that every closing probe corresponds to a distinct
physical M5 defect class.

No Reading Point residue is assigned to an M5 state.

No quaternion element is assigned to a particular winding value.

## Next reading point

Control for the asymmetric half-winding seed implementation.

Test `q = +0.5` and `q = -0.5` under matched seed conventions and pass
the resulting tensors through the same M5 winding instrument.

The next test should determine whether the sign identification observed
in Result 005 persists under symmetric seed construction or depends on
the current `+0.5` special-case implementation.

No Reading Point residue-to-M5 assignment should be introduced during
this control.

## Script

`readingpoint/tests/test_007_m5_winding_seed_closure.py`
