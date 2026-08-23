#!/usr/bin/env python3
"""
Reading Point Test 033
======================

Reading Point residual-pair discriminator from canonical mod-3 / mod-5
characters.

Results 030-032 left the cross-system correspondence with one unresolved
binary choice.

Reading Point side:

    {7,13}
    {17,23}

M5 side:

    Tzbar
    TxTzbar

Result 032 fully distinguished the M5 pair using the existing C-sign
observable, but deliberately did not assign either Reading Point class to
+C or -C.

Result 033 remains entirely on the Reading Point side.

Question
--------

Does the existing arithmetic structure of (Z/30Z)^* supply an independently
defined second binary invariant that distinguishes {7,13} from {17,23}?

Candidate structure
-------------------

Use the canonical CRT factors of the unit group:

    (Z/30Z)^*
        ~= (Z/2Z)^* x (Z/3Z)^* x (Z/5Z)^*.

The mod-2 factor is trivial on units.

Two natural nontrivial binary characters are therefore:

    chi3:
        the unique nontrivial character of (Z/3Z)^*

        chi3(r) = +1  if r = 1 mod 3
                = -1  if r = 2 mod 3

    chi5:
        the quadratic character modulo 5

        chi5(r) = +1  for r = 1,4 mod 5
                = -1  for r = 2,3 mod 5.

The Result-003 quotient kernel is

    H = {1,19}.

For a character to define a Reading Point quotient label, H must lie in
its kernel. Equivalently, the character must take the same value on both
members of every H-coset.

No M5 quantity enters either character definition.

No C-sign is used.

No residue-to-M5 mapping is imposed.

Success levels
--------------

1. CHARACTER DESCENT

   chi3 and/or chi5 must be constant on every quotient coset.

2. RESIDUAL-PAIR DISCRIMINATION

   A descended character must distinguish

       {7,13}
       {17,23}.

3. FULL QUOTIENT LABELING

   The joint character signature (chi3, chi5) should uniquely identify
   all four quotient classes.

A successful result supplies intrinsic Reading Point-side binary labels.
A separate test is still required to compare those labels to the
independently defined M5 norm and C-sign labels.
"""

from __future__ import annotations

from itertools import combinations


# ===========================================================================
# Reading Point parent group
# ===========================================================================

MODULUS = 30

MOD30_UNITS = (
    1,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
)

KERNEL = frozenset(
    {
        1,
        19,
    }
)


def mul(a, b):
    return (
        a * b
    ) % MODULUS


# ===========================================================================
# Quotient construction
# ===========================================================================

def coset(rep):
    return frozenset(
        mul(
            rep,
            h,
        )
        for h in KERNEL
    )


COSETS = tuple(
    sorted(
        {
            coset(u)
            for u in MOD30_UNITS
        },
        key=lambda c: tuple(
            sorted(c)
        ),
    )
)


def coset_name(c):
    return (
        "{"
        + ",".join(
            str(x)
            for x in sorted(c)
        )
        + "}"
    )


IDENTITY_COSET = KERNEL

TARGET_A = frozenset(
    {
        7,
        13,
    }
)

DISTINGUISHED_ORDER2 = frozenset(
    {
        11,
        29,
    }
)

TARGET_B = frozenset(
    {
        17,
        23,
    }
)


# ===========================================================================
# Parent-group orders — Result 030 control
# ===========================================================================

def element_order(a):
    x = 1

    for n in range(
        1,
        32,
    ):
        x = mul(
            x,
            a,
        )

        if x == 1:
            return n

    raise RuntimeError(
        f"multiplicative order not found for {a}"
    )


def parent_order_profile(c):
    return tuple(
        sorted(
            element_order(x)
            for x in c
        )
    )


# ===========================================================================
# Canonical characters
# ===========================================================================

def chi3(r):
    """
    Unique nontrivial real character of (Z/3Z)^*.

        1 mod 3 -> +1
        2 mod 3 -> -1
    """

    x = r % 3

    if x == 1:
        return +1

    if x == 2:
        return -1

    raise ValueError(
        f"{r} is not a unit modulo 3"
    )


def chi5(r):
    """
    Quadratic character modulo 5.

        quadratic residues 1,4 -> +1
        nonresidues       2,3 -> -1
    """

    x = r % 5

    if x in (
        1,
        4,
    ):
        return +1

    if x in (
        2,
        3,
    ):
        return -1

    raise ValueError(
        f"{r} is not a unit modulo 5"
    )


CHARACTERS = {
    "chi3": chi3,
    "chi5": chi5,
}


# ===========================================================================
# Character checks
# ===========================================================================

def is_multiplicative_character(
    character,
):
    for a in MOD30_UNITS:
        for b in MOD30_UNITS:
            lhs = character(
                mul(
                    a,
                    b,
                )
            )

            rhs = (
                character(a)
                * character(b)
            )

            if lhs != rhs:
                return False

    return True


def kernel_value_profile(
    character,
):
    return tuple(
        character(x)
        for x in sorted(
            KERNEL
        )
    )


def kernel_in_character_kernel(
    character,
):
    return all(
        character(h) == +1
        for h in KERNEL
    )


def coset_character_values(
    c,
    character,
):
    return tuple(
        character(x)
        for x in sorted(c)
    )


def character_descends(
    character,
):
    """
    Equivalent tests:

      * H lies in ker(character)
      * character is constant on every H-coset.
    """

    kernel_ok = (
        kernel_in_character_kernel(
            character
        )
    )

    coset_constant = all(
        len(
            set(
                coset_character_values(
                    c,
                    character,
                )
            )
        )
        == 1
        for c in COSETS
    )

    return (
        kernel_ok
        and coset_constant
    )


def quotient_character_value(
    c,
    character,
):
    values = set(
        coset_character_values(
            c,
            character,
        )
    )

    if len(values) != 1:
        raise RuntimeError(
            f"character does not descend on {coset_name(c)}: "
            f"{sorted(values)}"
        )

    return next(
        iter(values)
    )


# ===========================================================================
# Joint signatures
# ===========================================================================

def quotient_signature(c):
    return (
        quotient_character_value(
            c,
            chi3,
        ),
        quotient_character_value(
            c,
            chi5,
        ),
    )


def signature_classes():
    out = {}

    for c in COSETS:
        sig = quotient_signature(
            c
        )

        out.setdefault(
            sig,
            [],
        ).append(
            c
        )

    return out


# ===========================================================================
# Quotient multiplication
# ===========================================================================

def quotient_mul(A, B):
    a = min(A)
    b = min(B)

    return coset(
        mul(
            a,
            b,
        )
    )


# ===========================================================================
# Character homomorphism at quotient level
# ===========================================================================

def joint_signature_mul(
    sig_a,
    sig_b,
):
    return (
        sig_a[0]
        * sig_b[0],
        sig_a[1]
        * sig_b[1],
    )


def joint_signature_is_homomorphism():
    for A in COSETS:
        for B in COSETS:
            lhs = quotient_signature(
                quotient_mul(
                    A,
                    B,
                )
            )

            rhs = joint_signature_mul(
                quotient_signature(A),
                quotient_signature(B),
            )

            if lhs != rhs:
                return False

    return True


# ===========================================================================
# Structural tests
# ===========================================================================

def test_expected_cosets():
    assert set(COSETS) == {
        frozenset({1, 19}),
        frozenset({7, 13}),
        frozenset({11, 29}),
        frozenset({17, 23}),
    }


def test_result030_order_profiles():
    assert (
        parent_order_profile(
            TARGET_A
        )
        == (4, 4)
    )

    assert (
        parent_order_profile(
            DISTINGUISHED_ORDER2
        )
        == (2, 2)
    )

    assert (
        parent_order_profile(
            TARGET_B
        )
        == (4, 4)
    )


def test_characters_are_multiplicative():
    assert is_multiplicative_character(
        chi3
    )

    assert is_multiplicative_character(
        chi5
    )


def test_characters_descend():
    assert character_descends(
        chi3
    )

    assert character_descends(
        chi5
    )


def test_chi3_distinguishes_residual_pair():
    assert (
        quotient_character_value(
            TARGET_A,
            chi3,
        )
        !=
        quotient_character_value(
            TARGET_B,
            chi3,
        )
    )


def test_joint_signature_is_injective():
    signatures = {
        quotient_signature(c)
        for c in COSETS
    }

    assert len(signatures) == 4


def test_joint_signature_preserves_multiplication():
    assert joint_signature_is_homomorphism()


def run_all():
    test_expected_cosets()
    test_result030_order_profiles()
    test_characters_are_multiplicative()
    test_characters_descend()
    test_chi3_distinguishes_residual_pair()
    test_joint_signature_is_injective()
    test_joint_signature_preserves_multiplication()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    print()
    print("Reading Point Test 033")
    print("----------------------")
    print()

    print(
        "Reading Point residual-pair discriminator "
        "from canonical mod-3 / mod-5 characters"
    )

    print()
    print("Parent group:")
    print()
    print(
        "(Z/30Z)^*"
    )

    print()
    print("Result-003 quotient:")
    print()
    print(
        "(Z/30Z)^* / {1,19}"
    )

    print()
    print("Residual Reading Point pair from Result 030:")
    print()
    print(
        "{7,13}"
    )
    print(
        "{17,23}"
    )

    print()
    print(
        "M5 labels used in discriminator construction:"
    )
    print(
        "NONE"
    )

    print()
    print(
        "M5 C-sign used in discriminator construction:"
    )
    print(
        "NO"
    )

    print()
    print("=" * 72)
    print("Character definitions")
    print("=" * 72)
    print()

    print("chi3:")
    print(
        "  r mod 3 = 1 -> +1"
    )
    print(
        "  r mod 3 = 2 -> -1"
    )

    print()
    print("chi5:")
    print(
        "  r mod 5 in {1,4} -> +1"
    )
    print(
        "  r mod 5 in {2,3} -> -1"
    )

    print()
    print(
        "Parent-group multiplicativity:"
    )
    print()

    for name, character in (
        CHARACTERS.items()
    ):
        print(
            f"{name}: "
            + (
                "SUPPORTED"
                if is_multiplicative_character(
                    character
                )
                else "NOT SUPPORTED"
            )
        )

    print()
    print("=" * 72)
    print("Kernel / quotient descent")
    print("=" * 72)
    print()

    for name, character in (
        CHARACTERS.items()
    ):
        print(
            name
        )

        print(
            "  values on H={1,19}: "
            + str(
                kernel_value_profile(
                    character
                )
            )
        )

        print(
            "  H subset ker(character): "
            + str(
                kernel_in_character_kernel(
                    character
                )
            )
        )

        print(
            "  descends to quotient: "
            + str(
                character_descends(
                    character
                )
            )
        )

        print()

    print("=" * 72)
    print("Quotient character table")
    print("=" * 72)
    print()

    print(
        f"{'coset':12s}"
        f"{'orders':12s}"
        f"{'chi3':>8s}"
        f"{'chi5':>8s}"
        f"{'joint':>14s}"
    )

    print(
        "-" * 54
    )

    for c in COSETS:
        c_name = coset_name(c)

        orders = str(
            parent_order_profile(c)
        )

        c3 = quotient_character_value(
            c,
            chi3,
        )

        c5 = quotient_character_value(
            c,
            chi5,
        )

        sig = (
            c3,
            c5,
        )

        print(
            f"{c_name:12s}"
            f"{orders:12s}"
            f"{c3:8d}"
            f"{c5:8d}"
            f"{str(sig):>14s}"
        )

    print()
    print("=" * 72)
    print("Residual-pair test")
    print("=" * 72)
    print()

    a3 = quotient_character_value(
        TARGET_A,
        chi3,
    )

    b3 = quotient_character_value(
        TARGET_B,
        chi3,
    )

    print(
        f"chi3({coset_name(TARGET_A)}) = {a3:+d}"
    )

    print(
        f"chi3({coset_name(TARGET_B)}) = {b3:+d}"
    )

    print()
    print(
        "Residual pair distinguished by chi3:"
    )
    print(
        "SUPPORTED"
        if a3 != b3
        else "NOT SUPPORTED"
    )

    print()
    print(
        "chi5 on residual pair:"
    )

    print(
        f"chi5({coset_name(TARGET_A)}) = "
        f"{quotient_character_value(TARGET_A, chi5):+d}"
    )

    print(
        f"chi5({coset_name(TARGET_B)}) = "
        f"{quotient_character_value(TARGET_B, chi5):+d}"
    )

    print()
    print(
        "Interpretation of the two characters:"
    )
    print()

    print(
        "chi5 reproduces the Result-030 singleton-plus-pair distinction."
    )

    print(
        "chi3 supplies the independent second binary distinction "
        "between the two remaining order-(4,4) classes."
    )

    print()
    print("=" * 72)
    print("Joint quotient labeling")
    print("=" * 72)
    print()

    classes = (
        signature_classes()
    )

    for sig in sorted(
        classes
    ):
        names = [
            coset_name(c)
            for c in classes[sig]
        ]

        print(
            f"{sig}: "
            + ", ".join(
                names
            )
        )

    print()
    print(
        "joint signature class count:"
    )
    print(
        len(classes)
    )

    print()
    print(
        "all four quotient classes uniquely labeled:"
    )
    print(
        "SUPPORTED"
        if len(classes) == 4
        else "NOT SUPPORTED"
    )

    print()
    print(
        "joint character map preserves quotient multiplication:"
    )
    print(
        "SUPPORTED"
        if joint_signature_is_homomorphism()
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print()

    print(
        "Reading Point quotient intrinsic labeling:"
    )
    print(
        "FULLY DISTINGUISHED"
    )

    print()
    print(
        "First binary label:"
    )
    print(
        "chi5 / mod-5 quadratic character"
    )

    print()
    print(
        "Second binary label:"
    )
    print(
        "chi3 / nontrivial mod-3 unit character"
    )

    print()
    print(
        "Residual pair:"
    )
    print(
        f"{coset_name(TARGET_A)} -> chi3={a3:+d}"
    )
    print(
        f"{coset_name(TARGET_B)} -> chi3={b3:+d}"
    )

    print()
    print(
        "Reading Point residual-pair labeling:"
    )
    print(
        "SUPPORTED"
    )

    print()
    print(
        "M5 correspondence imposed by this test:"
    )
    print(
        "NONE"
    )

    print()
    print("Interpretation:")
    print()

    print(
        "The Result-003 kernel {1,19} lies in the kernels "
        "of both canonical binary characters chi3 and chi5."
    )

    print()
    print(
        "Therefore both characters descend from the mod-30 "
        "unit group to the four-element Reading Point quotient."
    )

    print()
    print(
        "The mod-5 quadratic character supplies the same "
        "singleton-plus-pair structure observed through parent "
        "orders in Result 030."
    )

    print()
    print(
        "The independent mod-3 character distinguishes the "
        "two remaining order-(4,4) quotient classes:"
    )

    print(
        f"  {coset_name(TARGET_A)} -> {a3:+d}"
    )

    print(
        f"  {coset_name(TARGET_B)} -> {b3:+d}"
    )

    print()
    print(
        "Together (chi3, chi5) give four distinct binary "
        "signatures and preserve quotient multiplication."
    )

    print()
    print(
        "Thus the Reading Point quotient is fully intrinsically "
        "labeled by canonical arithmetic inherited from its "
        "mod-3 and mod-5 CRT factors."
    )

    print()
    print(
        "This test does not compare chi3 to M5 C-sign or "
        "chi5 to the M5 geometric norm partition."
    )

    print()
    print(
        "A separate correspondence test is required before "
        "the remaining two M5 <-> Reading Point mappings can "
        "be reduced to one."
    )

    print()
    print(
        "Unique Reading Point -> M5 correspondence:"
    )
    print(
        "NOT YET TESTED"
    )

    print()
    print(
        "Reading Point -> M5 physical mapping:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print("PASS")


if __name__ == "__main__":
    main()
