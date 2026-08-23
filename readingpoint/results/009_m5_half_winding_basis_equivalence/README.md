# Result 009 — M5 half-winding basis equivalence

## Outcome

**SUPPORTED.**

The generic and symmetric half-winding tensor constructions tested in
Result 008 are related by a fixed global basis transformation.

For both:

`q = +0.5`

and:

`q = -0.5`

the maximum tensor mismatch after the basis transformation is:

`3.331 × 10^-16`

which is effectively machine precision for this test.

## Wound-plane transformation

The generic and symmetric constructions are related in the wound
`(1,3)` plane by swapping the two axes:

`e1 ↔ e3`

The corresponding 2D transformation is:

```text
[0 1]
[1 0]
```

Its determinant is:

`-1`

so the isolated 2D swap reverses orientation.

## Proper 3D embedding

The same tensor equivalence can be embedded into a proper 3D rotation by
also reversing the orthogonal axis:

`e1 → e3`

`e2 → -e2`

`e3 → e1`

The corresponding transformation is:

```text
[ 0  0  1]
[ 0 -1  0]
[ 1  0  0]
```

It has:

`det = +1`

and therefore lies in:

`SO(3)`.

## Numerical result

The executable test reports:

```text
Reading Point Test 009
----------------------

M5 half-winding basis-equivalence control

q=+0.5  max tensor equivalence error=3.331e-16
q=-0.5  max tensor equivalence error=3.331e-16

2D wound-plane transformation:

  swap axes 1 <-> 3
  determinant = -1

3D embedding:

  e1 -> e3
  e2 -> -e2
  e3 -> e1
  determinant = +1
  proper SO(3) transformation: PASS
```

Thus:

**generic ↔ symmetric tensor equivalence:** PASS

**proper `SO(3)` embedding:** PASS

The two matched half-winding conventions therefore do not define
physically distinct tensor configurations merely because their
coordinate expressions differ.

## Relation to Result 008

Result 008 found three behaviors.

### Current OpenWave convention

`+0.5 → +0.5`

`-0.5 → +0.5`

Result:

**SIGN_IDENTIFIED**

### Generic convention

`+0.5 → -0.5`

`-0.5 → +0.5`

Result:

**SIGN_DISTINGUISHED**

### Symmetric convention

`+0.5 → +0.5`

`-0.5 → -0.5`

Result:

**SIGN_DISTINGUISHED**

The M5 winding instrument therefore assigns opposite sign orientations
under the generic and symmetric matched conventions.

Result 009 shows that those underlying tensor constructions are related
by a fixed global basis transformation.

Therefore the sign returned by `winding_measure_biax` depends on the
orientation of the chosen `(1,3)` basis.

The scalar winding sign by itself is not yet a basis-invariant physical
label.

## Relation to Result 007

Result 007 established that both positive and negative half-winding
seeds close as apolar tensor fields after one circuit:

`n → -n`

for:

`q = +0.5`

and:

`q = -0.5`.

Thus the basis-equivalence result concerns two constructions that
already satisfy the same basic apolar closure condition.

Apolar closure does not select one of the two matched basis conventions.

## Relation to Result 005

Result 005 reproduced the current OpenWave behavior:

`+0.5 → +0.5`

`-0.5 → +0.5`

Result 008 showed that this sign identification depends on the
asymmetric current seed convention.

Result 009 adds a second qualification: even where matched conventions
distinguish positive and negative half-windings, the orientation
assigned to those signs changes under a global basis transformation.

The current sequence therefore establishes:

**half-winding apolar closure:** SUPPORTED

**current OpenWave sign identification:** REPRODUCED

**seed-convention dependence:** SUPPORTED

**basis dependence of winding-sign orientation:** SUPPORTED

**basis-invariant physical half-winding sign:** NOT ESTABLISHED

## Relation to Result 003

Result 003 established the mathematical quotient:

`(Z/30Z)* / {1,19} ≅ Q8 / {1,-1} ≅ C2 × C2`

That mathematical result remains unchanged.

Result 009 does not provide a physical identification between the
Reading Point quotient and M5.

Instead, it shows that the scalar half-winding sign currently available
from the tested M5 winding instrument is insufficient to fix such a
correspondence.

The common `C2 × C2` quotient therefore remains a mathematical
structural correspondence rather than an established physical mapping.

## Constraint

This result does not establish that winding sign has no physical
meaning.

It establishes that the sign returned by this particular
basis-dependent winding read cannot, by itself, determine a physical
distinction.

A physical orientation may still be fixed by additional M5 structure,
for example:

- handedness,
- chirality,
- helicity,
- a pseudoscalar invariant,
- oriented transport,
- an interaction observable,
- defect composition,
- or another basis-invariant quantity.

No such additional structure is assumed by Result 009.

No Reading Point residue is assigned to an M5 state.

No quaternion element is assigned to a particular winding sign.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**M5 half-winding apolar closure:** SUPPORTED

**Current OpenWave half-winding sign identification:** REPRODUCED

**M5 seed-convention dependence:** SUPPORTED

**M5 winding-sign basis dependence:** SUPPORTED

**Basis-invariant M5 half-winding sign:** NOT ESTABLISHED

**Physical `Q8/{1,-1}` reduction:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Search the existing M5 theory and implementation for an independently
defined orientation-sensitive quantity.

The next candidate should determine physical handedness or orientation
without depending solely on the arbitrary orientation of the `(1,3)`
coordinate basis.

Candidate structures include:

- chirality,
- handedness,
- helicity,
- pseudoscalar invariants,
- oriented transport,
- interaction sign,
- or composition of quaternion defect classes.

The next test should use an observable already defined by M5 rather than
introducing a Reading Point mapping.

Only after an independently specified M5 orientation observable is
identified should the physical meaning of half-winding sign, the
`Q8/{1,-1}` quotient, or a Reading Point correspondence be reconsidered.

## Script

`readingpoint/tests/test_009_m5_half_winding_basis_equivalence.py`
