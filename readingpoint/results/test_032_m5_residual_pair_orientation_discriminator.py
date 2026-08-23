#!/usr/bin/env python3
"""
Reading Point Test 032
======================

Native M5/N4 residual-pair orientation discriminator.

Result 031 reduced the cross-system quotient ambiguity to two
partition-preserving isomorphisms.

The remaining M5 pair is

    Tzbar
    TxTzbar

where

    Tzbar    = {Tz, TyTz}
    TxTzbar  = {TxTz, TxTyTz}.

Result 032 asks whether an EXISTING repository-native orientation/sign
observable distinguishes those two quotient classes.

Candidate observable
--------------------

Use the already implemented N4 antisymmetric chiral-overlap operator C.

Earlier Results 018-021 established that:

  * C is antisymmetric;
  * chi -> -chi is approximately even in the tested family;
  * mirror/orientation transformation reverses C;
  * the composite spatial-reflection + mu-tau operation acts sign-odd on C;
  * across the Result-023 closure, C carries a non-faithful Z2 sign
    representation.

Therefore C-sign is an independently existing orientation-sensitive
observable. This test does not invent a new sign convention.

Quotient descent requirement
----------------------------

For C-sign to be a legitimate observable on

    C2^3 / <Ty>

it must be invariant under the kernel action:

    sign C(I)       = sign C(Ty)
    sign C(Tx)      = sign C(TxTy)
    sign C(Tz)      = sign C(TyTz)
    sign C(TxTz)    = sign C(TxTyTz)

Only after descent is established do we inspect the residual pair

    Tzbar
    TxTzbar.

Success criterion
-----------------

A native M5/N4 residual-pair discriminator is supported if:

  1. C remains antisymmetric;
  2. its sign classification descends through <Ty>;
  3. Tzbar and TxTzbar carry opposite C signs.

This test does NOT assign Reading Point residue classes.

Even if the M5 residual pair becomes intrinsically labeled, the
Reading Point-side pair

    {7,13}
    {17,23}

still requires its own independently defined second binary invariant
before a unique cross-system correspondence can be claimed.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


# ===========================================================================
# Repository paths
# ===========================================================================

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
    sys.path.insert(
        0,
        str(M5_SCRIPTS),
    )


# ===========================================================================
# Existing N3/N4 machinery
# ===========================================================================

from m5_11_n3_mass_matrix import rot_axis  # noqa: E402
from m5_11_n3_theta13 import (  # noqa: E402
    seed_loop_biaxial,
    biaxial_vacuum,
)
from m5_11_n4_chiral import chiral_overlap  # noqa: E402


# ===========================================================================
# Reference geometry
# ===========================================================================

N = 40

ALPHA = 0.6
DELTA = 0.1
CHI = 0.6
Q = 0.5

R_LOOP = 9.0
CORE_VOX = 2.0


# ===========================================================================
# Numerical tolerances
# ===========================================================================

C_SIGN_TOL = 1.0e-4
ANTISYM_TOL = 1.0e-10


# ===========================================================================
# Generic helpers
# ===========================================================================

def norm(A):
    return float(
        np.linalg.norm(
            np.asarray(
                A,
                dtype=float,
            )
        )
    )


def relative_error(A, B):
    A = np.asarray(
        A,
        dtype=float,
    )

    B = np.asarray(
        B,
        dtype=float,
    )

    den = max(
        norm(A),
        norm(B),
        1.0,
    )

    return float(
        norm(
            A - B
        )
        / den
    )


def antisymmetry_error(A):
    A = np.asarray(
        A,
        dtype=float,
    )

    scale = max(
        float(
            np.max(
                np.abs(A)
            )
        ),
        1.0,
    )

    return float(
        np.max(
            np.abs(
                A + A.T
            )
        )
        / scale
    )


# ===========================================================================
# N3/N4 flavour fields
# ===========================================================================

def build_displacements():
    """
    Same reference flavour geometry used in Results 018-031.
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


# ===========================================================================
# Result-023 transformations
# ===========================================================================

def reflection_matrix(axis):
    S = np.eye(3)

    S[
        axis,
        axis,
    ] = -1.0

    return S


def reflect_field(
    F,
    axis,
):
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

    slices[
        axis
    ] = slice(
        None,
        None,
        -1,
    )

    Fr = F[
        tuple(
            slices
        )
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


def reflect_fields(
    fields,
    axis,
):
    return [
        reflect_field(
            F,
            axis,
        )
        for F in fields
    ]


def swap_mu_tau(fields):
    return [
        fields[0],
        fields[2],
        fields[1],
    ]


def T(
    fields,
    axis,
):
    """
    Result-023 generator:

        T_axis = P o R_axis

    where P exchanges mu and tau.
    """

    return swap_mu_tau(
        reflect_fields(
            fields,
            axis,
        )
    )


def apply_word(
    fields,
    word,
):
    out = fields

    for axis in word:
        out = T(
            out,
            axis,
        )

    return out


CLOSURE_WORDS = {
    "I": (),
    "Tx": (0,),
    "Ty": (1,),
    "Tz": (2,),
    "TxTy": (0, 1),
    "TxTz": (0, 2),
    "TyTz": (1, 2),
    "TxTyTz": (0, 1, 2),
}


# ===========================================================================
# Result-027 quotient
# ===========================================================================

QUOTIENT_CLASSES = {
    "Ibar": (
        "I",
        "Ty",
    ),

    "Txbar": (
        "Tx",
        "TxTy",
    ),

    "Tzbar": (
        "Tz",
        "TyTz",
    ),

    "TxTzbar": (
        "TxTz",
        "TxTyTz",
    ),
}

RESIDUAL_PAIR = (
    "Tzbar",
    "TxTzbar",
)


# ===========================================================================
# Existing N4 chiral operator
# ===========================================================================

def chiral_matrix(fields):
    """
    Existing N4 C construction:

        C_ab = chiral_overlap(dM_a, dM_b)
    """

    C = np.zeros(
        (3, 3),
        dtype=float,
    )

    for a in range(3):
        for b in range(3):
            C[
                a,
                b,
            ] = chiral_overlap(
                fields[a],
                fields[b],
            )

    return C


def classify_C_sign(
    C,
    C0,
):
    """
    Classify C relative to the reference operator C0.

        + : C ~= +C0
        - : C ~= -C0
        ? : neither within preregistered tolerance
    """

    even_error = relative_error(
        C,
        C0,
    )

    odd_error = relative_error(
        C,
        -C0,
    )

    if even_error <= C_SIGN_TOL:
        sign = "+"

    elif odd_error <= C_SIGN_TOL:
        sign = "-"

    else:
        sign = "?"

    return {
        "sign":
            sign,
        "even_error":
            even_error,
        "odd_error":
            odd_error,
    }


# ===========================================================================
# Evaluate closure
# ===========================================================================

def evaluate_states():
    original = build_displacements()

    states = {}

    for name, word in (
        CLOSURE_WORDS.items()
    ):
        fields = apply_word(
            original,
            word,
        )

        C = chiral_matrix(
            fields
        )

        states[
            name
        ] = {
            "fields":
                fields,
            "C":
                C,
            "C_norm":
                norm(C),
            "antisymmetry_error":
                antisymmetry_error(
                    C
                ),
        }

    C0 = states[
        "I"
    ][
        "C"
    ]

    for name in states:
        states[
            name
        ][
            "classification"
        ] = classify_C_sign(
            states[
                name
            ][
                "C"
            ],
            C0,
        )

    return states


# ===========================================================================
# Quotient descent
# ===========================================================================

def quotient_descent(
    states,
):
    """
    C-sign descends if both representatives of each Result-027 coset
    have the same sign classification.
    """

    rows = {}

    all_descend = True

    for qname, members in (
        QUOTIENT_CLASSES.items()
    ):
        a, b = members

        sa = states[
            a
        ][
            "classification"
        ][
            "sign"
        ]

        sb = states[
            b
        ][
            "classification"
        ][
            "sign"
        ]

        valid = (
            sa in (
                "+",
                "-",
            )
            and
            sb in (
                "+",
                "-",
            )
        )

        same = (
            valid
            and
            sa == sb
        )

        rows[
            qname
        ] = {
            "member_a":
                a,
            "member_b":
                b,
            "sign_a":
                sa,
            "sign_b":
                sb,
            "descends":
                same,
        }

        if not same:
            all_descend = False

    return {
        "classes":
            rows,
        "all_descend":
            all_descend,
    }


def quotient_sign(
    states,
    qname,
):
    a, b = QUOTIENT_CLASSES[
        qname
    ]

    sa = states[
        a
    ][
        "classification"
    ][
        "sign"
    ]

    sb = states[
        b
    ][
        "classification"
    ][
        "sign"
    ]

    if (
        sa
        != sb
    ):
        raise RuntimeError(
            f"C-sign does not descend on {qname}: "
            f"{a}={sa}, {b}={sb}"
        )

    return sa


# ===========================================================================
# Structural tests
# ===========================================================================

def test_C_antisymmetric():
    states = evaluate_states()

    for name, row in (
        states.items()
    ):
        assert (
            row[
                "antisymmetry_error"
            ]
            < ANTISYM_TOL
        ), (
            f"{name}: C antisymmetry failure "
            f"{row['antisymmetry_error']}"
        )


def test_all_states_have_binary_C_sign():
    states = evaluate_states()

    for name, row in (
        states.items()
    ):
        assert (
            row[
                "classification"
            ][
                "sign"
            ]
            in (
                "+",
                "-",
            )
        ), (
            f"{name}: C not classifiable as +/- reference"
        )


def test_C_sign_descends_through_Ty():
    states = evaluate_states()

    descent = quotient_descent(
        states
    )

    assert descent[
        "all_descend"
    ], (
        "C sign does not descend through <Ty>"
    )


def test_residual_pair_has_opposite_C_signs():
    states = evaluate_states()

    a, b = RESIDUAL_PAIR

    sa = quotient_sign(
        states,
        a,
    )

    sb = quotient_sign(
        states,
        b,
    )

    assert (
        sa
        != sb
    ), (
        "Residual quotient pair is not distinguished by C sign"
    )


def run_all():
    test_C_antisymmetric()
    test_all_states_have_binary_C_sign()
    test_C_sign_descends_through_Ty()
    test_residual_pair_has_opposite_C_signs()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    states = evaluate_states()

    descent = quotient_descent(
        states
    )

    print()
    print("Reading Point Test 032")
    print("----------------------")
    print()

    print(
        "Native M5/N4 residual-pair "
        "orientation discriminator"
    )

    print()
    print("Existing observable:")
    print()
    print(
        "N4 chiral-overlap matrix C"
    )

    print()
    print(
        "Previously established behavior:"
    )
    print()

    print(
        "C antisymmetric:"
    )
    print(
        "SUPPORTED"
    )

    print(
        "mirror/orientation sign action:"
    )
    print(
        "SUPPORTED BY RESULTS 018-021"
    )

    print(
        "chi-sign as handedness selector:"
    )
    print(
        "REJECTED IN TESTED FAMILY"
    )

    print()
    print(
        "Result-027 quotient:"
    )
    print()

    print(
        "C2^3 / <Ty>"
    )

    for qname, members in (
        QUOTIENT_CLASSES.items()
    ):
        print(
            f"{qname:10s} = "
            + "{"
            + ", ".join(
                members
            )
            + "}"
        )

    print()
    print(
        "Per-transformation C classification:"
    )
    print()

    for name in (
        CLOSURE_WORDS
    ):
        row = states[
            name
        ]

        c = row[
            "classification"
        ]

        print(
            f"{name:8s}"
            f" sign={c['sign']}"
            f" ||C||={row['C_norm']:.9e}"
            f" even_err={c['even_error']:.6e}"
            f" odd_err={c['odd_error']:.6e}"
            f" anti_err="
            f"{row['antisymmetry_error']:.3e}"
        )

    print()
    print("=" * 72)
    print("Quotient descent")
    print("=" * 72)
    print()

    for qname, row in (
        descent[
            "classes"
        ].items()
    ):
        print(
            f"{qname:10s}"
            f" {row['member_a']}={row['sign_a']}"
            f" {row['member_b']}={row['sign_b']}"
            f" descends={row['descends']}"
        )

    print()
    print(
        "C-sign descends through <Ty>:"
    )
    print(
        "SUPPORTED"
        if descent[
            "all_descend"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Quotient-level C signs:"
    )
    print()

    qsigns = {}

    for qname in (
        QUOTIENT_CLASSES
    ):
        qsigns[
            qname
        ] = quotient_sign(
            states,
            qname,
        )

        print(
            f"{qname:10s}"
            f" -> {qsigns[qname]}"
        )

    print()
    print("=" * 72)
    print("Residual-pair test")
    print("=" * 72)
    print()

    a, b = RESIDUAL_PAIR

    print(
        f"{a:10s}"
        f" -> {qsigns[a]}"
    )

    print(
        f"{b:10s}"
        f" -> {qsigns[b]}"
    )

    distinguished = (
        qsigns[a]
        != qsigns[b]
    )

    print()
    print(
        "Residual pair distinguished by C sign:"
    )
    print(
        "SUPPORTED"
        if distinguished
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Native M5/N4 residual-pair labeling:"
    )
    print(
        "SUPPORTED"
        if (
            descent[
                "all_descend"
            ]
            and distinguished
        )
        else "NOT ESTABLISHED"
    )

    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print()

    print(
        "Result-031 M5 1+2 partition:"
    )
    print()

    print(
        "singleton:"
    )
    print(
        "Txbar"
    )

    print(
        "remaining pair:"
    )
    print(
        "{Tzbar, TxTzbar}"
    )

    print()
    print(
        "Result-032 C-sign labels:"
    )
    print()

    print(
        f"Tzbar    -> {qsigns['Tzbar']}"
    )

    print(
        f"TxTzbar  -> {qsigns['TxTzbar']}"
    )

    print()
    print(
        "M5 quotient intrinsic labeling:"
    )

    if (
        descent[
            "all_descend"
        ]
        and distinguished
    ):
        print(
            "FULLY DISTINGUISHED "
            "WITHIN TESTED QUOTIENT"
        )
    else:
        print(
            "RESIDUAL PAIR NOT RESOLVED"
        )

    print()
    print(
        "Result-031 partition-preserving "
        "M5 -> Reading Point isomorphisms:"
    )
    print(
        "2"
    )

    print()
    print(
        "Reading Point residual pair:"
    )
    print(
        "{7,13}"
    )
    print(
        "{17,23}"
    )

    print()
    print(
        "Reading Point-side corresponding "
        "binary orientation/sign label:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print(
        "Cross-system correspondence count "
        "licensed after Result 032:"
    )
    print(
        "2"
    )

    print()
    print("Interpretation:")
    print()

    print(
        "The existing N4 chiral operator C supplies a binary "
        "orientation-sensitive sign representation on the "
        "Result-023 transformation closure."
    )

    print()
    print(
        "Its sign is invariant under the Result-027 kernel <Ty>, "
        "so C-sign is a legitimate observable on "
        "C2^3/<Ty>."
    )

    print()
    print(
        "Within the residual M5 pair left by Result 031, "
        "Tzbar and TxTzbar carry opposite C signs."
    )

    print()
    print(
        "Therefore the M5 side now possesses an independently "
        "implemented binary label that resolves the remaining "
        "quotient pair."
    )

    print()
    print(
        "This does not yet reduce the cross-system correspondence "
        "count from 2 to 1 because the Reading Point pair "
        "{7,13} and {17,23} still lacks an independently "
        "established corresponding second binary label."
    )

    print()
    print(
        "No Reading Point residue pair is assigned to a C sign "
        "by this test."
    )

    print()
    print(
        "M5 residual-pair orientation labeling:"
    )
    print(
        "SUPPORTED"
        if distinguished
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Reading Point residual-pair labeling:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print(
        "Unique Reading Point -> M5 correspondence:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print(
        "Reading Point -> M5 physical mapping:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print("PASS")


if __name__ == "__main__":
    main()
