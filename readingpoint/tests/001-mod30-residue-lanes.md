# Test 001 — Mod-30 residue lanes vs M5 topological charge

Status: specified

## Reading Point specification

For every prime p > 5,

p mod 30 ∈ {1, 7, 11, 13, 17, 19, 23, 29}.

This defines eight admissible residue classes modulo 30.

## OpenWave target

Model: M5 — Liquid Crystal

Criterion:
Charge quantization

Observable:
Integer topological winding / charge Q ∈ ℤ

Existing evidence:
openwave/xperiments/m5_liquid_crystal/.../m5_1_winding.py

OpenWave currently records the M5 hedgehog charge as Q = ±1.

## Question

Does the existing M5 topological-charge structure naturally induce an
eight-class partition that can be compared with the eight mod-30 residue
classes?

## Constraint

No mapping from residue class to field configuration or topological charge
is assumed.

Any proposed mapping must be derived from an independently specified M5
observable or symmetry.

## First test

Enumerate the topological-charge/state classes already produced by the
existing M5 charge instrumentation.

Record:

- distinct Q values;
- any additional discrete topological labels;
- symmetry equivalences;
- whether exactly eight naturally distinguished classes occur.

## Outcomes

SUPPORTED:
An independently defined M5 classification yields eight distinguished
classes and a non-arbitrary correspondence can be specified.

PARTIAL:
M5 supplies discrete structure relevant to the comparison, but not a
natural eight-class partition.

REJECTED:
The eight-way partition can only be obtained by imposing labels or grouping
states after the fact.

## Current expectation

Open.
## Baseline reproduction

Before testing the Reading Point specification, reproduce the existing
OpenWave M5 charge-quantization result.

Upstream observable:
topological winding / charge Q ∈ ℤ

Upstream evidence:
m5_1_winding.py

Expected upstream result:
Q = ±1 for the corresponding hedgehog orientation.

Reading Point modifications:
none

Purpose:
Establish that the fork reproduces the upstream observable before any
candidate mod-30 correspondence is introduced.

The existing validated Q = ±1 result by itself does not provide eight classes.
