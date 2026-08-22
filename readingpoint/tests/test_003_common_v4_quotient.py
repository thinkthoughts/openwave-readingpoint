# readingpoint/tests/test_003_common_v4_quotient.py

from itertools import product


MODULUS = 30
MOD30_UNITS = (1, 7, 11, 13, 17, 19, 23, 29)
MOD30_SUBGROUP = frozenset({1, 19})

Q8_ELEMENTS = (
    (1, "1"),
    (-1, "1"),
    (1, "i"),
    (-1, "i"),
    (1, "j"),
    (-1, "j"),
    (1, "k"),
    (-1, "k"),
)
Q8_CENTER = frozenset({(1, "1"), (-1, "1")})


def mod30_mul(a: int, b: int) -> int:
    return (a * b) % MODULUS


def q8_mul(a, b):
    sign_a, basis_a = a
    sign_b, basis_b = b
    sign = sign_a * sign_b

    table = {
        ("1", "1"): (1, "1"),
        ("1", "i"): (1, "i"),
        ("1", "j"): (1, "j"),
        ("1", "k"): (1, "k"),
        ("i", "1"): (1, "i"),
        ("j", "1"): (1, "j"),
        ("k", "1"): (1, "k"),
        ("i", "i"): (-1, "1"),
        ("j", "j"): (-1, "1"),
        ("k", "k"): (-1, "1"),
        ("i", "j"): (1, "k"),
        ("j", "k"): (1, "i"),
        ("k", "i"): (1, "j"),
        ("j", "i"): (-1, "k"),
        ("k", "j"): (-1, "i"),
        ("i", "k"): (-1, "j"),
    }

    table_sign, basis = table[(basis_a, basis_b)]
    return sign * table_sign, basis


def left_coset(element, subgroup, multiply):
    return frozenset(multiply(element, h) for h in subgroup)


def quotient_cosets(elements, subgroup, multiply):
    cosets = set()

    for element in elements:
        cosets.add(left_coset(element, subgroup, multiply))

    return tuple(cosets)


def quotient_mul(coset_a, coset_b, subgroup, multiply):
    a = next(iter(coset_a))
    b = next(iter(coset_b))
    return left_coset(multiply(a, b), subgroup, multiply)


def element_order(element, identity, multiply, max_steps=16):
    value = identity

    for n in range(1, max_steps + 1):
        value = multiply(value, element)
        if value == identity:
            return n

    raise RuntimeError(f"Could not determine order of {element!r}")


def q8_label(element):
    sign, basis = element

    if basis == "1":
        return "1" if sign == 1 else "-1"

    return basis if sign == 1 else f"-{basis}"


def test_mod30_subgroup():
    assert MOD30_SUBGROUP == frozenset({1, 19})
    assert mod30_mul(19, 19) == 1

    for a, b in product(MOD30_SUBGROUP, repeat=2):
        assert mod30_mul(a, b) in MOD30_SUBGROUP


def test_q8_center():
    assert len(Q8_CENTER) == 2

    for z in Q8_CENTER:
        for g in Q8_ELEMENTS:
            assert q8_mul(z, g) == q8_mul(g, z)


def test_mod30_quotient_has_four_cosets():
    cosets = quotient_cosets(
        MOD30_UNITS,
        MOD30_SUBGROUP,
        mod30_mul,
    )

    assert len(cosets) == 4
    assert all(len(coset) == 2 for coset in cosets)


def test_q8_quotient_has_four_cosets():
    cosets = quotient_cosets(
        Q8_ELEMENTS,
        Q8_CENTER,
        q8_mul,
    )

    assert len(cosets) == 4
    assert all(len(coset) == 2 for coset in cosets)


def test_mod30_quotient_is_v4():
    cosets = quotient_cosets(
        MOD30_UNITS,
        MOD30_SUBGROUP,
        mod30_mul,
    )

    identity = left_coset(1, MOD30_SUBGROUP, mod30_mul)

    for coset in cosets:
        squared = quotient_mul(
            coset,
            coset,
            MOD30_SUBGROUP,
            mod30_mul,
        )
        assert squared == identity


def test_q8_quotient_is_v4():
    cosets = quotient_cosets(
        Q8_ELEMENTS,
        Q8_CENTER,
        q8_mul,
    )

    identity = left_coset(
        (1, "1"),
        Q8_CENTER,
        q8_mul,
    )

    for coset in cosets:
        squared = quotient_mul(
            coset,
            coset,
            Q8_CENTER,
            q8_mul,
        )
        assert squared == identity


def test_common_quotient_structure():
    mod30_cosets = quotient_cosets(
        MOD30_UNITS,
        MOD30_SUBGROUP,
        mod30_mul,
    )

    q8_cosets = quotient_cosets(
        Q8_ELEMENTS,
        Q8_CENTER,
        q8_mul,
    )

    assert len(mod30_cosets) == len(q8_cosets) == 4

    mod30_identity = left_coset(
        1,
        MOD30_SUBGROUP,
        mod30_mul,
    )

    q8_identity = left_coset(
        (1, "1"),
        Q8_CENTER,
        q8_mul,
    )

    mod30_orders = sorted(
        element_order(
            coset,
            mod30_identity,
            lambda a, b: quotient_mul(
                a,
                b,
                MOD30_SUBGROUP,
                mod30_mul,
            ),
        )
        for coset in mod30_cosets
    )

    q8_orders = sorted(
        element_order(
            coset,
            q8_identity,
            lambda a, b: quotient_mul(
                a,
                b,
                Q8_CENTER,
                q8_mul,
            ),
        )
        for coset in q8_cosets
    )

    assert mod30_orders == [1, 2, 2, 2]
    assert q8_orders == [1, 2, 2, 2]


if __name__ == "__main__":
    mod30_cosets = quotient_cosets(
        MOD30_UNITS,
        MOD30_SUBGROUP,
        mod30_mul,
    )

    q8_cosets = quotient_cosets(
        Q8_ELEMENTS,
        Q8_CENTER,
        q8_mul,
    )

    test_mod30_subgroup()
    test_q8_center()
    test_mod30_quotient_has_four_cosets()
    test_q8_quotient_has_four_cosets()
    test_mod30_quotient_is_v4()
    test_q8_quotient_is_v4()
    test_common_quotient_structure()

    print("Reading Point Test 003")
    print("----------------------")
    print()

    print("mod-30 quotient cosets:")
    for coset in sorted(mod30_cosets, key=lambda c: min(c)):
        values = ", ".join(str(x) for x in sorted(coset))
        print(f"  {{{values}}}")

    print()
    print("Q8 / center cosets:")
    for coset in sorted(
        q8_cosets,
        key=lambda c: sorted(q8_label(x) for x in c),
    ):
        values = ", ".join(sorted(q8_label(x) for x in coset))
        print(f"  {{{values}}}")

    print()
    print("quotient cardinality match: PASS")
    print("quotient element-order profile: PASS")
    print("common quotient structure: SUPPORTED")
    print()
    print("Result:")
    print("(Z/30Z)^* / {1,19} is isomorphic to C2 x C2.")
    print("Q8 / {1,-1} is isomorphic to C2 x C2.")
    print()
    print("Interpretation:")
    print("The original eight-element groups are not isomorphic,")
    print("but independently defined two-element reductions produce")
    print("the same four-element quotient structure.")
    print()
    print("Physical correspondence: NOT ESTABLISHED")
