#!/usr/bin/env python3
"""
Reading Point Test 020 — N4 C spatial reflection.

Results 018–019 established that the N4 chiral operator C is:

  - approximately even under chi -> -chi;
  - exactly covariant under mu<->tau basis relabeling;
  - approximately odd under the tested mu/tau orientation mirror.

Result 020 asks a stronger question:

    Does an actual spatial reflection of the M5 tensor fields reverse C?

We use the physical-space reflection

    x -> -x

with spatial reflection matrix

    S = diag(-1, +1, +1).

For a rank-2 spatial tensor field M_ij(x), the reflected field is

    M'_sp(x) = S M_sp(S x) S^T.

On the discrete cubic grid this means:

  1. reverse the x-axis of the field array;
  2. conjugate the spatial 3x3 tensor block by S.

The time / g component is left unchanged.

The test compares the reflected chiral matrix against:

    -C

and, separately, against the mu<->tau basis-transformed forms

    P C P^T
    -P C P^T.

This keeps actual spatial parity distinct from flavour-basis relabeling.

No Reading Point residue mapping is introduced.
"""

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
# Controlled reference geometry
# ----------------------------------------------------------------------

N = 40
DX = 1.0

ALPHA = 0.6
DELTA = 0.1
CHI = 0.6
Q = 0.5

R_LOOP = 9.0
CORE_VOX = 2.0

ANTISYM_TOL = 1e-10
APPROX_TOL = 1e-4
MAG_TOL = 1e-4


def reflection_matrix_x():
    """
    Spatial reflection x -> -x.
    """
    return np.diag(
        [-1.0, 1.0, 1.0]
    )


def mu_tau_swap_matrix():
    """
    Flavour basis permutation:
        [e, mu, tau] -> [e, tau, mu]
    """
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )


def frobenius_norm(M):
    return float(
        np.linalg.norm(M)
    )


def relative_matrix_error(A, B):
    den = max(
        frobenius_norm(B),
        1e-30,
    )

    return float(
        frobenius_norm(A - B)
        / den
    )


def relative_scalar_error(a, b):
    return float(
        abs(a - b)
        / max(abs(b), 1e-30)
    )


def antisymmetry_error(C):
    scale = max(
        float(np.max(np.abs(C))),
        1.0,
    )

    return float(
        np.max(np.abs(C + C.T))
        / scale
    )


def normalized_operator(C):
    norm = frobenius_norm(C)

    if not np.isfinite(norm) or norm <= 1e-30:
        raise ValueError(
            "zero or non-finite C norm"
        )

    return C / norm


def build_displacements():
    """
    Standard N4 three-loop flavour displacement family.

    e   : reference
    mu  : +alpha
    tau : -alpha

    Both mu/tau use +CHI, matching the N4 branch.
    """

    Re = np.eye(3)

    Rmu = rot_axis(
        (1.0, 0.0, 0.0),
        +ALPHA,
    )

    Rtau = rot_axis(
        (1.0, 0.0, 0.0),
        -ALPHA,
    )

    Mvac = biaxial_vacuum(
        N,
        DELTA,
    )

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


def reflect_field_x(F):
    """
    Apply the actual spatial reflection x -> -x.

    Coordinate action:
        F(x,y,z) -> F(-x,y,z)

    Tensor action:
        M_sp -> S M_sp S^T

    The 0-index / time-g component is unchanged except for coordinate
    reversal.
    """

    S = reflection_matrix_x()

    # Reverse coordinate x.
    Fr = F[::-1, :, :, :, :].copy()

    # Transform spatial 3x3 tensor block.
    Msp = Fr[..., 1:4, 1:4]

    Msp_reflected = np.einsum(
        "ab,...bc,dc->...ad",
        S,
        Msp,
        S,
    )

    Fr[..., 1:4, 1:4] = Msp_reflected

    return Fr


def chiral_matrix(dfields):
    """
    Evaluate chiral_overlap on all ordered flavour pairs.
    """

    C = np.zeros((3, 3), dtype=float)

    for a in range(3):
        for b in range(3):
            C[a, b] = chiral_overlap(
                dfields[a],
                dfields[b],
            )

    return C


def evaluate():
    original_fields = build_displacements()

    reflected_fields = [
        reflect_field_x(F)
        for F in original_fields
    ]

    C = chiral_matrix(
        original_fields
    )

    Cr = chiral_matrix(
        reflected_fields
    )

    return {
        "C": C,
        "Cr": Cr,
        "norm": frobenius_norm(DX * C),
        "reflected_norm": frobenius_norm(DX * Cr),
        "anti_C": antisymmetry_error(C),
        "anti_Cr": antisymmetry_error(Cr),
        "C_hat": normalized_operator(C),
        "Cr_hat": normalized_operator(Cr),
    }


# ----------------------------------------------------------------------
# Structural tests
# ----------------------------------------------------------------------

def test_reflection_preserves_finiteness_and_nonzero_operator():
    row = evaluate()

    assert np.all(
        np.isfinite(row["C"])
    )

    assert np.all(
        np.isfinite(row["Cr"])
    )

    assert row["norm"] > 1e-8
    assert row["reflected_norm"] > 1e-8


def test_reflection_preserves_antisymmetry():
    row = evaluate()

    assert row["anti_C"] < ANTISYM_TOL
    assert row["anti_Cr"] < ANTISYM_TOL


def test_reflection_preserves_tensor_symmetry():
    """
    The reflected rank-2 spatial tensor should remain symmetric.
    """

    fields = build_displacements()

    for F in fields:
        Fr = reflect_field_x(F)

        Msp = Fr[..., 1:4, 1:4]

        err = float(
            np.max(
                np.abs(
                    Msp
                    - np.swapaxes(
                        Msp,
                        -1,
                        -2,
                    )
                )
            )
        )

        assert err < 1e-12


def run_all():
    test_reflection_preserves_finiteness_and_nonzero_operator()
    test_reflection_preserves_antisymmetry()
    test_reflection_preserves_tensor_symmetry()


def main():
    run_all()

    row = evaluate()

    C = row["C"]
    Cr = row["Cr"]

    P = mu_tau_swap_matrix()

    PCP = (
        P
        @ C
        @ P.T
    )

    # --------------------------------------------------------------
    # Direct spatial-reflection comparisons
    # --------------------------------------------------------------

    parity_even_error = relative_matrix_error(
        Cr,
        C,
    )

    parity_odd_error = relative_matrix_error(
        Cr,
        -C,
    )

    parity_norm_error = relative_scalar_error(
        row["reflected_norm"],
        row["norm"],
    )

    parity_even_shape_error = relative_matrix_error(
        row["Cr_hat"],
        row["C_hat"],
    )

    parity_odd_shape_error = relative_matrix_error(
        row["Cr_hat"],
        -row["C_hat"],
    )

    # --------------------------------------------------------------
    # Compare against mu/tau basis-transformed possibilities
    # --------------------------------------------------------------

    basis_even_error = relative_matrix_error(
        Cr,
        PCP,
    )

    basis_odd_error = relative_matrix_error(
        Cr,
        -PCP,
    )

    print("Reading Point Test 020")
    print("----------------------")
    print()

    print("N4 C actual spatial reflection")
    print()

    print(
        f"n={N}"
        f"  dx={DX}"
        f"  alpha={ALPHA}"
        f"  delta={DELTA}"
        f"  chi={CHI}"
        f"  q={Q}"
    )

    print()
    print("Spatial reflection:")
    print("x -> -x")

    print()
    print("Tensor transformation:")
    print(
        "M'_sp(x) = S M_sp(Sx) S^T"
    )
    print(
        "S = diag(-1, +1, +1)"
    )

    print()
    print("Original C:")
    print(
        np.array2string(
            C,
            precision=6,
            suppress_small=True,
        )
    )

    print()
    print("Reflected C:")
    print(
        np.array2string(
            Cr,
            precision=6,
            suppress_small=True,
        )
    )

    print()
    print("Direct parity diagnostics:")
    print()

    print(
        "evenness error "
        "||C_ref - C|| / ||C||:"
    )
    print(
        f"{parity_even_error:.6e}"
    )

    print()
    print(
        "oddness error "
        "||C_ref + C|| / ||C||:"
    )
    print(
        f"{parity_odd_error:.6e}"
    )

    print()
    print(
        "normalized even-shape error:"
    )
    print(
        f"{parity_even_shape_error:.6e}"
    )

    print()
    print(
        "normalized odd-shape error:"
    )
    print(
        f"{parity_odd_shape_error:.6e}"
    )

    print()
    print(
        "||dx*C_ref|| / ||dx*C||:"
    )
    print(
        f"{row['reflected_norm'] / row['norm']:.12f}"
    )

    print()
    print(
        "relative magnitude difference:"
    )
    print(
        f"{parity_norm_error:.6e}"
    )

    print()
    print("Basis-adjusted comparisons:")
    print()

    print(
        "error vs P C P^T:"
    )
    print(
        f"{basis_even_error:.6e}"
    )

    print()
    print(
        "error vs -P C P^T:"
    )
    print(
        f"{basis_odd_error:.6e}"
    )

    print()
    print("Antisymmetry:")
    print(
        f"original={row['anti_C']:.3e}"
        f"  reflected={row['anti_Cr']:.3e}"
    )
    print("PASS")

    # --------------------------------------------------------------
    # Verdicts
    # --------------------------------------------------------------

    print()
    print("Actual spatial reflection x -> -x:")
    print()

    print("Direct C sign reversal:")
    if parity_odd_error < APPROX_TOL:
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED")

    print()
    print("Direct C invariance:")
    if parity_even_error < APPROX_TOL:
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED")

    print()
    print("Magnitude preservation:")
    if parity_norm_error < MAG_TOL:
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED")

    print()
    print("Basis-adjusted parity relation:")
    if basis_odd_error < APPROX_TOL:
        print("C_ref approximately equals -P C P^T")
    elif basis_even_error < APPROX_TOL:
        print("C_ref approximately equals P C P^T")
    else:
        print("NO SIMPLE TESTED BASIS-ADJUSTED RELATION")

    print()
    print("Interpretation:")
    print(
        "This test applies an actual spatial reflection to the "
        "rank-2 M5 tensor fields rather than swapping flavour-loop "
        "orientation labels."
    )
    print(
        "It therefore separates physical-space parity behavior from "
        "the mu<->tau basis covariance established in Results 018-019."
    )
    print(
        "The result determines whether the effective chiral operator "
        "is directly odd, directly even, or requires a flavour-basis "
        "transformation under this spatial reflection."
    )

    print()
    print("Physical spatial-reflection law:")
    if parity_odd_error < APPROX_TOL:
        print("C_ref approximately equals -C")
    elif parity_even_error < APPROX_TOL:
        print("C_ref approximately equals C")
    elif basis_odd_error < APPROX_TOL:
        print("C_ref approximately equals -P C P^T")
    elif basis_even_error < APPROX_TOL:
        print("C_ref approximately equals P C P^T")
    else:
        print("NOT ESTABLISHED BY TESTED RELATIONS")

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    return True


if __name__ == "__main__":
    raise SystemExit(
        0 if main() else 1
    )
