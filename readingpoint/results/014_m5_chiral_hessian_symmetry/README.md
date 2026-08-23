# Result 014 — M5 chiral Hessian symmetry

## Outcome

**P2 SCALAR-ENERGY HESSIAN → N4 ANTISYMMETRIC `C`: STRUCTURALLY OBSTRUCTED.**

Result 014 applies the existing N3 effective-mass prescription to the
implemented P2 Lifshitz scalar energy and compares the projected result
with the existing N4 chiral matrix.

The numerical control shows that the projected P2 Hessian is exactly
symmetric, while the N4 matrix `C` is nonzero and antisymmetric to
machine precision.

Therefore the implemented P2 scalar-energy term cannot generate the N4
chiral matrix through the stated N3 energy-Hessian projection alone.

## N3 effective-mass prescription

The N3 field-theory bridge defines the flavour-space mass matrix from
the second variation of the Landau-de Gennes energy projected onto three
flavour field displacements.

Schematically:

`dM_a = M_a - M_vac`

and the real matrix is built from overlap terms such as

`K_ab = ∫ <∇dM_a, ∇dM_b>_s`

and

`P_ab = ∫ <dM_a, dM_b>_s`.

The resulting mass matrix is real and symmetric.

This supplies the M5-native reduction rule tested in Result 014.

## P2 chiral scalar energy

The P2 branch implements the chiral Lifshitz scalar energy

`F_chiral = ∫ 2 q0 Lc ε_ikl Q_ij ∂_k Q_lj d³r`.

For two perturbations `A` and `B`, define the raw bilinear

`B(A,B) = 2 q0 Lc ∫ ε_ikl A_ij ∂_k B_lj d³r`.

The ordinary second variation of the scalar quadratic energy is then

`H(A,B) = B(A,B) + B(B,A)`.

By construction, this Hessian is symmetric under exchange of `A` and
`B`.

## Controlled geometry

The executable control used:

- grid size `N = 24`;
- `alpha = 0.6`;
- `delta = 0.1`;
- `chi = 0.6`;
- `R_loop = 6.0`;
- `q = 0.5`;
- `core_vox = 2.0`;
- `dx = 1.0`;
- `q0 = 2π / 24`;
- `Lc = 1.0`.

The same three N4-style flavour displacements were used for both
projected P2 and N4 calculations.

## Projected P2 raw bilinear

The measured raw bilinear was:

```text
[[ 0.        3.045104  3.045104]
 [ 3.297047 22.260830  0.289569]
 [ 3.297047  0.289569 22.260830]]
```

This raw `B` need not itself be symmetric.

## Projected P2 scalar-energy Hessian

The second-variation matrix

`H = B + B^T`

was:

```text
[[ 0.        6.342151  6.342151]
 [ 6.342151 44.521660  0.579138]
 [ 6.342151  0.579138 44.521660]]
```

Measured symmetry error:

`0.000e+00`

Therefore:

**Projected P2 Hessian symmetric:** PASS

## N4 chiral matrix

The existing N4 `chiral_overlap()` evaluated on the same flavour fields
produced:

```text
[[  0.        14.863451 -14.899841]
 [-14.863451   0.       -12.021943]
 [ 14.899841  12.021943   0.      ]]
```

Measured antisymmetry error:

`3.577e-16`

Therefore:

**N4 `C` antisymmetric:** PASS

**N4 `C` nonzero:** PASS

## Symmetry-class comparison

The normalized Frobenius overlap between the projected P2 Hessian and
the N4 chiral matrix was:

`-1.291e-17`

which is numerically consistent with the expected orthogonality between
a symmetric matrix and an antisymmetric matrix.

The distinction is therefore structural rather than a matter of finding
the right scalar coefficient.

No ordinary real scalar `g` can turn a nonzero symmetric Hessian into
the nonzero antisymmetric matrix `C`.

## Result

The executable test reports:

**N3 effective-mass prescription:** ENERGY-HESSIAN PROJECTION

**P2 Lifshitz scalar energy:** IMPLEMENTED

**Projected P2 Hessian symmetric:** PASS

**N4 `C` antisymmetric:** PASS

**N4 `C` nonzero:** PASS

**P2 scalar-energy Hessian → N4 antisymmetric `C`: STRUCTURALLY OBSTRUCTED**

**Additional independently derived effective structure:** REQUIRED

## Relation to Result 013

Result 013 established that the P2 Lifshitz operator and N4 chiral
overlap are not directly identical as coded.

They differ in:

- differential order;
- tensor scope;
- contraction;
- and normalization.

Result 014 goes further.

Even after applying the M5-native N3 energy-Hessian projection rule to
the P2 scalar energy, the induced matrix belongs to the symmetric
matrix sector.

The existing N4 `C` belongs to the antisymmetric matrix sector.

Therefore the missing P2 → N4 bridge is not merely a missing
normalization or coefficient.

An additional effective structure is required.

## Relation to Result 012

Result 012 found that M5 already contains implemented P2 chiral substrate
machinery while N4 uses a separate free or phenomenological parameter
`g_chiral`.

Result 014 explains why an equation such as

`g_chiral = 2 * q0 * Lc`

cannot repair the provenance gap by itself.

The problem occurs before coefficient matching: the current P2
scalar-energy Hessian and N4 `C` have different symmetry classes.

## Constraint

Result 014 establishes a structural obstruction only for the stated N3
scalar-energy Hessian route.

It does not establish that no broader M5 effective theory can generate
the N4 term.

In particular, this result does not assume or establish any alternative
mechanism such as:

- Berry structure;
- symplectic structure;
- first-order kinetic terms;
- gyroscopic couplings;
- Wess-Zumino terms;
- holonomy;
- or another antisymmetric effective interaction.

Those remain candidate categories only if M5 already contains them or
derives them independently.

No such mechanism is introduced by Result 014.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**P2 chiral substrate machinery:** IMPLEMENTED

**N3 scalar-energy Hessian reduction:** IMPLEMENTED

**N4 antisymmetric chiral matrix:** IMPLEMENTED

**P2 → N4 through N3 scalar-energy Hessian:** STRUCTURALLY OBSTRUCTED

**Additional effective structure:** REQUIRED

**Physical P2 → N4 provenance bridge:** NOT ESTABLISHED

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Search the existing M5 repository for an independently defined
non-Hessian structure capable of producing a real antisymmetric
effective matrix before multiplication by `i`.

The search should remain narrow and M5-native.

Promising terms include:

- Berry;
- symplectic;
- first-order time derivative;
- gyroscopic;
- Wess-Zumino;
- connection;
- holonomy;
- antisymmetric kinetic coupling.

If such machinery exists, Test 015 should reproduce its definition and
determine whether it can act on the same N4 flavour-loop basis.

If no such structure exists, Result 015 should record that boundary
rather than inventing one.

The Reading Point residue mapping remains held.

## Script

`readingpoint/tests/test_014_m5_chiral_hessian_symmetry.py`
