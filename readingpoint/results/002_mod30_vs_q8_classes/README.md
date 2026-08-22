# Result 002 — Mod-30 units vs Q8 conjugacy classes

## Outcome

**REJECTED as a one-to-one conjugacy-class correspondence.**

The mod-30 unit group and Q8 both contain eight elements, but their
conjugacy-class structures differ.

### Reading Point

The units modulo 30 are:

`{1, 7, 11, 13, 17, 19, 23, 29}`

Because `(Z/30Z)*` is abelian, every element forms its own conjugacy class.

**Class structure:** `1 + 1 + 1 + 1 + 1 + 1 + 1 + 1`

**Class count:** `8`

### Q8

The quaternion group has conjugacy classes:

`{1}`  
`{-1}`  
`{i, -i}`  
`{j, -j}`  
`{k, -k}`

**Class structure:** `1 + 1 + 2 + 2 + 2`

**Class count:** `5`

## Result

The executable test confirms:

- element cardinality match: **PASS**
- conjugacy-class count match: **REJECTED**
- one-to-one conjugacy-class correspondence: **REJECTED**

Equal element cardinality therefore does not produce equal class structure.

## Next reading point

The direct group mapping failed in Result 001.

The conjugacy-class mapping failed in Result 002.

The next admissible comparison is a quotient:

`(Z/30Z)* / {1, 19}`

versus

`Q8 / {1, -1}`.

These independently defined reductions are candidates for a common
four-element structure. That claim remains to be tested.

## Script

`readingpoint/tests/test_002_mod30_vs_q8_classes.py`
