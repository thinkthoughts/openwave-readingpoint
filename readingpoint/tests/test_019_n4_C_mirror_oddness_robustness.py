#!/usr/bin/env python3
"""
Reading Point Test 019 — N4 C mirror-oddness robustness.

Result 018 established, for one controlled geometry:

  - exact mu/tau basis covariance:
        C_mirror = P C P^T

  - approximate mirror sign reversal:
        P C P^T ~ -C

  - approximate invariance under screw reversal:
        C(-chi) ~ C(+chi)

Result 019 asks whether those latter two approximate behaviors persist
across a broader geometry family.

The test varies:

    alpha = 0.4, 0.6, 0.8
    delta = 0.05, 0.1, 0.2
    chi   = 0.3, 0.6, 1.0

while holding:

    n        = 40
    dx       = 1
    R_loop   = 9
    core_vox = 2
    q        = 0.5

For each geometry the test measures separately:

  1. basis covariance:
         ||C_mirror - P C P^T|| / ||C||

  2. mirror oddness:
         ||P C P^T + C|| / ||C||

  3. screw-sign evenness:
         ||C(-chi) - C(+chi)|| / ||C(+chi)||

  4. antisymmetry

  5. magnitude stability under chi -> -chi

The test does not assume that basis covariance implies physical mirror
oddness, and it does not assume chi -> -chi is the physical handedness
operation.

No Reading Point residue mapping is introduced.
"""

from pathlib import Path
import itertools
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
# Controlled family
# ----------------------------------------------------------------------

N = 40
DX = 1.0

ALPHAS = (0.4, 0.6, 0.8)
DELTAS = (0.05, 0.1, 0.2)
CHIS = (0.3, 0.6, 1.0)

Q = 0.5
R_LOOP = 9.0
CORE_VOX = 2.0

ANTISYM_TOL = 1e-10

# Characterization thresholds.
# These are used only to classify the observed numerical behavior.
EXACT_COV_TOL = 1e-12
APPROX_ODD_TOL = 1e-3
APPROX_EVEN_TOL = 1e-3
MAG_TOL = 1e-3


def mu_tau_swap_matrix():
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )


def frobenius_norm(M):
    return float(np.linalg.norm(M))


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


def chiral_matrix(dfields):
    C = np.zeros((3, 3), dtype=float)

    for a in range(3):
        for b in range(3):
            C[a, b] = chiral_overlap(
                dfields[a],
                dfields[b],
            )

    return C


def build_displacements(
    *,
    alpha,
    delta,
    chi,
    mirrored_order=False,
):
    """
    Build the N4 three-loop flavour displacement family.

    Standard ordering:
        mu  = +alpha
        tau = -alpha

    Mirrored ordering:
        mu  = -alpha
        tau = +alpha
    """

    Re = np.eye(3)

    if mirrored_order:
        Rmu = rot_axis(
            (1.0, 0.0, 0.0),
            -alpha,
        )

        Rtau = rot_axis(
            (1.0, 0.0, 0.0),
            +alpha,
        )
    else:
        Rmu = rot_axis(
            (1.0, 0.0, 0.0),
            +alpha,
        )

        Rtau = rot_axis(
            (1.0, 0.0, 0.0),
            -alpha,
        )

    Mvac = biaxial_vacuum(
        N,
        delta,
    )

    fe = seed_loop_biaxial(
        N,
        Re,
        R_LOOP,
        delta,
        q=Q,
        core_vox=CORE_VOX,
        chi=0.0,
    )

    fmu = seed_loop_biaxial(
        N,
        Rmu,
        R_LOOP,
        delta,
        q=Q,
        core_vox=CORE_VOX,
        chi=chi,
    )

    ftau = seed_loop_biaxial(
        N,
        Rtau,
        R_LOOP,
        delta,
        q=Q,
        core_vox=CORE_VOX,
        chi=chi,
    )

    return [
        fe - Mvac,
        fmu - Mvac,
        ftau - Mvac,
    ]


def evaluate_C(
    *,
    alpha,
    delta,
    chi,
    mirrored_order=False,
):
    dfields = build_displacements(
        alpha=alpha,
        delta=delta,
        chi=chi,
        mirrored_order=mirrored_order,
    )

    C = chiral_matrix(
        dfields
    )

    return {
        "C": C,
        "norm": frobenius_norm(DX * C),
        "antisymmetry_error": antisymmetry_error(C),
    }


def evaluate_geometry(
    *,
    alpha,
    delta,
    chi,
):
    """
    Evaluate one (alpha, delta, |chi|) point.

    A: standard ordering, +chi
    B: standard ordering, -chi
    C: mirrored ordering, +chi
    D: mirrored ordering, -chi
    """

    A = evaluate_C(
        alpha=alpha,
        delta=delta,
        chi=+chi,
        mirrored_order=False,
    )

    B = evaluate_C(
        alpha=alpha,
        delta=delta,
        chi=-chi,
        mirrored_order=False,
    )

    C = evaluate_C(
        alpha=alpha,
        delta=delta,
        chi=+chi,
        mirrored_order=True,
    )

    D = evaluate_C(
        alpha=alpha,
        delta=delta,
        chi=-chi,
        mirrored_order=True,
    )

    P = mu_tau_swap_matrix()

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

    basis_cov_plus = relative_matrix_error(
        C["C"],
        expected_C,
    )

    basis_cov_minus = relative_matrix_error(
        D["C"],
        expected_D,
    )

    mirror_odd_plus = relative_matrix_error(
        expected_C,
        -A["C"],
    )

    mirror_odd_minus = relative_matrix_error(
        expected_D,
        -B["C"],
    )

    chi_even_error = relative_matrix_error(
        B["C"],
        A["C"],
    )

    chi_odd_error = relative_matrix_error(
        B["C"],
        -A["C"],
    )

    chi_norm_error = relative_scalar_error(
        B["norm"],
        A["norm"],
    )

    anti_err = max(
        A["antisymmetry_error"],
        B["antisymmetry_error"],
        C["antisymmetry_error"],
        D["antisymmetry_error"],
    )

    return {
        "alpha": alpha,
        "delta": delta,
        "chi": chi,

        "basis_cov_plus": basis_cov_plus,
        "basis_cov_minus": basis_cov_minus,

        "mirror_odd_plus": mirror_odd_plus,
        "mirror_odd_minus": mirror_odd_minus,

        "chi_even_error": chi_even_error,
        "chi_odd_error": chi_odd_error,
        "chi_norm_error": chi_norm_error,

        "antisymmetry_error": anti_err,

        "norm_plus": A["norm"],
        "norm_minus": B["norm"],
    }


def all_rows():
    rows = []

    for alpha, delta, chi in itertools.product(
        ALPHAS,
        DELTAS,
        CHIS,
    ):
        rows.append(
            evaluate_geometry(
                alpha=alpha,
                delta=delta,
                chi=chi,
            )
        )

    return rows


# ----------------------------------------------------------------------
# Structural tests
# ----------------------------------------------------------------------

def test_all_cases_are_finite():
    for row in all_rows():
        vals = [
            row["basis_cov_plus"],
            row["basis_cov_minus"],
            row["mirror_odd_plus"],
            row["mirror_odd_minus"],
            row["chi_even_error"],
            row["chi_odd_error"],
            row["chi_norm_error"],
            row["antisymmetry_error"],
            row["norm_plus"],
            row["norm_minus"],
        ]

        assert np.all(
            np.isfinite(vals)
        )


def test_all_cases_nonzero():
    for row in all_rows():
        assert row["norm_plus"] > 1e-8
        assert row["norm_minus"] > 1e-8


def test_all_cases_antisymmetric():
    for row in all_rows():
        assert (
            row["antisymmetry_error"]
            < ANTISYM_TOL
        )


def test_basis_covariance_exact():
    """
    This is the structural relabeling control and is expected to hold
    independently of the approximate mirror-oddness question.
    """

    for row in all_rows():
        assert (
            row["basis_cov_plus"]
            < EXACT_COV_TOL
        )

        assert (
            row["basis_cov_minus"]
            < EXACT_COV_TOL
        )


def run_all():
    test_all_cases_are_finite()
    test_all_cases_nonzero()
    test_all_cases_antisymmetric()
    test_basis_covariance_exact()


# ----------------------------------------------------------------------
# Summary helpers
# ----------------------------------------------------------------------

def summarize(values):
    arr = np.asarray(
        values,
        dtype=float,
    )

    return {
        "min": float(np.min(arr)),
        "median": float(np.median(arr)),
        "max": float(np.max(arr)),
        "mean": float(np.mean(arr)),
    }


def count_below(values, threshold):
    return sum(
        value < threshold
        for value in values
    )


def classify_fraction(
    count,
    total,
):
    frac = count / total

    if frac == 1.0:
        return "ROBUST ACROSS TESTED FAMILY"

    if frac >= 0.8:
        return "MOSTLY SUPPORTED / GEOMETRY DEPENDENT"

    if frac > 0.0:
        return "GEOMETRY DEPENDENT"

    return "NOT SUPPORTED"


def main():
    run_all()

    rows = all_rows()
    total = len(rows)

    mirror_odd_errors = [
        max(
            r["mirror_odd_plus"],
            r["mirror_odd_minus"],
        )
        for r in rows
    ]

    chi_even_errors = [
        r["chi_even_error"]
        for r in rows
    ]

    chi_odd_errors = [
        r["chi_odd_error"]
        for r in rows
    ]

    chi_norm_errors = [
        r["chi_norm_error"]
        for r in rows
    ]

    basis_cov_errors = [
        max(
            r["basis_cov_plus"],
            r["basis_cov_minus"],
        )
        for r in rows
    ]

    anti_errors = [
        r["antisymmetry_error"]
        for r in rows
    ]

    mirror_odd_count = count_below(
        mirror_odd_errors,
        APPROX_ODD_TOL,
    )

    chi_even_count = count_below(
        chi_even_errors,
        APPROX_EVEN_TOL,
    )

    chi_norm_count = count_below(
        chi_norm_errors,
        MAG_TOL,
    )

    mirror_summary = summarize(
        mirror_odd_errors
    )

    chi_even_summary = summarize(
        chi_even_errors
    )

    chi_odd_summary = summarize(
        chi_odd_errors
    )

    chi_norm_summary = summarize(
        chi_norm_errors
    )

    basis_summary = summarize(
        basis_cov_errors
    )

    anti_summary = summarize(
        anti_errors
    )

    print("Reading Point Test 019")
    print("----------------------")
    print()

    print("N4 C mirror-oddness robustness")
    print()

    print(
        f"n={N}"
        f"  dx={DX}"
        f"  R_loop={R_LOOP}"
        f"  core_vox={CORE_VOX}"
        f"  q={Q}"
    )

    print()
    print("Parameter family:")
    print(
        "alpha = "
        + ", ".join(
            f"{x:.2f}"
            for x in ALPHAS
        )
    )

    print(
        "delta = "
        + ", ".join(
            f"{x:.2f}"
            for x in DELTAS
        )
    )

    print(
        "chi = "
        + ", ".join(
            f"{x:.2f}"
            for x in CHIS
        )
    )

    print()
    print(
        f"tested geometry points: {total}"
    )

    print()
    print("Per-geometry diagnostics:")
    print()

    for row in rows:
        print(
            f"alpha={row['alpha']:.2f}"
            f"  delta={row['delta']:.2f}"
            f"  chi={row['chi']:.2f}"
            f"  cov={max(row['basis_cov_plus'], row['basis_cov_minus']):.3e}"
            f"  mirror_odd={max(row['mirror_odd_plus'], row['mirror_odd_minus']):.3e}"
            f"  chi_even={row['chi_even_error']:.3e}"
            f"  chi_odd={row['chi_odd_error']:.3e}"
            f"  chi_mag={row['chi_norm_error']:.3e}"
            f"  anti={row['antisymmetry_error']:.3e}"
        )

    print()
    print("Basis covariance:")
    print(
        "max error = "
        f"{basis_summary['max']:.6e}"
    )

    print()
    print("Mirror oddness:")
    print(
        f"threshold = {APPROX_ODD_TOL:.1e}"
    )
    print(
        f"supported points = "
        f"{mirror_odd_count}/{total}"
    )
    print(
        "min / median / max error = "
        f"{mirror_summary['min']:.6e} / "
        f"{mirror_summary['median']:.6e} / "
        f"{mirror_summary['max']:.6e}"
    )

    print()
    print("chi -> -chi approximate invariance:")
    print(
        f"threshold = {APPROX_EVEN_TOL:.1e}"
    )
    print(
        f"supported points = "
        f"{chi_even_count}/{total}"
    )
    print(
        "min / median / max error = "
        f"{chi_even_summary['min']:.6e} / "
        f"{chi_even_summary['median']:.6e} / "
        f"{chi_even_summary['max']:.6e}"
    )

    print()
    print("chi -> -chi oddness diagnostic:")
    print(
        "min / median / max error = "
        f"{chi_odd_summary['min']:.6e} / "
        f"{chi_odd_summary['median']:.6e} / "
        f"{chi_odd_summary['max']:.6e}"
    )

    print()
    print("chi reversal magnitude preservation:")
    print(
        f"threshold = {MAG_TOL:.1e}"
    )
    print(
        f"supported points = "
        f"{chi_norm_count}/{total}"
    )
    print(
        "min / median / max relative difference = "
        f"{chi_norm_summary['min']:.6e} / "
        f"{chi_norm_summary['median']:.6e} / "
        f"{chi_norm_summary['max']:.6e}"
    )

    print()
    print("Antisymmetry:")
    print(
        "max error = "
        f"{anti_summary['max']:.6e}"
    )
    print("PASS")

    print()
    print("Basis covariance across geometry:")
    print("SUPPORTED")

    print()
    print("Mirror oddness across geometry:")
    print(
        classify_fraction(
            mirror_odd_count,
            total,
        )
    )

    print()
    print("chi -> -chi approximate invariance:")
    print(
        classify_fraction(
            chi_even_count,
            total,
        )
    )

    print()
    print("chi reversal magnitude preservation:")
    print(
        classify_fraction(
            chi_norm_count,
            total,
        )
    )

    print()
    print("Interpretation:")
    print(
        "Exact mu-tau basis covariance is tested separately from "
        "the approximate mirror-odd relation P C P^T ~ -C."
    )
    print(
        "This determines whether the sign reversal observed in "
        "Result 018 is robust across geometry or only a special "
        "property of the original parameter point."
    )
    print(
        "The same family also tests whether C remains approximately "
        "even under chi -> -chi."
    )
    print(
        "No physical handedness identification is imposed by this test."
    )

    print()
    print("Physical handedness identification:")
    print("NOT YET ESTABLISHED")

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    return True


if __name__ == "__main__":
    raise SystemExit(
        0 if main() else 1
    )
