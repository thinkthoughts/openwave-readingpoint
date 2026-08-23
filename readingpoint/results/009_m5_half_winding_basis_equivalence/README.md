# Result 009 — M5 half-winding basis equivalence

## Outcome

**SUPPORTED.**

The generic and symmetric half-winding tensor constructions tested in
Result 008 are related by a fixed global basis transformation.

For both:

`q = +0.5`

and:

`q = -0.5`

the maximum tensor mismatch after the basis transformation is:

`3.331 × 10^-16`

which is effectively machine precision for this test.

## Wound-plane transformation

The generic and symmetric constructions are related in the wound
`(1,3)` plane by swapping the two axes:

`e1 ↔ e3`

The corresponding 2D transformation is:

```text
[0 1]
[1 0]
