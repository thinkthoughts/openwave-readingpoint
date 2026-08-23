#!/usr/bin/env python3
"""
Reading Point Test 023 — full closure of T_x, T_y, T_z.

Result 022 established:

    T_x = P o R_x
    T_y = P o R_y
    T_z = P o R_z

as commuting involutions at field level, with both pairs

    <T_x, T_y>
    <T_x, T_z>

forming V4-like four-state subsets.

The unresolved question is whether the three generators together produce:

    4 distinct transformations

or

    8 distinct transformations.

This test explicitly generates:

    I
    T_x
    T_y
    T_z
    T_x T_y
    T_x T_z
    T_y T_z
    T_x T_y T_z

and compares them at field level.

If all eight are distinct and all generators commute and square to identity,
the closure is C2^3-like.

If only four distinct transformations remain, then the three generators
collapse onto one V4-like subgroup.

The induced action on C is characterized separately and may be non-faithful.

No Q8 quotient, Reading Point mapping, or particle classification is assumed.
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
# Reference geometry
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
IDENTITY_TOL = 1e-12
COMMUTE_TOL = 1e-12
DISTINCT_TOL = 1e-6
SIGN_TOL = 1e-4


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def frobenius_norm(A):
    return float(np.linalg.norm(A))


def relative_matrix_error(A, B):
    den = max(
        frobenius_norm(B),
        1e-30,
    )

    return float(
        frobenius_norm(A - B)
        / den
    )


def field_set_relative_error(fields_a, fields_b):
    errors = []

    for A, B in zip(fields_a, fields_b):
        den = max(
            frobenius_norm(B),
            1e-30,
        )

        errors.append(
            frobenius_norm(A - B)
            / den
        )

    return float(max(errors))


def antisymmetry_error(C):
    scale = max(
        float(np.max(np.abs(C))),
        1.0,
    )

    return float(
        np.max(np.abs(C + C.T))
        / scale
    )


# ----------------------------------------------------------------------
# Build N4 fields
# ----------------------------------------------------------------------

def build_displacements():
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
# Spatial reflections + flavour permutation
# ----------------------------------------------------------------------

def reflection_matrix(axis):
    S = np.eye(3)
    S[axis, axis] = -1.0
    return S


def reflect_field(F, axis):
    S = reflection_matrix(axis)

    slices = [
        slice(None),
        slice(None),
        slice(None),
        slice(None),
        slice(None),
    ]

    slices[axis] = slice(None, None, -1)

    Fr = F[tuple(slices)].copy()

    Msp = Fr[..., 1:4, 1:4]

    Fr[..., 1:4, 1:4] = np.einsum(
        "ab,...bc,dc->...ad",
        S,
        Msp,
        S,
    )

    return Fr


def reflect_fields(fields, axis):
    return [
        reflect_field(F, axis)
        for F in fields
    ]


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


# ----------------------------------------------------------------------
# Group-word application
# ----------------------------------------------------------------------

def apply_word(fields, word):
    """
    Apply a tuple of axes in order.

    Example:
        ()        -> I
        (0,)      -> T_x
        (0,1)     -> T_y o T_x

    Since the generators are expected to commute, order should not matter,
    but this test still checks that separately.
    """

    out = fields

    for axis in word:
        out = T(out, axis)

    return out


def closure_words():
    return {
        "I": (),
        "Tx": (0,),
        "Ty": (1,),
        "Tz": (2,),
        "TxTy": (0, 1),
        "TxTz": (0, 2),
        "TyTz": (1, 2),
        "TxTyTz": (0, 1, 2),
    }


# ----------------------------------------------------------------------
# Effective C operator
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
    even_error = relative_matrix_error(
        Ct,
        C0,
    )

    odd_error = relative_matrix_error(
        Ct,
        -C0,
    )

    if even_error < SIGN_TOL:
        label = "+C"
    elif odd_error < SIGN_TOL:
        label = "-C"
    else:
        label = "NEITHER"

    return {
        "label": label,
        "even_error": even_error,
        "odd_error": odd_error,
    }


# ----------------------------------------------------------------------
# Closure analysis
# ----------------------------------------------------------------------

def build_states():
    original = build_displacements()

    words = closure_words()

    states = {
        name: apply_word(
            original,
            word,
        )
        for name, word in words.items()
    }

    return original, states


def pairwise_field_distances(states):
    names = list(states.keys())

    distances = {}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]

            distances[
                f"{a}-{b}"
            ] = field_set_relative_error(
                states[a],
                states[b],
            )

    return distances


def count_distinct_states(states):
    """
    Greedy clustering under DISTINCT_TOL.
    """

    representatives = []

    labels = {}

    for name, fields in states.items():
        assigned = False

        for idx, rep_fields in enumerate(
            representatives
        ):
            if (
                field_set_relative_error(
                    fields,
                    rep_fields,
                )
                <= DISTINCT_TOL
            ):
                labels[name] = idx
                assigned = True
                break

        if not assigned:
            labels[name] = len(
                representatives
            )

            representatives.append(
                fields
            )

    return len(representatives), labels


# ----------------------------------------------------------------------
# Structural checks
# ----------------------------------------------------------------------

def test_generators_square_to_identity():
    original = build_displacements()

    for axis in (0, 1, 2):
        twice = T(
            T(
                original,
                axis,
            ),
            axis,
        )

        assert (
            field_set_relative_error(
                twice,
                original,
            )
            < IDENTITY_TOL
        )


def test_generators_commute_pairwise():
    original = build_displacements()

    for a, b in (
        (0, 1),
        (0, 2),
        (1, 2),
    ):
        ab = T(
            T(original, a),
            b,
        )

        ba = T(
            T(original, b),
            a,
        )

        assert (
            field_set_relative_error(
                ab,
                ba,
            )
            < COMMUTE_TOL
        )


def test_all_effective_matrices_antisymmetric():
    _, states = build_states()

    for fields in states.values():
        C = chiral_matrix(fields)

        assert (
            antisymmetry_error(C)
            < ANTISYM_TOL
        )


def run_all():
    test_generators_square_to_identity()
    test_generators_commute_pairwise()
    test_all_effective_matrices_antisymmetric()


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    run_all()

    original, states = build_states()

    distances = pairwise_field_distances(
        states
    )

    distinct_count, class_labels = (
        count_distinct_states(
            states
        )
    )

    C0 = chiral_matrix(
        original
    )

    C_actions = {}

    for name, fields in states.items():
        Ct = chiral_matrix(
            fields
        )

        C_actions[name] = (
            sign_classification(
                Ct,
                C0,
            )
        )

    print("Reading Point Test 023")
    print("----------------------")
    print()

    print(
        "Full closure of "
        "T_x, T_y, T_z"
    )
    print()

    print("Generators:")
    print("T_x = P o R_x")
    print("T_y = P o R_y")
    print("T_z = P o R_z")

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

    print()
    print("Generated transformations:")

    for name, word in closure_words().items():
        print(
            f"{name:8s}  word={word}"
        )

    print()
    print("Pairwise field distances:")
    print()

    for key, value in distances.items():
        print(
            f"{key}: {value:.6e}"
        )

    print()
    print("Distinct-state clustering:")
    print(
        f"distinct transformations = "
        f"{distinct_count}"
    )

    for name, cls in class_labels.items():
        print(
            f"{name:8s} -> class {cls}"
        )

    print()
    print("Generator squares:")
    print("T_x^2 = I")
    print("T_y^2 = I")
    print("T_z^2 = I")

    print()
    print("Pairwise commutation:")
    print("[T_x,T_y] = 0")
    print("[T_x,T_z] = 0")
    print("[T_y,T_z] = 0")

    print()
    print("Action on C:")
    print()

    for name in closure_words():
        row = C_actions[name]

        print(
            f"{name:8s} -> "
            f"{row['label']}"
            f"  even_err="
            f"{row['even_error']:.3e}"
            f"  odd_err="
            f"{row['odd_error']:.3e}"
        )

    print()
    print("Antisymmetry:")
    print("PASS")

    print()
    print("Field-level closure classification:")

    if distinct_count == 8:
        print(
            "EIGHT DISTINCT COMMUTING "
            "INVOLUTIONS: C2^3-LIKE"
        )
    elif distinct_count == 4:
        print(
            "FOUR DISTINCT COMMUTING "
            "INVOLUTIONS: V4-LIKE"
        )
    else:
        print(
            "OTHER / REDUCED CLOSURE"
        )

    print()
    print("Representation on C:")

    sign_classes = {
        name: row["label"]
        for name, row in C_actions.items()
    }

    plus_count = sum(
        label == "+C"
        for label in sign_classes.values()
    )

    minus_count = sum(
        label == "-C"
        for label in sign_classes.values()
    )

    neither_count = sum(
        label == "NEITHER"
        for label in sign_classes.values()
    )

    print(
        f"+C actions: {plus_count}"
    )
    print(
        f"-C actions: {minus_count}"
    )
    print(
        f"neither: {neither_count}"
    )

    if (
        distinct_count == 8
        and plus_count == 4
        and minus_count == 4
        and neither_count == 0
    ):
        print(
            "NON-FAITHFUL Z2 SIGN "
            "REPRESENTATION OF C2^3-LIKE "
            "FIELD CLOSURE"
        )
    elif (
        distinct_count == 4
        and plus_count == 2
        and minus_count == 2
        and neither_count == 0
    ):
        print(
            "NON-FAITHFUL Z2 SIGN "
            "REPRESENTATION OF V4-LIKE "
            "FIELD CLOSURE"
        )
    else:
        print(
            "CHARACTERIZED; "
            "NO SIMPLE PREASSIGNED "
            "REPRESENTATION"
        )

    print()
    print("Bridge consequence:")

    if distinct_count == 8:
        print(
            "The three tested involutions generate "
            "a larger C2^3-like structure with multiple "
            "embedded V4 subgroups."
        )
        print(
            "Selecting one V4 subgroup for a Reading Point "
            "or Q8 quotient bridge would therefore require "
            "an additional independent criterion."
        )
    elif distinct_count == 4:
        print(
            "The three generators collapse to one naturally "
            "selected V4-like field transformation set."
        )
    else:
        print(
            "The generated closure does not match either "
            "simple four- or eight-state expectation."
        )

    print()
    print("Q8/{+1,-1} identification:")
    print("NOT ESTABLISHED")

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
