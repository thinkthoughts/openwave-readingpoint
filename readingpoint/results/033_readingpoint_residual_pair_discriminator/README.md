# Result 033 --- Reading Point Residual-Pair Discriminator

## Outcome

**SUPPORTED.**

The Reading Point quotient is now **fully intrinsically distinguished**
using two canonical binary characters inherited from the mod-3 and mod-5
factors of the mod-30 unit group.

No M5 label, M5 (C)-sign, or residue-to-M5 assignment is used in
constructing the discriminator.

## Question

Result 030 established an intrinsic Reading Point singleton-plus-pair
partition:

\[ {11,29} `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex} {{7,13},{17,23}}. \]

The remaining Reading Point ambiguity was therefore:

\[ {7,13} `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex} {17,23}. \]

Result 033 asks whether the arithmetic structure of

\[ (`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^\* \]

contains an independently defined second binary invariant that
distinguishes those two classes.

## Parent group and quotient

The unit group is

\[ (`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^\* =
{1,7,11,13,17,19,23,29}. \]

Result 003 uses the subgroup

\[ H={1,19}. \]

The quotient is

\[ (`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^\*/H
`\cong `{=tex}C_2`\times `{=tex}C_2 \]

with classes

\[ {1,19}, `\quad`{=tex} {7,13}, `\quad`{=tex} {11,29}, `\quad`{=tex}
{17,23}. \]

## Canonical binary characters

The Chinese remainder structure of the mod-30 units supplies natural
mod-3 and mod-5 factors.

### Mod-3 character

Define the nontrivial character of
((`\mathbb `{=tex}Z/3`\mathbb `{=tex}Z)\^\*):

\[ `\chi`{=tex}\_3(r)=
```{=tex}
\begin{cases}
+1,&r\equiv1\pmod3,\\
-1,&r\equiv2\pmod3.
\end{cases}
```
\]

The executable test confirms that (`\chi`{=tex}\_3) is multiplicative on
the parent unit group.

### Mod-5 quadratic character

Define

\[ `\chi`{=tex}\_5(r)=
```{=tex}
\begin{cases}
+1,&r\bmod5\in\{1,4\},\\
-1,&r\bmod5\in\{2,3\}.
\end{cases}
```
\]

This is the quadratic character modulo 5, and the executable test
confirms its multiplicativity on the parent group.

## Quotient descent

A character defines an observable on the Result-003 quotient only if it
is constant on every (H)-coset.

For both characters,

\[ `\chi`{=tex}(1)=`\chi`{=tex}(19)=+1. \]

Thus

\[ H`\subseteq`{=tex}`\ker`{=tex}`\chi`{=tex}\_3 \]

and

\[ H`\subseteq`{=tex}`\ker`{=tex}`\chi`{=tex}\_5. \]

The executable test independently checks coset constancy and reports:

``` text
chi3:
  values on H={1,19}: (1, 1)
  H subset ker(character): True
  descends to quotient: True

chi5:
  values on H={1,19}: (1, 1)
  H subset ker(character): True
  descends to quotient: True
```

Therefore both characters are legitimate quotient-level labels.

## Quotient character table

The measured quotient table is:

  ---------------------------------------------------------------------------------
  Reading      Parent orders   (`\chi`{=tex}\_3)   (`\chi`{=tex}\_5)          Joint
  Point class                                                             signature
  ----------- -------------- ------------------- ------------------- --------------
  ({1,19})           ((1,2))                (+1)                (+1)      ((+1,+1))

  ({7,13})           ((4,4))                (+1)                (-1)      ((+1,-1))

  ({11,29})          ((2,2))                (-1)                (+1)      ((-1,+1))

  ({17,23})          ((4,4))                (-1)                (-1)      ((-1,-1))
  ---------------------------------------------------------------------------------

All four joint signatures are distinct.

## Relation to Result 030

Result 030 distinguished

\[ {11,29} \]

from the other two nonidentity classes through the inherited
parent-order profile:

\[ (2,2) `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex} (4,4). \]

Result 033 finds that (`\chi`{=tex}\_5) reproduces this same
singleton-plus-pair structure:

\[ `\chi`{=tex}\_5({11,29})=+1, \]

while

\[ `\chi`{=tex}\_5({7,13}) = `\chi`{=tex}\_5({17,23}) = -1. \]

So (`\chi`{=tex}\_5) provides a canonical binary character realization
of the first Reading Point partition.

## Residual-pair discriminator

The remaining pair has equal parent-order profiles and equal
(`\chi`{=tex}\_5):

\[ {7,13}:(4,4), -1, \]

\[ {17,23}:(4,4), -1. \]

The independent mod-3 character separates them:

\[ `\boxed{
\chi_3(\{7,13\})=+1
}`{=tex} \]

and

\[ `\boxed{
\chi_3(\{17,23\})=-1.
}`{=tex} \]

Therefore:

``` text
Residual pair distinguished by chi3:
SUPPORTED

Reading Point residual-pair labeling:
SUPPORTED
```

## Joint quotient labeling

Together,

\[ (`\chi`{=tex}\_3,`\chi`{=tex}\_5) \]

gives:

\[ {1,19}`\to`{=tex}(+1,+1), \]

\[ {7,13}`\to`{=tex}(+1,-1), \]

\[ {11,29}`\to`{=tex}(-1,+1), \]

\[ {17,23}`\to`{=tex}(-1,-1). \]

The executable test finds:

``` text
joint signature class count:
4

all four quotient classes uniquely labeled:
SUPPORTED

joint character map preserves quotient multiplication:
SUPPORTED
```

Hence the joint character map realizes the quotient as a fully labeled
binary-sign group:

\[ (`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^\*/{1,19}
`\longrightarrow`{=tex} {`\pm1`{=tex}}`\times`{=tex}{`\pm1`{=tex}}. \]

Both sides have four elements, the signatures are unique, and
multiplication is preserved.

## Result

``` text
chi3 multiplicativity:
SUPPORTED

chi5 multiplicativity:
SUPPORTED

chi3 descent through {1,19}:
SUPPORTED

chi5 descent through {1,19}:
SUPPORTED

Residual Reading Point pair discrimination:
SUPPORTED

Reading Point residual-pair labeling:
SUPPORTED

Joint signature multiplication:
SUPPORTED

Reading Point quotient intrinsic labeling:
FULLY DISTINGUISHED

PASS
```

## Cross-system constraint

Result 033 is intentionally a **Reading Point-only** construction.

It does not assert

\[ `\chi`{=tex}\_3 `\leftrightarrow `{=tex}C`\text{-sign}`{=tex} \]

or

\[ `\chi`{=tex}\_5
`\leftrightarrow `{=tex}`\text{M5 geometric norm label}`{=tex}. \]

Those quantities were constructed independently on opposite sides of the
comparison.

Therefore Result 033 does **not** by itself reduce the two Result-031
cross-system correspondences to one.

``` text
M5 correspondence imposed by Result 033:
NONE

Unique Reading Point -> M5 correspondence:
NOT YET TESTED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Where the bridge now stands

Result 031 reduced the abstract sixfold (V_4) correspondence freedom to
two using independently obtained singleton-plus-pair partitions:

\[ 6`\rightarrow2`{=tex}. \]

Result 032 then fully distinguished the M5 quotient internally:

\[ `\bar `{=tex}T_x `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
`\bar `{=tex}T_z(+C), `\quad`{=tex} `\overline{T_xT_z}`{=tex}(-C). \]

Result 033 now fully distinguishes the Reading Point quotient
internally:

\[ {11,29} `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
{7,13}(`\chi`{=tex}\_3=+1), `\quad`{=tex} {17,23}(`\chi`{=tex}\_3=-1).
\]

Thus both systems now possess independently constructed intrinsic
labels.

What remains unresolved is whether those labels have an independently
justified **cross-system correspondence**.

## Next reading point

Result 034 should audit the two remaining quotient isomorphisms.

The test should keep the independently obtained labels explicit:

### M5

-   geometric norm partition;
-   (C)-sign.

### Reading Point

-   (`\chi`{=tex}\_5);
-   (`\chi`{=tex}\_3).

It should enumerate the two Result-031 partition-preserving isomorphisms
and determine exactly what additional assumption would be required to
select one.

The critical distinction is:

> Complete intrinsic labeling on both sides does not automatically
> establish that one system's sign coordinate corresponds physically or
> structurally to the other system's sign coordinate.

Result 034 can therefore determine whether the current evidence licenses

\[ 2`\rightarrow1`{=tex} \]

or whether the twofold bridge ambiguity remains.

## Script

`readingpoint/tests/test_033_readingpoint_residual_pair_discriminator.py`
