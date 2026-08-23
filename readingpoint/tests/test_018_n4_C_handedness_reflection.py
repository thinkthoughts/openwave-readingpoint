#!/usr/bin/env python3
"""
Reading Point Test 018 — N4 C handedness / reflection behavior.

Results 016–017 established that the existing N4 chiral-overlap matrix C:

  - has a converging normalized operator shape under refinement;
  - admits the lattice normalization dx * C in the tested family.

Result 018 asks whether the operator transforms as a genuine chiral /
handedness-sensitive object.

Two controls are tested separately:

  1. screw reversal:
         chi -> -chi

  2. flavour-loop mirror ordering:
         (R_mu, R_tau) = (+alpha, -alpha)
         ->
         (-alpha, +alpha)

The test does NOT assume these two operations are physically identical.

For screw reversal we test whether:

    C(-chi) ~ -C(+chi)

while preserving:

    ||C||_F
    antisymmetry
    normalized operator shape after sign correction.

For mirror ordering we compare the resulting matrix against the permutation
transformation expected from swapping the mu and tau basis labels.

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
# Controlled geometry
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


def build_displacements(
    *,
    chi,
    mirrored_order=False,
):
    """
    Build the three N4 flavour-loop displacements.

    Standard order:
        e   = reference
        mu  = +alpha
        tau = -alpha

    mirrored_order:
        e   = reference
        mu  = -alpha
        tau = +alpha

    Both mu and tau use the same supplied screw handedness chi,
    matching the N4 construction.
    """

    Re = np.eye(3)

    if mirrored_order:
        Rmu = rot_axis(
            (1.0, 0.0, 0.0),
            -ALPHA,
        )
        Rtau = rot_axis(
            (1.0, 0.0, 0.0),
            +ALPHA,
        )
    else:
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
        chi=chi,
    )

    ftau = seed_loop_biaxial(
        N,
        Rtau,
        R_LOOP,
        DELTA,
        q=Q,
        core_vox=CORE_VOX,
        chi=chi,
    )

    return [
        fe - Mvac,
        fmu - Mvac,
        ftau - Mvac,
    ]


def chiral_matrix(dfields):
    """
    Evaluate the existing chiral_overlap on every ordered pair.

    Antisymmetry is measured rather than imposed.
    """

    C = np.zeros((3, 3), dtype=float)

    for a in range(3):
        for b in range(3):
            C[a, b] = chiral_overlap(
                dfields[a],
                dfields[b],
            )

    return C


def frobenius_norm(M):
    return float(
        np.linalg.norm(M)
    )


def normalized_operator(C):
    norm = frobenius_norm(C)

    if not np.isfinite(norm) or norm <= 1e-30:
        raise ValueError(
            "zero or non-finite C norm"
        )

    return C / norm


def antisymmetry_error(C):
    scale = max(
        float(np.max(np.abs(C))),
        1.0,
    )

    return float(
        np.max(np.abs(C + C.T))
        / scale
    )


def relative_matrix_error(A, B):
    """
    Relative Frobenius error ||A-B|| / ||B||.
    """

    den = max(
        frobenius_norm(B),
        1e-30,
    )

    return float(
        frobenius_norm(A - B)
        / den
    )


def mu_tau_swap_matrix():
    """
    Permutation matrix swapping flavour basis labels mu <-> tau.

    Basis:
        [e, mu, tau]
    """

    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )


def evaluate_case(
    name,
    *,
    chi,
    mirrored_order,
):
    dfields = build_displacements(
        chi=chi,
        mirrored_order=mirrored_order,
    )

    C = chiral_matrix(
        dfields
    )

    return {
        "name": name,
        "chi": chi,
        "mirrored_order": mirrored_order,
        "C": C,
        "C_norm": frobenius_norm(C),
        "C_eff": DX * C,
        "C_eff_norm": frobenius_norm(DX * C),
        "C_hat": normalized_operator(C),
        "antisymmetry_error": antisymmetry_error(C),
    }


# ----------------------------------------------------------------------
# Structural checks
# ----------------------------------------------------------------------

def test_all_cases_finite_nonzero_antisymmetric():
    cases = (
        ("A", +CHI, False),
        ("B", -CHI, False),
        ("C", +CHI, True),
        ("D", -CHI, True),
    )

    for name, chi, mirrored in cases:
        row = evaluate_case(
            name,
            chi=chi,
            mirrored_order=mirrored,
        )

        assert np.all(
            np.isfinite(row["C"])
        )

        assert row["C_norm"] > 1e-8

        assert (
            row["antisymmetry_error"]
            < ANTISYM_TOL
        )


def run_all():
    test_all_cases_finite_nonzero_antisymmetric()


def main():
    run_all()

    A = evaluate_case(
        "A",
        chi=+CHI,
        mirrored_order=False,
    )

    B = evaluate_case(
        "B",
        chi=-CHI,
        mirrored_order=False,
    )

    C = evaluate_case(
        "C",
        chi=+CHI,
        mirrored_order=True,
    )

    D = evaluate_case(
        "D",
        chi=-CHI,
        mirrored_order=True,
    )

    P = mu_tau_swap_matrix()

    # --------------------------------------------------------------
    # Screw reversal
    # --------------------------------------------------------------

    screw_sign_error = relative_matrix_error(
        B["C"],
        -A["C"],
    )

    screw_norm_ratio = (
        B["C_eff_norm"]
        / A["C_eff_norm"]
    )

    screw_shape_error = relative_matrix_error(
        B["C_hat"],
        -A["C_hat"],
    )

    # --------------------------------------------------------------
    # Mirror-order / basis-swap control
    # --------------------------------------------------------------

    expected_C = (
        P
        @ A["C"]
        @ P.T
    )

    expected_D = (
        P
        @ B["C"]
        @ P.T
    )

    mirror_error_plus = relative_matrix_error(
        C["C"],
        expected_C,
    )

    mirror_error_minus = relative_matrix_error(
        D["C"],
        expected_D,
    )

    # Does the mu<->tau swap also happen to produce -C?
    mirror_as_sign_error = relative_matrix_error(
        C["C"],
        -A["C"],
    )

    print("Reading Point Test 018")
    print("----------------------")
    print()

    print("N4 C handedness / reflection behavior")
    print()

    print(
        f"n={N}"
        f"  dx={DX}"
        f"  alpha={ALPHA}"
        f"  delta={DELTA}"
        f"  |chi|={CHI}"
        f"  q={Q}"
    )

    print()
    print("Cases:")
    print(
        "A = standard alpha ordering, chi=+0.6"
    )
    print(
        "B = standard alpha ordering, chi=-0.6"
    )
    print(
        "C = mirrored alpha ordering, chi=+0.6"
    )
    print(
        "D = mirrored alpha ordering, chi=-0.6"
    )

    print()
    print("Case matrices:")
    print()

    for row in (A, B, C, D):
        print(row["name"])
        print(
            np.array2string(
                row["C"],
                precision=6,
                suppress_small=True,
            )
        )
        print(
            f"||dx*C||_F="
            f"{row['C_eff_norm']:.6e}"
            f"  anti_err="
            f"{row['antisymmetry_error']:.3e}"
        )
        print()

    print("Screw reversal control:")
    print()

    print(
        "relative error in "
        "C(-chi) = -C(+chi):"
    )
    print(
        f"{screw_sign_error:.6e}"
    )

    print()
    print(
        "||dx*C(-chi)|| / "
        "||dx*C(+chi)||:"
    )
    print(
        f"{screw_norm_ratio:.12f}"
    )

    print()
    print(
        "normalized shape error after "
        "sign correction:"
    )
    print(
        f"{screw_shape_error:.6e}"
    )

    print()
    print("Mirror-order control:")
    print()

    print(
        "expected transformation:"
    )
    print(
        "C_mirror = P C P^T"
    )

    print()
    print(
        "relative error, chi=+:"
    )
    print(
        f"{mirror_error_plus:.6e}"
    )

    print()
    print(
        "relative error, chi=-:"
    )
    print(
        f"{mirror_error_minus:.6e}"
    )

    print()
    print(
        "mirror-as-simple-sign-flip error:"
    )
    print(
        f"{mirror_as_sign_error:.6e}"
    )

    print()
    print("Antisymmetry:")
    print("PASS")

    print()
    print("Interpretation:")
    print(
        "The screw-reversal control tests whether the "
        "existing N4 effective operator is odd under "
        "chi -> -chi."
    )
    print(
        "The mirror-order control is treated separately: "
        "swapping the +alpha and -alpha flavour-loop "
        "orientations should transform C by the corresponding "
        "mu<->tau basis permutation rather than being assumed "
        "to equal a simple sign flip."
    )
    print(
        "The run therefore distinguishes handedness reversal "
        "from flavour-basis relabeling."
    )

    print()
    print("Screw handedness oddness:")
    if screw_sign_error < 1e-8:
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED AS EXACT SIGN REVERSAL")

    print()
    print("Screw-reversal magnitude preservation:")
    if abs(
        screw_norm_ratio - 1.0
    ) < 1e-8:
        print("SUPPORTED")
    else:
        print("NOT EXACTLY PRESERVED")

    print()
    print("Mirror basis covariance:")
    if (
        mirror_error_plus < 1e-8
        and mirror_error_minus < 1e-8
    ):
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED")

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    return True


if __name__ == "__main__":
    raise SystemExit(
        0 if main() else 1
    )
