# readingpoint/tests/test_014_m5_chiral_hessian_symmetry.py

from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]

M5_SCRIPTS = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
)

if str(M5_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(M5_SCRIPTS))

from m5_11_n3_mass_matrix import rot_axis  # noqa: E402
from m5_11_n3_theta13 import (  # noqa: E402
    seed_loop_biaxial,
    biaxial_vacuum,
)
from m5_11_n4_chiral import chiral_overlap  # noqa: E402


# ----------------------------------------------------------------------
# Controlled geometry
# ----------------------------------------------------------------------

N = 24
ALPHA = 0.6
DELTA = 0.1
CHI = 0.6

R_LOOP = 6.0
Q = 0.5
CORE_VOX = 2.0

DX = 1.0
Q0 = 2.0 * np.pi / 24.0
LC = 1.0

TOL = 1e-10


# Levi-Civita permutations:
# (i, k, l, epsilon_ikl), using P2's 1-based spatial indices.
PERMS = (
    (1, 2, 3, +1.0),
    (2, 3, 1, +1.0),
    (3, 1, 2, +1.0),
    (1, 3, 2, -1.0),
    (3, 2, 1, -1.0),
    (2, 1, 3, -1.0),
)


def build_n4_displacements():
    """
    Build the same three flavour-type loop fields used by the N4
    construction:

        e   : reference orientation
        mu  : +alpha
        tau : -alpha

    mu and tau carry the same secondary screw handedness chi.
    """

    Re = np.eye(3)
    Rmu = rot_axis((1.0, 0.0, 0.0), +ALPHA)
    Rtau = rot_axis((1.0, 0.0, 0.0), -ALPHA)

    Mvac = biaxial_vacuum(N, DELTA)

    fe = seed_loop_biaxial(
        N,
        Re,
        R_LOOP,
        DELTA,
        q=Q,
        core_vox=CORE_VOX,
        chi=0.0,
    )

    fmu = seed_loop_biaxial(
        N,
        Rmu,
        R_LOOP,
        DELTA,
        q=Q,
        core_vox=CORE_VOX,
        chi=CHI,
    )

    ftau = seed_loop_biaxial(
        N,
        Rtau,
        R_LOOP,
        DELTA,
        q=Q,
        core_vox=CORE_VOX,
        chi=CHI,
    )

    return [
        fe - Mvac,
        fmu - Mvac,
        ftau - Mvac,
    ]


def p2_lifshitz_bilinear(A, B, q0=Q0, Lc=LC, dx=DX):
    """
    Bilinear form underlying the implemented P2 scalar Lifshitz energy.

    P2 computes schematically

        E_chiral[Q]
          = 2 q0 Lc ∫ epsilon_ikl Q_ij d_k Q_lj d^3x.

    Define

        B(A,B)
          = 2 q0 Lc ∫ epsilon_ikl A_ij d_k B_lj d^3x.

    Then the ordinary second variation / Hessian contribution of the
    scalar quadratic energy is

        H(A,B) = B(A,B) + B(B,A),

    which is symmetric under A <-> B regardless of whether B itself is
    symmetric.
    """

    Asp = A[..., 1:4, 1:4]
    Bsp = B[..., 1:4, 1:4]

    inv2dx = 1.0 / (2.0 * dx)

    gx = np.zeros_like(Bsp)
    gy = np.zeros_like(Bsp)
    gz = np.zeros_like(Bsp)

    gx[1:-1] = (
        Bsp[2:] - Bsp[:-2]
    ) * inv2dx

    gy[:, 1:-1] = (
        Bsp[:, 2:] - Bsp[:, :-2]
    ) * inv2dx

    gz[:, :, 1:-1] = (
        Bsp[:, :, 2:] - Bsp[:, :, :-2]
    ) * inv2dx

    grads = {
        1: gx,
        2: gy,
        3: gz,
    }

    dens = np.zeros(
        Asp.shape[:3],
        dtype=float,
    )

    for pi, pk, pl, sign in PERMS:
        grad = grads[pk]

        dens += sign * np.einsum(
            "...j,...j->...",
            Asp[..., pi - 1, :],
            grad[..., pl - 1, :],
        )

    interior = np.zeros(
        dens.shape,
        dtype=bool,
    )

    interior[
        1:-1,
        1:-1,
        1:-1,
    ] = True

    return float(
        np.sum(
            2.0
            * q0
            * Lc
            * dens[interior]
        )
        * dx**3
    )


def projected_p2_bilinear_matrix(dfields):
    """
    Raw P2 bilinear B_ab = B(dM_a, dM_b).
    """

    B = np.zeros((3, 3))

    for a in range(3):
        for b in range(3):
            B[a, b] = p2_lifshitz_bilinear(
                dfields[a],
                dfields[b],
            )

    return B


def projected_p2_hessian(dfields):
    """
    Hessian / second-variation matrix of the scalar P2 Lifshitz energy:

        H_ab = B_ab + B_ba.

    This must be symmetric.
    """

    B = projected_p2_bilinear_matrix(
        dfields
    )

    H = B + B.T

    return H, B


def n4_chiral_matrix(dfields):
    """
    Evaluate the existing N4 chiral_overlap for every ordered flavour
    pair without imposing antisymmetry by hand.
    """

    C = np.zeros((3, 3))

    for a in range(3):
        for b in range(3):
            C[a, b] = chiral_overlap(
                dfields[a],
                dfields[b],
            )

    return C


def relative_symmetry_error(M):
    scale = max(
        float(np.max(np.abs(M))),
        1.0,
    )

    return float(
        np.max(np.abs(M - M.T))
        / scale
    )


def relative_antisymmetry_error(M):
    scale = max(
        float(np.max(np.abs(M))),
        1.0,
    )

    return float(
        np.max(np.abs(M + M.T))
        / scale
    )


def normalized_frobenius_inner(A, B):
    num = float(
        np.sum(A * B)
    )

    den = float(
        np.linalg.norm(A)
        * np.linalg.norm(B)
    )

    if den < 1e-30:
        return 0.0

    return num / den


def test_p2_projected_hessian_is_symmetric():
    dfields = build_n4_displacements()

    H, _ = projected_p2_hessian(
        dfields
    )

    assert relative_symmetry_error(H) < TOL


def test_n4_C_is_antisymmetric():
    dfields = build_n4_displacements()

    C = n4_chiral_matrix(
        dfields
    )

    assert relative_antisymmetry_error(C) < TOL


def test_n4_C_is_nonzero():
    dfields = build_n4_displacements()

    C = n4_chiral_matrix(
        dfields
    )

    assert np.max(np.abs(C)) > 1e-8


def test_symmetric_hessian_is_orthogonal_to_antisymmetric_C():
    dfields = build_n4_displacements()

    H, _ = projected_p2_hessian(
        dfields
    )

    C = n4_chiral_matrix(
        dfields
    )

    overlap = normalized_frobenius_inner(
        H,
        C,
    )

    assert abs(overlap) < TOL


def test_direct_scalar_hessian_cannot_generate_nonzero_n4_C():
    """
    A nonzero antisymmetric matrix cannot equal a symmetric Hessian
    multiplied by an ordinary real scalar.

    This is the structural obstruction being tested.
    """

    dfields = build_n4_displacements()

    H, _ = projected_p2_hessian(
        dfields
    )

    C = n4_chiral_matrix(
        dfields
    )

    h_sym = (
        relative_symmetry_error(H)
        < TOL
    )

    c_antisym = (
        relative_antisymmetry_error(C)
        < TOL
    )

    c_nonzero = (
        np.max(np.abs(C))
        > 1e-8
    )

    assert h_sym
    assert c_antisym
    assert c_nonzero


if __name__ == "__main__":
    dfields = build_n4_displacements()

    H, B = projected_p2_hessian(
        dfields
    )

    C = n4_chiral_matrix(
        dfields
    )

    test_p2_projected_hessian_is_symmetric()
    test_n4_C_is_antisymmetric()
    test_n4_C_is_nonzero()
    test_symmetric_hessian_is_orthogonal_to_antisymmetric_C()
    test_direct_scalar_hessian_cannot_generate_nonzero_n4_C()

    h_sym_err = relative_symmetry_error(H)
    c_anti_err = relative_antisymmetry_error(C)

    hc_overlap = normalized_frobenius_inner(
        H,
        C,
    )

    print("Reading Point Test 014")
    print("----------------------")
    print()

    print("N3 effective-mass prescription:")
    print("ENERGY-HESSIAN PROJECTION")

    print()
    print("P2 Lifshitz scalar energy:")
    print("IMPLEMENTED")

    print()
    print("Projected P2 raw bilinear B:")
    print(np.array2string(
        B,
        precision=6,
        suppress_small=True,
    ))

    print()
    print("Projected P2 scalar-energy Hessian H = B + B^T:")
    print(np.array2string(
        H,
        precision=6,
        suppress_small=True,
    ))

    print()
    print(
        "Projected P2 Hessian symmetry error:"
    )
    print(f"{h_sym_err:.3e}")

    print()
    print("N4 chiral matrix C:")
    print(np.array2string(
        C,
        precision=6,
        suppress_small=True,
    ))

    print()
    print(
        "N4 C antisymmetry error:"
    )
    print(f"{c_anti_err:.3e}")

    print()
    print(
        "Normalized Frobenius overlap <H,C>:"
    )
    print(f"{hc_overlap:.3e}")

    print()
    print("Projected P2 Hessian symmetric:")
    print(
        "PASS"
        if h_sym_err < TOL
        else "FAIL"
    )

    print()
    print("N4 C antisymmetric:")
    print(
        "PASS"
        if c_anti_err < TOL
        else "FAIL"
    )

    print()
    print("N4 C nonzero:")
    print(
        "PASS"
        if np.max(np.abs(C)) > 1e-8
        else "FAIL"
    )

    print()
    print("P2 scalar-energy Hessian -> N4 antisymmetric C:")
    print("STRUCTURALLY OBSTRUCTED")

    print()
    print("Interpretation:")
    print(
        "The existing N3 reduction defines flavour-space mass terms "
        "through the second variation of a scalar energy."
    )
    print(
        "Projecting the implemented P2 Lifshitz scalar energy onto the "
        "same type of flavour field directions produces a symmetric "
        "Hessian matrix."
    )
    print(
        "The existing N4 chiral overlap instead produces a nonzero "
        "real antisymmetric matrix C."
    )
    print(
        "Therefore the P2 scalar-energy term cannot generate N4 C "
        "through the stated N3 energy-Hessian projection alone."
    )

    print()
    print("Additional independently derived effective structure:")
    print("REQUIRED")

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")
