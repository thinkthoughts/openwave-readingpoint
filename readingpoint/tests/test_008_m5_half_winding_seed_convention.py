# readingpoint/tests/test_008_m5_half_winding_seed_convention.py

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

from m5_17_energy import grid_coords  # noqa: E402
from m5_20_1_b_seeds import (  # noqa: E402
    H,
    NR,
    NZ,
    winding_measure_biax,
)


R0 = 17.0
Q_MAG = 0.5
RADII = (3.0, 4.0, 5.0, 6.0)

# Keep the wound-plane eigenvalues distinct so the eigenframe is readable.
LAMBDA_P = 1.0
LAMBDA_M = 0.3

TOL = 0.05
MIX_TOL = 0.05


def director_components(chi, q, convention):
    """
    Return (n1, n3) for one of three controlled half-winding conventions.

    current:
        Reproduce OpenWave winding_director() behavior:
        +0.5 gets the special cos/sin branch.
        -0.5 gets the generic sin/cos branch.

    generic:
        Use sin(q*chi), cos(q*chi) for both signs.

    symmetric:
        Use cos(q*chi), sin(q*chi) for both signs.
    """

    if convention == "current":
        if abs(q - 0.5) < 1e-12:
            n1 = np.cos(0.5 * chi)
            n3 = np.sin(0.5 * chi)
        else:
            n1 = np.sin(q * chi)
            n3 = np.cos(q * chi)

    elif convention == "generic":
        n1 = np.sin(q * chi)
        n3 = np.cos(q * chi)

    elif convention == "symmetric":
        n1 = np.cos(q * chi)
        n3 = np.sin(q * chi)

    else:
        raise ValueError(f"Unknown convention: {convention}")

    norm = np.sqrt(n1**2 + n3**2)
    norm = np.where(norm < 1e-12, 1.0, norm)

    return n1 / norm, n3 / norm


def build_synthetic_tensor(q, convention):
    """
    Construct a simple biaxial/apolar tensor field on the M5 grid.

    The spatial (1,3) plane carries the winding director.
    The orthogonal eigenvector p is perpendicular to n.

    M = lambda_p n n^T + lambda_m p p^T

    This isolates angular convention from the radial/core details of the
    production seed while preserving the same quadratic apolar structure
    read by winding_measure_biax().
    """

    R, Z = grid_coords(NR, NZ, H)

    chi = np.arctan2(Z, R - R0)

    n1, n3 = director_components(
        chi,
        q,
        convention,
    )

    p1 = -n3
    p3 = n1

    M = np.zeros(R.shape + (4, 4), dtype=float)

    M[..., 1, 1] = (
        LAMBDA_P * n1 * n1
        + LAMBDA_M * p1 * p1
    )

    M[..., 3, 3] = (
        LAMBDA_P * n3 * n3
        + LAMBDA_M * p3 * p3
    )

    m13 = (
        LAMBDA_P * n1 * n3
        + LAMBDA_M * p1 * p3
    )

    M[..., 1, 3] = m13
    M[..., 3, 1] = m13

    # Out-of-plane axis stays unmixed.
    M[..., 2, 2] = 0.0

    return M


def measure(q, convention):
    M = build_synthetic_tensor(
        q,
        convention,
    )

    reads = {}

    for radius in RADII:
        q_meas, mix = winding_measure_biax(
            M,
            NR,
            NZ,
            H,
            R0,
            0.0,
            r_w=radius,
        )

        reads[radius] = {
            "q": float(q_meas),
            "mix": float(mix),
        }

    return reads


def classify_pair(qp, qn):
    if not (
        np.isfinite(qp)
        and np.isfinite(qn)
    ):
        return "UNREADABLE"

    if abs(qp - qn) <= TOL:
        return "SIGN_IDENTIFIED"

    if abs(qp + qn) <= TOL:
        return "SIGN_DISTINGUISHED"

    return "OTHER"


def test_all_conventions_are_readable():
    for convention in (
        "current",
        "generic",
        "symmetric",
    ):
        for q in (+Q_MAG, -Q_MAG):
            reads = measure(q, convention)

            for item in reads.values():
                assert np.isfinite(item["q"])
                assert np.isfinite(item["mix"])
                assert item["mix"] < MIX_TOL


def test_all_half_winding_tensors_are_closed():
    """
    Every convention here uses q = +/- 1/2, so the apolar tensor should
    close after one complete circuit even if the oriented director flips.
    """

    chi0 = 0.0
    chi2 = 2.0 * np.pi

    for convention in (
        "current",
        "generic",
        "symmetric",
    ):
        for q in (+Q_MAG, -Q_MAG):
            n10, n30 = director_components(
                chi0,
                q,
                convention,
            )
            n12, n32 = director_components(
                chi2,
                q,
                convention,
            )

            n0 = np.array([n10, n30])
            n2 = np.array([n12, n32])

            M0 = np.outer(n0, n0)
            M2 = np.outer(n2, n2)

            assert np.max(np.abs(M2 - M0)) < 1e-12


if __name__ == "__main__":
    test_all_conventions_are_readable()
    test_all_half_winding_tensors_are_closed()

    print("Reading Point Test 008")
    print("----------------------")
    print()
    print("M5 half-winding seed-convention control")
    print()

    summary = {}

    for convention in (
        "current",
        "generic",
        "symmetric",
    ):
        positive = measure(
            +Q_MAG,
            convention,
        )

        negative = measure(
            -Q_MAG,
            convention,
        )

        print(f"convention={convention}")

        classifications = []

        for radius in RADII:
            qp = positive[radius]["q"]
            qn = negative[radius]["q"]

            mixp = positive[radius]["mix"]
            mixn = negative[radius]["mix"]

            classification = classify_pair(
                qp,
                qn,
            )

            classifications.append(
                classification
            )

            print(
                f"  r={radius:.1f}"
                f"  q(+0.5)={qp:+.4f}"
                f"  q(-0.5)={qn:+.4f}"
                f"  mix+={mixp:.4f}"
                f"  mix-={mixn:.4f}"
                f"  {classification}"
            )

        unique = sorted(
            set(classifications)
        )

        summary[convention] = unique

        print(
            "  behavior:",
            ", ".join(unique),
        )
        print()

    print("Summary")
    print("-------")

    for convention, behavior in summary.items():
        print(
            f"{convention:10s}: "
            + ", ".join(behavior)
        )

    print()
    print("Interpretation rule:")
    print(
        "If sign identification persists under both symmetric control "
        "conventions, the Result 005 behavior is not explained solely "
        "by OpenWave's +0.5 special-case branch."
    )
    print(
        "If the behavior changes with convention, the half-winding "
        "readout is seed-convention dependent and Result 005 must be "
        "qualified accordingly."
    )
    print()
    print("Physical Q8/{1,-1} identification:")
    print("NOT ASSUMED")
