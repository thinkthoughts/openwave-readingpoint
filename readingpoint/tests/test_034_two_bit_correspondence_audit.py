#!/usr/bin/env python3
"""
Reading Point Test 034
======================

Two-bit M5 <-> Reading Point correspondence audit.

Results 031-033 established:

M5 quotient
-----------

    C2^3 / <Ty>

with nonidentity classes

    Txbar
    Tzbar
    TxTzbar

and independently defined native labels:

    Result 031:
        geometric norm partition

            Txbar
            |
            {Tzbar, TxTzbar}

    Result 032:
        C-sign on the residual pair

            Tzbar   -> +C
            TxTzbar -> -C

Thus the M5 quotient is fully internally distinguished.

Reading Point quotient
----------------------

    (Z/30Z)^* / {1,19}

with nonidentity classes

    {7,13}
    {11,29}
    {17,23}

and independently defined native labels:

    Result 030 / Result 033:
        chi5 partition

            {11,29}
            |
            {{7,13}, {17,23}}

    Result 033:
        chi3 on the residual pair

            {7,13}  -> +1
            {17,23} -> -1

Thus the Reading Point quotient is also fully internally distinguished.

Result 031 already licensed the partition-level correspondence

    Txbar <-> {11,29}

and reduced the abstract V4 isomorphism count

    6 -> 2.

Question
--------

Do the independently constructed second binary labels

    M5 C-sign

and

    Reading Point chi3

license a unique correspondence?

Critical constraint
-------------------

Complete intrinsic labeling on each side does NOT itself establish that
the sign meanings correspond.

There are two possible cross-system sign conventions:

    aligned:
        +C <-> chi3=+1
        -C <-> chi3=-1

    reversed:
        +C <-> chi3=-1
        -C <-> chi3=+1

Result 034 enumerates both remaining partition-preserving quotient
isomorphisms and determines which one is compatible with each sign
convention.

The test does not choose between the aligned and reversed conventions
unless an independently established cross-system orientation rule exists.

No such rule is introduced by this test.
"""

from __future__ import annotations


# ===========================================================================
# M5 quotient labels
# ===========================================================================

M5_CLASSES = (
    "Ibar",
    "Txbar",
    "Tzbar",
    "TxTzbar",
)

M5_IDENTITY = "Ibar"

# Result-031 geometric partition:
#
#   Txbar is the distinguished nonidentity singleton.
#
# Result-032 residual C-sign:
#
#   Tzbar    -> +
#   TxTzbar  -> -
#
# Ibar / Txbar C-sign values are also retained from Result 032, but the
# residual-pair comparison is the decisive second-bit structure.

M5_C_SIGN = {
    "Ibar": +1,
    "Txbar": -1,
    "Tzbar": +1,
    "TxTzbar": -1,
}

M5_NORM_CLASS = {
    "Ibar": "high",
    "Txbar": "high",
    "Tzbar": "low",
    "TxTzbar": "low",
}

# For the Result-031 nonidentity 1+2 structure:
M5_DISTINGUISHED_NONIDENTITY = "Txbar"

M5_RESIDUAL_PAIR = (
    "Tzbar",
    "TxTzbar",
)


# ===========================================================================
# Reading Point quotient labels
# ===========================================================================

RP_CLASSES = (
    "{1,19}",
    "{7,13}",
    "{11,29}",
    "{17,23}",
)

RP_IDENTITY = "{1,19}"

# Result-033 canonical character signatures.
#
# Stored as:
#
#     (chi3, chi5)

RP_SIGNATURE = {
    "{1,19}": (+1, +1),
    "{7,13}": (+1, -1),
    "{11,29}": (-1, +1),
    "{17,23}": (-1, -1),
}

RP_CHI3 = {
    name: sig[0]
    for name, sig in RP_SIGNATURE.items()
}

RP_CHI5 = {
    name: sig[1]
    for name, sig in RP_SIGNATURE.items()
}

RP_DISTINGUISHED_NONIDENTITY = "{11,29}"

RP_RESIDUAL_PAIR = (
    "{7,13}",
    "{17,23}",
)


# ===========================================================================
# Quotient multiplication
# ===========================================================================

# Use explicit C2 x C2 coordinates for each quotient.
#
# M5:
#
#   Ibar      = (0,0)
#   Txbar     = (1,0)
#   Tzbar     = (0,1)
#   TxTzbar   = (1,1)

M5_BITS = {
    "Ibar": (0, 0),
    "Txbar": (1, 0),
    "Tzbar": (0, 1),
    "TxTzbar": (1, 1),
}

BITS_TO_M5 = {
    bits: name
    for name, bits in M5_BITS.items()
}


def m5_multiply(a, b):
    aa = M5_BITS[a]
    bb = M5_BITS[b]

    return BITS_TO_M5[
        (
            aa[0] ^ bb[0],
            aa[1] ^ bb[1],
        )
    ]


# Reading Point quotient coordinates derived from Result-033 signatures.
#
# Convert signs to bits:
#
#   +1 -> 0
#   -1 -> 1
#
# using (chi5-bit, chi3-bit) only as an internal quotient coordinate.
#
# This does NOT identify chi5 physically with the M5 norm coordinate or
# chi3 physically with C-sign.

def sign_to_bit(s):
    if s == +1:
        return 0

    if s == -1:
        return 1

    raise ValueError(
        f"invalid binary sign {s}"
    )


RP_BITS = {
    name: (
        sign_to_bit(
            RP_CHI5[name]
        ),
        sign_to_bit(
            RP_CHI3[name]
        ),
    )
    for name in RP_CLASSES
}

BITS_TO_RP = {
    bits: name
    for name, bits in RP_BITS.items()
}


def rp_multiply(a, b):
    aa = RP_BITS[a]
    bb = RP_BITS[b]

    return BITS_TO_RP[
        (
            aa[0] ^ bb[0],
            aa[1] ^ bb[1],
        )
    ]


# ===========================================================================
# Result-031 partition-preserving mappings
# ===========================================================================

# Once the distinguished nonidentity singleton is fixed:
#
#   Txbar <-> {11,29}
#
# there are exactly two remaining mappings, corresponding to the swap of
# the residual pair.

MAPPING_A = {
    "Ibar": "{1,19}",
    "Txbar": "{11,29}",
    "Tzbar": "{7,13}",
    "TxTzbar": "{17,23}",
}

MAPPING_B = {
    "Ibar": "{1,19}",
    "Txbar": "{11,29}",
    "Tzbar": "{17,23}",
    "TxTzbar": "{7,13}",
}

PARTITION_PRESERVING_MAPPINGS = (
    (
        "A",
        MAPPING_A,
    ),
    (
        "B",
        MAPPING_B,
    ),
)


# ===========================================================================
# Structural checks
# ===========================================================================

def is_bijection(mapping):
    return (
        set(
            mapping.keys()
        )
        == set(
            M5_CLASSES
        )
        and
        set(
            mapping.values()
        )
        == set(
            RP_CLASSES
        )
    )


def is_homomorphism(mapping):
    for a in M5_CLASSES:
        for b in M5_CLASSES:
            lhs = mapping[
                m5_multiply(
                    a,
                    b,
                )
            ]

            rhs = rp_multiply(
                mapping[a],
                mapping[b],
            )

            if lhs != rhs:
                return False

    return True


def preserves_result031_partition(mapping):
    """
    Require the independently established singleton-level bridge:

        Txbar <-> {11,29}

    while identity maps to identity.
    """

    return (
        mapping[
            M5_IDENTITY
        ]
        == RP_IDENTITY
        and
        mapping[
            M5_DISTINGUISHED_NONIDENTITY
        ]
        == RP_DISTINGUISHED_NONIDENTITY
        and
        {
            mapping[x]
            for x in M5_RESIDUAL_PAIR
        }
        == set(
            RP_RESIDUAL_PAIR
        )
    )


# ===========================================================================
# Second-bit convention audit
# ===========================================================================

def residual_sign_relation(
    mapping,
):
    """
    Compare M5 C-sign to Reading Point chi3 only on the residual pair.

    Returns:

        +1  if chi3(mapping(x)) = C_sign(x) for both residual classes
        -1  if chi3(mapping(x)) = -C_sign(x) for both residual classes
         0  otherwise
    """

    relations = []

    for m5_class in (
        M5_RESIDUAL_PAIR
    ):
        rp_class = mapping[
            m5_class
        ]

        c_sign = M5_C_SIGN[
            m5_class
        ]

        chi3 = RP_CHI3[
            rp_class
        ]

        relations.append(
            chi3
            * c_sign
        )

    if (
        relations[0]
        == relations[1]
        == +1
    ):
        return +1

    if (
        relations[0]
        == relations[1]
        == -1
    ):
        return -1

    return 0


def sign_relation_label(value):
    if value == +1:
        return "ALIGNED"

    if value == -1:
        return "REVERSED"

    return "INCONSISTENT"


# ===========================================================================
# Full label-coordinate comparisons
# ===========================================================================

def mapping_rows(
    mapping,
):
    rows = []

    for m5_class in (
        M5_CLASSES
    ):
        rp_class = mapping[
            m5_class
        ]

        rows.append(
            {
                "m5":
                    m5_class,
                "rp":
                    rp_class,
                "m5_C":
                    M5_C_SIGN[
                        m5_class
                    ],
                "rp_chi3":
                    RP_CHI3[
                        rp_class
                    ],
                "rp_chi5":
                    RP_CHI5[
                        rp_class
                    ],
            }
        )

    return rows


# ===========================================================================
# Tests
# ===========================================================================

def test_two_partition_preserving_mappings():
    assert (
        len(
            PARTITION_PRESERVING_MAPPINGS
        )
        == 2
    )

    for _, mapping in (
        PARTITION_PRESERVING_MAPPINGS
    ):
        assert is_bijection(
            mapping
        )

        assert is_homomorphism(
            mapping
        )

        assert preserves_result031_partition(
            mapping
        )


def test_residual_sign_conventions_are_opposite():
    rel_a = residual_sign_relation(
        MAPPING_A
    )

    rel_b = residual_sign_relation(
        MAPPING_B
    )

    assert rel_a in (
        +1,
        -1,
    )

    assert rel_b in (
        +1,
        -1,
    )

    assert (
        rel_a
        == -rel_b
    )


def test_one_mapping_per_sign_convention():
    aligned = [
        name
        for name, mapping in (
            PARTITION_PRESERVING_MAPPINGS
        )
        if residual_sign_relation(
            mapping
        )
        == +1
    ]

    reversed_ = [
        name
        for name, mapping in (
            PARTITION_PRESERVING_MAPPINGS
        )
        if residual_sign_relation(
            mapping
        )
        == -1
    ]

    assert len(
        aligned
    ) == 1

    assert len(
        reversed_
    ) == 1


def run_all():
    test_two_partition_preserving_mappings()
    test_residual_sign_conventions_are_opposite()
    test_one_mapping_per_sign_convention()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    print()
    print("Reading Point Test 034")
    print("----------------------")
    print()

    print(
        "Two-bit M5 <-> Reading Point "
        "correspondence audit"
    )

    print()
    print(
        "Previously licensed partition-level bridge:"
    )
    print()

    print(
        "Txbar <-> {11,29}"
    )

    print()
    print(
        "Result-031 partition-preserving "
        "isomorphisms:"
    )
    print(
        "2"
    )

    print()
    print("=" * 72)
    print("Independent native labels")
    print("=" * 72)
    print()

    print("M5:")
    print()
    print(
        "  first label:"
    )
    print(
        "    full-frame G/R norm partition"
    )

    print(
        "  second label:"
    )
    print(
        "    N4 C-sign"
    )

    print()
    print("Reading Point:")
    print()
    print(
        "  first label:"
    )
    print(
        "    chi5 / mod-5 quadratic character"
    )

    print(
        "  second label:"
    )
    print(
        "    chi3 / nontrivial mod-3 character"
    )

    print()
    print(
        "Cross-system identification between "
        "C-sign and chi3 assumed:"
    )
    print(
        "NO"
    )

    print()
    print("=" * 72)
    print("Remaining quotient isomorphisms")
    print("=" * 72)
    print()

    for name, mapping in (
        PARTITION_PRESERVING_MAPPINGS
    ):
        print(
            f"Mapping {name}:"
        )

        for m5_class in (
            M5_CLASSES
        ):
            print(
                f"  {m5_class:10s}"
                f" -> "
                f"{mapping[m5_class]}"
            )

        print()

        print(
            "  bijection:"
        )
        print(
            f"    {is_bijection(mapping)}"
        )

        print(
            "  multiplication preserving:"
        )
        print(
            f"    {is_homomorphism(mapping)}"
        )

        print(
            "  Result-031 partition preserving:"
        )
        print(
            f"    {preserves_result031_partition(mapping)}"
        )

        relation = (
            residual_sign_relation(
                mapping
            )
        )

        print(
            "  residual C-sign / chi3 relation:"
        )
        print(
            f"    {sign_relation_label(relation)}"
        )

        print()

        print(
            "  residual pair details:"
        )

        for m5_class in (
            M5_RESIDUAL_PAIR
        ):
            rp_class = mapping[
                m5_class
            ]

            print(
                f"    {m5_class:10s}"
                f" C={M5_C_SIGN[m5_class]:+d}"
                f" -> "
                f"{rp_class:8s}"
                f" chi3="
                f"{RP_CHI3[rp_class]:+d}"
            )

        print()

    print("=" * 72)
    print("Sign-convention audit")
    print("=" * 72)
    print()

    aligned = []

    reversed_ = []

    for name, mapping in (
        PARTITION_PRESERVING_MAPPINGS
    ):
        relation = (
            residual_sign_relation(
                mapping
            )
        )

        if relation == +1:
            aligned.append(
                name
            )

        elif relation == -1:
            reversed_.append(
                name
            )

    print(
        "Mappings satisfying:"
    )
    print(
        "  C-sign = chi3"
    )
    print(
        ", ".join(
            aligned
        )
        if aligned
        else "NONE"
    )

    print()
    print(
        "Mappings satisfying:"
    )
    print(
        "  C-sign = -chi3"
    )
    print(
        ", ".join(
            reversed_
        )
        if reversed_
        else "NONE"
    )

    print()
    print(
        "Aligned convention selects one mapping:"
    )
    print(
        "SUPPORTED"
        if len(
            aligned
        )
        == 1
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Reversed convention selects one mapping:"
    )
    print(
        "SUPPORTED"
        if len(
            reversed_
        )
        == 1
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Correspondence boundary")
    print("=" * 72)
    print()

    print(
        "Independent rule establishing"
    )
    print(
        "  C-sign = chi3"
    )
    print(
        "or"
    )
    print(
        "  C-sign = -chi3"
    )
    print(
        "FOUND:"
    )
    print(
        "NO"
    )

    print()
    print(
        "Therefore:"
    )
    print()

    print(
        "Both remaining quotient isomorphisms "
        "are compatible with the independently "
        "constructed internal labels."
    )

    print()
    print(
        "They differ only by the unresolved "
        "cross-system orientation convention."
    )

    print()
    print(
        "Result-031 correspondence count:"
    )
    print(
        "2"
    )

    print()
    print(
        "Result-034 correspondence count:"
    )
    print(
        "2"
    )

    print()
    print(
        "2 -> 1 reduction:"
    )
    print(
        "NOT LICENSED"
    )

    print()
    print(
        "Unique structural correspondence:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print("Interpretation:")
    print()

    print(
        "Results 032 and 033 fully label the M5 "
        "and Reading Point quotients independently."
    )

    print()
    print(
        "However, intrinsic labels on two different "
        "systems do not automatically identify their "
        "sign conventions."
    )

    print()
    print(
        "One remaining isomorphism corresponds to "
        "treating M5 C-sign and Reading Point chi3 "
        "as aligned."
    )

    print()
    print(
        "The other corresponds to treating them as "
        "oppositely oriented."
    )

    print()
    print(
        "Both preserve the quotient multiplication "
        "and the independently established Result-031 "
        "singleton-plus-pair bridge."
    )

    print()
    print(
        "No existing cross-system rule tested here "
        "selects the aligned convention over the "
        "reversed convention."
    )

    print()
    print(
        "Therefore complete internal labeling does "
        "not yet imply a unique M5 <-> Reading Point "
        "correspondence."
    )

    print()
    print(
        "Unique Reading Point -> M5 correspondence:"
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
