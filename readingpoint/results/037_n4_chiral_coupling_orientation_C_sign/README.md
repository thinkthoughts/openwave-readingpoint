       # Result 037 — Native N4 chiral-coupling sign → C-sign orientation audit

## Outcome

**PASS — the tested native N4 chiral signs do not anchor the geometric \(C\)-sign.**

The decisive result is:

```text
g_chiral sign reverses geometric C:
NOT SUPPORTED

g_chiral sign leaves geometric C even:
SUPPORTED

g_chiral sign reverses weighted K = g_chiral*C:
SUPPORTED

chi sign reverses geometric C:
NOT SUPPORTED

chi sign leaves geometric C even:
SUPPORTED
```

Therefore `g_chiral` supplies a native sign for the **weighted chiral interaction term**, but not for the geometric chiral-overlap matrix \(C\) used in Result 032.

## Existing implementation

Result 037 uses:

```text
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4_chiral.py
```

and the existing functions:

```text
chiral_mass_matrix(...)
chiral_overlap(...)
```

The native construction is:

\[
M_H=M_r+i\,g_{\rm chiral}C.
\]

The test therefore keeps three objects separate:

1. the geometric chiral-overlap matrix \(C\);
2. the coupling sign \(g_{\rm chiral}\);
3. the weighted chiral term
   \[
   K=g_{\rm chiral}C.
   \]

This separation prevents the trivial sign change of \(g_{\rm chiral}C\) from being misidentified as a sign change of \(C\).

## Parameter set

```text
n          = 40
alpha      = 0.6
delta      = 0.1
|chi|      = 0.6
|g_chiral| = 1.0
R_loop     = 9.0
q          = 0.5
core_vox   = 2.0
kappa      = 0.0
```

The tested states are:

```text
(+chi,+g)
(+chi,-g)
(-chi,+g)
(-chi,-g)
```

No Reading Point label or \(\chi_3\) sign is used.

## Per-state readout

```text
state          chi       g         ||C||       ||gC||
--------------------------------------------------------
chi+_g+      +0.600   +1.000   2.619763e+00  2.619763e+00
chi+_g-      +0.600   -1.000   2.619763e+00  2.619763e+00
chi-_g+      -0.600   +1.000   2.619759e+00  2.619759e+00
chi-_g-      -0.600   -1.000   2.619759e+00  2.619759e+00
```

All tested \(C\) matrices remain antisymmetric, and all real overlap matrices remain symmetric.

## Pure \(g_{\rm chiral}\)-sign flip

At fixed positive \(\chi\):

```text
Geometric C:
r_odd           = 1.000000000e+00
r_even          = 0.000000000e+00
magnitude ratio = 1.000000000e+00
verdict         = EVEN
```

while:

```text
Weighted K = g_chiral*C:
r_odd           = 0.000000000e+00
r_even          = 1.000000000e+00
magnitude ratio = 1.000000000e+00
verdict         = ODD
```

The same result reproduces at negative \(\chi\).

Thus:

\[
C(\chi,-g)=C(\chi,+g)
\]

exactly within the tested implementation, while:

\[
(-g)C=-gC.
\]

So the sign reversal belongs to the coupling-weighted term rather than to the geometric overlap.

## Pure screw-sign flip

At fixed positive \(g_{\rm chiral}\):

```text
Geometric C:
r_odd           = 1.000000000e+00
r_even          = 4.185726694e-06
magnitude ratio = 9.999985576e-01
verdict         = EVEN
```

The same result reproduces at negative \(g_{\rm chiral}\).

The real overlap matrix is even to numerical precision:

```text
r_even = 6.191268694e-17
```

Therefore changing the sign of the secondary screw parameter \(\chi\) does not reverse \(C\) in the tested family.

## Component audit

For the \(\chi\)-sign flip:

```text
C_01:
+chi = +1.009873677
-chi = +1.009884024

C_02:
+chi = -1.009884326
-chi = -1.009873376

C_12:
+chi = -1.179774791
-chi = -1.179771112
```

No independent component changes sign.

## Combined sign flip

For:

\[
(+\chi,+g)\rightarrow(-\chi,-g),
\]

the geometric \(C\) remains even:

```text
r_even = 4.185726694e-06
```

while the weighted term is odd:

```text
r_odd = 4.185726694e-06
```

This is exactly the behavior expected if the coupling sign carries the sign reversal while the geometric overlap remains approximately unchanged.

## Controls

All controls pass:

```text
C antisymmetry:
SUPPORTED

Mr symmetry:
SUPPORTED

M_H = Mr + i*g*C reconstruction:
SUPPORTED

repeatability C residual:
0.000000000e+00

repeatability Mr residual:
0.000000000e+00

repeatability:
SUPPORTED
```

## Aggregate interpretation

The executable result is:

```text
Native C-sign anchor from tested chiral signs:
NO_NATIVE_C_SIGN_ANCHOR_FROM_TESTED_CHIRAL_SIGNS
```

and:

```text
Native role of g_chiral:
G_CHIRAL_FLIPS_WEIGHTED_TERM_NOT_GEOMETRIC_C
```

Thus `g_chiral` is a meaningful native signed coupling, but that sign cannot be substituted for the geometric \(C\)-sign used to distinguish the Result-032 quotient pair.

## Relation to Results 035–036

The current orientation-anchor sequence is:

```text
035  right-handed full eigenframe
     -> does not anchor C-sign

036  self-linking N -> -N
     -> no clean C-sign anchor

037  g_chiral / chi sign
     -> no geometric C-sign anchor
```

Result 037 does independently establish:

```text
g_chiral sign anchors g_chiral*C:
SUPPORTED
```

but this is a different object from \(C\).

## Correspondence boundary

Result 034 retained two admissible mappings:

```text
Mapping A:
C-sign = chi3

Mapping B:
C-sign = -chi3
```

Result 037 licenses neither.

Therefore:

```text
Result-034 admissible mappings: 2
Result-037 admissible mappings: 2

2 -> 1 reduction:
NOT LICENSED
```

and:

```text
Unique Reading Point -> M5 correspondence:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Required result statement

**RESULT 037:**

Native reversal of `g_chiral` leaves the geometric chiral-overlap matrix \(C\) unchanged while reversing the weighted chiral term

\[
g_{\rm chiral}C.
\]

Reading Point \(\chi_3\) sign mapping remains unassigned by Test 037.

## Next reading point

The strongest remaining field-derived candidate is the existing signed Mermin–Ho / topological-charge machinery.

A next test should ask whether that independently implemented signed geometric quantity has an executable relation to the same Result-032 \(C\)-sign.

If that route also fails, the remaining twofold correspondence becomes increasingly well-defined as a current implementation boundary rather than an unresolved algebraic calculation.

## Script

`readingpoint/tests/test_037_n4_chiral_coupling_orientation_C_sign.py`
