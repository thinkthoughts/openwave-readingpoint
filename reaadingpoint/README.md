# OpenWave Reading Point 

An experimental fork of OpenWave for translating specified structure into testable model constraints.

## Reading Point <img height="49" src="assets/logo/reading-point-badge-dark-512.png" />

 https://github.com/thinkthoughts/reading-point

 [readingpoint.app](https://readingpoint.app) begins with a simple arithmetic specification:

**(1 + 1) × 3 × 5 = 30**

Every prime **p > 5** resists division by **2, 3, and 5**. Equivalently,

**gcd(p, 30) = 1,**

so every such prime occupies one of eight residue classes:

**p mod 30 ∈ {1, 7, 11, 13, 17, 19, 23, 29}.**

The interactive Reading Point interface treats these eight mod-30 residues as persistent lanes through which integers can be read.

Its visual language may describe admissible numbers as resisting **gravity** toward factors of (2), (3), and (5). Gravity here is an interface metaphor; the underlying mathematical constraint is divisibility.

This gives the project a concrete example of its general method:

**object → reading rule → admissible states → measurable structure**

## OpenWave bridge

OpenWave provides an arena for comparing candidate physical models against common criteria, observables, evidence, and result states.

This fork asks whether additional mathematical or representational structure can specify useful constraints for those tests.

The working path is:

**specified structure → candidate constraint → OpenWave observable → test → support, refine, or reject**

No physical correspondence between mod-30 residues and particle states is assumed.

## First experiment

The first target is the charge-space structure exposed by Garrett Lisi's Elementary Particle Explorer.

Rather than assume a correspondence between charge-space points, prime residues, and candidate field configurations, this project treats each proposed correspondence as something to specify and test.

A candidate mapping should:

1. identify a precise relation in the Explorer or Reading Point;
2. express that relation as a measurable constraint;
3. identify or implement an OpenWave observable capable of testing it;
4. run the constraint against applicable candidate models;
5. preserve positive, partial, and negative results.

A failed correspondence is a result.

## Project structure

```text
readingpoint/
├── README.md
├── specifications/   # candidate constraints and their provenance
├── tests/            # executable translations into OpenWave tests
└── results/          # outputs produced by completed tests
```

The existing OpenWave model implementations and evaluation infrastructure remain upstream unless an experiment requires a specific extension.

## Current status

**Reading point:** specification.

The mod-30 structure is established number theory.

The Explorer charge-space structure is separately specified by the Explorer.

OpenWave supplies candidate models and an evaluation arena.

Any mapping among these structures remains a hypothesis until it produces a defined observable and passes a specified test.

## References

* OpenWave — upstream model-comparison framework
* Elementary Particle Explorer — charge-space visualization and interaction explorer
* arXiv:2108.07896 — liquid-crystal-based particle-model framework
* readingpoint.app — interactive mod-30 reading-point experiment

## Principle

**Specify → compute → measure → compare → refine or reject.**
