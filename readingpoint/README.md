# OpenWave ReadingPoint

An experimental OpenWave fork for turning specified mathematical structure into executable tests.

<div align="center">
  <img height="96" src="assets/logo/reading-point-badge-dark-512.png" alt="ReadingPoint logo" />
</div>

## ReadingPoint

**ReadingPoint** begins with a small arithmetic structure:

\[
(1+1)\times3\times5=30.
\]

Every prime \(p>5\) is coprime to 30, so it lies in one of eight residue classes:

\[
p \bmod 30 \in \{1,7,11,13,17,19,23,29\}.
\]

The interactive interface at **readingpoint.app** treats these eight residues as persistent lanes through which integers can be read.

Repository:

https://github.com/thinkthoughts/reading-point

The arithmetic is elementary. The research question is what happens when a similarly explicit reading rule is brought to a model with independently implemented structure.

That gives the project its basic workflow:

**structure → reading rule → candidate correspondence → executable test → result**

## Why OpenWave?

OpenWave already provides something especially useful for this experiment: candidate physical models with executable observables rather than only conceptual descriptions.

ReadingPoint therefore does not begin by assigning the eight residues to particles.

It asks a narrower question:

> If ReadingPoint and an OpenWave model contain independently constructed structures with the same mathematical organization, how much of a correspondence can actually be established by executable evidence?

The distinction matters.

An abstract isomorphism is evidence of common structure.

A physical identification requires more.

## First model: M5 liquid-crystal structure

The first sustained test sequence uses the M5 liquid-crystal implementation associated with Jarek Duda's topological-defect framework.

The experiment began without assuming that a mod-30 residue corresponds to a particle, charge, handedness, or field state.

Instead, the tests looked for independently defined structure on each side.

The ReadingPoint side starts with

\[
(\mathbb Z/30\mathbb Z)^*
=
\{1,7,11,13,17,19,23,29\}.
\]

Quotienting by the native pair

\[
\{1,19\}
\]

produces four classes:

```text
{1,19}
{7,13}
{11,29}
{17,23}
```

with the multiplication structure of

\[
C_2\times C_2.
\]

Separately, the tested M5 transformation structure produces a repository-native four-class quotient:

```text
Ibar
Txbar
Tzbar
TxTzbar
```

with the same abstract multiplication structure.

So there is a genuine common quotient:

```text
ReadingPoint quotient     C2 × C2
M5 quotient               C2 × C2
```

That observation starts the correspondence problem rather than finishing it.

## What the tests found

Two copies of \(C_2\times C_2\) have six identity-preserving isomorphisms.

The next question was therefore whether independently implemented information could reduce those six possibilities.

It could.

ReadingPoint has an intrinsic singleton-plus-pair structure:

```text
singleton:
{11,29}

remaining pair:
{7,13}
{17,23}
```

The tested M5 full-frame observables independently produce:

```text
singleton:
Txbar

remaining pair:
Tzbar
TxTzbar
```

That licenses the partition-level bridge

```text
Txbar <-> {11,29}
```

and reduces the correspondence count:

```text
6 -> 2
```

This reduction is executable and does not require choosing a particle interpretation.

## The remaining two mappings

The two surviving quotient isomorphisms are:

```text
Mapping A

Ibar     -> {1,19}
Txbar    -> {11,29}
Tzbar    -> {7,13}
TxTzbar  -> {17,23}
```

and:

```text
Mapping B

Ibar     -> {1,19}
Txbar    -> {11,29}
Tzbar    -> {17,23}
TxTzbar  -> {7,13}
```

ReadingPoint can distinguish its final pair intrinsically using the nontrivial mod-3 character:

```text
chi3({7,13})   = +1
chi3({17,23})  = -1
```

M5 can also distinguish its final pair intrinsically using the sign of the existing N4 chiral-overlap observable \(C\):

```text
C-sign(Tzbar)    = +1
C-sign(TxTzbar)  = -1
```

So both systems are internally fully labeled.

There is still one important ambiguity.

Nothing tested so far independently says that

```text
C-sign = chi3
```

rather than

```text
C-sign = -chi3.
```

Those choices select Mapping A and Mapping B respectively.

## Why we stopped at two

Tests 035–038 deliberately looked for an M5-native orientation rule that could resolve the final sign convention.

They tested several existing structures rather than inventing a rule for the desired mapping:

```text
035  right-handed full-frame convention
036  self-linking orientation N -> -N
037  chi and g_chiral sign reversals
038  Mermin-Ho / topological-flux sign
```

The useful result is that none licenses the final cross-system identification.

For example, Test 037 finds that changing `g_chiral` reverses the weighted term

\[
g_{\rm chiral}C
\]

while leaving the geometric overlap \(C\) itself unchanged.

That distinguishes a coupling-sign convention from the geometric \(C\)-sign used in the quotient audit.

Test 039 collects the evidence and marks the current boundary:

```text
shared V4 quotient:
SUPPORTED

independent partition bridge:
SUPPORTED

6 -> 2 reduction:
SUPPORTED

2 -> 1 reduction:
NOT LICENSED

unique ReadingPoint -> M5 correspondence:
NOT ESTABLISHED

ReadingPoint -> M5 physical mapping:
NOT ESTABLISHED
```

That is the current result.

## Why the negative boundary matters

The purpose of the fork is not to make every proposed correspondence work.

It is to find the point where independently implemented structure stops supporting the next inference.

Here the result is unusually clean:

\[
6 \longrightarrow 2
\]

is supported by executable structure.

\[
2 \longrightarrow 1
\]

currently requires an additional cross-system orientation rule.

Rather than choose that rule by convention, ReadingPoint keeps both mappings visible.

A future derivation, observable, or physical argument can therefore resolve the ambiguity without rewriting the earlier evidence.

## Reproducing the work

The ReadingPoint-specific work is organized as:

```text
readingpoint/
├── README.md
├── specifications/
├── tests/
└── results/
```

`tests/` contains the executable audits.

`results/` contains their recorded outputs and result summaries.

The tests are cumulative: later correspondence claims are licensed only by distinctions established in earlier tests.

For the current correspondence boundary, the most useful reading sequence is:

```text
027  repository-native M5 quotient
028  abstract quotient isomorphisms

030  ReadingPoint native 1+2 partition
031  M5 native 1+2 partition

032  M5 residual C-sign
033  ReadingPoint residual chi3

034  two-bit correspondence audit

035  full-frame orientation audit
036  self-linking orientation audit
037  chiral-coupling orientation audit
038  Mermin-Ho / topological-flux audit

039  evidence-ledger synthesis
```

If you only want the current conclusion, start with **Test 039** and work backward into whichever evidence step you want to inspect.

## What would change the result?

The next useful result is not another arbitrary labeling of the four quotient classes.

The missing object is specific:

> an independently motivated cross-system rule that gives the M5 orientation sign and ReadingPoint `chi3` sign the same operational meaning.

Such a result could establish either

\[
C\text{-sign}=\chi_3
\]

or

\[
C\text{-sign}=-\chi_3.
\]

Either outcome is acceptable.

Until one is established, both mappings remain admissible.

## Relation to particle physics

The current result is structural.

It does **not** establish that:

- a residue class is a particle;
- a ReadingPoint lane is an electric charge;
- `chi3` is physical handedness;
- the M5 quotient has a unique ReadingPoint assignment;
- or ReadingPoint supplies a physical mapping of the M5 model.

Those would be later claims requiring their own observables and tests.

The current result is simpler:

> Two independently constructed systems contain compatible four-state quotient structure, and independently measured structure reduces their six abstract identifications to two.

That is where the executable evidence currently ends.

## References

- **OpenWave** — upstream simulation and model-comparison framework
- **Jarek Duda, arXiv:2108.07896** — liquid-crystal / topological-defect framework used by the M5 implementation
- **ReadingPoint** — mod-30 arithmetic specification and interactive reading interface
- **Elementary Particle Explorer** — an additional structural reference for charge-space exploration

## Working principle

**Specify → compute → measure → compare → keep the boundary visible.**
