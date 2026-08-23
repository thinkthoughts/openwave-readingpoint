#!/usr/bin/env python3
"""
Reading Point Test 021 — N4 C composite reflection symmetry.

Result 020 established at one geometry:

    spatial reflection R_x:
        C_ref ~ C

and also:

        C_ref ~ -P C P^T

where P swaps the mu and tau flavour basis labels.

Equivalently, applying the flavour swap after spatial reflection suggests
the composite operation

    T = P o R_x

acts approximately as

    T(C) ~ -C.

Result 021 tests that composite operation directly and asks whether:

    1. T(C) ~ -C

    2. T^2(C) ~ C

    3. the composite preserves ||dx*C|| and antisymmetry

    4. these relations persist across a small geometry family.

The field-level operation is explicit:

    R_x:
        x -> -x
        M_sp(x) -> S M_sp(Sx) S^T
        S = diag(-1,+1,+1)

    P:
        [e, mu, tau] -> [e, tau, mu]

Since R_x acts on spatial fields and P acts on flavour labels, the two
operations commute. Both are involutions, so the exact field-level composite
should satisfy T^2 = identity.

The question is whether its induced action on the effective N4 chiral matrix
is the sign representation:

    T(C) ~ -C.

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
# Controlled geometry family
# ----------------------------------------------------------------------

N = 40
DX = 1.0

ALPHAS = (0.4, 0.6, 0.8)
DELTAS = (0.05, 0.1, 0.2)

CHI = 0.6
Q = 0.5

R_LOOP = 9.0
CORE_VOX = 2.0

ANTISYM_TOL = 1e-10
COMPOSITE_ODD_TOL = 1e-3
INVOLUTION_TOL = 1e-12
MAG_TOL = 1e-3


def reflection_matrix_x():
    return np.diag(
        [-1.0, 1.0, 1.0]
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


def build_displacements(
    *,
    alpha,
    delta,
):
    """
    Standard N4 flavour-loop family:

        e   = reference
        mu  = +alpha
        tau = -alpha

    Both mu and tau carry +CHI.
    """

    Re = np.eye(3)

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
        chi=CHI,
    )

    ftau = seed_loop_biaxial(
        N,
        Rtau,
        R_LOOP,
        delta,
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
    Spatial reflection:

        x -> -x

        M'_sp(x) = S M_sp(Sx) S^T

    with S = diag(-1,+1,+1).
    """

    S = reflection_matrix_x()

    Fr = F[::-1, :, :, :, :].copy()

    Msp = Fr[..., 1:4, 1:4]

    Fr[..., 1:4, 1:4] = np.einsum(
        "ab,...bc,dc->...ad",
        S,
        Msp,
        S,
    )

    return Fr


def swap_mu_tau(fields):
    """
    Flavour-basis permutation:

        [e, mu, tau] -> [e, tau, mu]
    """

    return [
        fields[0],
        fields[2],
        fields[1],
    ]


def composite_transform(fields):
    """
    T = P o R_x.

    Reflect every field spatially, then swap mu and tau.
    """

    reflected = [
        reflect_field_x(F)
        for F in fields
    ]

    return swap_mu_tau(
        reflected
    )


def chiral_matrix(fields):
    C = np.zeros(
        (3, 3),
        dtype=float,
    )

    for a in range(3):
        for b in range(3):
            C[a, b] = chiral_overlap(
                fields[a],
                fields[b],
            )

    return C


def max_field_relative_error(
    fields_a,
    fields_b,
):
    """
    Largest relative Frobenius error across the three flavour fields.
    """

    errors = []

    for A, B in zip(
        fields_a,
        fields_b,
    ):
        den = max(
            frobenius_norm(B),
            1e-30,
        )

        errors.append(
            frobenius_norm(A - B)
            / den
        )

    return float(
        max(errors)
    )


def evaluate_geometry(
    *,
    alpha,
    delta,
):
    original = build_displacements(
        alpha=alpha,
        delta=delta,
    )

    once = composite_transform(
        original
    )

    twice = composite_transform(
        once
    )

    C0 = chiral_matrix(
        original
    )

    C1 = chiral_matrix(
        once
    )

    C2 = chiral_matrix(
        twice
    )

    norm0 = frobenius_norm(
        DX * C0
    )

    norm1 = frobenius_norm(
        DX * C1
    )

    norm2 = frobenius_norm(
        DX * C2
    )

    return {
        "alpha": alpha,
        "delta": delta,

        "C0": C0,
        "C1": C1,
        "C2": C2,

        "composite_odd_error":
            relative_matrix_error(
                C1,
                -C0,
            ),

        "composite_even_error":
            relative_matrix_error(
                C1,
                C0,
            ),

        "matrix_involution_error":
            relative_matrix_error(
                C2,
                C0,
            ),

        "field_involution_error":
            max_field_relative_error(
                twice,
                original,
            ),

        "norm0": norm0,
        "norm1": norm1,
        "norm2": norm2,

        "first_norm_error":
            relative_scalar_error(
                norm1,
                norm0,
            ),

        "second_norm_error":
            relative_scalar_error(
                norm2,
                norm0,
            ),

        "anti0":
            antisymmetry_error(C0),

        "anti1":
            antisymmetry_error(C1),

        "anti2":
            antisymmetry_error(C2),
    }


def all_rows():
    return [
        evaluate_geometry(
            alpha=alpha,
            delta=delta,
        )
        for alpha, delta in itertools.product(
            ALPHAS,
            DELTAS,
        )
    ]


# ----------------------------------------------------------------------
# Structural tests
# ----------------------------------------------------------------------

def test_all_matrices_finite_nonzero():
    for row in all_rows():
        for key in (
            "C0",
            "C1",
            "C2",
        ):
            assert np.all(
                np.isfinite(
                    row[key]
                )
            )

            assert (
                frobenius_norm(
                    row[key]
                )
                > 1e-8
            )


def test_antisymmetry_preserved():
    for row in all_rows():
        assert (
            max(
                row["anti0"],
                row["anti1"],
                row["anti2"],
            )
            < ANTISYM_TOL
        )


def test_composite_is_field_level_involution():
    """
    Reflection squared is identity.

    Mu/tau swap squared is identity.

    They act on different spaces, so the composite should square to
    identity at the field level.
    """

    for row in all_rows():
        assert (
            row[
                "field_involution_error"
            ]
            < INVOLUTION_TOL
        )


def run_all():
    test_all_matrices_finite_nonzero()
    test_antisymmetry_preserved()
    test_composite_is_field_level_involution()


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
        "median": float(
            np.median(arr)
        ),
        "max": float(np.max(arr)),
    }


def main():
    run_all()

    rows = all_rows()

    odd_errors = [
        r["composite_odd_error"]
        for r in rows
    ]

    even_errors = [
        r["composite_even_error"]
        for r in rows
    ]

    matrix_involution_errors = [
        r["matrix_involution_error"]
        for r in rows
    ]

    field_involution_errors = [
        r["field_involution_error"]
        for r in rows
    ]

    norm_errors = [
        r["first_norm_error"]
        for r in rows
    ]

    anti_errors = [
        max(
            r["anti0"],
            r["anti1"],
            r["anti2"],
        )
        for r in rows
    ]

    odd_summary = summarize(
        odd_errors
    )

    even_summary = summarize(
        even_errors
    )

    matrix_inv_summary = summarize(
        matrix_involution_errors
    )

    field_inv_summary = summarize(
        field_involution_errors
    )

    norm_summary = summarize(
        norm_errors
    )

    anti_summary = summarize(
        anti_errors
    )

    odd_count = sum(
        e < COMPOSITE_ODD_TOL
        for e in odd_errors
    )

    norm_count = sum(
        e < MAG_TOL
        for e in norm_errors
    )

    total = len(rows)

    print("Reading Point Test 021")
    print("----------------------")
    print()

    print(
        "N4 C composite spatial-reflection "
        "+ mu-tau symmetry"
    )
    print()

    print("Composite operation:")
    print(
        "T = P o R_x"
    )

    print()
    print("R_x:")
    print(
        "x -> -x, "
        "M_sp -> S M_sp(Sx) S^T"
    )

    print()
    print("P:")
    print(
        "[e, mu, tau] -> "
        "[e, tau, mu]"
    )

    print()
    print("Tested geometry family:")
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
        f"chi={CHI}"
        f"  q={Q}"
        f"  R_loop={R_LOOP}"
        f"  core_vox={CORE_VOX}"
    )
    print()

    print(
        f"tested points: {total}"
    )

    print()
    print("Per-geometry diagnostics:")
    print()

    for row in rows:
        print(
            f"alpha={row['alpha']:.2f}"
            f"  delta={row['delta']:.2f}"
            f"  T_odd={row['composite_odd_error']:.3e}"
            f"  T_even={row['composite_even_error']:.3e}"
            f"  T2_matrix={row['matrix_involution_error']:.3e}"
            f"  T2_field={row['field_involution_error']:.3e}"
            f"  mag={row['first_norm_error']:.3e}"
            f"  anti={max(row['anti0'], row['anti1'], row['anti2']):.3e}"
        )

    print()
    print("Composite sign action:")
    print(
        "T(C) approximately equals -C"
    )

    print()
    print(
        f"supported points = "
        f"{odd_count}/{total}"
    )

    print(
        "min / median / max oddness error = "
        f"{odd_summary['min']:.6e} / "
        f"{odd_summary['median']:.6e} / "
        f"{odd_summary['max']:.6e}"
    )

    print()
    print("Competing evenness diagnostic:")
    print(
        "min / median / max error = "
        f"{even_summary['min']:.6e} / "
        f"{even_summary['median']:.6e} / "
        f"{even_summary['max']:.6e}"
    )

    print()
    print("Composite involution:")
    print()

    print(
        "field-level T^2 error "
        "(min / median / max):"
    )

    print(
        f"{field_inv_summary['min']:.6e} / "
        f"{field_inv_summary['median']:.6e} / "
        f"{field_inv_summary['max']:.6e}"
    )

    print()
    print(
        "matrix-level T^2 error "
        "(min / median / max):"
    )

    print(
        f"{matrix_inv_summary['min']:.6e} / "
        f"{matrix_inv_summary['median']:.6e} / "
        f"{matrix_inv_summary['max']:.6e}"
    )

    print()
    print("Magnitude preservation:")
    print(
        f"supported points = "
        f"{norm_count}/{total}"
    )

    print(
        "min / median / max relative difference = "
        f"{norm_summary['min']:.6e} / "
        f"{norm_summary['median']:.6e} / "
        f"{norm_summary['max']:.6e}"
    )

    print()
    print("Antisymmetry:")
    print(
        "max error = "
        f"{anti_summary['max']:.6e}"
    )
    print("PASS")

    print()
    print("Composite operation T:")
    if odd_count == total:
        print(
            "SIGN-ODD ACROSS TESTED FAMILY"
        )
    else:
        print(
            "SIGN-ODDNESS NOT ROBUST"
        )

    print()
    print("Composite square T^2:")
    if (
        field_inv_summary["max"]
        < INVOLUTION_TOL
        and
        matrix_inv_summary["max"]
        < INVOLUTION_TOL
    ):
        print("IDENTITY")
    else:
        print(
            "NOT IDENTITY WITHIN TESTED TOLERANCE"
        )

    print()
    print("Algebraic classification:")
    if (
        odd_count == total
        and field_inv_summary["max"]
        < INVOLUTION_TOL
        and matrix_inv_summary["max"]
        < INVOLUTION_TOL
    ):
        print(
            "Z2-LIKE SIGN REPRESENTATION "
            "ON C SUPPORTED"
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Interpretation:")
    print(
        "Spatial reflection and mu-tau flavour exchange are "
        "kept as explicit separate operations."
    )
    print(
        "Their composite is an exact involution at the field "
        "level because both operations square to identity and "
        "act on different spaces."
    )
    print(
        "The test determines whether the induced action on the "
        "effective N4 chiral matrix is the nontrivial sign "
        "representation C -> -C."
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
