# Result 026 --- Existing M → Full Eigenframe → Connection/Curvature Discriminator

## Question

Does the already implemented M5 full-eigenframe connection/curvature
machinery distinguish transformations inside the four-element (C)-sign
classes left unresolved by Result 024?

Result 025 had reached a stopping boundary for the specifically examined
route

\[ M `\rightarrow `{=tex}(q_0,q) `\rightarrow `{=tex}`\Gamma`{=tex}/R,
\]

because no implemented (M`\rightarrow`{=tex}(q_0,q)) projection was
found.

A subsequent repository-wide audit found a different existing M5 route
in:

``` text
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_22_4_a_fullf.py
```

That implementation begins directly from (M):

\[ M `\rightarrow`{=tex} O(M) `\rightarrow`{=tex} `\Gamma`{=tex}*i
`\rightarrow`{=tex} G_i `\rightarrow`{=tex} R*{ij}. \]

Result 026 tests this existing route. It introduces neither a new
(M`\to `{=tex}q) projection nor a new flavour-space contraction.

## Prior state

Result 023 established eight distinct commuting involutions at field
level:

\[ I, T_x, T_y, T_z, T_xT_y, T_xT_z, T_yT_z, T_xT_yT_z, \]

classified as a (C_2\^3)-like closure.

The N4 antisymmetric operator (C) reduced these to two sign sectors:

\[ K\_+ = {I,T_y,T_z,T_yT_z}, \]

\[ K\_- = {T_x,T_xT_y,T_xT_z,T_xT_yT_z}. \]

Result 024 showed that the independently defined real overlap sector
(M_r) adds no discrimination within those sectors.

## Existing geometric route

The tested M5 implementation constructs the oriented full spatial
eigenframe (O(M)), then evaluates the connection-vector fields
associated with

\[ `\Gamma`{=tex}\_i = O\^T`\partial`{=tex}\_i O. \]

The three connection-vector fields are retained as (G_x,G_y,G_z).

The tested curvature-vector fields are

\[ R\_{xy}=G_x`\times `{=tex}G_y, `\qquad`{=tex}
R\_{xz}=G_x`\times `{=tex}G_z, `\qquad`{=tex}
R\_{yz}=G_y`\times `{=tex}G_z. \]

For the N3/N4 (4`\times4`{=tex}) field representation, the existing
spatial (SO(3)) full-frame routine is applied to the spatial block

\[ M\_{`\rm sp`{=tex}}=M\[...,1:4,1:4\]. \]

No (M`\rightarrow`{=tex}(q_0,q)) conversion is used.

## Parameters

``` text
n        = 40
dx       = 1.0
alpha    = 0.6
delta    = 0.1
chi      = 0.6
q        = 0.5
R_loop   = 9.0
core_vox = 2.0
kappa    = 0.0
```

The preregistered normalized-field equivalence threshold was:

``` text
1.0e-4
```

## Per-transformation norms

``` text
I        C=+  ||G||=8.366680e+01  ||R||=1.150419e+01
Tx       C=-  ||G||=8.366680e+01  ||R||=1.150419e+01
Ty       C=+  ||G||=8.366680e+01  ||R||=1.150419e+01
Tz       C=+  ||G||=8.265405e+01  ||R||=1.082988e+01
TxTy     C=-  ||G||=8.366680e+01  ||R||=1.150419e+01
TxTz     C=-  ||G||=8.265405e+01  ||R||=1.082988e+01
TyTz     C=+  ||G||=8.265405e+01  ||R||=1.082988e+01
TxTyTz   C=-  ||G||=8.265405e+01  ||R||=1.082988e+01
```

The norm alone does not distinguish all eight states. The full
normalized field shapes do.

## Discrimination inside the Result-024 kernels

There are 12 unordered pairs lying within the two equal-(C)-sign
sectors.

Result 026 found:

``` text
normalized G separates:      12 / 12
normalized R separates:      12 / 12
G or R separates:            12 / 12
```

The observed normalized-field distances are large relative to the
(10\^{-4}) equivalence threshold. For the equal-(C)-sign pairs, the
reported (G) distances range from approximately (0.882) to (1.439),
while the (R) distances range from approximately (1.212) to (1.508).

Thus the full-frame geometric sector adds substantial discrimination
that is absent from the (C+M_r) effective readout.

## Joint geometric partition

Using (C) sign together with the normalized full-frame (G) and (R)
fields gives:

``` text
class 0: I
class 1: Tx
class 2: Ty
class 3: Tz
class 4: TxTy
class 5: TxTz
class 6: TyTz
class 7: TxTyTz
```

Therefore:

\[ `\boxed{\text{class count}=8}`{=tex} \]

Every tested Result-023 field transformation is separately resolved.

## Composition compatibility

The measured eight-class partition was checked against the Result-023
(C_2\^3)-like composition law.

``` text
composition compatibility: SUPPORTED
violations: 0
```

Because every state is a singleton class, the geometric readout
preserves the full tested field-level distinction rather than imposing a
smaller quotient.

## Result

\[ `\boxed{
C_2^3\text{-like field closure}
\longrightarrow
\begin{cases}
C\text{ sign}: 2\text{ classes},\\
M_r: \text{no added discrimination},\\
O(M)\to\Gamma\to R: 8\text{ classes}.
\end{cases}
}`{=tex} \]

The existing full-eigenframe geometric sector therefore recovers
distinctions among all eight tested field states that were collapsed by
the N4 (C)-sign and real-overlap observables.

### Supported

``` text
Existing M -> O(M) -> Gamma -> R route:
SUPPORTED

Connection-vector discrimination:
12/12 equal-C-sign pairs

Curvature-vector discrimination:
12/12 equal-C-sign pairs

Eight-class geometric readout:
SUPPORTED

Composition compatibility:
SUPPORTED
```

### Not established

``` text
Unique V4 selection:
NOT ESTABLISHED

Q8/{+1,-1} identification:
NOT ESTABLISHED

Physical handedness identification:
NOT YET ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Relation to Result 025

Result 026 does not invalidate Result 025.

Result 025 correctly established that the specifically audited
field-level connection implementation beginning from ((q_0,q)) lacked an
examined executable bridge from the N3/N4 rank-2 (M) fields.

Result 026 records a subsequently discovered, independently implemented
route that begins directly from (M) through its oriented spatial
eigenframe.

The evidence trail is therefore:

\[ M`\rightarrow`{=tex}(q_0,q)`\rightarrow`{=tex}`\Gamma`{=tex}/R:
`\quad`{=tex} `\text{bridge not established in Result 025}`{=tex}, \]

while

\[
M`\rightarrow `{=tex}O(M)`\rightarrow`{=tex}`\Gamma`{=tex}`\rightarrow `{=tex}R:
`\quad`{=tex}
`\text{existing executable route supported in Result 026}`{=tex}. \]

## Consequence

The unresolved question is no longer whether the existing M5
implementation contains a geometric observable capable of distinguishing
the eight Result-023 states.

It does.

The next question is whether existing M5 geometry supplies an
independently motivated reduction of those eight states.

A subsequent test should therefore ask:

> Do existing geometric invariants or symmetry relations define a
> natural four-class reduction of the eight-state (C_2\^3)-like
> geometric structure without selecting a (V_4) subgroup by hand?

Until such a criterion is established, the eight-state geometric
resolution itself does not license a unique (V_4), a (Q_8/{+1,-1})
identification, or a Reading Point → M5 physical mapping.
