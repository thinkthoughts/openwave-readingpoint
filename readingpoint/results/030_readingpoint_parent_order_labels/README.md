# Result 030 — Reading Point parent-order quotient labels

## Outcome

**PARTIAL INTRINSIC LABELING SUPPORTED.**

The Reading Point quotient

`(Z/30Z)^* / {1,19} ≅ C2 × C2`

is not completely unlabeled when it is considered together with its independently defined parent group `(Z/30Z)^*`.

The multiplicative orders of the parent-group elements give the three nonidentity quotient classes the profiles

- `{7,13} → (4,4)`
- `{11,29} → (2,2)`
- `{17,23} → (4,4)`

Thus `{11,29}` is intrinsically distinguished on the Reading Point side, while `{7,13}` and `{17,23}` remain exchangeable under this invariant.

## Parent-group invariant

The eight units modulo 30 have multiplicative orders

```text
 1 -> 1
 7 -> 4
11 -> 2
13 -> 4
17 -> 4
19 -> 2
23 -> 4
29 -> 2
```

This invariant belongs to the Reading Point parent group and predates the M5 quotient comparison. No M5 observable or residue-to-M5 assignment is used to construct it.

## Quotient labels

Reducing by `{1,19}` gives

```text
{1,19}
{7,13}
{11,29}
{17,23}
```

For the three nonidentity classes, the inherited parent-order profiles are

```text
{7,13}  -> (4,4)
{11,29} -> (2,2)
{17,23} -> (4,4)
```

There are therefore two intrinsic nonidentity label types. The unique class is `{11,29}` with profile `(2,2)`. The residual Reading Point ambiguity is

`{7,13} ↔ {17,23}`.

Equivalently, the Reading Point-side permutation freedom has been reduced internally from `S3` to `C2`.

## Relation to Result 028

Result 028 found six multiplication-preserving isomorphisms between the M5 quotient and the Reading Point quotient because any permutation of the three nonidentity elements of V4 is an automorphism.

Result 030 supplies additional structure on the **Reading Point side only**. If a cross-system correspondence were required to preserve a matching parent-order-type label, only two permutations would remain: the exchange of the two `(4,4)` classes.

That does **not** yet establish a cross-system reduction from six mappings to two. No independently corresponding M5 invariant has identified which M5 quotient class should correspond to the unique Reading Point class `{11,29}`.

Therefore:

```text
Reading Point internal labeling:                    PARTIAL
Reading Point-side candidate count with label:      2
Currently licensed M5 -> Reading Point mappings:    6
Residue-pair -> M5 quotient-class assignment:       NOT ESTABLISHED
Reading Point -> M5 physical mapping:               NOT ESTABLISHED
```

## Constraint

The parent-order profile may be used as a Reading Point-native quotient label. It may not be copied onto an M5 class merely by choosing whichever M5 numerical signature looks distinctive.

A legitimate cross-system reduction requires an independently defined M5 property with a corresponding `1 + 2` structural partition.

## Result

**PASS.**

The Reading Point quotient carries partial intrinsic labeling inherited from `(Z/30Z)^*`:

`{11,29}` is uniquely `(2,2)`, while `{7,13}` and `{17,23}` share `(4,4)`.

This establishes a Reading Point-native `1 + 2` partition without establishing a particular M5 correspondence.

## Next reading point

Test the M5 quotient independently for a native binary invariant that partitions

`Txbar, Tzbar, TxTzbar`

as one distinguished class plus one equivalent pair.

If such a repository-native M5 partition exists and is established without using the Reading Point labels, it can be compared with Result 030's `1 + 2` partition. Only then can the Result-028 cross-system ambiguity legitimately be tested for a reduction from `6` to `2`.

## Script

`readingpoint/tests/test_030_readingpoint_parent_order_labels.py`
