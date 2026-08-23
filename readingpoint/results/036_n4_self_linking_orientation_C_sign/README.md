# Result 036 — Native N4 self-linking orientation → C-sign audit

## Outcome

**PASS — no clean self-linking orientation anchor for the N4 chiral-overlap matrix was established.**

Result 036 tests whether the existing signed self-linking variable

\[
N\in\mathbb Z
\]

provides the missing native orientation anchor for the N4 chiral-overlap matrix \(C\).

The executable result is negative:

```text
Full C:
NO CLEAN FULL-C ORIENTATION ANCHOR

Baseline-subtracted dC:
NO CLEAN DELTA-C ORIENTATION ANCHOR
```

The Reading Point ↔ M5 correspondence count therefore remains **2**.

## Existing implementation

The test uses existing repository-native machinery:

```text
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4_topo.py
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4_chiral.py
```

with:

```text
topo_mass_matrix(...)
chiral_overlap(...)
```

The native orientation variable is the integer self-linking number \(N\), and the audited reversal is:

\[
N\rightarrow -N.
\]

No Reading Point mapping or \(\chi_3\) sign assignment is used.

## Parameter set

```text
n          = 40
alpha      = 0.6
delta      = 0.1
chi        = 0.6
g_chiral   = 1.0
R_loop     = 9.0
q          = 0.5
core_vox   = 2.0
kappa      = 0.0

tested N = [-2, -1, 0, 1, 2]
```

## Per-\(N\) chiral-overlap readout

| \(N\) | \(C_{01}\) | \(C_{02}\) | \(C_{12}\) | \(\|C\|_F\) |
|---:|---:|---:|---:|---:|
| -2 | +1.058248 | -1.054916 | -1.208446 | 2.717748 |
| -1 | +1.030290 | -1.028742 | -1.194177 | 2.663031 |
| 0 | +1.009874 | -1.009884 | -1.179775 | 2.619763 |
| +1 | +0.997457 | -0.998893 | -1.165587 | 2.588938 |
| +2 | +0.993057 | -0.995885 | -1.151906 | 2.570928 |

The \(N=0\) matrix is nonzero:

```text
[[ 0.          1.00987368 -1.00988433]
 [-1.00987368  0.         -1.17977479]
 [ 1.00988433  1.17977479  0.        ]]
```

Therefore Result 036 does not assume:

\[
N=0\Rightarrow C=0.
\]

## Full-\(C\) parity test

For each matched pair \(\pm N\), the preregistered residuals are:

\[
r_{\rm odd}
=
\frac{\|C(-N)+C(+N)\|_F}
{\|C(-N)\|_F+\|C(+N)\|_F},
\]

and

\[
r_{\rm even}
=
\frac{\|C(-N)-C(+N)\|_F}
{\|C(-N)\|_F+\|C(+N)\|_F}.
\]

### \(|N|=1\)

```text
r_odd          = 9.999984949e-01
r_even         = 1.421393175e-02
magnitude ratio = 1.028619041
verdict         = NO_CLEAN_RELATION
```

The complete \(C\) matrices are much closer to even than odd, but the magnitude difference is too large for the preregistered clean-even classification.

### \(|N|=2\)

```text
r_odd          = 9.999945217e-01
r_even         = 2.795778096e-02
magnitude ratio = 1.057107652
verdict         = NO_CLEAN_RELATION
```

Again the matrices are far from odd and qualitatively closer to even, but they do not satisfy the clean-even gate.

## Component audit

No independent upper-triangle component reverses sign under \(N\to -N\).

For \(|N|=1\):

```text
C_01: + / +   reverses=False
C_02: - / -   reverses=False
C_12: - / -   reverses=False
```

For \(|N|=2\):

```text
C_01: + / +   reverses=False
C_02: - / -   reverses=False
C_12: - / -   reverses=False
```

Thus the native self-linking sign reversal does not act as the binary \(C\)-sign reversal needed to resolve Result 034.

## Baseline-subtracted test

Because \(C(0)\neq0\), Result 036 separately tests:

\[
\Delta C(N)=C(N)-C(0).
\]

### \(|N|=1\)

```text
||dC(+N)||      = 3.086370468e-02
||dC(-N)||      = 4.426909346e-02
r_odd_delta      = 2.112234355e-01
r_even_delta     = 9.935890914e-01
magnitude ratio  = 1.434341532
verdict          = NO_CLEAN_RELATION
```

### \(|N|=2\)

```text
||dC(+N)||      = 5.010910642e-02
||dC(-N)||      = 1.018813209e-01
r_odd_delta      = 4.118794054e-01
r_even_delta     = 9.728221194e-01
magnitude ratio  = 2.033189738
verdict          = NO_CLEAN_RELATION
```

The \(N\)-dependent contribution therefore also fails to provide a clean odd or even orientation law.

## Controls

All preregistered controls pass:

```text
repeatability residual:
0.000000000e+00

repeatability:
SUPPORTED

antisymmetry for all N:
SUPPORTED

+/-N parameter identity:
SUPPORTED

replication at |N|=1 and |N|=2:
SUPPORTED
```

## Aggregate verdict

```text
Full C:
NO CLEAN FULL-C ORIENTATION ANCHOR

Baseline-subtracted dC:
NO CLEAN DELTA-C ORIENTATION ANCHOR
```

Therefore:

```text
Native self-linking orientation anchors full C-sign:
NOT ESTABLISHED

Native self-linking orientation anchors baseline-subtracted dC sign:
NOT ESTABLISHED
```

## Relation to Result 034

Result 034 retained two admissible cross-system mappings:

```text
Mapping A:
C-sign = chi3

Mapping B:
C-sign = -chi3
```

Result 036 licenses neither relation.

The correspondence count remains:

```text
Result 034: 2
Result 036: 2
```

Therefore:

```text
2 -> 1 reduction:
NOT LICENSED
```

## Interpretation

The signed self-linking integer \(N\) is a native N4 orientation variable, but the executable `topo_mass_matrix` construction does not make the full chiral-overlap matrix \(C\) an odd function of \(N\).

The full matrix remains qualitatively close to even under \(N\to -N\), while drifting in magnitude. The baseline-subtracted contribution \(\Delta C\) also fails to show a clean odd/even transformation law.

Result 036 therefore rules out self-linking sign as the missing direct \(C\)-sign anchor within the tested construction.

This does not invalidate \(N\) as a signed topological/framing quantity. It establishes only that the tested executable relation

\[
N\rightarrow -N
\quad\not\Rightarrow\quad
C\rightarrow -C
\]

is unsupported.

## Qualification

Test 036 treats \(N\to -N\) exactly as the signed self-linking reversal supplied by the existing N4 topology construction.

It does not add a separate coordinate reflection.

If a complete repository-native physical reflection requires an additional spatial operation, Result 036 should be read as the parity of the executable \(\pm N\) construction rather than as a complete physical-space parity law.

## Current correspondence boundary

The bridge remains:

\[
6\rightarrow2.
\]

The remaining unresolved bit is still:

\[
C=\chi_3
\]

versus

\[
C=-\chi_3.
\]

Result 036 assigns neither.

```text
Unique Reading Point -> M5 correspondence:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Required result statement

**RESULT 036:**

Native N4 self-linking reversal \(N\to-N\) gives no clean odd/even relation for the full chiral-overlap matrix \(C\).

Baseline-subtracted result:

```text
NO CLEAN DELTA-C ORIENTATION ANCHOR
```

Reading Point \(\chi_3\) sign mapping remains unassigned by Test 036.

## Next reading point

Audit the remaining pre-existing M5 sign/orientation conventions and ask whether any has an **existing executable relation to \(C\)**.

Candidate families include:

- signed Mermin–Ho / topological charge;
- electric-charge sign convention;
- signed curvature;
- `g_chiral` sign;
- native chiral or mirror conventions.

If none supplies an independently implemented bridge to \(C\), the twofold ambiguity becomes a documented stopping boundary for the current implementation.

## Script

`readingpoint/tests/test_036_n4_self_linking_orientation_C_sign.py`
