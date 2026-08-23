# Result 029 --- Native M5 Axis/Flux Labels on the Result-027 Quotient

## Question

Result 027 established the repository-native M5 quotient

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex} `\cong`{=tex} V_4, \]

with classes

\[ `\bar `{=tex}I={I,T_y}, \]

\[ `\bar `{=tex}T_x={T_x,T_xT_y}, \]

\[ `\bar `{=tex}T_z={T_z,T_yT_z}, \]

and

\[ `\overline{T_xT_z}`{=tex}={T_xT_z,T_xT_yT_z}. \]

Result 028 then showed that this quotient is abstractly isomorphic to
the Reading Point quotient, but that all six permutations of the three
nonidentity elements remain algebraically admissible.

Result 029 asks:

> Which existing M5 scalar observables are genuinely defined on the
> Result-027 quotient, and do any of them intrinsically distinguish
> (`\bar `{=tex}T_x), (`\bar `{=tex}T_z), and
> (`\overline{T_xT_z}`{=tex})?

The distinction is important because an observable that still
distinguishes the two representatives inside a quotient class carries
valid eight-state information, but it is not itself a function on the
quotient.

## Repository-native candidates

The tested observables come directly from:

``` text
openwave/xperiments/m5_liquid_crystal/research/scripts/m5_22_4_a_fullf.py
```

The existing scalar reads are:

``` text
comp1   short-axis full-F curvature component
comp2   middle-axis full-F curvature component
comp3   long-axis full-F curvature component
norm3   signed full-curvature magnitude
basic   longest-axis / Mermin-Ho basic instrument
```

Each is evaluated at the existing flux scales:

``` text
half6
half12
half18
```

No new scalar observable or classifier is introduced.

## Quotient-descent requirement

The Result-027 kernel is

\[ `\langle `{=tex}T_y`\rangle`{=tex}={I,T_y}. \]

A scalar observable (f) can label the quotient only where it is constant
on every coset:

\[ f(I)`\simeq `{=tex}f(T_y), \]

\[ f(T_x)`\simeq `{=tex}f(T_xT_y), \]

\[ f(T_z)`\simeq `{=tex}f(T_yT_z), \]

\[ f(T_xT_z)`\simeq `{=tex}f(T_xT_yT_z). \]

The preregistered scalar equivalence tolerance is

\[ 10\^{-8}. \]

Only an observable satisfying all four relations is admitted as an
intrinsic observable on

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex}. \]

## Full-F axis/component reads

The full-F reads do not descend through the quotient.

### `comp1`

``` text
half6   max descent error = 8.973397e-02
half12  max descent error = 1.220418e-02
half18  max descent error = 2.317145e-05
```

### `comp2`

``` text
half6   max descent error = 4.454986e-02
half12  max descent error = 2.877405e-01
half18  max descent error = 2.630657e-03
```

### `comp3`

``` text
half6   max descent error = 1.271715e-02
half12  max descent error = 4.289527e-04
half18  max descent error = 1.173227e-05
```

### `norm3`

``` text
half6   max descent error = 3.702051e-02
half12  max descent error = 7.469753e-03
half18  max descent error = 2.188746e-04
```

All remain above the (10\^{-8}) quotient-equivalence threshold.

Therefore these observables retain information that distinguishes states
inside the Result-027 cosets.

That information is meaningful at the eight-state field level, but these
reads are not admissible as quotient-level labels.

## The `basic` instrument

The existing longest-axis/Mermin-Ho `basic` read behaves differently.

### `basic.half6`

The maximum descent error is

\[ 1.444477`\times10`{=tex}\^{-16}. \]

Thus `basic.half6` descends through
(`\langle `{=tex}T_y`\rangle`{=tex}).

Its three nonidentity quotient signatures are:

``` text
Txbar:
[-1.146741472e+00, -1.083055504e-01, -1.079678755e-01]

Tzbar:
[-1.042859801e+00, -2.867537697e-01, -2.693187098e-01]

TxTzbar:
[-1.042859801e+00, -2.693187098e-01, -2.867537697e-01]
```

Pairwise distances are:

``` text
Txbar   vs Tzbar:    2.265102e-01
Txbar   vs TxTzbar:  2.265296e-01
Tzbar   vs TxTzbar:  2.212189e-02
```

All three nonidentity quotient classes are distinct.

### `basic.half12`

The maximum descent error is

\[ 1.387779`\times10`{=tex}\^{-16}. \]

The quotient signatures are:

``` text
Txbar:
[+1.801350272e-02, +2.900681130e-01, +2.869045814e-01]

Tzbar:
[-2.343001942e-02, -2.219693854e-01, -2.177119766e-01]

TxTzbar:
[-2.343001942e-02, -2.177119766e-01, -2.219693854e-01]
```

Pairwise distances are:

``` text
Txbar   vs Tzbar:    7.200957e-01
Txbar   vs TxTzbar:  7.200770e-01
Tzbar   vs TxTzbar:  6.020885e-03
```

Again, all three nonidentity classes are distinct.

### `basic.half18`

The maximum descent error is

\[ 2.256730`\times10`{=tex}\^{-18}. \]

The quotient signatures are:

``` text
Txbar:
[-4.541505500e-06, -2.601580131e-04, -2.631723357e-04]

Tzbar:
[-1.525195992e-04, -4.091048998e-04, -4.063453524e-04]

TxTzbar:
[-1.525195992e-04, -4.063453524e-04, -4.091048998e-04]
```

Pairwise distances are:

``` text
Txbar   vs Tzbar:    2.541283e-04
Txbar   vs TxTzbar:  2.540956e-04
Tzbar   vs TxTzbar:  3.902589e-06
```

All three remain distinct.

## Summary of descent

Of the 15 repository-native scalar candidates tested:

``` text
comp1.half6
comp1.half12
comp1.half18

comp2.half6
comp2.half12
comp2.half18

comp3.half6
comp3.half12
comp3.half18

norm3.half6
norm3.half12
norm3.half18

basic.half6
basic.half12
basic.half18
```

only:

``` text
basic.half6
basic.half12
basic.half18
```

descend through the Result-027 kernel.

And all three descended `basic` reads distinguish:

\[ `\bar `{=tex}T_x, `\qquad`{=tex} `\bar `{=tex}T_z, `\qquad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

Therefore:

\[ `\boxed{
\text{Native M5 quotient labeling: SUPPORTED}
}`{=tex} \]

## Information hierarchy

The results now separate three levels of information.

### Full field geometry

The full eigenframe connection/curvature sector resolves all eight
states:

\[ C_2\^3 `\longrightarrow
8`{=tex}`\text{ geometric states}`{=tex}. \]

### Quotient selection

The `basic` instrument identifies the kernel

\[ `\langle `{=tex}T_y`\rangle`{=tex} \]

and produces

\[ C_2\^3/`\langle `{=tex}T_y`\rangle`{=tex} `\cong`{=tex} V_4. \]

### Quotient-level native labels

The same `basic` instrument descends through that kernel and gives
distinct signatures to the three nonidentity classes:

\[ `\bar `{=tex}T_x, `\qquad`{=tex} `\bar `{=tex}T_z, `\qquad`{=tex}
`\overline{T_xT_z}`{=tex}. \]

Thus the M5 quotient is not merely an unlabeled abstract (V_4). It
carries repository-native numerical/geometric labels.

## Relation to Result 028

Result 028 established six valid abstract isomorphisms between the M5
quotient and the Reading Point quotient.

Result 029 does **not** yet reduce that cross-system count.

The reason is precise.

The M5 side is now internally labeled, but the Reading Point side still
has three unlabeled nonidentity classes:

\[ {7,13}, `\qquad`{=tex} {11,29}, `\qquad`{=tex} {17,23}. \]

Without an independently defined Reading Point-side structure that can
be compared with the M5 labels, all six cross-system permutations remain
admissible.

Therefore:

``` text
Result-028 admissible M5 -> Reading Point mappings:
6

Reading Point residue-pair -> M5 quotient-class assignment:
NOT ESTABLISHED
```

## Result

### Supported

``` text
Native M5 quotient labeling:
SUPPORTED

Kernel descent by basic:
SUPPORTED

Scale stability across half6 / half12 / half18:
SUPPORTED

Txbar, Tzbar, TxTzbar distinguished:
SUPPORTED

PASS
```

### Still open

``` text
Result-028 sixfold cross-system ambiguity:
REMAINS 6

Reading Point residue-pair -> M5 class assignment:
NOT ESTABLISHED

Physical Q8/{+1,-1} identification:
NOT ESTABLISHED

Reading Point -> M5 physical mapping:
NOT ESTABLISHED
```

## Next reading point

The next test should move to the Reading Point side.

Result 030 should ask:

> Does the existing Reading Point/mod-30 construction independently
> distinguish the three nonidentity residue-pair classes
>
> \[ {7,13},`\quad `{=tex}{11,29},`\quad `{=tex}{17,23} \]
>
> through a pre-existing algebraic, geometric, orientation, ordering, or
> other label that can be compared to the native M5 quotient signatures
> without selecting a permutation after seeing the result?

The target is now clear.

The M5 side has intrinsic quotient labels.

A cross-system correspondence requires an independently established
corresponding structure on the Reading Point side.

Until that is found,

\[ `\boxed{
\text{Reading Point}\rightarrow\text{M5 physical mapping:
NOT ESTABLISHED}
}`{=tex} \]
