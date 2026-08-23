# readingpoint/tests/test_007_m5_winding_seed_closure.py

import numpy as np


Q_VALUES = (-1.0, -0.5, -0.25, 0.25, 0.5, 1.0)
TOL = 1e-12


def director_from_chi(chi, q):
    """
    Reproduce the angular part of M5 winding_director(), excluding the
    radial axis_blend because this test concerns monodromy around a
    closed loop at fixed nonzero radius.
    """
    if abs(q - 0.5) < 1e-12:
        n1 = np.cos(0.5 * chi)
        n3 = np.sin(0.5 * chi)
    else:
        n1 = np.sin(q * chi)
        n3 = np.cos(q * chi)

    n = np.array([n1, n3], dtype=float)
    return n / np.linalg.norm(n)


def apolar_tensor(n):
    """
    Minimal 2D apolar tensor carrying the director identification n ~ -n.

    The full M5 tensor also contains eigenvalue weights, but n n^T is
    sufficient to test whether the angular director closes as an apolar
    field after one circuit.
    """
    return np.outer(n, n)


def endpoint_data(q):
    n0 = director_from_chi(0.0, q)
    n2pi = director_from_chi(2.0 * np.pi, q)

    M0 = apolar_tensor(n0)
    M2pi = apolar_tensor(n2pi)

    oriented_error = float(np.max(np.abs(n2pi - n0)))
    sign_reversed_error = float(np.max(np.abs(n2pi + n0)))
    tensor_error = float(np.max(np.abs(M2pi - M0)))

    director_return = oriented_error <= TOL
    director_sign_return = sign_reversed_error <= TOL
    apolar_closure = tensor_error <= TOL

    return {
        "q": q,
        "n0": n0,
        "n2pi": n2pi,
        "oriented_error": oriented_error,
        "sign_reversed_error": sign_reversed_error,
        "tensor_error": tensor_error,
        "director_return": director_return,
        "director_sign_return": director_sign_return,
        "apolar_closure": apolar_closure,
    }


def test_half_and_integer_windings_close_as_apolar_fields():
    for q in (-1.0, -0.5, 0.5, 1.0):
        result = endpoint_data(q)
        assert result["apolar_closure"]


def test_quarter_windings_do_not_close_as_apolar_fields():
    for q in (-0.25, 0.25):
        result = endpoint_data(q)
        assert not result["apolar_closure"]


def test_positive_half_special_branch_closes_by_sign():
    result = endpoint_data(0.5)

    assert result["director_sign_return"]
    assert result["apolar_closure"]


def test_negative_half_generic_branch_also_closes_apolarly():
    result = endpoint_data(-0.5)

    assert result["apolar_closure"]


if __name__ == "__main__":
    test_half_and_integer_windings_close_as_apolar_fields()
    test_quarter_windings_do_not_close_as_apolar_fields()
    test_positive_half_special_branch_closes_by_sign()
    test_negative_half_generic_branch_also_closes_apolarly()

    print("Reading Point Test 007")
    print("----------------------")
    print()
    print("M5 winding-seed monodromy / apolar closure")
    print()

    for q in Q_VALUES:
        result = endpoint_data(q)

        if result["director_return"]:
            director_status = "n -> n"
        elif result["director_sign_return"]:
            director_status = "n -> -n"
        else:
            director_status = "no ±n return"

        closure = (
            "CLOSED"
            if result["apolar_closure"]
            else "NOT CLOSED"
        )

        print(
            f"q={q:+.2f}"
            f"  director: {director_status:12s}"
            f"  tensor_error={result['tensor_error']:.3e}"
            f"  apolar field: {closure}"
        )

    print()
    print("Result:")
    print("integer and half-integer probes close as apolar fields.")
    print("quarter-winding probes do not close after one circuit.")
    print()
    print("Interpretation:")
    print(
        "The q=0.25 behavior in Result 006 is therefore not evidence "
        "for a quarter-winding topological sector."
    )
    print(
        "It probes winding_measure_biax with a synthetic seed whose "
        "apolar field does not close around the loop."
    )
    print(
        "The q=0.5 and q=1.0 probes satisfy the basic closed-field "
        "condition and are the more meaningful sectors for further "
        "instrument analysis."
    )
    print()
    print("Code-path note:")
    print(
        "M5 winding_director() special-cases q=+0.5; q=-0.5 uses "
        "the generic sin(q*chi), cos(q*chi) branch."
    )
    print("The consequences of that branch asymmetry remain to be tested.")
