#!/usr/bin/env python3
"""
Reading Point Test 022 — second independent involution for N4 C.

Result 021 established one explicit order-2 transformation

    T_x = P o R_x

with

    T_x(C) ~ -C
    T_x^2 = identity

across the tested family.

One involution is insufficient to establish V4 or any larger discrete
structure.

Result 022 therefore preregisters the two remaining coordinate-reflection
candidates:

    T_y = P o R_y
    T_z = P o R_z

where:

    P = mu/tau flavour exchange

and R_a is the actual spatial reflection of coordinate axis a with the
rank-2 spatial tensor transformed consistently.

For each candidate T_a, the test asks:

  1. Is T_a an involution at field level?
  2. Is T_a distinct from T_x on the tested fields?
  3. How does T_a act on C: +C, -C, or neither?
  4. Do T_x and T_a commute?
  5. Is U = T_x T_a also an involution?
  6. Are {I, T_x, T_a, U} four distinct field transformations?
  7. What representation do these operations induce on C?

Only if the field-level operations are four distinct commuting involutions
will the result describe the transformation set as V4-like.

Even if that occurs, the action on C may be non-faithful. For example,
T_x(C) = -C and T_a(C) = -C imply

    (T_x T_a)(C) = +C,

so the four field transformations collapse to two signs on C.

No identification with Q8/{+1,-1}, the Reading Point quotient, or physical
particle states is introduced.
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
INVOLUTION_TOL = 1e-12
COMMUTE_TOL = 1e-12

SIGN_TOL = 1e-4

# Distinct transformations need only be clearly separated from numerical
# noise. This is a field-space diagnostic, not a physical-distance scale.
DISTINCT_TOL = 1e-6


# ----------------------------------------------------------------------
# Basic helpers
# ----------------------------------------------------------------------

def frobenius_norm(A):
    return float(
        np.linalg.norm(A)
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


def antisymmetry_error(C):
    scale = max(
        float(np.max(np.abs(C))),
        1.0,
    )

    return float(
        np.max(np.abs(C + C.T))
        / scale
    )


def field_set_relative_error(fields_a, fields_b):
    """
    Maximum relative Frobenius error over the three flavour fields.
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


def fields_are_distinct(fields_a, fields_b):
    return (
        field_set_relative_error(
            fields_a,
            fields_b,
        )
        > DISTINCT_TOL
    )


# ----------------------------------------------------------------------
# N4 flavour fields
# ----------------------------------------------------------------------

def build_displacements():
    """
    Standard N4 reference family:

        e   = reference
        mu  = +alpha
        tau = -alpha

    mu/tau both use +CHI.
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


# ----------------------------------------------------------------------
# Spatial reflections
# ----------------------------------------------------------------------

def reflection_matrix(axis):
    """
    Rank-3 spatial reflection matrix.

    axis=0: x -> -x
    axis=1: y -> -y
    axis=2: z -> -z
    """

    S = np.eye(3)

    S[axis, axis] = -1.0

    return S


def reflect_field(F, axis):
    """
    Apply a genuine spatial reflection of one coordinate axis.

    Coordinate action:
        x_axis -> -x_axis

    Tensor action:
        M'_sp(x) = S M_sp(Sx) S^T
    """

    S = reflection_matrix(
        axis
    )

    slices = [
        slice(None),
        slice(None),
        slice(None),
        slice(None),
        slice(None),
    ]

    slices[axis] = slice(
        None,
        None,
        -1,
    )

    Fr = F[
        tuple(slices)
    ].copy()

    Msp = Fr[
        ...,
        1:4,
        1:4,
    ]

    Fr[
        ...,
        1:4,
        1:4,
    ] = np.einsum(
        "ab,...bc,dc->...ad",
        S,
        Msp,
        S,
    )

    return Fr


def reflect_fields(fields, axis):
    return [
        reflect_field(
            F,
            axis,
        )
        for F in fields
    ]


# ----------------------------------------------------------------------
# Flavour permutation and composite generators
# ----------------------------------------------------------------------

def swap_mu_tau(fields):
    return [
        fields[0],
        fields[2],
        fields[1],
    ]


def T(fields, axis):
    """
    T_axis = P o R_axis.
    """

    return swap_mu_tau(
        reflect_fields(
            fields,
            axis,
        )
    )


def compose_T(
    fields,
    first_axis,
    second_axis,
):
    """
    Apply T_second after T_first.

    Returned order:
        T_second o T_first.
    """

    return T(
        T(
            fields,
            first_axis,
        ),
        second_axis,
    )


# ----------------------------------------------------------------------
# Effective operator
# ----------------------------------------------------------------------

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


def sign_classification(Ct, C0):
    """
    Classify the induced matrix action as approximately:

        +C
        -C
        neither
    """

    even_error = relative_matrix_error(
        Ct,
        C0,
    )

    odd_error = relative_matrix_error(
        Ct,
        -C0,
    )

    if odd_error < SIGN_TOL:
        label = "-C"
    elif even_error < SIGN_TOL:
        label = "+C"
    else:
        label = "NEITHER"

    return {
        "label": label,
        "even_error": even_error,
        "odd_error": odd_error,
    }


# ----------------------------------------------------------------------
# Candidate evaluation
# ----------------------------------------------------------------------

def evaluate_candidate(candidate_axis):
    """
    Compare T_x with one second candidate:

        candidate_axis = 1  -> T_y
        candidate_axis = 2  -> T_z
    """

    original = build_displacements()

    Tx = T(
        original,
        0,
    )

    Ta = T(
        original,
        candidate_axis,
    )

    Tx2 = T(
        Tx,
        0,
    )

    Ta2 = T(
        Ta,
        candidate_axis,
    )

    # Products in both orders.
    Tx_then_Ta = compose_T(
        original,
        0,
        candidate_axis,
    )

    Ta_then_Tx = compose_T(
        original,
        candidate_axis,
        0,
    )

    # Apply the product twice.
    product_twice = compose_T(
        Tx_then_Ta,
        0,
        candidate_axis,
    )

    C0 = chiral_matrix(
        original
    )

    Cx = chiral_matrix(
        Tx
    )

    Ca = chiral_matrix(
        Ta
    )

    Cu = chiral_matrix(
        Tx_then_Ta
    )

    Cu_reverse = chiral_matrix(
        Ta_then_Tx
    )

    Cu2 = chiral_matrix(
        product_twice
    )

    sign_x = sign_classification(
        Cx,
        C0,
    )

    sign_a = sign_classification(
        Ca,
        C0,
    )

    sign_u = sign_classification(
        Cu,
        C0,
    )

    # Pairwise field-space distances among:
    # I, Tx, Ta, U.
    states = {
        "I": original,
        "Tx": Tx,
        "Ta": Ta,
        "U": Tx_then_Ta,
    }

    names = list(
        states.keys()
    )

    distances = {}

    all_distinct = True

    for i in range(
        len(names)
    ):
        for j in range(
            i + 1,
            len(names),
        ):
            a = names[i]
            b = names[j]

            d = field_set_relative_error(
                states[a],
                states[b],
            )

            distances[
                f"{a}-{b}"
            ] = d

            if d <= DISTINCT_TOL:
                all_distinct = False

    return {
        "candidate_axis": candidate_axis,

        "Tx_field_involution_error":
            field_set_relative_error(
                Tx2,
                original,
            ),

        "Ta_field_involution_error":
            field_set_relative_error(
                Ta2,
                original,
            ),

        "commutation_field_error":
            field_set_relative_error(
                Tx_then_Ta,
                Ta_then_Tx,
            ),

        "product_field_involution_error":
            field_set_relative_error(
                product_twice,
                original,
            ),

        "Tx_vs_Ta_field_error":
            field_set_relative_error(
                Tx,
                Ta,
            ),

        "all_four_field_states_distinct":
            all_distinct,

        "pairwise_field_distances":
            distances,

        "sign_x": sign_x,
        "sign_a": sign_a,
        "sign_u": sign_u,

        "product_matrix_commutation_error":
            relative_matrix_error(
                Cu,
                Cu_reverse,
            ),

        "product_matrix_involution_error":
            relative_matrix_error(
                Cu2,
                C0,
            ),

        "anti_original":
            antisymmetry_error(C0),

        "anti_x":
            antisymmetry_error(Cx),

        "anti_a":
            antisymmetry_error(Ca),

        "anti_u":
            antisymmetry_error(Cu),

        "norm_original":
            frobenius_norm(
                DX * C0
            ),

        "norm_x":
            frobenius_norm(
                DX * Cx
            ),

        "norm_a":
            frobenius_norm(
                DX * Ca
            ),

        "norm_u":
            frobenius_norm(
                DX * Cu
            ),
    }


# ----------------------------------------------------------------------
# Structural tests
# ----------------------------------------------------------------------

def test_each_candidate_is_field_involution():
    for axis in (1, 2):
        row = evaluate_candidate(
            axis
        )

        assert (
            row[
                "Ta_field_involution_error"
            ]
            < INVOLUTION_TOL
        )


def test_Tx_remains_involution():
    for axis in (1, 2):
        row = evaluate_candidate(
            axis
        )

        assert (
            row[
                "Tx_field_involution_error"
            ]
            < INVOLUTION_TOL
        )


def test_coordinate_candidates_commute_with_Tx():
    """
    Coordinate-axis reflections commute, and P acts only in flavour
    space, so these composites should commute exactly at field level.
    """

    for axis in (1, 2):
        row = evaluate_candidate(
            axis
        )

        assert (
            row[
                "commutation_field_error"
            ]
            < COMMUTE_TOL
        )


def test_product_is_involution():
    for axis in (1, 2):
        row = evaluate_candidate(
            axis
        )

        assert (
            row[
                "product_field_involution_error"
            ]
            < INVOLUTION_TOL
        )


def test_antisymmetry_preserved():
    for axis in (1, 2):
        row = evaluate_candidate(
            axis
        )

        assert (
            max(
                row["anti_original"],
                row["anti_x"],
                row["anti_a"],
                row["anti_u"],
            )
            < ANTISYM_TOL
        )


def run_all():
    test_each_candidate_is_field_involution()
    test_Tx_remains_involution()
    test_coordinate_candidates_commute_with_Tx()
    test_product_is_involution()
    test_antisymmetry_preserved()


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------

def axis_name(axis):
    return {
        0: "x",
        1: "y",
        2: "z",
    }[axis]


def candidate_is_v4_like(row):
    return (
        row[
            "Tx_field_involution_error"
        ] < INVOLUTION_TOL
        and
        row[
            "Ta_field_involution_error"
        ] < INVOLUTION_TOL
        and
        row[
            "commutation_field_error"
        ] < COMMUTE_TOL
        and
        row[
            "product_field_involution_error"
        ] < INVOLUTION_TOL
        and
        row[
            "all_four_field_states_distinct"
        ]
    )


def main():
    run_all()

    rows = [
        evaluate_candidate(1),
        evaluate_candidate(2),
    ]

    print("Reading Point Test 022")
    print("----------------------")
    print()

    print(
        "Second independent involution "
        "for N4 C"
    )
    print()

    print("Established generator:")
    print(
        "T_x = P o R_x"
    )

    print()
    print("Preregistered candidates:")
    print(
        "T_y = P o R_y"
    )
    print(
        "T_z = P o R_z"
    )

    print()
    print(
        f"n={N}"
        f"  dx={DX}"
        f"  alpha={ALPHA}"
        f"  delta={DELTA}"
        f"  chi={CHI}"
        f"  q={Q}"
        f"  R_loop={R_LOOP}"
        f"  core_vox={CORE_VOX}"
    )

    for row in rows:
        axis = axis_name(
            row["candidate_axis"]
        )

        print()
        print("=" * 72)
        print(
            f"Candidate T_{axis}"
        )
        print("=" * 72)

        print()
        print("Field involutions:")
        print(
            "T_x^2 error = "
            f"{row['Tx_field_involution_error']:.6e}"
        )
        print(
            f"T_{axis}^2 error = "
            f"{row['Ta_field_involution_error']:.6e}"
        )

        print()
        print("Generator independence:")
        print(
            f"field distance "
            f"T_x vs T_{axis} = "
            f"{row['Tx_vs_Ta_field_error']:.6e}"
        )

        print()
        print("Commutation:")
        print(
            f"||T_x T_{axis} - "
            f"T_{axis} T_x||_field = "
            f"{row['commutation_field_error']:.6e}"
        )

        print()
        print("Product involution:")
        print(
            f"(T_x T_{axis})^2 "
            f"field error = "
            f"{row['product_field_involution_error']:.6e}"
        )

        print()
        print("Four field states:")
        print(
            "{I, T_x, T_a, T_x T_a}"
        )

        for key, value in (
            row[
                "pairwise_field_distances"
            ].items()
        ):
            print(
                f"{key}: {value:.6e}"
            )

        print()
        print(
            "all four distinct:"
        )
        print(
            row[
                "all_four_field_states_distinct"
            ]
        )

        print()
        print("Action on C:")
        print(
            f"T_x(C): "
            f"{row['sign_x']['label']}"
            f"  even_err="
            f"{row['sign_x']['even_error']:.3e}"
            f"  odd_err="
            f"{row['sign_x']['odd_error']:.3e}"
        )

        print(
            f"T_{axis}(C): "
            f"{row['sign_a']['label']}"
            f"  even_err="
            f"{row['sign_a']['even_error']:.3e}"
            f"  odd_err="
            f"{row['sign_a']['odd_error']:.3e}"
        )

        print(
            f"(T_x T_{axis})(C): "
            f"{row['sign_u']['label']}"
            f"  even_err="
            f"{row['sign_u']['even_error']:.3e}"
            f"  odd_err="
            f"{row['sign_u']['odd_error']:.3e}"
        )

        print()
        print("Matrix composition:")
        print(
            "product-order error = "
            f"{row['product_matrix_commutation_error']:.6e}"
        )

        print(
            "product-square error = "
            f"{row['product_matrix_involution_error']:.6e}"
        )

        print()
        print("Antisymmetry:")
        print(
            "max error = "
            f"{max(row['anti_original'], row['anti_x'], row['anti_a'], row['anti_u']):.6e}"
        )

        print()
        print("Field-level classification:")
        if candidate_is_v4_like(
            row
        ):
            print(
                "FOUR DISTINCT COMMUTING "
                "INVOLUTIONS: V4-LIKE"
            )
        else:
            print(
                "V4-LIKE FOUR-STATE "
                "STRUCTURE NOT ESTABLISHED"
            )

        print()
        print("Representation on C:")

        labels = (
            row["sign_x"]["label"],
            row["sign_a"]["label"],
            row["sign_u"]["label"],
        )

        if labels == (
            "-C",
            "-C",
            "+C",
        ):
            print(
                "NON-FAITHFUL SIGN "
                "REPRESENTATION: "
                "T_x -> -1, "
                f"T_{axis} -> -1, "
                "product -> +1"
            )
        else:
            print(
                "CHARACTERIZED; "
                "NO PREASSIGNED GROUP "
                "REPRESENTATION"
            )

    v4_candidates = [
        axis_name(
            row["candidate_axis"]
        )
        for row in rows
        if candidate_is_v4_like(
            row
        )
    ]

    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print()

    print("Independent second involution:")
    if v4_candidates:
        print(
            "SUPPORTED CANDIDATE(S): "
            + ", ".join(
                f"T_{x}"
                for x in v4_candidates
            )
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Field-level V4-like structure:")
    if v4_candidates:
        print(
            "SUPPORTED FOR TESTED "
            "CANDIDATE(S)"
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Important constraint:")
    print(
        "A V4-like transformation set at field level "
        "does not establish Q8/{+1,-1}, a particle "
        "classification, or a Reading Point mapping."
    )

    print()
    print(
        "The representation on C may be non-faithful: "
        "different field transformations can act with "
        "the same sign on the single effective operator C."
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
