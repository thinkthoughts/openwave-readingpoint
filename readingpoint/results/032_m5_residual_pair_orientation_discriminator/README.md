# Result 032 --- Native M5/N4 Residual-Pair Orientation Discriminator

## Question

Result 031 reduced the admissible M5 ↔ Reading Point quotient
correspondences from six to two by independently matching a
singleton-plus-pair structure on both sides.

The remaining M5 ambiguity was:

\[ `\bar `{=tex}T_z `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

Result 032 asks:

> Does an existing M5/N4 orientation-sensitive observable descend
> through the Result-027 kernel and distinguish this residual pair?

The candidate observable is the already implemented N4 chiral-overlap
matrix

\[ C. \]

No Reading Point residue assignment is used to construct the test.

## Existing observable

The N4 chiral operator is defined through the existing `chiral_overlap`
machinery:

\[ C\_{ab} = `\operatorname{chiral\_overlap}`{=tex}(dM_a,dM_b). \]

Earlier Results 018--021 established that:

-   \(C\) is antisymmetric;
-   the tested mirror/orientation operation reverses its sign;
-   (`\chi`{=tex}`\to`{=tex}-`\chi`{=tex}) is approximately even in the
    tested family rather than acting as the handedness selector;
-   the Result-023 transformation closure carries a binary (C)-sign
    representation.

Result 032 uses that existing behavior as the candidate residual label.

## Result-027 quotient

The quotient is:

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}. \]

Its classes are:

\[ `\bar `{=tex}I={I,T_y}, \]

\[ `\bar `{=tex}T_x={T_x,T_xT_y}, \]

\[ `\bar `{=tex}T_z={T_z,T_yT_z}, \]

and

\[ `\overline{T_xT_z}`{=tex}={T_xT_z,T_xT_yT_z}. \]

Result 031 had already established the native M5 partition:

\[ `\bar `{=tex}T_x `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
{`\bar `{=tex}T_z,`\overline{T_xT_z}`{=tex}}. \]

The only unresolved M5 pair was therefore:

\[ `\bar `{=tex}T_z `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

## Per-transformation (C) classification

The measured classifications are:

``` text
I        sign=+  ||C||=2.619763253e+00
Tx       sign=-  ||C||=2.619759475e+00
Ty       sign=+  ||C||=2.619759475e+00
Tz       sign=+  ||C||=2.619763253e+00
TxTy     sign=-  ||C||=2.619763253e+00
TxTz     sign=-  ||C||=2.619759475e+00
TyTz     sign=+  ||C||=2.619759475e+00
TxTyTz   sign=-  ||C||=2.619763253e+00
```

Antisymmetry remains at machine precision across all eight states.

## Quotient descent

For (C)-sign to be a legitimate observable on

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}, \]

the sign must be invariant within every quotient class.

The measured descent is:

``` text
Ibar      I=+       Ty=+        descends=True
Txbar     Tx=-      TxTy=-      descends=True
Tzbar     Tz=+      TyTz=+      descends=True
TxTzbar   TxTz=-    TxTyTz=-    descends=True
```

Therefore:

\[ `\boxed{
C\text{-sign descends through }\langle T_y\rangle:
\ \text{SUPPORTED}
}`{=tex} \]

and the quotient-level signs are:

\[ `\bar `{=tex}I`\to `{=tex}+, \]

\[ `\bar `{=tex}T_x`\to `{=tex}-, \]

\[ `\bar `{=tex}T_z`\to `{=tex}+, \]

\[ `\overline{T_xT_z}`{=tex}`\to `{=tex}-. \]

## Residual-pair discrimination

The remaining M5 pair from Result 031 is:

\[ `\bar `{=tex}T_z `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

Result 032 finds:

\[ `\boxed{
\bar T_z\to +C
}`{=tex} \]

and

\[ `\boxed{
\overline{T_xT_z}\to -C.
}`{=tex} \]

Thus:

``` text
Residual pair distinguished by C sign:
SUPPORTED

Native M5/N4 residual-pair labeling:
SUPPORTED
```

## M5 quotient labeling after Result 032

Results 031 and 032 now provide complementary native M5 labels.

### First label: full-frame norm partition

Result 031 gave:

\[ `\bar `{=tex}T_x `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
{`\bar `{=tex}T_z,`\overline{T_xT_z}`{=tex}}. \]

The existing connection and curvature norms independently singled out
(`\bar `{=tex}T_x).

### Second label: chiral orientation sign

Result 032 gives:

\[ `\bar `{=tex}T_z`\to `{=tex}+C, `\qquad`{=tex}
`\overline{T_xT_z}`{=tex}`\to `{=tex}-C. \]

Together, these existing observables distinguish all three nonidentity
M5 quotient classes.

Therefore:

\[ `\boxed{
\text{M5 quotient intrinsic labeling:
FULLY DISTINGUISHED WITHIN TESTED QUOTIENT}
}`{=tex} \]

## Relation to the Reading Point quotient

Result 030 established the Reading Point-side partition:

\[ {11,29} `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex} {{7,13},{17,23}}. \]

Result 031 matched that structure to:

\[ `\bar `{=tex}T_x `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
{`\bar `{=tex}T_z,`\overline{T_xT_z}`{=tex}}, \]

which licensed:

\[ `\bar `{=tex}T_x`\leftrightarrow`{=tex}{11,29} \]

at the partition-label level and reduced the number of structurally
admissible isomorphisms:

\[ 6`\rightarrow2`{=tex}. \]

Result 032 fully labels the **M5 side**, but it does not yet select
between the two Reading Point classes

\[ {7,13} `\quad`{=tex}`\text{and}`{=tex}`\quad`{=tex} {17,23}. \]

There is still no independently established Reading Point-side label
corresponding to the M5 (+C/-C) distinction.

Therefore:

``` text
Result-031 partition-preserving mappings:
2

Cross-system correspondence count licensed after Result 032:
2
```

## Result

### Supported

``` text
C antisymmetry:
SUPPORTED

C-sign descent through <Ty>:
SUPPORTED

Tzbar C-sign:
+

TxTzbar C-sign:
-

Residual M5 pair discrimination:
SUPPORTED

Native M5/N4 residual-pair labeling:
SUPPORTED

M5 quotient intrinsic labeling:
FULLY DISTINGUISHED WITHIN TESTED QUOTIENT

PASS
```

### Still open

``` text
Reading Point second binary label for {7,13} vs {17,23}:
NOT ESTABLISHED

Licensed cross-system correspondence count:
2

Unique Reading Point -> M5 correspondence:
NOT ESTABLISHED

Physical Q8/{+1,-1} identification:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Interpretation

Result 032 removes the final ambiguity **inside the M5 quotient**.

The quotient now carries two independent repository-native labels:

1.  a geometric norm label that singles out (`\bar `{=tex}T_x);
2.  a chiral orientation sign that distinguishes (`\bar `{=tex}T_z) from
    (`\overline{T_xT_z}`{=tex}).

So the M5 quotient is no longer an unlabeled (V_4), nor merely a
singleton-plus-pair partition. All three nonidentity classes are
internally distinguishable.

The remaining uncertainty is entirely on the Reading Point side.

## Next reading point

Result 033 should be a Reading Point-side residual-pair audit.

Its question should be:

> Does the existing Reading Point/mod-30 construction contain an
> independent second binary invariant that distinguishes
>
> \[ {7,13} `\quad`{=tex}`\text{from}`{=tex}`\quad`{=tex} {17,23} \]
>
> without assigning either pair to (+C) or (-C) after observing the M5
> result?

If such an invariant exists and has a independently comparable
structure, the remaining correspondence count can be tested for:

\[ 2`\rightarrow1`{=tex}. \]

Until then:

\[ `\boxed{
\text{Reading Point}\rightarrow\text{M5 physical mapping:
NOT ESTABLISHED}
}`{=tex} \]
