# Result 034 — Two-bit M5 ↔ Reading Point correspondence audit

## Outcome

**PASS — the remaining twofold correspondence ambiguity is explicit, and a 2 → 1 reduction is not licensed.**

Results 032 and 033 fully distinguish the M5 and Reading Point quotients internally. Result 034 tests whether those independently constructed labels are enough to select a unique cross-system isomorphism.

They are not.

The remaining ambiguity is exactly the unresolved relative sign/orientation convention between the M5 `C` sign and the Reading Point `chi3` character.

## Previously established bridge

Result 031 reduced the six abstract V4 isomorphisms to two by matching the independently established singleton-plus-pair partitions:

```text
M5 singleton:             Txbar
Reading Point singleton:  {11,29}
```

Therefore:

```text
Txbar ↔ {11,29}
```

is retained at the partition level.

The unresolved classes are:

```text
M5:
Tzbar
TxTzbar

Reading Point:
{7,13}
{17,23}
```

## Independent native labels

### M5

The existing M5/N4 machinery supplies two native labels:

```text
first label:
full-frame G/R norm partition

second label:
N4 C-sign
```

Result 032 gives the residual-pair signs:

```text
Tzbar    -> +C
TxTzbar  -> -C
```

### Reading Point

The mod-30 quotient has two canonical arithmetic characters:

```text
first label:
chi5 / mod-5 quadratic character

second label:
chi3 / nontrivial mod-3 unit character
```

Result 033 gives:

```text
{7,13}  -> chi3 = +1
{17,23} -> chi3 = -1
```

No identification between `C-sign` and `chi3` is assumed in Result 034.

## Mapping A — aligned convention

```text
Ibar      -> {1,19}
Txbar     -> {11,29}
Tzbar     -> {7,13}
TxTzbar   -> {17,23}
```

This mapping is:

```text
bijection:                       PASS
multiplication preserving:       PASS
Result-031 partition preserving: PASS
```

For the residual pair:

```text
Tzbar     C=+1 -> {7,13}   chi3=+1
TxTzbar   C=-1 -> {17,23}  chi3=-1
```

Thus Mapping A realizes:

```text
C-sign = chi3
```

## Mapping B — reversed convention

```text
Ibar      -> {1,19}
Txbar     -> {11,29}
Tzbar     -> {17,23}
TxTzbar   -> {7,13}
```

This mapping is also:

```text
bijection:                       PASS
multiplication preserving:       PASS
Result-031 partition preserving: PASS
```

For the residual pair:

```text
Tzbar     C=+1 -> {17,23}  chi3=-1
TxTzbar   C=-1 -> {7,13}   chi3=+1
```

Thus Mapping B realizes:

```text
C-sign = -chi3
```

## Sign-convention audit

Exactly one mapping satisfies each possible relative sign convention:

```text
C-sign = chi3   -> Mapping A
C-sign = -chi3  -> Mapping B
```

Therefore either convention would select a unique mapping **if that convention were independently established**.

Result 034 finds no such cross-system rule.

## Correspondence boundary

The correspondence count remains:

```text
Result 028: 6
Result 031: 2
Result 034: 2
```

Therefore:

```text
2 -> 1 reduction:
NOT LICENSED

Unique structural correspondence:
NOT ESTABLISHED

Unique Reading Point -> M5 correspondence:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Interpretation

The two quotient systems are now fully labeled internally.

That does not automatically identify the meanings of their binary labels across systems.

Mapping A treats the M5 orientation-sensitive `C` sign and Reading Point `chi3` sign as aligned. Mapping B treats them as oppositely oriented. Both preserve the quotient multiplication and the independently established Result-031 partition.

The remaining uncertainty has therefore been reduced to one explicit binary orientation/sign choice.

No additional correspondence is inferred from the numerical agreement of the labels alone.

## Constraint

**Complete intrinsic labeling on both sides does not establish correspondence between the meanings or orientations of those labels.**

A unique mapping requires an independently defined cross-system rule that fixes the relative sign convention.

## Next reading point

Audit the provenance of the two sign conventions.

Specifically, determine whether the existing Reading Point and M5 implementations already contain an independently defined orientation anchor that fixes either:

```text
C-sign = chi3
```

or:

```text
C-sign = -chi3
```

without choosing the relation after observing the two candidate mappings.

If no such anchor exists, the twofold ambiguity is a stopping boundary for the current implementation.

A natural next test is:

```text
readingpoint/tests/test_035_orientation_convention_provenance.py
```

## Script

```text
readingpoint/tests/test_034_two_bit_correspondence_audit.py
```
