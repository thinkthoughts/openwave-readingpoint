# Reading Point Test 037 — N4 chiral-coupling sign → C-sign orientation audit

## Outcome

**PASS.**

The tested native N4 chiral signs do not anchor the geometric `C`-sign.

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

Therefore `g_chiral` supplies a native sign for the **weighted chiral interaction term**, but not for the geometric chiral-overlap matrix `C` used in Result 032.

## Existing implementation

Result 037 uses:

```text
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4_chiral.py
```

with the existing functions:

```text
chiral_mass_matrix(...)
chiral_overlap(...)
```

The native construction is:

```text
M_H = Mr + i * g_chiral * C
```

The test keeps three objects separate:

```text
geometric chiral-overlap matrix: C
coupling sign:                   g_chiral
weighted chiral term:           K = g_chiral * C
```

This separation prevents the sign change of `g_chiral*C` from being read as a sign change of geometric `C`.

No Reading Point mapping or `chi3` label is used.

## Configuration

The exact tested parameter set is:

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

The four tested states are:

```text
(+chi,+g)
(+chi,-g)
(-chi,+g)
(-chi,-g)
```

## Per-state readout

```text
state          chi       g         ||C||       ||gC||
--------------------------------------------------------
chi+_g+      +0.600   +1.000   2.619763e+00  2.619763e+00
chi+_g-      +0.600   -1.000   2.619763e+00  2.619763e+00
chi-_g+      -0.600   +1.000   2.619759e+00  2.619759e+00
chi-_g-      -0.600   -1.000   2.619759e+00  2.619759e+00
```

All tested `C` matrices remain antisymmetric, and all real overlap matrices remain symmetric.

## Pure coupling-sign flip

At fixed positive `chi`:

```text
Geometric C:
  r_odd           = 1.000000000e+00
  r_even          = 0.000000000e+00
  magnitude ratio = 1.000000000e+00
  verdict         = EVEN

Weighted K = g_chiral * C:
  r_odd           = 0.000000000e+00
  r_even          = 1.000000000e+00
  magnitude ratio = 1.000000000e+00
  verdict         = ODD

Real overlap Mr:
  r_odd           = 1.000000000e+00
  r_even          = 0.000000000e+00
  magnitude ratio = 1.000000000e+00
  verdict         = EVEN
```

The same result reproduces at negative `chi`.

Thus the sign reversal belongs to the coupling-weighted term rather than to the geometric overlap.

## Pure screw-sign flip

At fixed positive `g_chiral`:

```text
Geometric C:
  r_odd           = 1.000000000e+00
  r_even          = 4.185726694e-06
  magnitude ratio = 9.999985576e-01
  verdict         = EVEN

Weighted K = g_chiral * C:
  r_odd           = 1.000000000e+00
  r_even          = 4.185726694e-06
  magnitude ratio = 9.999985576e-01
  verdict         = EVEN

Real overlap Mr:
  r_odd           = 1.000000000e+00
  r_even          = 6.191268694e-17
  magnitude ratio = 1.000000000e+00
  verdict         = EVEN
```

The same result reproduces at negative `g_chiral`.

Changing the sign of `chi` therefore does not reverse geometric `C` in the tested family.

## Combined sign flip

For:

```text
(+chi,+g) -> (-chi,-g)
```

geometric `C` remains even:

```text
r_even = 4.185726694e-06
```

while the weighted term is odd:

```text
r_odd = 4.185726694e-06
```

The replicated combined flip

```text
(+chi,-g) -> (-chi,+g)
```

gives the same classification.

## Component audit

For the `chi`-sign flip:

```text
C_01: +chi=+1.009873677e+00  -chi=+1.009884024e+00
C_02: +chi=-1.009884326e+00  -chi=-1.009873376e+00
C_12: +chi=-1.179774791e+00  -chi=-1.179771112e+00
```

No tested component reverses sign.

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

Thus `g_chiral` is a native signed coupling, but that sign does not supply the geometric `C`-sign used to distinguish the Result-032 quotient pair.

## Relation to Results 035–036

The orientation-anchor sequence through Result 037 is:

```text
035  right-handed full-frame convention
     -> no C-sign anchor

036  self-linking N -> -N
     -> no clean C-sign anchor

037  g_chiral / chi signs
     -> weighted-term sign only
```

Result 037 independently establishes:

```text
g_chiral sign anchors g_chiral*C:
SUPPORTED
```

but `g_chiral*C` is a different object from geometric `C`.

## Correspondence boundary

Result 034 retained two admissible mappings:

```text
Mapping A:
C-sign = chi3

Mapping B:
C-sign = -chi3
```

Result 037 licenses neither convention.

Therefore:

```text
Result-034 admissible mappings: 2
Result-037 admissible mappings: 2

2 -> 1 reduction:
NOT LICENSED
```

Accordingly:

**Unique Reading Point → M5 correspondence: NOT ESTABLISHED.**

**Reading Point → M5 physical mapping: NOT ESTABLISHED.**

## Result

**RESULT 037**

Native reversal of `g_chiral` leaves the geometric chiral-overlap matrix `C` unchanged while reversing the weighted chiral term `g_chiral*C`.

Reading Point `chi3` sign mapping remains unassigned by Test 037.

**PASS**

## Next reading point

Test the existing signed Mermin-Ho / topological-flux machinery as an independent native orientation candidate.

The next test should ask whether that signed geometric quantity supplies an executable relation to the Result-032 `C`-sign.

## Script

`readingpoint/tests/test_037_n4_chiral_coupling_orientation_C_sign.py`
