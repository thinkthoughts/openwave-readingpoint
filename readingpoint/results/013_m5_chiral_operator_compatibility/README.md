# Result 013 — M5 chiral operator compatibility

## Outcome

**DIRECT P2 LIFSHITZ → N4 CHIRAL-OVERLAP OPERATOR IDENTITY NOT SUPPORTED.**

Result 012 established that M5 contains an implemented chiral Lifshitz
substrate term in the P2 branch, while the N4 branch uses a separate
effective coefficient `g_chiral`.

Result 013 compares the actual operators implemented on the two sides.

The result is that the P2 Lifshitz functional and the N4 chiral-overlap
matrix `C` are not directly the same operator as currently coded.

An additional effective reduction is required before a P2 → N4
parameter provenance bridge can be claimed.

## P2 chiral operator

The P2 implementation evaluates a Landau-de Gennes chiral Lifshitz
functional of the schematic form:

`F_chiral = ∫ 2 q0 Lc ε_ikl Q_ij ∂_k Q_lj d³r`

The implemented structure therefore has:

- one explicit field factor `Q`;
- one spatial derivative `∂Q`;
- the spatial `3 × 3` tensor block;
- an explicit central-difference factor `1/(2 dx)`;
- and an explicit volume factor `dx³`.

The overall coefficient structure is:

`2 * q0 * Lc`

This is a one-derivative Lifshitz operator.

## N4 chiral operator

The N4 chiral matrix is built from the antisymmetric bilinear:

`C_ab = chiral_overlap(dM_a, dM_b)`

with terms of the form:

`<∂x dM_a, ∂y dM_b>_s - <∂y dM_a, ∂x dM_b>_s`

together with the corresponding cyclic `y-z` and `z-x` contributions.

The N4 implementation therefore has:

- one derivative acting on each field;
- a gradient-gradient bilinear;
- the full `4 × 4` field representation;
- the engine `SIGN_MAT` signed inner product;
- central differences with default `dx = 1`;
- and a direct voxel sum with no explicit `dx³` factor in
  `chiral_overlap()`.

This is a different effective operator from the P2 `Q × ∂Q` Lifshitz
density.

## Executable result

Reading Point Test 013 reports:

**P2 chiral operator:** `Q × dQ` — one derivative

**P2 tensor scope:** spatial `3 × 3` block

**P2 normalization:** explicit `dx` in the gradient and explicit `dx³`
volume factor

**N4 chiral operator:** `dA × dB` — gradient-gradient bilinear

**N4 tensor contraction:** full field with engine `SIGN_MAT` signed inner
product

**N4 normalization:** central differences default to `dx = 1`, followed
by a direct sum with no explicit `dx³`

Therefore:

**Direct P2 Lifshitz == N4 C operator identity:** NOT SUPPORTED

**Additional effective reduction required:** YES

## Parameter consequence

Because the operators themselves are not directly identical, Result 013
does not support the parameter identification:

`g_chiral = 2 * q0 * Lc`

The fact that `2*q0*Lc` multiplies the P2 Lifshitz term does not establish
that it is the coefficient multiplying the N4 chiral matrix.

A valid parameter bridge requires the operator bridge first.

## Relation to Result 011

Result 011 reproduced that:

- the N4 geometric chiral overlap `C` is nonzero;
- the achiral theory is handedness-degenerate;
- and CP selection appears only when `g_chiral` is introduced.

That left the physical provenance of `g_chiral` open.

Result 013 does not resolve that provenance.

Instead, it establishes that the most obvious direct identification with
the P2 Lifshitz coefficient is unsupported by the implemented operator
definitions.

## Relation to Result 012

Result 012 found:

**P2 chiral substrate machinery:** IMPLEMENTED

**N4 chiral coefficient:** `g_chiral`

**Explicit P2 → N4 parameter bridge:** NOT FOUND

Result 013 explains why the missing bridge matters at the operator level.

P2 and N4 are not merely using different variable names for the same
coded interaction.

They implement different chiral structures.

Therefore an explicit effective-theory step is required between them.

## What would count as a bridge

A future P2 → N4 bridge would need an independently defined M5-side
operation such as:

- projection onto the N4 three-state loop basis;
- coarse-graining of the P2 substrate functional;
- integration over unresolved degrees of freedom;
- an integration-by-parts derivation;
- a controlled overlap reduction;
- or another explicit effective-theory construction.

Such a derivation would need to show how the P2 substrate interaction
induces an antisymmetric matrix proportional to the existing N4 `C`.

Only after that operator relation is established should an effective
coefficient `g_eff` be measured or derived.

## Constraint

Result 013 does **not** prove that the P2 and N4 chiral structures can
never be related.

It establishes only that they are not directly identical in the
examined implementations.

No projection or reduction is assumed.

No coefficient is fitted.

No Reading Point residue structure enters the test.

## Current bridge status

**Reading Point common V4 quotient:** MATHEMATICALLY SUPPORTED

**P2 chiral substrate machinery:** IMPLEMENTED

**N4 chiral overlap:** IMPLEMENTED

**Direct P2 → N4 chiral operator identity:** NOT SUPPORTED

**Direct `g_chiral = 2*q0*Lc` identification:** NOT SUPPORTED

**Additional effective reduction:** REQUIRED

**Effective P2 → N4 provenance bridge:** OPEN

**Reading Point residue ↔ M5 state mapping:** NOT ESTABLISHED

## Next reading point

Before constructing a new effective reduction, search the current M5
repository for an existing projection or derivation connecting a
substrate energy functional to the N3/N4 three-state mass matrix.

Useful targets include existing code or documentation containing concepts
such as:

- effective reduction;
- projection;
- overlap reduction;
- coarse-graining;
- integrating out fields;
- collective coordinates;
- matrix elements derived from an energy functional;
- or a substrate-to-mass-matrix construction.

If M5 already contains such a derivation, Test 014 should reproduce and
apply it to the chiral sector.

If no such derivation exists, Result 014 should record that provenance
boundary before any new effective-theory construction is attempted.

The Reading Point residue mapping remains held until the M5-side
provenance is established.

## Examined upstream sources

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_p2_heliknoton.py`

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n4_chiral.py`

`openwave/xperiments/m5_liquid_crystal/research/scripts/m5_11_n1_precision_method.py`

## Script

`readingpoint/tests/test_013_m5_chiral_operator_compatibility.py`
