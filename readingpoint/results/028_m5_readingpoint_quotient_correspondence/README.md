# Result 028 --- M5 Quotient → Reading Point Quotient Correspondence Audit

## Question

Result 027 established a repository-native four-class M5 quotient

\[ C_2^3/`\langle `{=tex}T_y`\rangle `{=tex}`\cong `{=tex}C_2^2
`\cong `{=tex}V_4. \]

Reading Point work independently established the four-class quotient

\[ (`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^`\times`{=tex}/{1,19}
`\cong `{=tex}C_2`\times `{=tex}C_2 `\cong `{=tex}V_4. \]

Result 028 asks a stronger question than whether these groups are
abstractly isomorphic:

> Does their multiplication structure uniquely determine which
> nonidentity M5 class corresponds to which nonidentity Reading Point
> residue-pair class?

No residue-to-M5 assignment is imposed before the test.

## M5 quotient

The kernel selected by the existing M5 `basic` instrument in Result 027
is

\[ `\langle `{=tex}T_y`\rangle`{=tex}={I,T_y}. \]

The four quotient classes are therefore

\[ `\bar `{=tex}I={I,T_y}, \]

\[ `\bar `{=tex}T_x={T_x,T_xT_y}, \]

\[ `\bar `{=tex}T_z={T_z,T_yT_z}, \]

and

\[ `\overline{T_xT_z}`{=tex}={T_xT_z,T_xT_yT_z}. \]

Their multiplication table is:

  -----------------------------------------------------------------------------------------------------------------------------------------------------
  ×                             (`\bar `{=tex}I)              (`\bar `{=tex}T_x)            (`\bar `{=tex}T_z)            (`\overline{T_xT_z}`{=tex})
  ----------------------------- ----------------------------- ----------------------------- ----------------------------- -----------------------------
  (`\bar `{=tex}I)              (`\bar `{=tex}I)              (`\bar `{=tex}T_x)            (`\bar `{=tex}T_z)            (`\overline{T_xT_z}`{=tex})

  (`\bar `{=tex}T_x)            (`\bar `{=tex}T_x)            (`\bar `{=tex}I)              (`\overline{T_xT_z}`{=tex})   (`\bar `{=tex}T_z)

  (`\bar `{=tex}T_z)            (`\bar `{=tex}T_z)            (`\overline{T_xT_z}`{=tex})   (`\bar `{=tex}I)              (`\bar `{=tex}T_x)

  (`\overline{T_xT_z}`{=tex})   (`\overline{T_xT_z}`{=tex})   (`\bar `{=tex}T_z)            (`\bar `{=tex}T_x)            (`\bar `{=tex}I)
  -----------------------------------------------------------------------------------------------------------------------------------------------------

Thus every nonidentity element has order two and

\[ G\_{`\mathrm{M5}`{=tex}}`\cong `{=tex}V_4. \]

## Reading Point quotient

The mod-30 unit group is

\[ (`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^`\times`{=tex} =
{1,7,11,13,17,19,23,29}. \]

Using the order-two subgroup

\[ H={1,19}, \]

the quotient classes generated directly by multiplication modulo 30 are

\[ {1,19}, `\qquad`{=tex} {7,13}, `\qquad`{=tex} {11,29}, `\qquad`{=tex}
{17,23}. \]

Their multiplication table is:

  ×         {1,19}    {7,13}    {11,29}   {17,23}
  --------- --------- --------- --------- ---------
  {1,19}    {1,19}    {7,13}    {11,29}   {17,23}
  {7,13}    {7,13}    {1,19}    {17,23}   {11,29}
  {11,29}   {11,29}   {17,23}   {1,19}    {7,13}
  {17,23}   {17,23}   {11,29}   {7,13}    {1,19}

Again, every nonidentity element has order two:

\[ G\_{`\mathrm{RP}`{=tex}} =
(`\mathbb `{=tex}Z/30`\mathbb `{=tex}Z)\^`\times`{=tex}/{1,19}
`\cong `{=tex}V_4. \]

## Abstract compatibility

The two measured/established quotient structures therefore satisfy

\[ `\boxed{
C_2^3/\langle T_y\rangle
\cong
(\mathbb Z/30\mathbb Z)^\times/\{1,19\}
\cong
V_4
}`{=tex} \]

at the level of abstract group structure.

The test then asks whether that fact fixes a unique element-by-element
correspondence.

## Exhaustive correspondence audit

The identity classes must correspond:

\[ `\bar `{=tex}I `\longmapsto `{=tex}{1,19}. \]

That leaves three nonidentity M5 classes and three nonidentity Reading
Point classes.

There are

\[ 3! = 6 \]

identity-preserving bijections.

Result 028 enumerates all six and checks multiplication preservation
directly.

### Mapping 1

\[ `\bar `{=tex}T_x`\to`{=tex}{7,13}, `\quad`{=tex}
`\bar `{=tex}T_z`\to`{=tex}{11,29}, `\quad`{=tex}
`\overline{T_xT_z}`{=tex}`\to`{=tex}{17,23}. \]

### Mapping 2

\[ `\bar `{=tex}T_x`\to`{=tex}{7,13}, `\quad`{=tex}
`\bar `{=tex}T_z`\to`{=tex}{17,23}, `\quad`{=tex}
`\overline{T_xT_z}`{=tex}`\to`{=tex}{11,29}. \]

### Mapping 3

\[ `\bar `{=tex}T_x`\to`{=tex}{11,29}, `\quad`{=tex}
`\bar `{=tex}T_z`\to`{=tex}{7,13}, `\quad`{=tex}
`\overline{T_xT_z}`{=tex}`\to`{=tex}{17,23}. \]

### Mapping 4

\[ `\bar `{=tex}T_x`\to`{=tex}{11,29}, `\quad`{=tex}
`\bar `{=tex}T_z`\to`{=tex}{17,23}, `\quad`{=tex}
`\overline{T_xT_z}`{=tex}`\to`{=tex}{7,13}. \]

### Mapping 5

\[ `\bar `{=tex}T_x`\to`{=tex}{17,23}, `\quad`{=tex}
`\bar `{=tex}T_z`\to`{=tex}{7,13}, `\quad`{=tex}
`\overline{T_xT_z}`{=tex}`\to`{=tex}{11,29}. \]

### Mapping 6

\[ `\bar `{=tex}T_x`\to`{=tex}{17,23}, `\quad`{=tex}
`\bar `{=tex}T_z`\to`{=tex}{11,29}, `\quad`{=tex}
`\overline{T_xT_z}`{=tex}`\to`{=tex}{7,13}. \]

All six preserve multiplication.

Therefore:

``` text
Identity-preserving bijections tested:
6

Multiplication-preserving isomorphisms:
6
```

## Residual symmetry

The quotient algebra distinguishes the identity from the three
nonidentity elements, but it supplies no further label among those three
elements.

The residual freedom is therefore the full permutation group

\[ S_3 \]

acting on the three nonidentity classes.

Equivalently,

\[ \|`\operatorname{Aut}`{=tex}(V_4)\|=6. \]

Thus abstract quotient compatibility cannot choose one of the six
mappings.

## Relation to (Q_8/{`\pm1`{=tex}})

The quaternion quotient

\[ Q_8/{+1,-1} \]

also has four elements and the same abstract multiplication structure:

\[ Q_8/{`\pm1`{=tex}}`\cong `{=tex}V_4. \]

Result 028 performs the same abstract comparison and finds six
identity-preserving, multiplication-preserving isomorphisms.

Therefore

\[ `\boxed{
C_2^3/\langle T_y\rangle
\cong
(\mathbb Z/30\mathbb Z)^\times/\{1,19\}
\cong
Q_8/\{\pm1\}
\cong V_4
}`{=tex} \]

is supported as an **abstract quotient statement**.

It does not select which M5 nonidentity class should be called
(\[`\pm `{=tex}i\]), (\[`\pm `{=tex}j\]), or (\[`\pm `{=tex}k\]).

## Result

### Supported

``` text
M5 quotient classification:
V4

Reading Point quotient classification:
V4

Abstract M5 -> Reading Point quotient isomorphism:
SUPPORTED

Identity-preserving bijections:
6

Multiplication-preserving isomorphisms:
6

Residual correspondence symmetry:
S3

Q8/{+1,-1} abstract quotient compatibility:
SUPPORTED

PASS
```

### Not established

``` text
Unique generator correspondence:
NOT SUPPORTED

Reading Point residue-pair -> M5 class assignment:
NOT ESTABLISHED

Physical Q8/{+1,-1} identification:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Interpretation

Results 023--027 progressively reduced the structural problem:

\[ 8`\text{-state }`{=tex}C_2\^3`\text{-like field closure}`{=tex} \]

followed by the repository-native `basic` observable,

\[ C_2\^3 `\longrightarrow`{=tex}
C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}, \]

giving a four-class (V_4) quotient.

Result 028 establishes that the independently defined Reading Point
quotient has exactly the same abstract multiplication structure.

The remaining problem is therefore no longer:

> Is there a four-state structure?

There is.

It is also no longer:

> Does the abstract quotient algebra match?

It does.

The unresolved question is:

> Which independently defined physical or geometric structure
> distinguishes the three nonidentity classes?

Without such a structure, all six generator correspondences remain
equally admissible.

## Next reading point

Result 029 should audit existing M5 provenance for a native distinction
among

\[ `\bar `{=tex}T_x,`\qquad`{=tex} `\bar `{=tex}T_z,`\qquad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

Candidate sources include already-defined:

-   spatial-axis roles,
-   orientation conventions,
-   electric or magnetic reads,
-   charge signs,
-   topological quantities,
-   calibrated defect labels,
-   particle/defect analog labels,
-   other repository-native transformation properties.

The audit should remain independent of the Reading Point residue labels.

The target is measurable:

\[ 6 `\text{admissible correspondences}`{=tex}
`\quad`{=tex}`\longrightarrow`{=tex}`\quad`{=tex}
`\text{fewer than }`{=tex}6 \]

only where an independently established M5 constraint licenses that
reduction.

A unique Reading Point correspondence requires:

\[ 6`\longrightarrow1`{=tex}. \]

Until such a constraint is established,

\[ `\boxed{
\text{Reading Point}\rightarrow\text{M5 physical mapping:
NOT ESTABLISHED}
}`{=tex} \]
