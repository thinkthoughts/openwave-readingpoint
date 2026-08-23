# Reading Point M5 Test Program

This directory contains executable tests for the proposed relationship
between Reading Point structure and the M5 liquid-crystal model.

The tests are deliberately cumulative. Each test asks what the existing
M5 implementation and the Reading Point arithmetic actually support before
a stronger algebraic or physical identification is made.

The current evidence ledger reaches **Result 039**.

The strongest licensed statement is:

```text
shared V4 quotient:
SUPPORTED

independent 1+2 partition bridge:
SUPPORTED

abstract quotient isomorphisms:
6

partition-preserving isomorphisms:
2

independent rule selecting between the final two:
NOT FOUND

unique Reading Point -> M5 correspondence:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED

current implementation stopping boundary:
SUPPORTED
```

## Current reading order

The present correspondence chain is:

```text
implemented N3/N4 structure
    ->
C2^3-like transformation closure
    ->
repository-native M5 V4 quotient
    ->
Reading Point V4 quotient
    ->
six abstract V4 isomorphisms
    ->
independent 1+2 partitions on both sides
    ->
two partition-preserving isomorphisms
    ->
independent residual-pair labels on both sides
    ->
orientation-convention audit
    ->
two admissible mappings remain
```

In words:

1. the implemented N4 chiral matrix `C` is a non-Hessian antisymmetric
   observable with a reproducible transformation structure;
2. three commuting involutions generate an eight-state `C2^3`-like
   field-level closure;
3. a repository-native quotient by `<Ty>` produces a four-element
   `C2 x C2` structure on the M5 side;
4. independently, `(Z/30Z)^* / {1,19}` is also `C2 x C2`;
5. abstractly, the two V4 quotients admit six identity-preserving
   isomorphisms;
6. Reading Point parent orders and canonical mod-5 arithmetic distinguish
   one nonidentity quotient class from the remaining pair;
7. existing M5 full-frame `G/R` norms independently produce the same
   singleton-plus-pair structure;
8. that partition-level bridge reduces the admissible correspondence count
   from six to two;
9. N4 `C`-sign distinguishes the remaining M5 pair;
10. the canonical Reading Point `chi3` character distinguishes the remaining
    Reading Point pair;
11. complete internal labeling on both sides still leaves an aligned versus
    reversed cross-system orientation convention;
12. Results 035--038 audit native M5 orientation candidates and do not supply
    an independent rule identifying `C-sign = chi3` or
    `C-sign = -chi3`;
13. Result 039 therefore records the present implementation boundary:
    **6 -> 2 is supported; 2 -> 1 is not licensed.**

This boundary is a positive result: the executable program now states
precisely which structural correspondence is supported and exactly which
additional cross-system rule would be required to make it unique.

## Test sequence

  ---------------------------------------------------------------------------------------------------------------------------------------
  Test              Question                                  Result                                             Consequence
  ----------------- ----------------------------------------- -------------------------------------------------- ------------------------
  014               Can the implemented P2 scalar-energy      **Structurally obstructed.** The projected         An additional
                    Hessian generate the N4 antisymmetric     scalar-energy Hessian is symmetric while (C) is    independently derived
                    (C)?                                      nonzero and antisymmetric.                         effective structure is
                                                                                                                 required.

  015               Does M5 already contain a non-Hessian     **Yes, as a candidate ingredient.** M5 implements  Connection/curvature is
                    geometric structure that could supply     an antisymmetric (so(3)) connection and curvature, a legitimate candidate
                    such a sector?                            but no examined provenance bridge identifies them  sector, not an
                                                              with N4 (C).                                       established origin of
                                                                                                                 (C).

  016               Does the dimensionless shape of N4 (C)    **Characterized.** Antisymmetry persists and the   The relative
                    persist under lattice refinement?         normalized operator converges across the tested    three-flavour structure
                                                              resolutions.                                       is not an obvious
                                                                                                                 single-resolution
                                                                                                                 artifact.

  017               What lattice normalization is supported   **(dx,C) supported among the tested integer        A candidate continuum
                    for raw (C)?                              powers.**                                          normalization is
                                                                                                                 available without
                                                                                                                 imposing a physical
                                                                                                                 source normalization.

  018               What reverses the sign of (C):            \(C\) is approximately **even** under              Screw-sign reversal and
                    (`\chi`{=tex}`\to`{=tex}-`\chi`{=tex}), a (`\chi`{=tex}`\to`{=tex}-`\chi`{=tex}). The        mirror/orientation
                    mirror orientation swap, or neither?      (`\mu`{=tex}`\leftrightarrow`{=tex}`\tau`{=tex})   reversal are distinct
                                                              orientation swap acts as (PCP\^T) and is           operations.
                                                              approximately sign-reversing in the tested         
                                                              geometry.                                          

  019               Is the mirror-odd behavior robust across  **Yes across the tested family.** Basis covariance The Result-018 mirror
                    geometry?                                 is exact in the test and (PCP\^T`\approx`{=tex}-C) relation is not confined
                                                              is robust over the 27 tested points.               to one parameter point.

  020               How does (C) transform under an actual    Directly (C\_{`\rm ref`{=tex}}`\approx `{=tex}C);  Physical-space
                    spatial reflection (x`\to`{=tex}-x)?      after the                                          reflection must be
                                                              (`\mu`{=tex}`\leftrightarrow`{=tex}`\tau`{=tex})   distinguished from
                                                              basis adjustment,                                  flavour-label exchange.
                                                              (C\_{`\rm ref`{=tex}}`\approx`{=tex}-PCP\^T).      

  021               What is the action of the composite       **Sign-odd across the tested family:**             A (Z_2)-like sign
                    (T_x=P`\circ `{=tex}R_x)?                 (T_x(C)`\approx`{=tex}-C), with (T_x\^2=I).        representation on (C) is
                                                                                                                 supported for this
                                                                                                                 composite operation.

  022               Is there a second independent involution? **Yes.** (T_y=P`\circ `{=tex}R_y) and              Multiple (V_4)-like
                                                              (T_z=P`\circ `{=tex}R_z) are independent tested    substructures exist; no
                                                              candidates; each forms a four-state                unique one is selected.
                                                              commuting-involution structure with (T_x).         

  023               What is the full closure generated by     **Eight distinct commuting involutions:            The field-level
                    (T_x,T_y,T_z)?                            (C_2\^3)-like.** (C) carries a non-faithful binary structure is larger than
                                                              sign representation: four states act as (+C), four any single (V_4)
                                                              as (-C).                                           candidate.

  024               Does the independently defined real       **No.** The normalized (M_r) matrices agree to     The joint (C+M_r)
                    overlap sector (M_r=K+`\kappa `{=tex}P)   numerical precision across the eight               readout still produces
                    distinguish states that have the same (C) transformations.                                   only two
                    sign?                                                                                        composition-compatible
                                                                                                                 classes.

  025               Does the already implemented M5           **No executable bridge found.** The connection     The current implemented
                    connection/curvature sector supply        begins with ((q_0,q)); N3/N4 uses rank-2 (M)       bridge reaches its
                    another discriminator on those unresolved flavour fields; no examined (M`\to`{=tex}(q_0,q))  stopping boundary.
                    states?                                   or equivalent projection is implemented.           
  ---------------------------------------------------------------------------------------------------------------------------------------

## Result 014 --- symmetric Hessian versus antisymmetric N4 sector

The N3 effective-mass prescription uses an energy-Hessian projection.

Projecting the implemented P2 Lifshitz scalar energy onto the same type
of flavour directions produces a symmetric Hessian:

\[ H = B+B\^T. \]

The N4 branch instead contains a nonzero real antisymmetric matrix (C).

The normalized Frobenius overlap between the tested symmetric Hessian
and antisymmetric (C) vanishes to numerical precision.

The resulting structural statement is:

> The implemented P2 scalar-energy term cannot generate N4 (C) through
> the stated N3 energy-Hessian projection alone.

This does not rule out an additional non-Hessian effective sector.

## Result 015 --- existing non-Hessian M5 machinery

M5 independently implements the symbolic connection

\[ `\Gamma`{=tex}\_i = O\^T`\partial`{=tex}\_i O, \]

with (`\Gamma`{=tex}\_i) antisymmetric in the tested construction.

The field-level regularized hedgehog implementation contains

\[ `\Gamma`{=tex}\_i = q_0`\partial`{=tex}\_iq -
(`\partial`{=tex}\_iq_0)q + q`\times`{=tex}`\partial`{=tex}\_iq, \]

and curvature

\[ R\_{ij}=`\Gamma`{=tex}\_i`\times`{=tex}`\Gamma`{=tex}\_j. \]

This is genuine non-Hessian geometric machinery.

However, the examined N4 branch constructs its antisymmetric flavour
matrix through `chiral_overlap(dA, dB)`. Result 015 found no implemented
projection from (`\Gamma`{=tex}*i) or (R*{ij}) to that N4 matrix.

Thus connection/curvature is an existing candidate ingredient, while its
identification with N4 (C) remains unestablished.

## Results 016--017 --- lattice characterization of (C)

Result 016 separated the normalized operator shape from the raw lattice
norm.

Across the tested refinement

\[ n=24, 32, 40, 48, \]

antisymmetry persisted and the successive normalized-operator changes
decreased:

``` text
24 -> 32 : 1.753148e-02
32 -> 40 : 8.100647e-03
40 -> 48 : 4.549089e-03
```

The raw norm itself scaled approximately as

\[ \|C\_{`\rm raw`{=tex}}\|\_F `\sim `{=tex}n\^{0.8702}. \]

Result 017 then expressed the same refinement in terms of physical
lattice spacing. The measured raw scaling was

\[ \|C\_{`\rm raw`{=tex}}\| `\sim `{=tex}dx\^{-0.8702}, \]

compared with the continuum-counting expectation (dx\^{-1}).

Among the tested integer powers (dx\^p C), (p=1) gave the smallest
spread:

\[ C\_{`\rm candidate`{=tex}}=dx,C. \]

This supports a candidate lattice normalization. It does not by itself
fix a source/action normalization or identify (C) with a measured
physical coupling.

## Results 018--020 --- separating reversal operations

Result 018 showed that the sign of the screw parameter (`\chi`{=tex}) is
not the operation that reverses (C).

For the tested geometry,

\[ C(-`\chi`{=tex})`\approx `{=tex}C(+`\chi`{=tex}), \]

rather than

\[ C(-`\chi`{=tex})`\approx`{=tex}-C(+`\chi`{=tex}). \]

The (`\mu`{=tex}`\leftrightarrow`{=tex}`\tau`{=tex}) orientation swap
instead obeys exact basis covariance in the test:

\[ C\_{`\rm mirror`{=tex}}=PCP\^T. \]

For the tested geometry this is also approximately

\[ PCP\^T`\approx`{=tex}-C. \]

Result 019 extended that observation over

\[ `\alpha`{=tex}`\in`{=tex}{0.40,0.60,0.80}, \]

\[ `\delta`{=tex}`\in`{=tex}{0.05,0.10,0.20}, \]

\[ `\chi`{=tex}`\in`{=tex}{0.30,0.60,1.00}. \]

All 27 tested points supported the approximate mirror-odd relation at
the preregistered threshold, while
(`\chi`{=tex}`\to`{=tex}-`\chi`{=tex}) remained approximately even.

Result 020 then applied an actual spatial reflection

\[ R_x:`\quad `{=tex}x`\to`{=tex}-x \]

with the rank-2 tensor transformation

\[ M'*{`\rm sp`{=tex}}(x)=S,M*{`\rm sp`{=tex}}(Sx),S\^T, `\qquad`{=tex}
S=`\operatorname{diag}`{=tex}(-1,+1,+1). \]

Directly,

\[ C\_{`\rm ref`{=tex}}`\approx `{=tex}C. \]

With the (`\mu`{=tex}`\leftrightarrow`{=tex}`\tau`{=tex}) basis
adjustment,

\[ C\_{`\rm ref`{=tex}}`\approx`{=tex}-PCP\^T. \]

Thus spatial reflection, flavour exchange, and screw-sign reversal are
separate transformations in the implemented construction.

## Results 021--023 --- field-level transformation algebra

Define

\[ T_x=P`\circ `{=tex}R_x. \]

Result 021 found across the tested family

\[ T_x(C)`\approx`{=tex}-C \]

and

\[ T_x\^2=I. \]

Result 022 then tested

\[ T_y=P`\circ `{=tex}R_y, `\qquad`{=tex} T_z=P`\circ `{=tex}R_z. \]

Both supplied independent commuting involutions at the tested field
point.

Result 023 generated the complete closure of

\[ T_x, T_y, T_z. \]

The eight transformations were

\[ I, T_x, T_y, T_z, T_xT_y, T_xT_z, T_yT_z, T_xT_yT_z. \]

They were all distinct at field level, each generator squared to the
identity, and all generator pairs commuted.

The resulting field-level classification is therefore:

\[ `\boxed{C_2^3\text{-like}}`{=tex} \]

for the tested implementation.

### Action on (C)

The eight states split into two measured sign classes:

\[ K\_+ = {I,T_y,T_z,T_yT_z}, \]

\[ K\_- = {T_x,T_xT_y,T_xT_z,T_xT_yT_z}. \]

The first class acts approximately as (+C); the second approximately as
(-C).

Therefore (C) carries a non-faithful (Z_2) sign representation of the
larger field-level closure.

This is a measured effective representation. It is not a particle
classification.

## Result 024 --- second implemented effective observable

Result 024 recomputed the existing real N3/N4 overlap sector

\[ M_r=K+`\kappa `{=tex}P \]

for every transformation in the Result-023 closure.

At the tested point with (`\kappa=0`{=tex}), all normalized (M_r)
matrices agreed to numerical precision.

The number of equal-(C)-sign pairs separated by (M_r) was

``` text
0 / 12
```

The joint observable partition therefore remained

``` text
class 0: I, Ty, Tz, TyTz
class 1: Tx, TxTy, TxTz, TxTyTz
```

and this partition was compatible with the measured Result-023
composition law.

The induced two-class multiplication table was

``` text
      0  1
0:    0  1
1:    1  0
```

Thus the implemented effective readout through Result 024 has the form

\[ C_2\^3`\text{-like field closure}`{=tex} `\longrightarrow`{=tex}
C_2`\text{-like measured quotient}`{=tex}. \]

No unique embedded (V_4) is selected by (C+M_r).

## Result 025 --- current implemented-bridge boundary

Result 025 returned to the independent M5 connection/curvature sector
and asked a deliberately conservative question:

> Is there already an executable repository path that applies an
> independently defined connection/curvature observable to the
> Result-023 N3/N4 flavour states?

The audit confirmed:

``` text
symbolic Gamma_i = O^T d_i O: IMPLEMENTED
field-level Gamma_i(q0,q): IMPLEMENTED
field-level curvature: IMPLEMENTED
curvature scalar/profile observable: IMPLEMENTED
```

It also confirmed the representation mismatch:

``` text
connection begins with (q0, q): YES
N3/N4 rank-2 M flavour fields: YES
```

But:

``` text
Explicit M-field -> (q0,q) conversion:
NOT FOUND IN EXAMINED SOURCES

N3/N4 -> connection/curvature executable bridge:
NOT FOUND IN EXAMINED SOURCES
```

Therefore:

``` text
Independent connection/curvature observable:
SUPPORTED

Existing input/projection bridge:
NOT ESTABLISHED

Existing executable discriminator:
NOT FOUND

Stopping-boundary verdict:
REACHED FOR CURRENT IMPLEMENTED BRIDGE
```

This is an implementation boundary, not an impossibility theorem.

M5 contains both:

1.  N3/N4 rank-2 (M) flavour fields, and
2.  independently implemented connection/curvature machinery.

The examined code does not supply the transformation connecting those
two representations.

Applying (`\Gamma`{=tex}*i) or (R*{ij}) to the eight flavour states now
would therefore require an additional derived mapping rather than
execution of an already implemented observable.

## Current supported structure

The strongest compact statement supported by Results 014--025 is:

\[ `\boxed{
C_2^3\text{-like field closure}
\longrightarrow
C_2\text{-like measured sign quotient}
}`{=tex} \]

where the binary measured distinction is carried by the N4 antisymmetric
operator (C).

The existing real overlap sector (M_r) does not refine this quotient.

The independently implemented connection/curvature sector may contain
additional information, but the examined implementation currently lacks
the projection needed to evaluate that possibility on the N3/N4 flavour
states.

## Current boundary

The test program stops here because the next operation would change the
kind of work being performed.

Results 014--025 test and characterize **existing implemented
structure**.

A next step that defines, for example,

\[ M`\rightarrow`{=tex}(q_0,q), \]

or an equivalent

\[ `\text{rank-2 flavour field}`{=tex} `\rightarrow`{=tex}
`\text{connection/curvature observable}`{=tex} \]

would be a **new derived bridge** unless that mapping can first be
located in the M5/OpenWave implementation or independently derived from
its stated field theory.

The next admissible research question is therefore:

> **Can an (M`\rightarrow`{=tex}(q_0,q)), or equivalent rank-2-field →
> connection/curvature projection, be derived from M5 itself rather than
> selected to reproduce a desired Reading Point structure?**

If an existing derivation is found, it can become the basis for a
subsequent executable test.

If the mapping must be introduced by this project, that should begin a
separately identified model-development phase rather than being
presented as another test of the existing bridge.

## Results 027--028 — native M5 quotient and abstract correspondence

Result 027 identified the repository-native quotient

```text
C2^3 / <Ty>
```

with classes

```text
Ibar     = {I, Ty}
Txbar    = {Tx, TxTy}
Tzbar    = {Tz, TyTz}
TxTzbar  = {TxTz, TxTyTz}
```

giving a four-element `C2 x C2` quotient.

Result 028 compared this quotient with the independently established
Reading Point quotient

```text
(Z/30Z)^* / {1,19}
```

whose classes are

```text
{1,19}
{7,13}
{11,29}
{17,23}
```

Both are V4. With identity fixed, all permutations of the three
nonidentity elements preserve the abstract V4 structure, so the initial
cross-system correspondence count is:

```text
6
```

No physical interpretation follows from that abstract isomorphism alone.

## Results 029--031 — independent singleton-plus-pair structure

Result 030 showed that the Reading Point quotient is already partially
labeled by structure inherited from its parent group `(Z/30Z)^*`.

The parent-order profiles are:

```text
{11,29}  -> (2,2)
{7,13}   -> (4,4)
{17,23}  -> (4,4)
```

Therefore the Reading Point side has the native partition

```text
singleton = {11,29}
pair      = {{7,13}, {17,23}}
```

Result 031 then found the same abstract `1+2` pattern independently in
existing M5 full-frame geometric norms:

```text
singleton = Txbar
pair      = {Tzbar, TxTzbar}
```

Both `||G||_F` and `||R||_F` support this partition and descend through
the Result-027 kernel `<Ty>`.

The partition-level bridge therefore fixes:

```text
Txbar <-> {11,29}
```

and reduces the six abstract V4 isomorphisms to two:

```text
6 -> 2
SUPPORTED
```

The unresolved exchange is:

```text
Tzbar / TxTzbar
    <->
{7,13} / {17,23}
```

## Results 032--033 — independent residual-pair labels

Result 032 showed that the existing N4 chiral-overlap matrix `C` supplies
a quotient-level sign label that descends through `<Ty>`:

```text
Ibar     -> +
Txbar    -> -
Tzbar    -> +
TxTzbar  -> -
```

Within the residual M5 pair:

```text
Tzbar    -> +
TxTzbar  -> -
```

so the M5 quotient is fully distinguished within the tested quotient.

Result 033 independently constructed the canonical Reading Point binary
characters

```text
chi3:
  r mod 3 = 1 -> +1
  r mod 3 = 2 -> -1

chi5:
  r mod 5 in {1,4} -> +1
  r mod 5 in {2,3} -> -1
```

Both have `{1,19}` in their kernels and therefore descend to the Reading
Point quotient.

Their joint quotient labels are:

```text
{1,19}   -> (+1,+1)
{7,13}   -> (+1,-1)
{11,29}  -> (-1,+1)
{17,23}  -> (-1,-1)
```

`chi5` reproduces the singleton-plus-pair distinction, while `chi3`
distinguishes the remaining pair:

```text
{7,13}   -> chi3 = +1
{17,23}  -> chi3 = -1
```

Thus both quotient systems are internally fully labeled.

## Result 034 — two-bit correspondence audit

Result 034 compared the two remaining partition-preserving isomorphisms.

```text
Mapping A

Ibar     -> {1,19}
Txbar    -> {11,29}
Tzbar    -> {7,13}
TxTzbar  -> {17,23}

residual C-sign / chi3 relation:
ALIGNED
```

and

```text
Mapping B

Ibar     -> {1,19}
Txbar    -> {11,29}
Tzbar    -> {17,23}
TxTzbar  -> {7,13}

residual C-sign / chi3 relation:
REVERSED
```

Both are bijective, multiplication-preserving, and preserve the
independently established Result-031 partition.

Therefore complete internal labeling does not itself select a unique
cross-system orientation convention.

The correspondence count remains:

```text
2
```

## Results 035--038 — native orientation-anchor audit

Results 035--038 tested whether existing M5 structures independently
select the aligned or reversed convention.

### Result 035 — right-handed full-frame convention

The existing full-frame construction

```text
e3 = oriented long axis
e1 = oriented short axis
e2 = e3 x e1
O  = [e1,e2,e3]
```

is right-handed by construction.

However, an actual orientation-reversing spatial reflection leaves the
computed `C` approximately invariant after the implementation reconstructs
a right-handed eigenframe.

Therefore:

```text
right-handed full-frame convention anchors C-sign:
NOT SUPPORTED
```

### Result 036 — self-linking `N -> -N`

The existing N4 topology construction was evaluated for

```text
N = -2, -1, 0, 1, 2
```

Neither the full `C` matrix nor the baseline-subtracted `dC` obeyed a clean
odd/even sign law under `N -> -N`.

Therefore:

```text
native self-linking orientation anchors full C-sign:
NOT ESTABLISHED

native self-linking orientation anchors dC sign:
NOT ESTABLISHED
```

### Result 037 — native chiral-coupling signs

The native construction

```text
M_H = Mr + i * g_chiral * C
```

was audited under `g_chiral` and `chi` sign reversals.

The result is:

```text
g_chiral sign leaves geometric C even:
SUPPORTED

g_chiral sign reverses weighted g_chiral*C:
SUPPORTED

chi sign leaves geometric C even:
SUPPORTED
```

Thus `g_chiral` supplies a native sign for the weighted interaction term,
not an independent sign anchor for geometric `C`.

### Result 038 — Mermin-Ho / topological-flux sign

The existing signed Mermin-Ho / topological-flux machinery supplies the
same residual-pair sign structure on the tested M5 quotient.

That strengthens the native M5-side orientation labeling, but it does not
create an independent Reading Point rule identifying that sign with
`chi3` rather than `-chi3`.

Therefore Result 038 also leaves the cross-system correspondence count at
two.

## Result 039 — evidence-ledger / correspondence-boundary synthesis

Result 039 introduces no new M5 observable, no new Reading Point label,
and no new cross-system sign convention.

It reconstructs the strongest correspondence licensed by the executable
evidence.

The ledger is:

```text
Result 003  common V4 quotient                                  SUPPORTED
Result 027  repository-native M5 quotient                       SUPPORTED
Result 028  abstract M5 <-> Reading Point quotient isomorphisms SUPPORTED
Result 029  native M5 quotient observables                      SUPPORTED
Result 030  Reading Point native 1+2 partition                  SUPPORTED
Result 031  M5 native 1+2 partition                             SUPPORTED
Result 032  M5 residual-pair C-sign label                       SUPPORTED
Result 033  Reading Point residual-pair chi3 label              SUPPORTED
Result 034  two-bit cross-system correspondence audit           SUPPORTED
Result 035  right-handed full-frame C-sign anchor               NOT_SUPPORTED
Result 036  self-linking N -> -N C-sign anchor                  NOT_ESTABLISHED
Result 037  native chiral-sign C anchor                         NOT_ESTABLISHED
Result 038  Mermin-Ho/topological-flux C-sign anchor            NOT_ESTABLISHED
```

The resulting boundary is:

```text
common quotient structure:
SUPPORTED

repository-native M5 quotient:
SUPPORTED

Reading Point quotient intrinsically labeled:
SUPPORTED

M5 quotient intrinsically labeled:
SUPPORTED

partition-level cross-system correspondence:
SUPPORTED

abstract quotient isomorphisms:
6

partition-preserving isomorphisms:
2

currently admissible cross-system mappings:
2

independent orientation-alignment rule:
NOT_FOUND

unique structural correspondence:
NOT_ESTABLISHED

Reading Point -> M5 physical mapping:
NOT_ESTABLISHED
```

The implementation therefore supports:

```text
6 -> 2
```

but does not license:

```text
2 -> 1
```

without an additional independently established cross-system orientation
rule.

**Current implementation stopping boundary: SUPPORTED.**


## Claims not established

Results through 039 do not establish:

- a unique Reading Point ↔ M5 quotient isomorphism;
- an independently fixed cross-system orientation convention;
- `C-sign = chi3`;
- `C-sign = -chi3`;
- a unique residue-pair → M5 quotient-class assignment;
- a particle classification from the quotient correspondence;
- or a Reading Point → M5 physical mapping.

These remain open requirements rather than assumptions.

## Current program status

**Shared Reading Point / M5 V4 quotient structure: SUPPORTED.**

**Independent singleton-plus-pair bridge: SUPPORTED.**

**Abstract correspondence reduction `6 -> 2`: SUPPORTED.**

**Cross-system reduction `2 -> 1`: NOT LICENSED.**

**Unique Reading Point → M5 correspondence: NOT ESTABLISHED.**

**Reading Point → M5 physical mapping: NOT ESTABLISHED.**

**Current implementation stopping boundary through Result 039: SUPPORTED.**

## Next reading point

A further reduction requires evidence that is genuinely cross-system rather
than another internal label on either quotient.

The next admissible test should therefore require an independently motivated
rule that gives the M5 orientation sign and the Reading Point `chi3` sign the
same operational meaning.

Until such a rule is found or derived, the two remaining mappings should be
retained explicitly rather than selecting one by convention.
