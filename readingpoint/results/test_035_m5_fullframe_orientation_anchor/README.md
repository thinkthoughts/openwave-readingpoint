# Result 035 — M5 full-frame orientation anchor

## Outcome

**RIGHT-HANDED FULL-FRAME CONVENTION: SUPPORTED**

**C-SIGN ANCHOR FROM THAT CONVENTION: NOT SUPPORTED**

Result 035 tests whether an existing M5 orientation convention can fix
the remaining sign ambiguity identified in Result 034.

The candidate is the full eigenframe implemented in:

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_22_4_a_fullf.py`

The existing construction is:

```text
e3 = oriented long axis
e1 = oriented short axis
e2 = e3 × e1
O  = [e1,e2,e3]
```

The source defines this frame as right-handed by construction.

## Question

Results 032 and 033 independently supplied complete binary labels on the
M5 and Reading Point quotients.

Result 034 nevertheless retained two possible cross-system mappings:

```text
C-sign = chi3
```

or

```text
C-sign = -chi3
```

The purpose of Result 035 is to determine whether the existing M5
right-handed full-frame convention independently fixes the M5 side of
this orientation ambiguity.

## Actual spatial reflection

The test applies an improper spatial transformation to the underlying
tensor fields:

```text
x -> -x
```

with

```text
Sx = diag(-1,+1,+1)
```

and

```text
M_sp'(x) = Sx M_sp(Sx x) Sx^T
```

The transformation satisfies:

```text
det(Sx) = -1
```

Therefore the tested transformation genuinely reverses spatial
orientation.

**Improper spatial transformation: SUPPORTED**

## Native full-frame handedness

For all three flavour fields, the existing `full_frame(M)` construction
produces:

```text
det(O) = +1
```

to floating-point precision.

Maximum deviations from +1 were:

```text
e    1.776e-15
mu   2.220e-15
tau  1.998e-15
```

Therefore:

**NATIVE FULL FRAMES RIGHT-HANDED: SUPPORTED**

## Reflected-field full-frame handedness

The same full-frame construction was evaluated after applying the
actual improper spatial transformation to the tensor fields.

Again:

```text
det(O_reflected) = +1
```

to floating-point precision.

The maximum deviations were again:

```text
e    1.776e-15
mu   2.220e-15
tau  1.998e-15
```

Thus the existing implementation reconstructs its native right-handed
frame convention after the underlying spatial reflection.

**REFLECTED-FIELD FULL FRAMES RIGHT-HANDED: SUPPORTED**

## Frame-reversal control

As a derived control only, the test exchanges `e1` and `e2` after
constructing the native frame.

This produces:

```text
det(O_reversed) = -1
```

with determinant sign-flip errors of:

```text
e    4.441e-16
mu   6.661e-16
tau  6.661e-16
```

Therefore the determinant responds correctly to a literal reversal of
the frame orientation.

This frame-only operation is **not** used to compute `C`.

Its purpose is only to verify the handedness control.

## N4 C under actual spatial reflection

The native N4 chiral-overlap matrix is approximately:

```text
[[ 0.        1.009874 -1.009884]
 [-1.009874  0.       -1.179775]
 [ 1.009884  1.179775  0.      ]]
```

After the actual improper spatial reflection:

```text
[[ 0.        1.009884 -1.009873]
 [-1.009884  0.       -1.179771]
 [ 1.009873  1.179771  0.      ]]
```

Both matrices remain antisymmetric:

```text
native antisymmetry error     = 2.823e-15
reflected antisymmetry error  = 6.023e-15
```

The parity comparison gives:

```text
||C_ref - C|| / ||C|| = 8.371447e-06
||C_ref + C|| / ||C|| = 1.999999e+00
```

Therefore:

**C APPROXIMATELY EVEN UNDER DIRECT SPATIAL REFLECTION: SUPPORTED**

**C SIGN REVERSAL UNDER DIRECT SPATIAL REFLECTION: NOT SUPPORTED**

## Orientation-anchor result

The experiment establishes all three relevant facts:

1. the underlying spatial transformation has determinant `-1`;
2. the M5 full-frame implementation reconstructs `det(O)=+1`;
3. the independently recomputed N4 `C` matrix remains approximately
   unchanged.

Therefore:

**C-SIGN ANCHORED BY THE RIGHT-HANDED FULL FRAME: NOT SUPPORTED**

The right-handed full-frame convention is a genuine native M5
orientation convention, but it does not determine the sign of the
Result-032 `C` discriminator.

## Relation to earlier results

Result 020 found that direct spatial parity leaves `C` approximately
even.

Result 032 established that `C` nevertheless supplies a binary sign
label on the Result-027 quotient under the previously tested composite
transformation closure.

Result 035 reconciles these observations.

The `C` sign used in Result 032 cannot be identified simply with the
handedness of the spatial full eigenframe.

Its sign behavior belongs to the larger composite
orientation/flavour transformation structure tested in Results 018–021
and 032.

## Effect on Result 034

Before Result 035, two partition-preserving M5 → Reading Point
isomorphisms remained:

```text
Mapping A:
C-sign = chi3
```

and

```text
Mapping B:
C-sign = -chi3
```

Result 035 licenses neither equation.

Therefore:

```text
Result-034 correspondence count: 2
Result-035 correspondence count: 2
```

and:

**2 → 1 REDUCTION: NOT LICENSED**

## Current correspondence boundary

The supported structural bridge remains:

```text
Reading Point quotient
(Z/30Z)* / {1,19}
        |
        | common V4 structure
        v
M5 quotient
C2^3 / <Ty>
```

The independently established label structure has progressed to:

```text
Reading Point:
  singleton {11,29}
  residual pair {7,13}, {17,23}
  chi3 distinguishes residual pair

M5:
  singleton Txbar
  residual pair Tzbar, TxTzbar
  C-sign distinguishes residual pair
```

The singleton correspondence is structurally constrained:

```text
Txbar <-> {11,29}
```

The residual correspondence remains:

```text
Tzbar     <-> {7,13}
TxTzbar   <-> {17,23}
```

or:

```text
Tzbar     <-> {17,23}
TxTzbar   <-> {7,13}
```

Result 035 does not select between them.

## Constraint

No equation of the form

```text
C-sign = chi3
```

or

```text
C-sign = -chi3
```

is established by this result.

The right-handed M5 full-frame convention cannot be used as the missing
cross-system sign rule.

## Physical interpretation

**Reading Point → M5 physical mapping: NOT ESTABLISHED**

Result 035 tests an existing M5 geometric orientation convention. It
does not introduce a new Reading Point → M5 physical identification.

The result instead eliminates one plausible repository-native mechanism
for resolving the final twofold structural ambiguity.

## Next reading point

Audit the remaining pre-existing M5 orientation/sign conventions for an
executable relation to the Result-032 `C` sign.

Candidate existing structures include:

```text
topological winding sign
electric-charge sign convention
signed curvature
basis / winding orientation
chiral or mirror conventions
```

The next test should ask whether any of these already supplies both:

1. an independently implemented M5 sign anchor tied to `C`; and
2. a corresponding structure that can be compared with the canonical
   Reading Point `chi3` character.

If no such existing bridge is found, the remaining twofold
correspondence becomes a documented implementation stopping boundary.

## Script

`readingpoint/tests/test_035_m5_fullframe_orientation_anchor.py`
