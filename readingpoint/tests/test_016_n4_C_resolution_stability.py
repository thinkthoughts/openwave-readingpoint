#!/usr/bin/env python3
"""
Reading Point Test 016 — N4 C resolution stability.

Question:

    Does the dimensionless antisymmetric structure of the existing N4
    chiral-overlap matrix C persist under lattice refinement?

This test intentionally separates:

    1. operator shape:
           C_hat = C / ||C||_F

    2. raw normalization:
           ||C||_F

The physical/dimensionless loop geometry is held fixed relative to the
grid size:

    R_loop / n   = 9 / 40
    core_vox / n = 2 / 40

while refining

    n = 24, 32, 40, 48.

Other parameters are fixed:

    alpha = 0.6
    delta = 0.1
    chi   = 0.6
    q     = 0.5

No Reading Point residue mapping is introduced.

This is a characterization test. It asserts only the exact structural
properties expected of C (finite, nonzero, antisymmetric) and measures
resolution convergence without forcing a preselected convergence verdict.
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
# Controlled refinement family
# ----------------------------------------------------------------------

RESOLUTIONS = (24, 32, 40, 48)

REFERENCE_N = 40
REFERENCE_R_LOOP = 9.0
REFERENCE_CORE_VOX = 2.0

R_LOOP_OVER_N = REFERENCE_R_LOOP / REFERENCE_N
CORE_OVER_N = REFERENCE_CORE_VOX / REFERENCE_N

ALPHA = 0.6
DELTA = 0.1
CHI = 0.6
Q = 0.5

ANTISYM_TOL = 1e-10


def geometry_for_n(n):
    """
    Scale loop radius and core width with n so their ratios to the
    computational grid remain fixed.
    """
    return {
        "R_loop": R_LOOP_OVER_N * n,
        "core_vox": CORE_OVER_N * n,
    }


def build_displacements(n):
    """
    Build the same three N4-style flavour-loop displacement fields at
    one resolution.

    e   : reference orientation, chi = 0
    mu  : +alpha orientation, chi = +CHI
    tau : -alpha orientation, chi = +CHI
    """

    geom = geometry_for_n(n)

    Re = np.eye(3)
    Rmu = rot_axis((1.0, 0.0, 0.0), +ALPHA)
    Rtau = rot_axis((1.0, 0.0, 0.0), -ALPHA)

    Mvac = biaxial_vacuum(n, DELTA)

    fe = seed_loop_biaxial(
        n,
        Re,
        geom["R_loop"],
        DELTA,
        q=Q,
        core_vox=geom["core_vox"],
        chi=0.0,
    )

    fmu = seed_loop_biaxial(
        n,
        Rmu,
        geom["R_loop"],
        DELTA,
        q=Q,
        core_vox=geom["core_vox"],
        chi=CHI,
    )

    ftau = seed_loop_biaxial(
        n,
        Rtau,
        geom["R_loop"],
        DELTA,
        q=Q,
        core_vox=geom["core_vox"],
        chi=CHI,
    )

    return [
        fe - Mvac,
        fmu - Mvac,
        ftau - Mvac,
    ]


def chiral_matrix(dfields):
    """
    Evaluate the existing N4 chiral_overlap on every ordered pair.

    We do not impose antisymmetry by hand; the test measures it directly.
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
    return float(np.linalg.norm(M))


def normalized_operator(C):
    norm = frobenius_norm(C)

    if not np.isfinite(norm) or norm <= 1e-30:
        raise ValueError("C has zero or non-finite Frobenius norm")

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


def shape_distance(A_hat, B_hat):
    """
    Frobenius distance between two unit-normalized operators.

    0 means identical normalized matrices.
    """
    return float(
        np.linalg.norm(A_hat - B_hat)
    )


def evaluate_resolution(n):
    geom = geometry_for_n(n)

    dfields = build_displacements(n)
    C = chiral_matrix(dfields)

    norm = frobenius_norm(C)
    C_hat = normalized_operator(C)

    return {
        "n": n,
        "R_loop": geom["R_loop"],
        "core_vox": geom["core_vox"],
        "C": C,
        "C_norm": norm,
        "C_hat": C_hat,
        "antisymmetry_error": antisymmetry_error(C),
    }


def fit_raw_norm_scaling(rows):
    """
    Fit

        ||C||_F ~ n^p

    as a diagnostic only.

    Result 013 already established that N4 C has no explicit dx^3
    normalization, so raw magnitude scaling is expected to require
    separate interpretation.
    """

    ns = np.array(
        [r["n"] for r in rows],
        dtype=float,
    )

    norms = np.array(
        [r["C_norm"] for r in rows],
        dtype=float,
    )

    coeff = np.polyfit(
        np.log(ns),
        np.log(norms),
        1,
    )

    return float(coeff[0])


# ----------------------------------------------------------------------
# Structural tests
# ----------------------------------------------------------------------

def test_all_resolution_matrices_are_finite():
    for n in RESOLUTIONS:
        row = evaluate_resolution(n)

        assert np.all(np.isfinite(row["C"]))


def test_all_resolution_matrices_are_nonzero():
    for n in RESOLUTIONS:
        row = evaluate_resolution(n)

        assert row["C_norm"] > 1e-8


def test_all_resolution_matrices_are_antisymmetric():
    for n in RESOLUTIONS:
        row = evaluate_resolution(n)

        assert row["antisymmetry_error"] < ANTISYM_TOL


def test_dimensionless_geometry_is_fixed():
    for n in RESOLUTIONS:
        geom = geometry_for_n(n)

        assert abs(
            geom["R_loop"] / n
            - R_LOOP_OVER_N
        ) < 1e-15

        assert abs(
            geom["core_vox"] / n
            - CORE_OVER_N
        ) < 1e-15


def run_all():
    test_all_resolution_matrices_are_finite()
    test_all_resolution_matrices_are_nonzero()
    test_all_resolution_matrices_are_antisymmetric()
    test_dimensionless_geometry_is_fixed()


def main():
    run_all()

    rows = [
        evaluate_resolution(n)
        for n in RESOLUTIONS
    ]

    finest = rows[-1]
    finest_hat = finest["C_hat"]

    print("Reading Point Test 016")
    print("----------------------")
    print()

    print("N4 chiral-overlap resolution stability")
    print()

    print("Fixed dimensionless geometry:")
    print(f"R_loop / n   = {R_LOOP_OVER_N:.6f}")
    print(f"core_vox / n = {CORE_OVER_N:.6f}")

    print()
    print(
        f"alpha={ALPHA}"
        f"  delta={DELTA}"
        f"  chi={CHI}"
        f"  q={Q}"
    )

    print()
    print("Resolution sweep:")
    print()

    for row in rows:
        dist = shape_distance(
            row["C_hat"],
            finest_hat,
        )

        print(
            f"n={row['n']:>2d}"
            f"  R_loop={row['R_loop']:.3f}"
            f"  core_vox={row['core_vox']:.3f}"
            f"  ||C||_F={row['C_norm']:.6e}"
            f"  anti_err={row['antisymmetry_error']:.3e}"
            f"  shape_dist_to_n{finest['n']}={dist:.6e}"
        )

    print()
    print("Raw C matrices:")
    print()

    for row in rows:
        print(f"n={row['n']}")
        print(
            np.array2string(
                row["C"],
                precision=6,
                suppress_small=True,
            )
        )
        print()

    print("Normalized C matrices:")
    print()

    for row in rows:
        print(f"n={row['n']}")
        print(
            np.array2string(
                row["C_hat"],
                precision=6,
                suppress_small=True,
            )
        )
        print()

    print("Pairwise normalized-operator changes:")
    print()

    pairwise = []

    for left, right in zip(rows[:-1], rows[1:]):
        dist = shape_distance(
            left["C_hat"],
            right["C_hat"],
        )

        pairwise.append(dist)

        print(
            f"n={left['n']} -> n={right['n']}: "
            f"{dist:.6e}"
        )

    raw_exponent = fit_raw_norm_scaling(rows)

    print()
    print("Raw norm scaling diagnostic:")
    print(
        f"||C||_F ~ n^{raw_exponent:.4f}"
    )

    print()
    print("Antisymmetry across refinement:")
    print("PASS")

    print()
    print("Normalized C convergence:")
    print("CHARACTERIZED")

    print()
    print("Raw C normalization:")
    print("CHARACTERIZED")

    print()
    print("Interpretation:")
    print(
        "The test separates the dimensionless shape of the N4 "
        "antisymmetric operator from its raw lattice normalization."
    )
    print(
        "Convergence of C_hat indicates whether the relative "
        "three-flavour chiral structure persists under refinement."
    )
    print(
        "Scaling of ||C||_F is recorded separately because the current "
        "N4 definition sums lattice contributions without an explicit "
        "physical volume normalization."
    )
    print(
        "No normalization law is imposed by this test."
    )

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
