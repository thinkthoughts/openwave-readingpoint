# readingpoint/tests/test_009_m5_half_winding_basis_equivalence.py

import numpy as np


Q_VALUES = (+0.5, -0.5)
CHI_VALUES = np.linspace(0.0, 2.0 * np.pi, 721)

LAMBDA_P = 1.0
LAMBDA_M = 0.3
TOL = 1e-12


def director(chi, q, convention):
    if convention == "generic":
        n1 = np.sin(q * chi)
        n3 = np.cos(q * chi)

    elif convention == "symmetric":
        n1 = np.cos(q * chi)
        n3 = np.sin(q * chi)

    else:
        raise ValueError(convention)

    n = np.array([n1, n3], dtype=float)
    return n / np.linalg.norm(n)


def tensor_13(n):
    """
    2x2 representation of the wound (1,3) block:

        M = lambda_p n n^T + lambda_m p p^T

    where p is perpendicular to n.
    """
    p = np.array([-n[1], n[0]], dtype=float)

    return (
        LAMBDA_P * np.outer(n, n)
        + LAMBDA_M * np.outer(p, p)
    )


# Swap the two wound-plane axes.
SWAP_13 = np.array(
    [
        [0.0, 1.0],
        [1.0, 0.0],
    ]
)


def transformed(M):
    return SWAP_13 @ M @ SWAP_13.T


def max_equivalence_error(q):
    errors = []

    for chi in CHI_VALUES:
        n_sym = director(
            chi,
            q,
            "symmetric",
        )

        n_gen = director(
            chi,
            q,
            "generic",
        )

        M_sym = tensor_13(n_sym)
        M_gen = tensor_13(n_gen)

        errors.append(
            np.max(
                np.abs(
                    M_gen
                    - transformed(M_sym)
                )
            )
        )

    return float(max(errors))


def test_generic_and_symmetric_are_globally_basis_equivalent():
    for q in Q_VALUES:
        err = max_equivalence_error(q)
        assert err < TOL


def test_swap_is_orthogonal():
    I = np.eye(2)

    assert np.max(
        np.abs(
            SWAP_13.T @ SWAP_13 - I
        )
    ) < TOL


def test_swap_has_reflection_orientation_in_2d():
    """
    In the isolated (1,3) plane the axis swap has determinant -1.

    Embedded in 3D, an additional sign flip of the orthogonal axis
    can turn this into a proper SO(3) basis transformation.
    """
    assert abs(
        np.linalg.det(SWAP_13) + 1.0
    ) < TOL


def test_proper_3d_embedding_exists():
    """
    Embed the 1<->3 swap together with a sign reversal of axis 2:

        e1 -> e3
        e2 -> -e2
        e3 -> e1

    This matrix has determinant +1 and therefore lies in SO(3).
    """

    R3 = np.array(
        [
            [0.0, 0.0, 1.0],
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
        ]
    )

    I = np.eye(3)

    assert np.max(
        np.abs(
            R3.T @ R3 - I
        )
    ) < TOL

    assert abs(
        np.linalg.det(R3) - 1.0
    ) < TOL


if __name__ == "__main__":
    test_generic_and_symmetric_are_globally_basis_equivalent()
    test_swap_is_orthogonal()
    test_swap_has_reflection_orientation_in_2d()
    test_proper_3d_embedding_exists()

    print("Reading Point Test 009")
    print("----------------------")
    print()
    print("M5 half-winding basis-equivalence control")
    print()

    for q in Q_VALUES:
        err = max_equivalence_error(q)

        print(
            f"q={q:+.1f}"
            f"  max tensor equivalence error="
            f"{err:.3e}"
        )

    print()
    print("2D wound-plane transformation:")
    print("  swap axes 1 <-> 3")
    print("  determinant = -1")
    print()
    print("3D embedding:")
    print("  e1 -> e3")
    print("  e2 -> -e2")
    print("  e3 -> e1")
    print("  determinant = +1")
    print("  proper SO(3) transformation: PASS")
    print()
    print("Result:")
    print(
        "The generic and symmetric half-winding tensor constructions "
        "are related by a fixed global basis transformation."
    )
    print()
    print("Interpretation:")
    print(
        "Their opposite winding-sign readouts in Result 008 therefore "
        "cannot by themselves select one convention as physically "
        "distinct."
    )
    print(
        "The sign reported by winding_measure_biax depends on the chosen "
        "(1,3)-plane basis orientation."
    )
    print(
        "A physical sign convention requires an independently specified "
        "orientation, handedness, transport rule, or interaction observable."
    )
    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")
