# Reading Point Test 038 — M5 Mermin-Ho orientation anchor

## Outcome

**PASS.**

The existing M5 longest-axis / Mermin-Ho signed-flux instrument
**numerically distinguishes** the residual quotient pair

`Tzbar` and `TxTzbar`,

but its tested signed summaries give both classes the **same native
topological sign**.

Therefore:

- numerical Mermin-Ho quotient labeling: **SUPPORTED**
- native signed binary orientation discriminator: **NOT SUPPORTED**
- Mermin-Ho sign anchor for Result-032 C-sign: **NOT ESTABLISHED**
- Result-034 correspondence count: **2**
- Result-038 correspondence count: **2**

No `2 -> 1` reduction is licensed.

## Existing implementation

The audit uses the repository-native full-F implementation:

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_22_4_a_fullf.py`

with the existing reader:

`reads(...)[basic]`

The `basic` read is the longest-axis / Mermin-Ho signed cube-flux
instrument.

The closure machinery is taken from:

`readingpoint/tests/test_026_m5_fullframe_connection_discriminator.py`

No Reading Point mapping or `chi3` label is used to construct the M5
readout.

## Configuration

The tested native configuration is:

```text
n      = 40
delta  = 0.1
h      = 1.2

flux scales:
half6
half12
half18
```

## Quotient descent

The Result-027 quotient is

`C2^3 / <Ty>`,

with classes:

```text
Ibar      = {I, Ty}
Txbar     = {Tx, TxTy}
Tzbar     = {Tz, TyTz}
TxTzbar   = {TxTz, TxTyTz}
```

At all three flux scales, the complete `basic` triplets descend through
`<Ty>` to numerical precision.

Thus the Mermin-Ho triplets are legitimate observables on the tested
quotient.

## Residual pair

Results 031–032 leave the M5 residual pair

```text
Tzbar
TxTzbar
```

with Result-032 C labels:

```text
Tzbar    -> +C
TxTzbar  -> -C
```

Test 038 withholds those labels until after computing the native
Mermin-Ho readout.

## Signed Mermin-Ho result

At `half6`:

```text
Tzbar
[-1.042859801, -0.286753770, -0.269318710]
signs = (-,-,-)
net sign = -

TxTzbar
[-1.042859801, -0.269318710, -0.286753770]
signs = (-,-,-)
net sign = -
```

The triplet distance is approximately `2.466e-2`.

At `half12` the triplets remain numerically distinct, with distance
approximately `6.021e-3`, while both retain

```text
signs = (-,-,-)
net sign = -
```

At `half18` the distance is approximately `3.903e-6`, and again both
classes retain the same component signs and net sign.

## What the instrument distinguishes

The detailed Mermin-Ho triplets distinguish `Tzbar` from `TxTzbar`.

In particular, the second and third components exchange their numerical
roles between the two classes.

That is valid quotient-level numerical information.

However, the preregistered orientation summaries do not turn this
difference into an opposite binary sign:

```text
opposite component-sign tuples: NOT SUPPORTED
opposite net signed flux:       NOT SUPPORTED

same component-sign tuples:     SUPPORTED
same net sign:                  SUPPORTED
```

The native orientation verdict is therefore:

`SAME_NATIVE_TOPOLOGICAL_SIGN`

## Relation to Result 032

Result 032 distinguishes the residual pair using N4 C-sign:

```text
Tzbar    -> +
TxTzbar  -> -
```

Test 038 does not reproduce that opposition using the native
Mermin-Ho/topological-flux sign.

Therefore the relation between the tested Mermin-Ho sign summary and
Result-032 C-sign is:

**NONE ESTABLISHED.**

Numerical distinction alone does not establish an orientation-sign
correspondence.

## Correspondence boundary

The cross-system state remains:

```text
Result-034 admissible mappings: 2
Result-038 admissible mappings: 2

2 -> 1 reduction:
NOT LICENSED
```

Test 038 assigns no Reading Point `chi3` sign to either M5 residual
class.

Accordingly:

**Unique Reading Point -> M5 correspondence: NOT ESTABLISHED.**

**Reading Point -> M5 physical mapping: NOT ESTABLISHED.**

## Result

**RESULT 038**

The existing Mermin-Ho/topological-flux instrument numerically
distinguishes the residual M5 quotient pair, but its preregistered signed
summaries do not supply an opposite binary orientation sign for that
pair.

Reading Point `chi3` sign mapping remains unassigned by Test 038.

**PASS**

## Next reading point

Given Results 001–038, determine the strongest Reading Point -> M5
correspondence licensed by the executable evidence without adding an
extra cross-system orientation convention.

That synthesis should preserve the established quotient, partition, and
intrinsic-label results while keeping the remaining twofold
correspondence ambiguity explicit.
