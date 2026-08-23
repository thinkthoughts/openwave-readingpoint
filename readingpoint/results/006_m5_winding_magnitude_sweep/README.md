# Result 006 --- M5 winding-magnitude sweep

## Outcome

**CHARACTERIZED across the tested synthetic winding magnitudes.**

The current M5 biaxial eigenframe-winding observable was evaluated on
synthetic inputs with three winding magnitudes:

`|q| = 0.25`

`|q| = 0.5`

`|q| = 1.0`

Each magnitude was tested with both signs across:

-   `delta = 0.1, 0.3, 0.5`
-   `pair_1d`
-   `pair_d0`
-   read radii `3, 4, 5, 6`

A total of **72 sign-pair measurements** were characterized.

## Observed regimes

  Synthetic input     Measured `+q`   Measured `-q` Behavior
  ----------------- --------------- --------------- --------------------
  `|q| = 0.25`                  `0`             `0` Aliased to zero
  `|q| = 0.5`                `+0.5`          `+0.5` Sign identified
  `|q| = 1.0`                  `-1`            `+1` Sign distinguished

These behaviors were stable across every tested `delta`, pairing, and
read radius.

The reported out-of-plane mixing monitor remained zero throughout the
sweep.

## Result

The M5 winding observable does **not** implement one uniform sign rule
across the tested synthetic winding magnitudes.

Instead, three distinct responses appear.

### `|q| = 0.25`

Both signs are measured as approximately zero.

`+0.25 → 0`

`-0.25 → 0`

This sector is therefore best described as **aliased to zero** by the
current instrument.

### `|q| = 0.5`

Both signs are measured as `+0.5`.

`+0.5 → +0.5`

`-0.5 → +0.5`

This reproduces Result 005 and establishes **sign identification in the
tested half-winding sector**.

### `|q| = 1.0`

The two input signs remain distinguishable:

`+1.0 → -1.0`

`-1.0 → +1.0`

The sign reversal reflects the orientation convention of the current
measurement; the important result is that the two inputs remain
numerically distinct.

## Relation to Result 003

Result 003 established the mathematical quotient:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

Result 005 showed that the M5 winding observable identifies opposite
signs at `|q| = 0.5`.

Result 006 shows that this sign identification does **not** extend
uniformly across the tested synthetic winding magnitudes.

Therefore:

**Reading Point V4 quotient:** mathematically supported

**M5 `q ~ -q` behavior at `|q| = 0.5`:** supported in the tested sector

**Universal M5 `q ~ -q` identification:** not supported

**Full physical `Q8/{1,-1}` reduction:** not established

## Constraint

The additional `q` values in this sweep are **synthetic instrument
probes**.

This result does not assert that:

-   `|q| = 0.25` is an admissible physical M5 defect class;
-   `|q| = 1.0` is an admissible physical M5 defect class;
-   the three measured regimes correspond to particle states;
-   the Reading Point residue pairs correspond to any specific M5
    winding class.

No residue-to-quaternion assignment is introduced here.

## Interpretation

The current eigenframe-winding read is magnitude-dependent.

The observed progression is:

`|q| = 0.25 → zero`

`|q| = 0.5 → sign identified`

`|q| = 1.0 → sign distinguished`

This means the sign-insensitive behavior found in Result 005 is a
property of the tested half-winding sector rather than a universal
property of the M5 winding observable.

## Next reading point

Determine why `winding_measure_biax` produces these three regimes.

The next test should inspect the measurement itself:

`two_theta = atan2(2 M13, M11 - M33)`

followed by angular unwrapping and:

`q_meas = Σ Δ(two_theta) / 4π`.

The immediate questions are:

-   why quarter-winding inputs alias to zero;
-   why half-winding inputs lose sign;
-   why unit-winding inputs retain sign;
-   and which winding values correspond to independently admissible M5
    topological sectors rather than synthetic probes.

The Reading Point residue structure should remain outside the next test
until the M5 measurement behavior is understood.

## Script

`readingpoint/tests/test_006_m5_winding_magnitude_sweep.py`
