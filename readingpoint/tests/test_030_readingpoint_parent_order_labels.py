#!/usr/bin/env python3
"""
Reading Point Test 030
======================

Reading Point parent-group order labels on the common V4 quotient.

Result 028 established six abstract isomorphisms between

    C2^3 / <Ty>

and

    (Z/30Z)^* / {1,19}

because the three nonidentity V4 elements can be permuted arbitrarily.

Result 029 supplied intrinsic M5-side labels through the repository-native
basic Mermin-Ho instrument.

Test 030 asks whether the Reading Point quotient itself already carries
intrinsic labels inherited from the parent group (Z/30Z)^*.

The candidate invariant is parent-element multiplicative order modulo 30.

This invariant predates the M5 correspondence and was already computed in
the early Reading Point mod-30 group tests.

No M5 labels are used to construct the invariant.
No residue-to-M5 assignment is imposed.
"""

from __future__ import annotations


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
    ) % 30


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
        f"order not found for {a}"
    )


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
        key=lambda c:
            tuple(
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


def parent_order_profile(c):
    return tuple(
        sorted(
            element_order(x)
            for x in c
        )
    )


def test_unit_orders():
    expected = {
        1: 1,
        7: 4,
        11: 2,
        13: 4,
        17: 4,
        19: 2,
        23: 4,
        29: 2,
    }

    measured = {
        u:
            element_order(u)
        for u in MOD30_UNITS
    }

    assert measured == expected


def test_quotient_cosets():
    expected = {
        frozenset({1, 19}),
        frozenset({7, 13}),
        frozenset({11, 29}),
        frozenset({17, 23}),
    }

    assert set(COSETS) == expected


def test_nonidentity_parent_profiles():
    identity = KERNEL

    nonidentity = [
        c
        for c in COSETS
        if c != identity
    ]

    profiles = {
        coset_name(c):
            parent_order_profile(c)
        for c in nonidentity
    }

    assert profiles[
        "{7,13}"
    ] == (
        4,
        4,
    )

    assert profiles[
        "{11,29}"
    ] == (
        2,
        2,
    )

    assert profiles[
        "{17,23}"
    ] == (
        4,
        4,
    )


def main():
    test_unit_orders()
    test_quotient_cosets()
    test_nonidentity_parent_profiles()

    print()
    print("Reading Point Test 030")
    print("----------------------")
    print()

    print(
        "Reading Point parent-order "
        "labels on the common V4 quotient"
    )

    print()
    print("Parent group:")
    print(
        "(Z/30Z)^*"
    )

    print()
    print("Parent-element orders:")
    print()

    for u in MOD30_UNITS:
        print(
            f"{u:2d} -> order "
            f"{element_order(u)}"
        )

    print()
    print("Quotient:")
    print(
        "(Z/30Z)^* / {1,19}"
    )

    print()
    print(
        "Nonidentity quotient classes "
        "with inherited parent-order profiles:"
    )
    print()

    nonidentity = [
        c
        for c in COSETS
        if c != KERNEL
    ]

    profiles = {}

    for c in nonidentity:
        name = coset_name(c)

        profile = (
            parent_order_profile(
                c
            )
        )

        profiles[
            name
        ] = profile

        print(
            f"{name:10s} -> "
            f"{profile}"
        )

    profile_classes = {}

    for name, profile in (
        profiles.items()
    ):
        profile_classes.setdefault(
            profile,
            [],
        ).append(
            name
        )

    print()
    print(
        "Distinct inherited "
        "nonidentity label classes:"
    )
    print(
        len(
            profile_classes
        )
    )

    print()

    for profile, names in sorted(
        profile_classes.items()
    ):
        print(
            f"profile {profile}: "
            + ", ".join(
                names
            )
        )

    unique_profiles = [
        (
            profile,
            names,
        )
        for profile, names in (
            profile_classes.items()
        )
        if len(
            names
        ) == 1
    ]

    print()
    print(
        "Uniquely labeled nonidentity "
        "Reading Point classes:"
    )

    if unique_profiles:
        for profile, names in (
            unique_profiles
        ):
            print(
                f"{names[0]} "
                f"via profile {profile}"
            )
    else:
        print(
            "NONE"
        )

    print()
    print(
        "Residual Reading Point "
        "nonidentity ambiguity:"
    )

    ambiguous = [
        names
        for names in (
            profile_classes.values()
        )
        if len(
            names
        ) > 1
    ]

    if ambiguous:
        for names in ambiguous:
            print(
                " <-> ".join(
                    names
                )
            )
    else:
        print(
            "NONE"
        )

    # With one nonidentity V4 element distinguished,
    # only the transposition of the remaining two survives.
    residual_isomorphism_count = 2

    print()
    print(
        "Reading Point intrinsic quotient labeling:"
    )
    print(
        "PARTIAL"
    )

    print()
    print(
        "Result-028 abstract correspondence count:"
    )
    print(
        "6"
    )

    print()
    print(
        "Residual correspondence count after "
        "Reading Point parent-order label:"
    )
    print(
        residual_isomorphism_count
    )

    print()
    print(
        "Residual permutation freedom:"
    )
    print(
        "C2 / swap of the two (4,4) classes"
    )

    print()
    print("Interpretation:")
    print()

    print(
        "The Reading Point quotient is not completely "
        "unlabeled when viewed together with its parent group."
    )

    print()
    print(
        "The class {11,29} is intrinsically distinguished "
        "because both of its representatives have order 2 "
        "in (Z/30Z)^*."
    )

    print()
    print(
        "The classes {7,13} and {17,23} both inherit the "
        "same parent-order profile (4,4), so parent-element "
        "order does not distinguish those two classes."
    )

    print()
    print(
        "Thus the Reading Point side reduces the three-way "
        "S3 labeling freedom to a two-way exchange."
    )

    print()
    print(
        "However, this test does not identify which M5 "
        "quotient class corresponds to the uniquely labeled "
        "Reading Point class {11,29}."
    )

    print()
    print(
        "An independent M5 invariant with a corresponding "
        "binary structural meaning is still required before "
        "the cross-system isomorphism count can legitimately "
        "be reduced."
    )

    print()
    print(
        "Reading Point residue-pair -> "
        "M5 quotient-class assignment:"
    )
    print(
        "NOT ESTABLISHED"
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
