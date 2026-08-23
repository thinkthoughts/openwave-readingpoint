# Result 027 --- Repository-Native Four-Class Quotient from the Basic Full-F Instrument

## Question

Do existing M5 full-frame scalar instruments define a natural four-class
reduction of the eight-state (C_2\^3)-like field closure without
choosing a (V_4) subgroup by hand?

Result 026 established that the full eigenframe connection and curvature
fields distinguish all eight tested states.

Result 027 asks whether any **existing scalar instrument** in the same
M5 full-F implementation naturally forgets exactly one binary degree of
freedom and thereby produces four composition-compatible classes.

## Source

The tested scalar instruments are defined in:

``` text
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_22_4_a_fullf.py
```

The repository-native reads are:

-   `comp3`
-   `comp2`
-   `comp1`
-   `norm3`
-   `basic`

Each is already evaluated through the existing cube-flux instrument at:

-   `half6`
-   `half12`
-   `half18`

No new scalar observable is introduced.

## Starting field structure

Result 023 established the eight-state field closure

\[ {I,T_x,T_y,T_z,T_xT_y,T_xT_z,T_yT_z,T_xT_yT_z}, \]

with three commuting order-2 generators.

The tested field-level composition is therefore:

\[ C_2\^3`\text{-like}`{=tex}. \]

Result 026 then showed that the existing full eigenframe
connection/curvature geometry retains all eight of those distinctions.

## Scalar search

Result 027 evaluates the ordered flavour triplet for each existing
scalar read and clusters the eight transformations using a preregistered
numerical equivalence rule.

A natural four-state quotient candidate is accepted only if:

1.  the scalar read gives exactly four classes;
2.  all four classes have size two;
3.  the measured equivalence relation is compatible with the Result-023
    composition law;
4.  no class pairing is selected by hand.

## `comp3`, `comp2`, `comp1`, and `norm3`

For every tested flux scale, these four full-F scalar reads retain all
eight states.

For each of:

``` text
comp3.half6
comp3.half12
comp3.half18

comp2.half6
comp2.half12
comp2.half18

comp1.half6
comp1.half12
comp1.half18

norm3.half6
norm3.half12
norm3.half18
```

the result is:

``` text
class_count = 8
class_sizes = [1,1,1,1,1,1,1,1]
composition_compatible = True
violations = 0
```

Thus these full-F reads preserve the complete eight-state distinction.

## `basic`

The existing `basic` longest-axis/Mermin-Ho instrument behaves
differently.

At all three tested flux scales it produces exactly four classes of size
two.

### `basic.half6`

``` text
class 0: I, Ty
class 1: Tx, TxTy
class 2: Tz, TyTz
class 3: TxTz, TxTyTz
```

### `basic.half12`

``` text
class 0: I, Ty
class 1: Tx, TxTy
class 2: Tz, TyTz
class 3: TxTz, TxTyTz
```

### `basic.half18`

``` text
class 0: I, Ty
class 1: Tx, TxTy
class 2: Tz, TyTz
class 3: TxTz, TxTyTz
```

For each scale:

``` text
class_count = 4
class_sizes = [2,2,2,2]
composition_compatible = True
violations = 0
four_classes_of_two = True
```

The same partition therefore appears independently at all three existing
flux scales.

## Kernel selected by the basic instrument

The identity class is:

\[ {I,T_y}. \]

Because (T_y\^2=I), this is the order-2 subgroup

\[ H=`\langle `{=tex}T_y`\rangle`{=tex}={I,T_y}. \]

The remaining measured classes are exactly its cosets:

\[ T_xH={T_x,T_xT_y}, \]

\[ T_zH={T_z,T_yT_z}, \]

\[ T_xT_zH={T_xT_z,T_xT_yT_z}. \]

Thus the repository-native `basic` scalar instrument defines the
quotient

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}. \]

Since the quotient has two remaining independent order-2 generators,

\[ `\boxed{
C_2^3/\langle T_y\rangle
\cong
C_2^2
\cong
V_4
}`{=tex} \]

for the tested transformation structure.

## Why this is stronger than selecting an embedded (V_4)

Result 023 showed that a (C_2\^3)-like group contains multiple embedded
four-element (V_4) subgroups.

Choosing one of those subgroups merely because it has four elements
would be arbitrary.

Result 027 does something different.

The existing M5 `basic` observable itself defines an equivalence
relation. Its kernel is (`\langle `{=tex}T_y`\rangle`{=tex}), and its
measured equivalence classes are the cosets of that kernel.

So the four-state structure is a **quotient selected by a
repository-native observable**, rather than a subgroup chosen
externally.

## Full-F versus basic information

The result also clarifies the relationship between the full and basic M5
electric instruments.

The full-F scalar components:

``` text
comp1
comp2
comp3
norm3
```

retain all eight states.

The older/basic longest-axis instrument retains only four classes.

Schematically:

\[ C_2\^3 `\overset{\text{full-F scalars}}{\longrightarrow}`{=tex}
8`\text{ resolved states}`{=tex}, \]

while

\[ C_2\^3 `\overset{\text{basic}}{\longrightarrow}`{=tex}
C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex} `\cong `{=tex}V_4. \]

The `basic` instrument therefore forgets precisely the (T_y) bit in this
tested closure.

## Scale stability

The same kernel and coset partition appear for:

\[ `\texttt{half6}`{=tex},`\quad`{=tex}
`\texttt{half12}`{=tex},`\quad`{=tex} `\texttt{half18}`{=tex}. \]

Thus the four-class reduction is not confined to one cube-flux scale in
this test.

## Result

### Supported

``` text
Repository-native four-class quotient:
SUPPORTED

Successful existing scalar instruments:
basic.half6
basic.half12
basic.half18

Kernel:
<Ty> = {I, Ty}

Measured quotient:
C2^3 / <Ty>

Abstract quotient structure:
C2^2 ≅ V4

Composition compatibility:
SUPPORTED

Scale stability across half6 / half12 / half18:
SUPPORTED
```

### Still open

``` text
Identification with Q8/{+1,-1}:
NOT ESTABLISHED

Correspondence to the Reading Point quotient:
NOT ESTABLISHED

Physical handedness identification:
NOT YET ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Relation to the earlier effective readouts

The tested information hierarchy is now:

\[ C_2\^3`\text{-like field closure}`{=tex} \]

with several different observable resolutions:

\[ C`\text{ sign}`{=tex} `\rightarrow
2`{=tex}`\text{ classes}`{=tex}, \]

\[ M_r `\rightarrow`{=tex} `\text{no added discrimination}`{=tex}, \]

\[ O(M)`\rightarrow`{=tex}`\Gamma`{=tex}`\rightarrow `{=tex}R
`\rightarrow
8`{=tex}`\text{ classes}`{=tex}, \]

\[ `\texttt{basic}`{=tex} `\rightarrow
4`{=tex}`\text{ classes}`{=tex} =
C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}. \]

Different existing observables therefore expose different amounts of the
same tested field-level transformation structure.

## Next reading point

The existence of a repository-native (V_4)-quotient candidate makes the
next question much sharper.

Result 028 should ask whether the quotient

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex} \]

has an independently defined generator correspondence to the previously
established four-element quotients

\[ Q_8/{+1,-1} \]

and the Reading Point quotient.

Abstract group isomorphism is insufficient because all three are
(V_4)-type structures and the three nonidentity elements can be
permuted.

So the next test must require a correspondence based on independently
defined actions, labels, or observables rather than an arbitrary
permutation chosen after seeing the result.

Until that correspondence is established:

\[
`\boxed{\text{Reading Point} \rightarrow \text{M5 physical mapping: NOT ESTABLISHED}}`{=tex}
\]
