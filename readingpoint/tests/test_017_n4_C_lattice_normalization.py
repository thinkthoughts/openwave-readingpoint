#!/usr/bin/env python3
"""
Reading Point Test 017 — N4 C lattice normalization.

Result 016 found:

    - the normalized operator shape C / ||C||_F converges under refinement;
    - the raw magnitude ||C||_F grows with resolution.

This test asks whether that raw scaling is explained by the lattice
normalization already implicit in chiral_overlap().

N4 currently computes:

    C_ab ~ sum_voxels [
        <d_x A, d_y B>_s - <d_y A, d_x B>_s + cyclic terms
    ]

where _grads() defaults to dx=1.

For a fixed physical geometry sampled with physical lattice spacing h:

    coded gradient ~ h * physical gradient
    product of two coded gradients ~ h^2
    voxel sum ~ h^-3 * physical integral

so the raw coded overlap is expected to scale as:

    C_raw ~ h^-1

if it approximates a continuum gradient-gradient volume integral.

Therefore the candidate physical normalization is:

    C_h = h * C_raw.

This test measures that claim.

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
# Fixed physical geometry
# ----------------------------------------------------------------------

RESOLUTIONS = (24, 32, 40, 48)

REFERENCE_N = 40
REFERENCE_DX = 1.0

R_LOOP_PHYS = 9.0
CORE_PHYS = 2.0

ALPHA = 0.6
DELTA = 0.1
CHI = 0.6
Q = 0.5

ANTISYM_TOL = 1e-10


def physical_dx(n):
    """
    Hold the physical box size fixed.

    At the reference n=40 lattice, dx=1.
    """
    return REFERENCE_DX * REFERENCE_N / n


def geometry_for_n(n):
    """
    Convert fixed physical loop geometry to voxel coordinates expected by
    the current N4 seed implementation.
    """
    dx = physical_dx(n)

    return {
        "dx": dx,
        "R_loop_vox": R_LOOP_PHYS / dx,
        "core_vox": CORE_PHYS / dx,
    }


def build_displacements(n):
    geom = geometry_for_n(n)

    Re = np.eye(3)
    Rmu = rot_axis((1.0, 0.0, 0.0), +ALPHA)
    Rtau = rot_axis((1.0, 0.0, 0.0), -ALPHA)

    Mvac = biaxial_vacuum(n, DELTA)

    fe = seed_loop_biaxial(
        n,
        Re,
        geom["R_loop_vox"],
        DELTA,
        q=Q,
        core_vox=geom["core_vox"],
        chi=0.0,
    )

    fmu = seed_loop_biaxial(
        n,
        Rmu,
        geom["R_loop_vox"],
        DELTA,
        q=Q,
        core_vox=geom["core_vox"],
        chi=CHI,
    )

    ftau = seed_loop_biaxial(
        n,
        Rtau,
        geom["R_loop_vox"],
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


def antisymmetry_error(C):
    scale = max(
        float(np.max(np.abs(C))),
        1.0,
    )

    return float(
        np.max(np.abs(C + C.T))
        / scale
    )


def normalized_shape(C):
    norm = frobenius_norm(C)

    if norm <= 1e-30:
        raise ValueError("zero C norm")

    return C / norm


def evaluate(n):
    geom = geometry_for_n(n)

    dfields = build_displacements(n)
    C_raw = chiral_matrix(dfields)

    dx = geom["dx"]

    return {
        "n": n,
        "dx": dx,
        "R_loop_vox": geom["R_loop_vox"],
        "core_vox": geom["core_vox"],
        "C_raw": C_raw,
        "raw_norm": frobenius_norm(C_raw),
        "C_dx": dx * C_raw,
        "dx_norm": frobenius_norm(dx * C_raw),
        "C_dx2": dx**2 * C_raw,
        "dx2_norm": frobenius_norm(dx**2 * C_raw),
        "C_dx3": dx**3 * C_raw,
        "dx3_norm": frobenius_norm(dx**3 * C_raw),
        "shape": normalized_shape(C_raw),
        "antisymmetry_error": antisymmetry_error(C_raw),
    }


def relative_spread(values):
    values = np.asarray(values, dtype=float)

    mean = float(np.mean(values))

    if abs(mean) < 1e-30:
        return float("inf")

    return float(
        (np.max(values) - np.min(values))
        / abs(mean)
    )


def consecutive_relative_changes(values):
    out = []

    for a, b in zip(values[:-1], values[1:]):
        out.append(
            abs(b - a)
            / max(abs(b), 1e-30)
        )

    return out


def fit_raw_dx_exponent(rows):
    """
    Fit

        ||C_raw|| ~ dx^p

    A continuum gradient-gradient integral coded with dx=1 predicts
    approximately p = -1.
    """
    dxs = np.array(
        [r["dx"] for r in rows],
        dtype=float,
    )

    norms = np.array(
        [r["raw_norm"] for r in rows],
        dtype=float,
    )

    p, intercept = np.polyfit(
        np.log(dxs),
        np.log(norms),
        1,
    )

    return float(p), float(intercept)


def best_candidate_power(rows):
    """
    Compare candidate normalizations dx^p * C for p=0,1,2,3.

    Choose by relative spread of the Frobenius norm.
    """
    candidates = {}

    for p in (0, 1, 2, 3):
        vals = [
            (r["dx"] ** p) * r["raw_norm"]
            for r in rows
        ]

        candidates[p] = {
            "values": vals,
            "spread": relative_spread(vals),
        }

    best = min(
        candidates,
        key=lambda p: candidates[p]["spread"],
    )

    return best, candidates


def test_fixed_physical_geometry():
    for n in RESOLUTIONS:
        geom = geometry_for_n(n)

        assert abs(
            geom["R_loop_vox"] * geom["dx"]
            - R_LOOP_PHYS
        ) < 1e-12

        assert abs(
            geom["core_vox"] * geom["dx"]
            - CORE_PHYS
        ) < 1e-12


def test_all_C_are_finite_nonzero_and_antisymmetric():
    for n in RESOLUTIONS:
        row = evaluate(n)

        assert np.all(np.isfinite(row["C_raw"]))
        assert row["raw_norm"] > 1e-8
        assert row["antisymmetry_error"] < ANTISYM_TOL


def run_all():
    test_fixed_physical_geometry()
    test_all_C_are_finite_nonzero_and_antisymmetric()


def main():
    run_all()

    rows = [
        evaluate(n)
        for n in RESOLUTIONS
    ]

    raw_dx_exponent, _ = fit_raw_dx_exponent(rows)
    best_p, candidates = best_candidate_power(rows)

    print("Reading Point Test 017")
    print("----------------------")
    print()

    print("N4 chiral-overlap lattice normalization")
    print()

    print("Fixed physical geometry:")
    print(f"R_loop = {R_LOOP_PHYS}")
    print(f"core    = {CORE_PHYS}")
    print()

    print(
        f"alpha={ALPHA}"
        f"  delta={DELTA}"
        f"  chi={CHI}"
        f"  q={Q}"
    )

    print()
    print("Resolution / lattice-spacing sweep:")
    print()

    for row in rows:
        print(
            f"n={row['n']:>2d}"
            f"  dx={row['dx']:.6f}"
            f"  R_vox={row['R_loop_vox']:.3f}"
            f"  core_vox={row['core_vox']:.3f}"
            f"  ||C||={row['raw_norm']:.6e}"
            f"  ||dx*C||={row['dx_norm']:.6e}"
        )

    print()
    print("Raw scaling fit:")
    print(
        f"||C_raw|| ~ dx^{raw_dx_exponent:.4f}"
    )

    print()
    print("Continuum counting prediction:")
    print("C_raw ~ dx^-1")

    print()
    print("Candidate normalization spreads:")
    print()

    for p in (0, 1, 2, 3):
        vals = candidates[p]["values"]

        print(
            f"dx^{p} * ||C||"
            f"  spread={candidates[p]['spread']:.6e}"
            f"  values="
            + ", ".join(f"{v:.6e}" for v in vals)
        )

    print()
    print("Best tested power:")
    print(f"p = {best_p}")

    dx_values = [
        row["dx_norm"]
        for row in rows
    ]

    dx_changes = consecutive_relative_changes(
        dx_values
    )

    print()
    print("Successive changes in ||dx*C||:")
    print()

    for left, right, change in zip(
        RESOLUTIONS[:-1],
        RESOLUTIONS[1:],
        dx_changes,
    ):
        print(
            f"n={left} -> n={right}: "
            f"{change:.6e}"
        )

    print()
    print("Antisymmetry across refinement:")
    print("PASS")

    print()
    print("Candidate physical lattice normalization:")
    if best_p == 1:
        print("dx * C")
    else:
        print(f"dx^{best_p} * C")

    print()
    print("Normalization verdict:")
    if best_p == 1:
        print("dx * C SUPPORTED AMONG TESTED INTEGER POWERS")
    else:
        print(
            "dx * C NOT BEST AMONG TESTED INTEGER POWERS"
        )

    print()
    print("Interpretation:")
    print(
        "The current chiral_overlap uses two coded central-difference "
        "gradients with dx=1 and then directly sums lattice cells."
    )
    print(
        "For fixed physical geometry, continuum counting predicts that "
        "the raw matrix should scale approximately as dx^-1."
    )
    print(
        "This test measures the raw scaling and compares explicit "
        "dx^p normalizations rather than assuming the continuum factor."
    )
    print(
        "A stable dx*C magnitude would provide the missing lattice "
        "normalization for treating C as a continuum effective operator."
    )

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
