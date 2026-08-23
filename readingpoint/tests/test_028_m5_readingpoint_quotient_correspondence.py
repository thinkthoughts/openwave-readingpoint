#!/usr/bin/env python3
"""
Reading Point Test 028
======================

M5 quotient -> Reading Point quotient correspondence audit.

Result 027 established a repository-native four-class quotient selected by
the existing M5 `basic` full-F instrument:

    C2^3 / <Ty>

with cosets

    [I]      = {I, Ty}
    [Tx]     = {Tx, TxTy}
    [Tz]     = {Tz, TyTz}
    [TxTz]   = {TxTz, TxTyTz}

and abstract structure

    C2^3 / <Ty> ~= C2^2 ~= V4.

Reading Point Result 003 independently established

    (Z/30Z)^* / {1,19} ~= C2 x C2

and also noted the abstract compatibility

    (Z/30Z)^* / {1,19}
        ~= Q8 / {1,-1}
        ~= C2 x C2,

without assigning any particular Reading Point residue pair to a particular
quaternion coset or M5 state.

Result 028 asks:

    Does the abstract quotient structure uniquely determine a correspondence
    between the three nonidentity M5 quotient classes and the three
    nonidentity Reading Point quotient classes?

The test constructs the Reading Point quotient directly from multiplication
mod 30, constructs the M5 quotient from the Result-027 kernel <Ty>, enumerates
all identity-preserving bijections, and checks multiplication preservation.

No residue-to-M5 assignment is imposed.
No quaternion labeling is imposed.
No preferred generator correspondence is assumed.

Expected mathematical boundary:

    if both quotients are V4 and no independent labeling constraint is added,
    all 3! = 6 permutations of the three nonidentity elements remain valid
    group isomorphisms.

That ambiguity is itself the result to measure.
"""

from __future__ import annotations

from itertools import permutations


# ===========================================================================
# Generic finite-group helpers
# ===========================================================================

def assert_group_table(elements, identity, multiply):
    """
    Lightweight structural checks sufficient for this finite audit.
    """

    elems = list(elements)
    elem_set = set(elems)

    assert identity in elem_set

    # closure
    for a in elems:
        for b in elems:
            c = multiply(a, b)
            assert c in elem_set, (
                f"group not closed: {a} * {b} = {c}"
            )

    # identity
    for a in elems:
        assert multiply(identity, a) == a
        assert multiply(a, identity) == a

    # associativity
    for a in elems:
        for b in elems:
            for c in elems:
                assert (
                    multiply(
                        multiply(a, b),
                        c,
                    )
                    ==
                    multiply(
                        a,
                        multiply(b, c),
                    )
                )

    # inverse existence
    for a in elems:
        assert any(
            multiply(a, b) == identity
            and multiply(b, a) == identity
            for b in elems
        )


def multiplication_table(elements, multiply):
    return {
        (a, b): multiply(a, b)
        for a in elements
        for b in elements
    }


def is_abelian(elements, multiply):
    return all(
        multiply(a, b) == multiply(b, a)
        for a in elements
        for b in elements
    )


def nonidentity_orders(elements, identity, multiply):
    out = {}

    for a in elements:
        if a == identity:
            continue

        x = identity

        for n in range(1, 17):
            x = multiply(x, a)

            if x == identity:
                out[a] = n
                break

        if a not in out:
            out[a] = None

    return out


def is_v4(elements, identity, multiply):
    """
    Characterize V4 as:
      - order 4
      - abelian
      - every nonidentity element has order 2.
    """

    if len(elements) != 4:
        return False

    if not is_abelian(
        elements,
        multiply,
    ):
        return False

    orders = nonidentity_orders(
        elements,
        identity,
        multiply,
    )

    return all(
        order == 2
        for order in orders.values()
    )


# ===========================================================================
# M5 quotient from Result 027
# ===========================================================================

# Result 023 generator-bit representation:
#
#   Tx = (1,0,0)
#   Ty = (0,1,0)
#   Tz = (0,0,1)
#
# Result 027 quotients by <Ty>, so only the Tx and Tz bits survive.

M5_ELEMENTS = (
    "Ibar",
    "Txbar",
    "Tzbar",
    "TxTzbar",
)

M5_IDENTITY = "Ibar"

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

    cc = (
        aa[0] ^ bb[0],
        aa[1] ^ bb[1],
    )

    return BITS_TO_M5[cc]


M5_COSETS = {
    "Ibar": ("I", "Ty"),
    "Txbar": ("Tx", "TxTy"),
    "Tzbar": ("Tz", "TyTz"),
    "TxTzbar": ("TxTz", "TxTyTz"),
}


# ===========================================================================
# Reading Point quotient: (Z/30Z)^* / {1,19}
# ===========================================================================

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

RP_KERNEL = frozenset(
    {
        1,
        19,
    }
)


def mod30_mul(a, b):
    return (
        a * b
    ) % 30


def make_coset(rep):
    return frozenset(
        mod30_mul(
            rep,
            h,
        )
        for h in RP_KERNEL
    )


RP_COSET_SET = {
    make_coset(
        u
    )
    for u in MOD30_UNITS
}

RP_ELEMENTS = tuple(
    sorted(
        RP_COSET_SET,
        key=lambda c: tuple(
            sorted(c)
        ),
    )
)

RP_IDENTITY = RP_KERNEL


def canonical_rp_name(coset):
    vals = sorted(
        coset
    )

    return (
        "{"
        + ",".join(
            str(x)
            for x in vals
        )
        + "}"
    )


RP_NAMES = {
    coset: canonical_rp_name(
        coset
    )
    for coset in RP_ELEMENTS
}


def rp_multiply(A, B):
    """
    Multiply quotient cosets using representative multiplication mod 30.
    """

    a = min(A)
    b = min(B)

    return make_coset(
        mod30_mul(
            a,
            b,
        )
    )


# ===========================================================================
# Optional abstract Q8/{+1,-1} comparison
# ===========================================================================

Q8Q_ELEMENTS = (
    "1bar",
    "ibar",
    "jbar",
    "kbar",
)

Q8Q_IDENTITY = "1bar"

# Once the center {+1,-1} is quotiented out, signs disappear and the quotient
# multiplication is V4.
Q8Q_BITS = {
    "1bar": (0, 0),
    "ibar": (1, 0),
    "jbar": (0, 1),
    "kbar": (1, 1),
}

BITS_TO_Q8Q = {
    bits: name
    for name, bits in Q8Q_BITS.items()
}


def q8q_multiply(a, b):
    aa = Q8Q_BITS[a]
    bb = Q8Q_BITS[b]

    cc = (
        aa[0] ^ bb[0],
        aa[1] ^ bb[1],
    )

    return BITS_TO_Q8Q[cc]


# ===========================================================================
# Isomorphism enumeration
# ===========================================================================

def identity_preserving_bijections(
    source_elements,
    source_identity,
    target_elements,
    target_identity,
):
    """
    Enumerate all bijections fixing identity.

    For two 4-element sets this gives 3! = 6 candidates.
    """

    src_nonid = [
        x
        for x in source_elements
        if x != source_identity
    ]

    tgt_nonid = [
        x
        for x in target_elements
        if x != target_identity
    ]

    for perm in permutations(
        tgt_nonid
    ):
        mapping = {
            source_identity:
                target_identity
        }

        mapping.update(
            {
                s: t
                for s, t
                in zip(
                    src_nonid,
                    perm,
                )
            }
        )

        yield mapping


def is_homomorphism(
    mapping,
    source_elements,
    source_multiply,
    target_multiply,
):
    for a in source_elements:
        for b in source_elements:
            lhs = mapping[
                source_multiply(
                    a,
                    b,
                )
            ]

            rhs = target_multiply(
                mapping[a],
                mapping[b],
            )

            if lhs != rhs:
                return False

    return True


def enumerate_isomorphisms(
    source_elements,
    source_identity,
    source_multiply,
    target_elements,
    target_identity,
    target_multiply,
):
    candidates = list(
        identity_preserving_bijections(
            source_elements,
            source_identity,
            target_elements,
            target_identity,
        )
    )

    isos = [
        mapping
        for mapping in candidates
        if is_homomorphism(
            mapping,
            source_elements,
            source_multiply,
            target_multiply,
        )
    ]

    return (
        candidates,
        isos,
    )


# ===========================================================================
# Formatting
# ===========================================================================

def print_table(
    title,
    elements,
    multiply,
    display,
):
    print(title)

    width = max(
        8,
        max(
            len(
                display(x)
            )
            for x in elements
        )
        + 2,
    )

    header = (
        " " * width
        + "".join(
            f"{display(x):>{width}s}"
            for x in elements
        )
    )

    print(header)

    for a in elements:
        row = (
            f"{display(a):>{width}s}"
        )

        for b in elements:
            row += (
                f"{display(multiply(a, b)):>{width}s}"
            )

        print(row)


def format_mapping(
    mapping,
    source_elements,
    source_display,
    target_display,
):
    return ", ".join(
        f"{source_display(s)} -> "
        f"{target_display(mapping[s])}"
        for s in source_elements
    )


# ===========================================================================
# Structural tests
# ===========================================================================

def test_m5_quotient_is_v4():
    assert_group_table(
        M5_ELEMENTS,
        M5_IDENTITY,
        m5_multiply,
    )

    assert is_v4(
        M5_ELEMENTS,
        M5_IDENTITY,
        m5_multiply,
    )


def test_readingpoint_quotient_is_v4():
    assert len(
        RP_ELEMENTS
    ) == 4

    assert_group_table(
        RP_ELEMENTS,
        RP_IDENTITY,
        rp_multiply,
    )

    assert is_v4(
        RP_ELEMENTS,
        RP_IDENTITY,
        rp_multiply,
    )


def test_q8_center_quotient_is_v4():
    assert_group_table(
        Q8Q_ELEMENTS,
        Q8Q_IDENTITY,
        q8q_multiply,
    )

    assert is_v4(
        Q8Q_ELEMENTS,
        Q8Q_IDENTITY,
        q8q_multiply,
    )


def test_all_six_m5_to_rp_identity_bijections_are_isomorphisms():
    candidates, isos = (
        enumerate_isomorphisms(
            M5_ELEMENTS,
            M5_IDENTITY,
            m5_multiply,
            RP_ELEMENTS,
            RP_IDENTITY,
            rp_multiply,
        )
    )

    assert len(
        candidates
    ) == 6

    assert len(
        isos
    ) == 6


def run_all():
    test_m5_quotient_is_v4()
    test_readingpoint_quotient_is_v4()
    test_q8_center_quotient_is_v4()
    test_all_six_m5_to_rp_identity_bijections_are_isomorphisms()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    (
        m5_rp_candidates,
        m5_rp_isos,
    ) = enumerate_isomorphisms(
        M5_ELEMENTS,
        M5_IDENTITY,
        m5_multiply,
        RP_ELEMENTS,
        RP_IDENTITY,
        rp_multiply,
    )

    (
        m5_q8_candidates,
        m5_q8_isos,
    ) = enumerate_isomorphisms(
        M5_ELEMENTS,
        M5_IDENTITY,
        m5_multiply,
        Q8Q_ELEMENTS,
        Q8Q_IDENTITY,
        q8q_multiply,
    )

    print()
    print("Reading Point Test 028")
    print("----------------------")
    print()

    print(
        "M5 quotient -> Reading Point "
        "quotient correspondence audit"
    )

    print()
    print("M5 quotient:")
    print()
    print(
        "C2^3 / <Ty>"
    )
    print(
        f"order = {len(M5_ELEMENTS)}"
    )

    print()
    print("M5 quotient classes:")
    print()

    for name in M5_ELEMENTS:
        print(
            f"{name:9s} = "
            + "{"
            + ", ".join(
                M5_COSETS[name]
            )
            + "}"
        )

    print()
    print(
        "M5 quotient classification:"
    )
    print(
        "V4"
        if is_v4(
            M5_ELEMENTS,
            M5_IDENTITY,
            m5_multiply,
        )
        else "NOT V4"
    )

    print()
    print("Reading Point quotient:")
    print()
    print(
        "(Z/30Z)^* / {1,19}"
    )
    print(
        f"order = {len(RP_ELEMENTS)}"
    )

    print()
    print(
        "Reading Point residue-pair classes:"
    )
    print()

    for coset in RP_ELEMENTS:
        print(
            RP_NAMES[coset]
        )

    print()
    print(
        "Reading Point quotient classification:"
    )
    print(
        "V4"
        if is_v4(
            RP_ELEMENTS,
            RP_IDENTITY,
            rp_multiply,
        )
        else "NOT V4"
    )

    print()
    print_table(
        "M5 quotient multiplication table:",
        M5_ELEMENTS,
        m5_multiply,
        lambda x: x,
    )

    print()
    print_table(
        "Reading Point quotient multiplication table:",
        RP_ELEMENTS,
        rp_multiply,
        lambda x: RP_NAMES[x],
    )

    print()
    print(
        "Abstract quotient isomorphism:"
    )
    print(
        "SUPPORTED"
        if (
            is_v4(
                M5_ELEMENTS,
                M5_IDENTITY,
                m5_multiply,
            )
            and is_v4(
                RP_ELEMENTS,
                RP_IDENTITY,
                rp_multiply,
            )
        )
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Identity-preserving bijections tested:"
    )
    print(
        len(
            m5_rp_candidates
        )
    )

    print()
    print(
        "Multiplication-preserving "
        "M5 -> Reading Point isomorphisms:"
    )
    print(
        len(
            m5_rp_isos
        )
    )

    print()
    print(
        "All admissible M5 -> Reading Point "
        "generator correspondences:"
    )
    print()

    for idx, mapping in enumerate(
        m5_rp_isos,
        start=1,
    ):
        print(
            f"{idx}. "
            + format_mapping(
                mapping,
                M5_ELEMENTS,
                lambda x: x,
                lambda x: RP_NAMES[x],
            )
        )

    print()
    print(
        "Residual correspondence ambiguity:"
    )
    print()

    if len(
        m5_rp_isos
    ) == 1:
        print(
            "UNIQUE"
        )

    else:
        print(
            f"{len(m5_rp_isos)} "
            "equally valid group isomorphisms"
        )
        print(
            "three nonidentity classes retain "
            "S3 permutation freedom"
        )

    print()
    print(
        "Unique generator correspondence:"
    )

    if len(
        m5_rp_isos
    ) == 1:
        print(
            "SUPPORTED"
        )
    else:
        print(
            "NOT SUPPORTED"
        )

    print()
    print(
        "Q8/{+1,-1} abstract quotient comparison:"
    )
    print()

    print(
        f"identity-preserving bijections tested = "
        f"{len(m5_q8_candidates)}"
    )

    print(
        f"multiplication-preserving isomorphisms = "
        f"{len(m5_q8_isos)}"
    )

    print(
        "abstract compatibility = "
        + (
            "SUPPORTED"
            if len(
                m5_q8_isos
            ) > 0
            else "NOT SUPPORTED"
        )
    )

    print()
    print("Interpretation:")
    print()

    print(
        "Result 027 supplied a repository-native M5 quotient "
        "C2^3/<Ty> with four composition-compatible classes."
    )

    print()
    print(
        "Reading Point Result 003 independently supplied "
        "(Z/30Z)^*/{1,19}, also with V4 multiplication structure."
    )

    print()
    print(
        "The abstract group structures therefore agree."
    )

    print()
    print(
        "However, group structure alone does not distinguish the "
        "three nonidentity elements of V4."
    )

    print()
    print(
        "All six permutations of the three nonidentity M5 quotient "
        "classes produce valid multiplication-preserving mappings to "
        "the three nonidentity Reading Point residue-pair classes."
    )

    print()
    print(
        "Therefore no particular residue-pair -> M5 quotient-class "
        "assignment is licensed by the abstract quotient algebra alone."
    )

    print()
    print(
        "The same sixfold ambiguity applies to an abstract "
        "Q8/{+1,-1} quotient comparison unless an additional "
        "independently defined physical or geometric constraint is supplied."
    )

    print()
    print(
        "Q8/{+1,-1} abstract quotient compatibility:"
    )
    print(
        "SUPPORTED"
    )

    print()
    print(
        "Physical Q8/{+1,-1} identification:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print(
        "Reading Point residue-pair -> M5 class assignment:"
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
