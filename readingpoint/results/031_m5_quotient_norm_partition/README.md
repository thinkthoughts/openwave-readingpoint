# Result 031 --- Native M5 1+2 Quotient Partition from Full-Frame Norms

## Question

Result 030 established a partial intrinsic label structure on the
Reading Point quotient:

\[ {11,29} `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex} {{7,13},{17,23}}. \]

The class ({11,29}) is uniquely distinguished by the inherited
parent-group order profile

\[ (2,2), \]

while the other two nonidentity classes both carry

\[ (4,4). \]

Result 031 asks whether an independently defined existing M5 observable
produces the same **singleton + pair** structure on the three
nonidentity classes of

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}. \]

The candidate M5 observables are the existing full-frame geometric norms

\[ \|G\|\_F \]

and

\[ \|R\|\_F \]

from the already implemented route

\[
M`\rightarrow `{=tex}O(M)`\rightarrow `{=tex}`\Gamma`{=tex}*i`\rightarrow `{=tex}G_i`\rightarrow `{=tex}R*{ij}.
\]

No Reading Point residue assignment is imposed.

## Result-027 quotient

The quotient classes are

\[ `\bar `{=tex}I={I,T_y}, \]

\[ `\bar `{=tex}T_x={T_x,T_xT_y}, \]

\[ `\bar `{=tex}T_z={T_z,T_yT_z}, \]

and

\[ `\overline{T_xT_z}`{=tex}={T_xT_z,T_xT_yT_z}. \]

The relevant nonidentity classes are therefore

\[ `\bar `{=tex}T_x,`\qquad`{=tex} `\bar `{=tex}T_z,`\qquad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

## Existing geometric observables

The tested observables are:

``` text
||G||_F
    Frobenius norm of the stacked full-eigenframe
    connection-vector fields.

||R||_F
    Frobenius norm of the stacked full-eigenframe
    curvature-vector fields.
```

They are not newly fitted scalars. They are the existing geometric
quantities already measured in Result 026.

## Per-transformation values

``` text
I        ||G||=8.366680495e+01  ||R||=1.150418722e+01
Tx       ||G||=8.366680495e+01  ||R||=1.150418722e+01
Ty       ||G||=8.366680495e+01  ||R||=1.150418722e+01
Tz       ||G||=8.265404600e+01  ||R||=1.082988097e+01
TxTy     ||G||=8.366680495e+01  ||R||=1.150418722e+01
TxTz     ||G||=8.265404600e+01  ||R||=1.082988097e+01
TyTz     ||G||=8.265404600e+01  ||R||=1.082988097e+01
TxTyTz   ||G||=8.265404600e+01  ||R||=1.082988097e+01
```

Already at the eight-state level, the norms separate the closure into
two norm levels.

The first requirement is to determine whether those norms genuinely
descend through the Result-027 kernel.

## Quotient descent

For an observable (f) to be well-defined on

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}, \]

it must satisfy

\[ f(I)`\simeq `{=tex}f(T_y), \]

\[ f(T_x)`\simeq `{=tex}f(T_xT_y), \]

\[ f(T_z)`\simeq `{=tex}f(T_yT_z), \]

and

\[ f(T_xT_z)`\simeq `{=tex}f(T_xT_yT_z). \]

### (G)-norm

The descent errors are:

``` text
Ibar      0.000000e+00
Txbar     1.698506e-16
Tzbar     1.719317e-16
TxTzbar   1.719317e-16
```

Maximum:

\[ 1.719317`\times10`{=tex}\^{-16}. \]

Therefore:

``` text
G_norm descends through <Ty>:
SUPPORTED
```

### (R)-norm

The descent errors are:

``` text
Ibar      0.000000e+00
Txbar     1.544096e-16
Tzbar     3.280473e-16
TxTzbar   3.280473e-16
```

Maximum:

\[ 3.280473`\times10`{=tex}\^{-16}. \]

Therefore:

``` text
R_norm descends through <Ty>:
SUPPORTED
```

Both observables are therefore legitimate quotient-level M5 observables.

## Native M5 partition from (\|G\|\_F)

The nonidentity quotient values are:

``` text
Txbar      8.366680495e+01
Tzbar      8.265404600e+01
TxTzbar    8.265404600e+01
```

Relative pair errors are:

``` text
Txbar   vs Tzbar:    1.210467e-02
Txbar   vs TxTzbar:  1.210467e-02
Tzbar   vs TxTzbar:  0.000000e+00
```

Thus:

\[ `\boxed{
\bar T_x
\quad\big|\quad
\{\bar T_z,\overline{T_xT_z}\}
}`{=tex} \]

is supported by the existing connection norm.

## Native M5 partition from (\|R\|\_F)

The nonidentity quotient values are:

``` text
Txbar      1.150418722e+01
Tzbar      1.082988097e+01
TxTzbar    1.082988097e+01
```

Relative pair errors are:

``` text
Txbar   vs Tzbar:    5.861398e-02
Txbar   vs TxTzbar:  5.861398e-02
Tzbar   vs TxTzbar:  0.000000e+00
```

Again:

\[ `\boxed{
\bar T_x
\quad\big|\quad
\{\bar T_z,\overline{T_xT_z}\}
}`{=tex} \]

is independently recovered.

## Consistent M5 1+2 partition

Both existing geometric norm observables therefore give the same
partition:

``` text
singleton:
Txbar

equivalent pair:
{Tzbar, TxTzbar}
```

Hence:

\[ `\boxed{
\text{Native M5 1+2 quotient partition: SUPPORTED}
}`{=tex} \]

## Reading Point comparison

Result 030 independently established:

``` text
Reading Point singleton:
{11,29}

Reading Point pair:
{{7,13}, {17,23}}
```

through the parent-element order profiles

\[ (2,2) \]

versus

\[ (4,4). \]

The M5 and Reading Point quotient label structures therefore have the
same independently obtained abstract form:

\[ 1+2. \]

Schematically:

\[ `\bar `{=tex}T_x `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
{`\bar `{=tex}T_z,`\overline{T_xT_z}`{=tex}} \]

matches

\[ {11,29} `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex} {{7,13},{17,23}}. \]

## Correspondence reduction

Result 028 found six abstract quotient isomorphisms.

Before Result 031:

\[ 6 \]

mappings were algebraically admissible.

If an isomorphism is now required to preserve the independently
established singleton-plus-pair structures, then the distinguished
singleton must map to the distinguished singleton:

\[ `\boxed{
\bar T_x \leftrightarrow \{11,29\}
}`{=tex} \]

at the **partition-label level**.

The remaining pair may still be exchanged:

\[ `\bar `{=tex}T_z,`\overline{T_xT_z}`{=tex}
`\quad`{=tex}`\leftrightarrow`{=tex}`\quad`{=tex} {7,13},{17,23}. \]

Therefore the structurally admissible correspondence count is reduced
to:

\[ `\boxed{
6\rightarrow2
}`{=tex} \]

with residual symmetry

\[ C_2. \]

## Result

### Supported

``` text
G_norm quotient descent:
SUPPORTED

R_norm quotient descent:
SUPPORTED

Native M5 1+2 partition:
SUPPORTED

M5 singleton:
Txbar

M5 equivalent pair:
{Tzbar, TxTzbar}

Reading Point / M5 partition compatibility:
SUPPORTED

Distinguished singleton correspondence:
Txbar <-> {11,29}
SUPPORTED AT PARTITION LEVEL

Partition-preserving isomorphisms:
2
```

### Still open

``` text
Which of Tzbar / TxTzbar corresponds to {7,13}:
NOT ESTABLISHED

Which of Tzbar / TxTzbar corresponds to {17,23}:
NOT ESTABLISHED

Unique Reading Point -> M5 correspondence:
NOT ESTABLISHED

Physical Q8/{+1,-1} identification:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Interpretation

Result 031 is the first point in the test program where independently
defined labels on the two sides constrain the same quotient isomorphism.

The M5 full-frame geometry independently produces

\[ `\bar `{=tex}T_x `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex}
{`\bar `{=tex}T_z,`\overline{T_xT_z}`{=tex}}, \]

while the Reading Point parent group independently produces

\[ {11,29} `\quad`{=tex}`\big`{=tex}\|`\quad`{=tex} {{7,13},{17,23}}. \]

That shared (1+2) structure is stronger than an abstract (V_4)
isomorphism because it removes the full (S_3) freedom among the three
nonidentity elements.

What remains is exactly one binary ambiguity.

## Next reading point

Result 032 should ask whether an independently defined orientation,
sign, ordering, or other repository-native invariant distinguishes the
remaining pair on both sides.

The target is now:

\[ 2`\rightarrow1`{=tex}. \]

On the M5 side the unresolved pair is

\[ `\bar `{=tex}T_z `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

On the Reading Point side it is

\[ {7,13} `\quad`{=tex}`\text{vs}`{=tex}`\quad`{=tex} {17,23}. \]

A unique correspondence can be claimed only if a pre-existing or
independently derived invariant distinguishes these pairs in
corresponding fashion.

Until then:

\[ `\boxed{
\text{Reading Point}\rightarrow\text{M5 physical mapping:
NOT ESTABLISHED}
}`{=tex} \]
