# readingpoint/tests/test_001_mod30_vs_q8.py

from itertools import product


MODULUS = 30
MOD30_UNITS = (1, 7, 11, 13, 17, 19, 23, 29)

# Represent Q8 elements as (sign, basis), where basis ∈ {1, i, j, k}.
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


def element_order(element, identity, multiply, max_steps=32) -> int:
    value = identity
    for n in range(1, max_steps + 1):
        value = multiply(value, element)
        if value == identity:
            return n
    raise RuntimeError(f"Could not determine order of {element!r}")


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


def test_mod30_units_form_group():
    units = set(MOD30_UNITS)

    assert len(units) == 8
    assert 1 in units

    for a, b in product(units, repeat=2):
        assert mod30_mul(a, b) in units

    for a in units:
        assert mod30_mul(a, a) == 1


def test_mod30_unit_orders():
    orders = {
        a: element_order(a, 1, mod30_mul)
        for a in MOD30_UNITS
    }

    assert orders[1] == 1
    assert all(order == 2 for a, order in orders.items() if a != 1)


def test_mod30_units_are_abelian():
    for a, b in product(MOD30_UNITS, repeat=2):
        assert mod30_mul(a, b) == mod30_mul(b, a)


def test_q8_has_eight_elements():
    assert len(set(Q8_ELEMENTS)) == 8


def test_q8_is_nonabelian():
    i = (1, "i")
    j = (1, "j")

    assert q8_mul(i, j) != q8_mul(j, i)


def test_q8_element_orders():
    identity = (1, "1")

    orders = {
        element: element_order(element, identity, q8_mul)
        for element in Q8_ELEMENTS
    }

    assert orders[(1, "1")] == 1
    assert orders[(-1, "1")] == 2

    order_four = [
        element
        for element, order in orders.items()
        if order == 4
    ]

    assert len(order_four) == 6


def test_equal_cardinality_but_no_group_isomorphism():
    assert len(MOD30_UNITS) == len(Q8_ELEMENTS) == 8

    mod30_is_abelian = all(
        mod30_mul(a, b) == mod30_mul(b, a)
        for a, b in product(MOD30_UNITS, repeat=2)
    )

    q8_is_abelian = all(
        q8_mul(a, b) == q8_mul(b, a)
        for a, b in product(Q8_ELEMENTS, repeat=2)
    )

    assert mod30_is_abelian is True
    assert q8_is_abelian is False


if __name__ == "__main__":
    test_mod30_units_form_group()
    test_mod30_unit_orders()
    test_mod30_units_are_abelian()
    test_q8_has_eight_elements()
    test_q8_is_nonabelian()
    test_q8_element_orders()
    test_equal_cardinality_but_no_group_isomorphism()

    print("Reading Point Test 001")
    print("----------------------")
    print("mod-30 units: 8")
    print("Q8 elements: 8")
    print("cardinality match: PASS")
    print("group isomorphism: REJECTED")
    print()
    print("Reason:")
    print("(Z/30Z)^* is abelian and every non-identity element has order 2.")
    print("Q8 is non-abelian and has six elements of order 4.")
