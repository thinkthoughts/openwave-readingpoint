#!/usr/bin/env python3
"""
Reading Point Test 037
======================

Native N4 chiral-coupling sign -> C-sign orientation audit.

Purpose
-------

Result 034 left two admissible Reading Point <-> M5 quotient mappings:

    Mapping A:
        C-sign = chi3

    Mapping B:
        C-sign = -chi3

Results 035 and 036 tested two independently implemented native M5
orientation candidates:

    035:
        right-handed M5 full eigenframe

    036:
        signed N4 self-linking N

Neither supplied the missing direct C-sign anchor.

Test 037 audits another pre-existing N4 sign structure:

    g_chiral

The native N4 construction is

    M_H = M_real + i * g_chiral * C

where C is the existing real antisymmetric chiral-overlap matrix.

Critical distinction
--------------------

Changing

    g_chiral -> -g_chiral

trivially changes the sign of the weighted term

    g_chiral * C

IF C itself is unchanged.

That does NOT establish that the geometric observable C changes sign.

Therefore Test 037 explicitly separates:

    1. geometric C
    2. chiral coupling g_chiral
    3. weighted chiral term K = g_chiral * C

and performs three matched transformations:

A. Coupling-sign flip

       (chi, +g)
           vs
       (chi, -g)

B. Screw-sign flip

       (+chi, g)
           vs
       (-chi, g)

C. Combined native sign flip

       (+chi, +g)
           vs
       (-chi, -g)

The purpose is to determine whether an already-existing N4 handedness
convention anchors:

    C-sign

or only:

    sign(g_chiral * C).

No Reading Point residue class, chi3 sign, or cross-system sign assignment
is used anywhere in this test.


Expected logical possibilities
------------------------------

1. g flip:

       C(-g) ~= C(+g)
       K(-g) ~= -K(+g)

   Then g_chiral is an external coupling-sign convention for the weighted
   chiral term, not an orientation anchor for geometric C.

2. chi flip:

       C(-chi) ~= -C(+chi)

   Then the native screw geometry itself supplies a C-sign orientation
   anchor.

3. combined flip:

       C(-chi,-g) ~= -C(+chi,+g)

   only matters for C if the geometry changes C. A sign change of K caused
   solely by g is not counted as a C-sign anchor.

The test must not infer C-sign orientation merely because i*g*C changes sign.


Repository-native implementation
--------------------------------

Uses:

    openwave/xperiments/m5_liquid_crystal/research/scripts/
        m5_11_n4_chiral.py

specifically the existing:

    chiral_mass_matrix(...)

which returns the native real overlap matrix Mr and chiral-overlap matrix C.


Reading Point constraint
------------------------

Reading Point mapping used:
    NO

chi3 used:
    NO

C = chi3 assumed:
    NO

C = -chi3 assumed:
    NO
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

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

CHIRAL_PATH = (
    M5_SCRIPTS
    / "m5_11_n4_chiral.py"
)

RESULT_DIR = (
    REPO_ROOT
    / "readingpoint"
    / "results"
    / "test_037_n4_chiral_coupling_orientation_C_sign"
)

JSON_PATH = (
    RESULT_DIR
    / "audit.json"
)

if str(M5_SCRIPTS) not in sys.path:
    sys.path.insert(
        0,
        str(M5_SCRIPTS),
    )


# ===========================================================================
# Established N3/N4 parameter set
# ===========================================================================

N_GRID = 40

ALPHA = 0.6
DELTA = 0.1

CHI_ABS = 0.6
G_ABS = 1.0

R_LOOP = 9.0
Q = 0.5
CORE_VOX = 2.0
KAPPA = 0.0


# ===========================================================================
# Numerical gates
# ===========================================================================

EPS = 1.0e-30

PARITY_TOL = 1.0e-4

ANTISYMMETRY_TOL = 1.0e-10

SYMMETRY_TOL = 1.0e-10

REPEATABILITY_TOL = 1.0e-12

MAGNITUDE_RATIO_TOL = 1.0e-3

COMPETING_PARITY_MIN = 0.5


# ===========================================================================
# Dynamic repository import
# ===========================================================================

def load_module(
    module_name: str,
    path: Path,
):
    if not path.exists():
        raise FileNotFoundError(
            f"Required repository source not found: {path}"
        )

    spec = importlib.util.spec_from_file_location(
        module_name,
        path,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"Could not import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


CHIRAL = load_module(
    "m5_11_n4_chiral_for_rp037",
    CHIRAL_PATH,
)

CHIRAL_MASS_MATRIX = getattr(
    CHIRAL,
    "chiral_mass_matrix",
    None,
)

CHIRAL_OVERLAP = getattr(
    CHIRAL,
    "chiral_overlap",
    None,
)

if not callable(
    CHIRAL_MASS_MATRIX
):
    raise RuntimeError(
        "Expected chiral_mass_matrix(...) not found"
    )

if not callable(
    CHIRAL_OVERLAP
):
    raise RuntimeError(
        "Expected chiral_overlap(...) not found"
    )


# ===========================================================================
# Generic helpers
# ===========================================================================

def fro_norm(
    A,
) -> float:
    return float(
        np.linalg.norm(
            np.asarray(A)
        )
    )


def normalized_difference(
    A,
    B,
) -> float:
    """
    ||A-B|| / (||A|| + ||B|| + eps)
    """

    A = np.asarray(A)
    B = np.asarray(B)

    return float(
        fro_norm(
            A - B
        )
        /
        (
            fro_norm(A)
            + fro_norm(B)
            + EPS
        )
    )


def odd_even_residuals(
    plus,
    minus,
):
    """
    Test:

        minus ~= -plus   [odd]
        minus ~= +plus   [even]

    Ideal normalization:

        perfect odd:
            r_odd = 0
            r_even = 1

        perfect even:
            r_odd = 1
            r_even = 0
    """

    plus = np.asarray(plus)
    minus = np.asarray(minus)

    den = (
        fro_norm(plus)
        + fro_norm(minus)
        + EPS
    )

    r_odd = float(
        fro_norm(
            minus + plus
        )
        / den
    )

    r_even = float(
        fro_norm(
            minus - plus
        )
        / den
    )

    return (
        r_odd,
        r_even,
    )


def magnitude_ratio(
    plus,
    minus,
):
    p = fro_norm(plus)
    m = fro_norm(minus)

    if p <= EPS:
        return float("nan")

    return float(
        m / p
    )


def antisymmetry_residual(
    C,
):
    C = np.asarray(
        C,
        dtype=float,
    )

    den = max(
        fro_norm(C),
        1.0,
    )

    return float(
        fro_norm(
            C + C.T
        )
        / den
    )


def symmetry_residual(
    M,
):
    M = np.asarray(
        M,
        dtype=float,
    )

    den = max(
        fro_norm(M),
        1.0,
    )

    return float(
        fro_norm(
            M - M.T
        )
        / den
    )


def classify_relation(
    plus,
    minus,
):
    r_odd, r_even = (
        odd_even_residuals(
            plus,
            minus,
        )
    )

    ratio = magnitude_ratio(
        plus,
        minus,
    )

    magnitude_ok = (
        np.isfinite(ratio)
        and
        abs(
            ratio - 1.0
        )
        <= MAGNITUDE_RATIO_TOL
    )

    odd_ok = (
        r_odd <= PARITY_TOL
        and
        r_even >= COMPETING_PARITY_MIN
        and
        magnitude_ok
    )

    even_ok = (
        r_even <= PARITY_TOL
        and
        r_odd >= COMPETING_PARITY_MIN
        and
        magnitude_ok
    )

    if odd_ok:
        verdict = "ODD"

    elif even_ok:
        verdict = "EVEN"

    else:
        verdict = "NO_CLEAN_RELATION"

    return {
        "r_odd":
            r_odd,
        "r_even":
            r_even,
        "magnitude_ratio":
            ratio,
        "verdict":
            verdict,
    }


# ===========================================================================
# Native N4 evaluation
# ===========================================================================

def parameter_set(
    chi,
    g,
):
    return {
        "n":
            N_GRID,
        "alpha":
            ALPHA,
        "delta":
            DELTA,
        "chi":
            float(chi),
        "g_chiral":
            float(g),
        "R_loop":
            R_LOOP,
        "q":
            Q,
        "core_vox":
            CORE_VOX,
        "kappa":
            KAPPA,
    }


def evaluate(
    chi,
    g,
):
    """
    Existing function expected to return:

        M_H, Mr, C

    where

        M_H = Mr + i*g*C.
    """

    result = CHIRAL_MASS_MATRIX(
        N_GRID,
        ALPHA,
        DELTA,
        float(chi),
        float(g),
        R_loop=R_LOOP,
        q=Q,
        core_vox=CORE_VOX,
        kappa=KAPPA,
    )

    if (
        not isinstance(
            result,
            tuple,
        )
        or len(result) < 3
    ):
        raise RuntimeError(
            "Unexpected chiral_mass_matrix(...) return. "
            "Expected at least (M_H, Mr, C)."
        )

    M_H = np.asarray(
        result[0],
        dtype=complex,
    )

    Mr = np.asarray(
        result[1],
        dtype=float,
    )

    C = np.asarray(
        result[2],
        dtype=float,
    )

    if C.shape != (
        3,
        3,
    ):
        raise RuntimeError(
            f"Expected C shape (3,3), got {C.shape}"
        )

    if Mr.shape != (
        3,
        3,
    ):
        raise RuntimeError(
            f"Expected Mr shape (3,3), got {Mr.shape}"
        )

    if M_H.shape != (
        3,
        3,
    ):
        raise RuntimeError(
            f"Expected M_H shape (3,3), got {M_H.shape}"
        )

    for name, A in (
        ("M_H", M_H),
        ("Mr", Mr),
        ("C", C),
    ):
        if not np.all(
            np.isfinite(A)
        ):
            raise RuntimeError(
                f"Non-finite {name} for chi={chi}, g={g}"
            )

    # Real weighted chiral coefficient matrix.
    #
    # The actual Hermitian contribution is i*K.
    K = (
        float(g)
        * C
    )

    reconstructed = (
        Mr.astype(complex)
        + 1j * K
    )

    reconstruction_error = (
        normalized_difference(
            M_H,
            reconstructed,
        )
    )

    return {
        "chi":
            float(chi),
        "g":
            float(g),

        "M_H":
            M_H,

        "Mr":
            Mr,

        "C":
            C,

        "K":
            K,

        "C_norm":
            fro_norm(C),

        "K_norm":
            fro_norm(K),

        "Mr_norm":
            fro_norm(Mr),

        "C_antisymmetry":
            antisymmetry_residual(C),

        "Mr_symmetry":
            symmetry_residual(Mr),

        "reconstruction_error":
            reconstruction_error,

        "components": {
            "C_01":
                float(C[0, 1]),
            "C_02":
                float(C[0, 2]),
            "C_12":
                float(C[1, 2]),
        },
    }


# ===========================================================================
# State set
# ===========================================================================

STATE_SPECS = {
    "chi+_g+": (
        +CHI_ABS,
        +G_ABS,
    ),

    "chi+_g-": (
        +CHI_ABS,
        -G_ABS,
    ),

    "chi-_g+": (
        -CHI_ABS,
        +G_ABS,
    ),

    "chi-_g-": (
        -CHI_ABS,
        -G_ABS,
    ),
}


def evaluate_states():
    return {
        name:
            evaluate(
                chi,
                g,
            )
        for name, (
            chi,
            g,
        ) in STATE_SPECS.items()
    }


# ===========================================================================
# Matched audits
# ===========================================================================

def compare_objects(
    state_a,
    state_b,
):
    """
    Return parity classifications separately for:

        C
        K = g*C
        Mr
    """

    return {
        "C":
            classify_relation(
                state_a["C"],
                state_b["C"],
            ),

        "K":
            classify_relation(
                state_a["K"],
                state_b["K"],
            ),

        "Mr":
            classify_relation(
                state_a["Mr"],
                state_b["Mr"],
            ),
    }


def audit_transformations(
    states,
):
    # A. Pure coupling-sign flip:
    #
    #   (+chi,+g) -> (+chi,-g)

    coupling_flip = compare_objects(
        states[
            "chi+_g+"
        ],
        states[
            "chi+_g-"
        ],
    )

    # Replicate at negative chi.
    coupling_flip_rep = compare_objects(
        states[
            "chi-_g+"
        ],
        states[
            "chi-_g-"
        ],
    )

    # B. Pure screw-sign flip:
    #
    #   (+chi,+g) -> (-chi,+g)

    screw_flip = compare_objects(
        states[
            "chi+_g+"
        ],
        states[
            "chi-_g+"
        ],
    )

    # Replicate at negative g.
    screw_flip_rep = compare_objects(
        states[
            "chi+_g-"
        ],
        states[
            "chi-_g-"
        ],
    )

    # C. Combined flip:
    #
    #   (+chi,+g) -> (-chi,-g)

    combined_flip = compare_objects(
        states[
            "chi+_g+"
        ],
        states[
            "chi-_g-"
        ],
    )

    # Reverse counterpart:
    #
    #   (+chi,-g) -> (-chi,+g)

    combined_flip_rep = compare_objects(
        states[
            "chi+_g-"
        ],
        states[
            "chi-_g+"
        ],
    )

    return {
        "coupling_flip":
            coupling_flip,

        "coupling_flip_replication":
            coupling_flip_rep,

        "screw_flip":
            screw_flip,

        "screw_flip_replication":
            screw_flip_rep,

        "combined_flip":
            combined_flip,

        "combined_flip_replication":
            combined_flip_rep,
    }


# ===========================================================================
# Component audit
# ===========================================================================

def component_pair(
    state_a,
    state_b,
):
    out = {}

    for key in (
        "C_01",
        "C_02",
        "C_12",
    ):
        a = state_a[
            "components"
        ][
            key
        ]

        b = state_b[
            "components"
        ][
            key
        ]

        out[
            key
        ] = {
            "a":
                a,
            "b":
                b,
            "sum":
                a + b,
            "difference":
                b - a,
        }

    return out


# ===========================================================================
# Controls
# ===========================================================================

def run_controls(
    states,
):
    antisymmetry_ok = all(
        row[
            "C_antisymmetry"
        ]
        <= ANTISYMMETRY_TOL
        for row in states.values()
    )

    symmetry_ok = all(
        row[
            "Mr_symmetry"
        ]
        <= SYMMETRY_TOL
        for row in states.values()
    )

    reconstruction_ok = all(
        row[
            "reconstruction_error"
        ]
        <= REPEATABILITY_TOL
        for row in states.values()
    )

    repeat_a = evaluate(
        +CHI_ABS,
        +G_ABS,
    )

    repeat_b = evaluate(
        +CHI_ABS,
        +G_ABS,
    )

    repeatability_C = (
        normalized_difference(
            repeat_a[
                "C"
            ],
            repeat_b[
                "C"
            ],
        )
    )

    repeatability_Mr = (
        normalized_difference(
            repeat_a[
                "Mr"
            ],
            repeat_b[
                "Mr"
            ],
        )
    )

    return {
        "C_antisymmetry":
            antisymmetry_ok,

        "Mr_symmetry":
            symmetry_ok,

        "M_H_reconstruction":
            reconstruction_ok,

        "repeatability_C":
            repeatability_C,

        "repeatability_Mr":
            repeatability_Mr,

        "repeatability_supported":
            (
                repeatability_C
                <= REPEATABILITY_TOL
                and
                repeatability_Mr
                <= REPEATABILITY_TOL
            ),
    }


# ===========================================================================
# Aggregate interpretation
# ===========================================================================

def both_verdict(
    audit,
    name_a,
    name_b,
    object_name,
    target,
):
    return (
        audit[
            name_a
        ][
            object_name
        ][
            "verdict"
        ]
        == target
        and
        audit[
            name_b
        ][
            object_name
        ][
            "verdict"
        ]
        == target
    )


def aggregate_verdict(
    audits,
):
    # Does pure g sign reverse geometric C?
    g_C_odd = both_verdict(
        audits,
        "coupling_flip",
        "coupling_flip_replication",
        "C",
        "ODD",
    )

    g_C_even = both_verdict(
        audits,
        "coupling_flip",
        "coupling_flip_replication",
        "C",
        "EVEN",
    )

    # Does pure g sign reverse weighted K=gC?
    g_K_odd = both_verdict(
        audits,
        "coupling_flip",
        "coupling_flip_replication",
        "K",
        "ODD",
    )

    # Does pure chi sign reverse C?
    chi_C_odd = both_verdict(
        audits,
        "screw_flip",
        "screw_flip_replication",
        "C",
        "ODD",
    )

    chi_C_even = both_verdict(
        audits,
        "screw_flip",
        "screw_flip_replication",
        "C",
        "EVEN",
    )

    if g_C_odd:
        C_anchor = (
            "G_CHIRAL_SIGN_ANCHORS_C"
        )

    elif chi_C_odd:
        C_anchor = (
            "CHI_SIGN_ANCHORS_C"
        )

    else:
        C_anchor = (
            "NO_NATIVE_C_SIGN_ANCHOR_FROM_TESTED_CHIRAL_SIGNS"
        )

    if (
        g_C_even
        and
        g_K_odd
    ):
        coupling_role = (
            "G_CHIRAL_FLIPS_WEIGHTED_TERM_NOT_GEOMETRIC_C"
        )

    else:
        coupling_role = (
            "NO_CLEAN_COUPLING_ROLE"
        )

    return {
        "g_flip_C_odd":
            g_C_odd,

        "g_flip_C_even":
            g_C_even,

        "g_flip_K_odd":
            g_K_odd,

        "chi_flip_C_odd":
            chi_C_odd,

        "chi_flip_C_even":
            chi_C_even,

        "C_sign_anchor":
            C_anchor,

        "coupling_role":
            coupling_role,
    }


# ===========================================================================
# Structural tests
# ===========================================================================

def test_existing_functions():
    assert callable(
        CHIRAL_MASS_MATRIX
    )

    assert callable(
        CHIRAL_OVERLAP
    )


def test_states_finite():
    states = evaluate_states()

    for row in states.values():
        assert np.all(
            np.isfinite(
                row[
                    "C"
                ]
            )
        )

        assert np.all(
            np.isfinite(
                row[
                    "Mr"
                ]
            )
        )

        assert np.all(
            np.isfinite(
                row[
                    "M_H"
                ]
            )
        )


def test_antisymmetry():
    states = evaluate_states()

    for name, row in states.items():
        assert (
            row[
                "C_antisymmetry"
            ]
            <= ANTISYMMETRY_TOL
        ), (
            f"{name}: C antisymmetry error "
            f"{row['C_antisymmetry']}"
        )


def test_mass_matrix_reconstruction():
    states = evaluate_states()

    for name, row in states.items():
        assert (
            row[
                "reconstruction_error"
            ]
            <= REPEATABILITY_TOL
        ), (
            f"{name}: M_H != Mr + i*g*C, "
            f"error={row['reconstruction_error']}"
        )


def run_all():
    test_existing_functions()
    test_states_finite()
    test_antisymmetry()
    test_mass_matrix_reconstruction()


# ===========================================================================
# JSON
# ===========================================================================

def json_safe(
    value: Any,
):
    if isinstance(
        value,
        np.ndarray,
    ):
        return value.tolist()

    if isinstance(
        value,
        np.generic,
    ):
        return value.item()

    if isinstance(
        value,
        complex,
    ):
        return {
            "real":
                float(
                    value.real
                ),
            "imag":
                float(
                    value.imag
                ),
        }

    if isinstance(
        value,
        dict,
    ):
        return {
            str(k):
                json_safe(v)
            for k, v in value.items()
        }

    if isinstance(
        value,
        (
            tuple,
            list,
        ),
    ):
        return [
            json_safe(v)
            for v in value
        ]

    return value


def write_json(
    states,
    audits,
    controls,
    aggregate,
):
    RESULT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "test":
            37,

        "title":
            (
                "Native N4 chiral-coupling sign "
                "-> C-sign orientation audit"
            ),

        "parameters": {
            "n":
                N_GRID,
            "alpha":
                ALPHA,
            "delta":
                DELTA,
            "chi_abs":
                CHI_ABS,
            "g_abs":
                G_ABS,
            "R_loop":
                R_LOOP,
            "q":
                Q,
            "core_vox":
                CORE_VOX,
            "kappa":
                KAPPA,
        },

        "implementation": {
            "source":
                str(
                    CHIRAL_PATH.relative_to(
                        REPO_ROOT
                    )
                ),
            "mass_matrix_function":
                "chiral_mass_matrix",
            "overlap_function":
                "chiral_overlap",
            "native_relation":
                "M_H = Mr + i * g_chiral * C",
        },

        "states": {
            name: {
                "chi":
                    row["chi"],
                "g":
                    row["g"],
                "C":
                    row["C"],
                "K_gC":
                    row["K"],
                "Mr":
                    row["Mr"],
                "C_norm":
                    row["C_norm"],
                "K_norm":
                    row["K_norm"],
                "C_antisymmetry":
                    row[
                        "C_antisymmetry"
                    ],
                "Mr_symmetry":
                    row[
                        "Mr_symmetry"
                    ],
                "reconstruction_error":
                    row[
                        "reconstruction_error"
                    ],
            }
            for name, row in states.items()
        },

        "audits":
            audits,

        "controls":
            controls,

        "aggregate":
            aggregate,

        "reading_point_mapping_used":
            False,

        "chi3_used":
            False,

        "result_034_mapping_count_before":
            2,

        "result_037_mapping_count_after":
            2,

        "reduction_2_to_1_licensed":
            False,

        "unique_readingpoint_to_m5_correspondence":
            "NOT ESTABLISHED",

        "readingpoint_to_m5_physical_mapping":
            "NOT ESTABLISHED",
    }

    JSON_PATH.write_text(
        json.dumps(
            json_safe(
                payload
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


# ===========================================================================
# Reporting helpers
# ===========================================================================

def print_relation(
    title,
    row,
):
    print(
        title
    )

    print(
        f"  r_odd           = "
        f"{row['r_odd']:.9e}"
    )

    print(
        f"  r_even          = "
        f"{row['r_even']:.9e}"
    )

    print(
        f"  magnitude ratio = "
        f"{row['magnitude_ratio']:.9e}"
    )

    print(
        f"  verdict         = "
        f"{row['verdict']}"
    )


def print_audit_block(
    title,
    audit,
):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)
    print()

    print_relation(
        "Geometric C:",
        audit[
            "C"
        ],
    )

    print()

    print_relation(
        "Weighted K = g_chiral * C:",
        audit[
            "K"
        ],
    )

    print()

    print_relation(
        "Real overlap Mr:",
        audit[
            "Mr"
        ],
    )


# ===========================================================================
# Main
# ===========================================================================

def main():
    run_all()

    states = evaluate_states()

    audits = audit_transformations(
        states
    )

    controls = run_controls(
        states
    )

    aggregate = aggregate_verdict(
        audits
    )

    print()
    print("Reading Point Test 037")
    print("----------------------")
    print()

    print(
        "Native N4 chiral-coupling sign "
        "-> C-sign orientation audit"
    )

    print()
    print("=" * 72)
    print("Existing implementation")
    print("=" * 72)
    print()

    print(
        "Source:"
    )

    print(
        CHIRAL_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print(
        "Existing functions:"
    )

    print(
        "chiral_mass_matrix(...)"
    )

    print(
        "chiral_overlap(...)"
    )

    print()
    print(
        "Native construction:"
    )

    print(
        "M_H = Mr + i * g_chiral * C"
    )

    print()
    print(
        "Reading Point mapping used:"
    )

    print(
        "NO"
    )

    print()
    print(
        "chi3 used:"
    )

    print(
        "NO"
    )

    print()
    print("=" * 72)
    print("Exact parameter set")
    print("=" * 72)
    print()

    print(
        f"n          = {N_GRID}"
    )

    print(
        f"alpha      = {ALPHA}"
    )

    print(
        f"delta      = {DELTA}"
    )

    print(
        f"|chi|      = {CHI_ABS}"
    )

    print(
        f"|g_chiral| = {G_ABS}"
    )

    print(
        f"R_loop     = {R_LOOP}"
    )

    print(
        f"q          = {Q}"
    )

    print(
        f"core_vox   = {CORE_VOX}"
    )

    print(
        f"kappa      = {KAPPA}"
    )

    print()
    print("=" * 72)
    print("Per-state readout")
    print("=" * 72)
    print()

    print(
        f"{'state':12s}"
        f"{'chi':>8s}"
        f"{'g':>8s}"
        f"{'||C||':>14s}"
        f"{'||gC||':>14s}"
        f"{'C anti':>12s}"
        f"{'Mr sym':>12s}"
    )

    print(
        "-" * 80
    )

    for name in STATE_SPECS:
        row = states[
            name
        ]

        print(
            f"{name:12s}"
            f"{row['chi']:8.3f}"
            f"{row['g']:8.3f}"
            f"{row['C_norm']:14.6e}"
            f"{row['K_norm']:14.6e}"
            f"{row['C_antisymmetry']:12.3e}"
            f"{row['Mr_symmetry']:12.3e}"
        )

    print_audit_block(
        "A. Pure coupling-sign flip at +chi",
        audits[
            "coupling_flip"
        ],
    )

    print_audit_block(
        "A2. Pure coupling-sign flip replication at -chi",
        audits[
            "coupling_flip_replication"
        ],
    )

    print_audit_block(
        "B. Pure screw-sign flip at +g",
        audits[
            "screw_flip"
        ],
    )

    print_audit_block(
        "B2. Pure screw-sign flip replication at -g",
        audits[
            "screw_flip_replication"
        ],
    )

    print_audit_block(
        "C. Combined (+chi,+g) -> (-chi,-g)",
        audits[
            "combined_flip"
        ],
    )

    print_audit_block(
        "C2. Combined (+chi,-g) -> (-chi,+g)",
        audits[
            "combined_flip_replication"
        ],
    )

    print()
    print("=" * 72)
    print("Component audit for screw-sign flip")
    print("=" * 72)
    print()

    comp = component_pair(
        states[
            "chi+_g+"
        ],
        states[
            "chi-_g+"
        ],
    )

    for key, row in comp.items():
        print(
            f"{key}:"
            f" +chi={row['a']:+.9e}"
            f" -chi={row['b']:+.9e}"
            f" sum={row['sum']:+.3e}"
            f" diff={row['difference']:+.3e}"
        )

    print()
    print("=" * 72)
    print("Controls")
    print("=" * 72)
    print()

    print(
        "C antisymmetry:"
    )

    print(
        "SUPPORTED"
        if controls[
            "C_antisymmetry"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Mr symmetry:"
    )

    print(
        "SUPPORTED"
        if controls[
            "Mr_symmetry"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "M_H = Mr + i*g*C reconstruction:"
    )

    print(
        "SUPPORTED"
        if controls[
            "M_H_reconstruction"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "repeatability C residual:"
    )

    print(
        f"{controls['repeatability_C']:.9e}"
    )

    print()
    print(
        "repeatability Mr residual:"
    )

    print(
        f"{controls['repeatability_Mr']:.9e}"
    )

    print()
    print(
        "repeatability:"
    )

    print(
        "SUPPORTED"
        if controls[
            "repeatability_supported"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Aggregate interpretation")
    print("=" * 72)
    print()

    print(
        "g_chiral sign reverses geometric C:"
    )

    print(
        "SUPPORTED"
        if aggregate[
            "g_flip_C_odd"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "g_chiral sign leaves geometric C even:"
    )

    print(
        "SUPPORTED"
        if aggregate[
            "g_flip_C_even"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "g_chiral sign reverses weighted "
        "K = g_chiral*C:"
    )

    print(
        "SUPPORTED"
        if aggregate[
            "g_flip_K_odd"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "chi sign reverses geometric C:"
    )

    print(
        "SUPPORTED"
        if aggregate[
            "chi_flip_C_odd"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "chi sign leaves geometric C even:"
    )

    print(
        "SUPPORTED"
        if aggregate[
            "chi_flip_C_even"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Native C-sign anchor from tested chiral signs:"
    )

    print(
        aggregate[
            "C_sign_anchor"
        ]
    )

    print()
    print(
        "Native role of g_chiral:"
    )

    print(
        aggregate[
            "coupling_role"
        ]
    )

    print()
    print("=" * 72)
    print("Correspondence boundary")
    print("=" * 72)
    print()

    C_anchor_supported = (
        aggregate[
            "C_sign_anchor"
        ]
        !=
        "NO_NATIVE_C_SIGN_ANCHOR_FROM_TESTED_CHIRAL_SIGNS"
    )

    print(
        "Result-032 geometric C-sign receives "
        "an independent native orientation anchor:"
    )

    print(
        "SUPPORTED"
        if C_anchor_supported
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Weighted chiral term has native "
        "g_chiral sign orientation:"
    )

    print(
        "SUPPORTED"
        if aggregate[
            "g_flip_K_odd"
        ]
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Does weighted-term sign alone establish "
        "the Result-032 C-sign?"
    )

    print(
        "NO"
    )

    print()
    print(
        "Reading Point chi3 sign assigned:"
    )

    print(
        "NO"
    )

    print()
    print(
        "Result-034 admissible mappings:"
    )

    print(
        "2"
    )

    print()
    print(
        "Result-037 admissible mappings:"
    )

    print(
        "2"
    )

    print()
    print(
        "2 -> 1 reduction:"
    )

    print(
        "NOT LICENSED"
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

    write_json(
        states,
        audits,
        controls,
        aggregate,
    )

    print()
    print(
        "JSON summary:"
    )

    print(
        JSON_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print("=" * 72)
    print("Required final statement")
    print("=" * 72)
    print()

    print("RESULT 037:")
    print()

    if (
        aggregate[
            "g_flip_C_odd"
        ]
    ):
        print(
            "Native reversal of g_chiral reverses "
            "the geometric chiral-overlap matrix C "
            "within the tested implementation."
        )

    elif (
        aggregate[
            "chi_flip_C_odd"
        ]
    ):
        print(
            "Native reversal of the secondary screw "
            "chi reverses the geometric chiral-overlap "
            "matrix C within the tested implementation."
        )

    elif (
        aggregate[
            "g_flip_C_even"
        ]
        and
        aggregate[
            "g_flip_K_odd"
        ]
    ):
        print(
            "Native reversal of g_chiral leaves the "
            "geometric chiral-overlap matrix C unchanged "
            "while reversing the weighted chiral term "
            "g_chiral*C."
        )

    else:
        print(
            "The tested native chiral sign reversals "
            "provide no clean orientation anchor for "
            "the geometric chiral-overlap matrix C."
        )

    print()
    print(
        "Reading Point chi3 sign mapping remains "
        "unassigned by Test 037."
    )

    print()
    print("PASS")


if __name__ == "__main__":
    main()
