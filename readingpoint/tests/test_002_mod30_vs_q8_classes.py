# readingpoint/tests/test_002_mod30_vs_q8_classes.py

from collections import defaultdict
from itertools import product


MODULUS = 30
MOD30_UNITS = (1, 7, 11, 13, 17, 19, 23, 29)

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


def mod30_mul(a: int, b: int) -> int:
    return (a * b) % MODULUS


def mod30_inv(a: int) -> int:
    for b in MOD30_UNITS:
        if mod30_mul(a, b) == 1:
            return b
    raise RuntimeError(f"No inverse found for {a}")


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


def q8_inv(a):
    identity = (1, "1")

    for b in Q8_ELEMENTS:
        if q8_mul(a, b) == identity and q8_mul(b, a) == identity:
            return b

    raise RuntimeError(f"No inverse found for {a}")


def conjugacy_class(element, elements, multiply, inverse):
    return frozenset(
        multiply(
            multiply(g, element),
            inverse(g),
        )
        for g in elements
    )


def all_conjugacy_classes(elements, multiply, inverse):
    remaining = set(elements)
    classes = []

    while remaining:
        element = next(iter(remaining))
        cls = conjugacy_class(element, elements, multiply, inverse)
        classes.append(cls)
        remaining -= cls

    return tuple(
        sorted(
            classes,
            key=lambda cls: (len(cls), sorted(map(str, cls))),
        )
    )


def element_order(element, identity, multiply, max_steps=32):
    value = identity

    for n in range(1, max_steps + 1):
        value = multiply(value, element)
        if value == identity:
            return n

    raise RuntimeError(f"Could not determine order for {element!r}")


def q8_label(element):
    sign, basis = element

    if basis == "1":
        return "1" if sign == 1 else "-1"

    return basis if sign == 1 else f"-{basis}"


def test_mod30_conjugacy_classes_are_singletons():
    classes = all_conjugacy_classes(
        MOD30_UNITS,
        mod30_mul,
        mod30_inv,
    )

    assert len(classes) == 8
    assert all(len(cls) == 1 for cls in classes)


def test_q8_conjugacy_class_structure():
    classes = all_conjugacy_classes(
        Q8_ELEMENTS,
        q8_mul,
        q8_inv,
    )

    class_sizes = sorted(len(cls) for cls in classes)

    assert len(classes) == 5
    assert class_sizes == [1, 1, 2, 2, 2]


def test_q8_expected_classes():
    classes = {
        frozenset(cls)
        for cls in all_conjugacy_classes(
            Q8_ELEMENTS,
            q8_mul,
            q8_inv,
        )
    }

    expected = {
        frozenset({(1, "1")}),
        frozenset({(-1, "1")}),
        frozenset({(1, "i"), (-1, "i")}),
        frozenset({(1, "j"), (-1, "j")}),
        frozenset({(1, "k"), (-1, "k")}),
    }

    assert classes == expected


def test_conjugacy_class_cardinality_does_not_match():
    mod30_classes = all_conjugacy_classes(
        MOD30_UNITS,
        mod30_mul,
        mod30_inv,
    )

    q8_classes = all_conjugacy_classes(
        Q8_ELEMENTS,
        q8_mul,
        q8_inv,
    )

    assert len(mod30_classes) == 8
    assert len(q8_classes) == 5
    assert len(mod30_classes) != len(q8_classes)


def test_order_profiles():
    mod30_orders = sorted(
        element_order(a, 1, mod30_mul)
        for a in MOD30_UNITS
    )

    q8_orders = sorted(
        element_order(a, (1, "1"), q8_mul)
        for a in Q8_ELEMENTS
    )

    assert mod30_orders == [1, 2, 2, 2, 4, 4, 4, 4]
    assert q8_orders == [1, 2, 4, 4, 4, 4, 4, 4]


if __name__ == "__main__":
    mod30_classes = all_conjugacy_classes(
        MOD30_UNITS,
        mod30_mul,
        mod30_inv,
    )

    q8_classes = all_conjugacy_classes(
        Q8_ELEMENTS,
        q8_mul,
        q8_inv,
    )

    test_mod30_conjugacy_classes_are_singletons()
    test_q8_conjugacy_class_structure()
    test_q8_expected_classes()
    test_conjugacy_class_cardinality_does_not_match()
    test_order_profiles()

    print("Reading Point Test 002")
    print("----------------------")
    print()

    print("mod-30 unit-group conjugacy classes:")
    for cls in sorted(mod30_classes, key=lambda c: min(c)):
        values = ", ".join(str(x) for x in sorted(cls))
        print(f"  {{{values}}}")

    print()
    print(f"class count: {len(mod30_classes)}")
    print("class sizes:", sorted(len(cls) for cls in mod30_classes))

    print()
    print("Q8 conjugacy classes:")
    for cls in sorted(
        q8_classes,
        key=lambda c: (
            len(c),
            sorted(q8_label(x) for x in c),
        ),
    ):
        values = ", ".join(
            sorted(q8_label(x) for x in cls)
        )
        print(f"  {{{values}}}")

    print()
    print(f"class count: {len(q8_classes)}")
    print("class sizes:", sorted(len(cls) for cls in q8_classes))

    print()
    print("conjugacy-class correspondence: REJECTED")
    print()
    print("Reason:")
    print("(Z/30Z)^* is abelian, so all 8 conjugacy classes are singletons.")
    print("Q8 has 5 conjugacy classes with sizes 1, 1, 2, 2, 2.")
    print("Therefore the eight Reading Point lanes cannot correspond")
    print("one-to-one with Q8 conjugacy classes.")
    print()
    print("Next admissible question:")
    print("Can a quotient, action, or representation define a")
    print("non-arbitrary relation between the two structures?")
