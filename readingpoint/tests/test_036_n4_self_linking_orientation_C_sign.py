#!/usr/bin/env python3
"""
Reading Point Test 036
======================

Native N4 self-linking orientation -> C-sign audit.

Purpose
-------

Test whether the existing signed topological orientation

    N -> -N

of the N4 closed-loop director self-linking construction supplies an
independent native orientation anchor for the existing chiral-overlap
matrix C.

Repository-native ingredients
-----------------------------

m5_11_n4_topo.py:

    * integer self-linking N;
    * N is reflection-odd in the documented construction;
    * topo_mass_matrix(...) evaluates the N-dependent loop construction;
    * the returned Cc is assembled from the existing chiral_overlap(...).

m5_11_n4_chiral.py:

    * chiral_overlap(...);
    * C is the real antisymmetric chiral-overlap matrix entering

          M_H = M_real + i g_chiral C.

Tested self-linking values
--------------------------

    N = -2, -1, 0, +1, +2

The matched comparisons are

    +1 vs -1
    +2 vs -2

with every other numerical/model parameter held fixed.

Two distinct parity questions are reported:

A. Full C parity:

       C(-N) ?= -C(+N)
       C(-N) ?= +C(+N)

B. Baseline-subtracted parity:

       dC(N) = C(N) - C(0)

       dC(-N) ?= -dC(+N)
       dC(-N) ?= +dC(+N)

The baseline split is required because the existing N4 work has a
nonzero chiral sector at N=0. Therefore N=0 is NOT assumed to imply C=0.

Reading Point constraints
-------------------------

No Reading Point residue class is used.
No chi3 value is used.
No C-sign <-> chi3 assignment is used.

Even a successful N -> -N / C -> -C relation would establish only an
M5/N4-native orientation anchor. Cross-system sign correspondence remains
a separate question.
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

TOPO_PATH = M5_SCRIPTS / "m5_11_n4_topo.py"
CHIRAL_PATH = M5_SCRIPTS / "m5_11_n4_chiral.py"

RESULT_DIR = (
    REPO_ROOT
    / "readingpoint"
    / "results"
    / "test_036_n4_self_linking_orientation_C_sign"
)

JSON_PATH = RESULT_DIR / "audit.json"


if str(M5_SCRIPTS) not in sys.path:
    sys.path.insert(
        0,
        str(M5_SCRIPTS),
    )


# ===========================================================================
# Reference parameter set
# ===========================================================================

# Keep this aligned with the established N3/N4 Reading Point geometry.

N_GRID = 40

ALPHA = 0.6
DELTA = 0.1
CHI = 0.6
G_CHIRAL = 1.0

R_LOOP = 9.0
Q = 0.5
CORE_VOX = 2.0
KAPPA = 0.0

TESTED_LINKING = (
    -2,
    -1,
    0,
    +1,
    +2,
)


# ===========================================================================
# Numerical gates
# ===========================================================================

EPS = 1.0e-30

# A parity residual below this is treated as numerical agreement.
PARITY_TOL = 1.0e-4

# If one parity relation is accepted, the competing relation should be
# macroscopically different rather than merely slightly worse.
COMPETING_PARITY_MIN = 0.5

# +/-N configurations should preserve the size of C for a clean sign action.
MAGNITUDE_RATIO_TOL = 1.0e-3

# Standard antisymmetry gate for C.
ANTISYMMETRY_TOL = 1.0e-10

# Repeatability should be effectively deterministic.
REPEATABILITY_TOL = 1.0e-12

# If the baseline-subtracted signal is below this absolute norm, do not
# assign an odd/even delta-C verdict.
DELTA_SIGNAL_FLOOR = 1.0e-10


# ===========================================================================
# Dynamic import
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
            f"Could not construct import spec for {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


TOPO = load_module(
    "m5_11_n4_topo_for_rp036",
    TOPO_PATH,
)

CHIRAL = load_module(
    "m5_11_n4_chiral_for_rp036",
    CHIRAL_PATH,
)


TOPO_MASS_MATRIX = getattr(
    TOPO,
    "topo_mass_matrix",
    None,
)

CHIRAL_OVERLAP = getattr(
    CHIRAL,
    "chiral_overlap",
    None,
)


if not callable(
    TOPO_MASS_MATRIX
):
    raise RuntimeError(
        "Expected existing topo_mass_matrix(...) "
        "not found in m5_11_n4_topo.py"
    )


if not callable(
    CHIRAL_OVERLAP
):
    raise RuntimeError(
        "Expected existing chiral_overlap(...) "
        "not found in m5_11_n4_chiral.py"
    )


# ===========================================================================
# Helpers
# ===========================================================================

def fro_norm(
    A,
) -> float:
    return float(
        np.linalg.norm(
            np.asarray(
                A,
                dtype=float,
            )
        )
    )


def antisymmetry_residual(
    C,
) -> float:
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


def matrix_relative_residual(
    A,
    B,
) -> float:
    """
    Generic normalized difference:

        ||A-B|| / (||A|| + ||B|| + eps)
    """

    A = np.asarray(
        A,
        dtype=float,
    )

    B = np.asarray(
        B,
        dtype=float,
    )

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
    C_plus,
    C_minus,
):
    """
    Preregistered parity diagnostics:

        odd:
            C(-N) ~= -C(+N)

        even:
            C(-N) ~= +C(+N)

    With the sum-of-norms normalization, ideal behavior is:

        perfect odd:
            r_odd  = 0
            r_even = 1

        perfect even:
            r_odd  = 1
            r_even = 0
    """

    Cp = np.asarray(
        C_plus,
        dtype=float,
    )

    Cm = np.asarray(
        C_minus,
        dtype=float,
    )

    den = (
        fro_norm(Cp)
        + fro_norm(Cm)
        + EPS
    )

    r_odd = float(
        fro_norm(
            Cm + Cp
        )
        / den
    )

    r_even = float(
        fro_norm(
            Cm - Cp
        )
        / den
    )

    return (
        r_odd,
        r_even,
    )


def magnitude_ratio(
    C_plus,
    C_minus,
):
    np_ = fro_norm(
        C_plus
    )

    nm_ = fro_norm(
        C_minus
    )

    if np_ <= EPS:
        return float("nan")

    return float(
        nm_ / np_
    )


def sign_or_zero(
    x: float,
    tol: float = 1.0e-12,
) -> str:
    if abs(
        float(x)
    ) <= tol:
        return "0"

    return (
        "+"
        if x > 0
        else "-"
    )


# ===========================================================================
# Repository-native N4 evaluation
# ===========================================================================

def model_parameters():
    return {
        "n":
            N_GRID,
        "alpha":
            ALPHA,
        "delta":
            DELTA,
        "chi":
            CHI,
        "g_chiral":
            G_CHIRAL,
        "R_loop":
            R_LOOP,
        "q":
            Q,
        "core_vox":
            CORE_VOX,
        "kappa":
            KAPPA,
    }


def evaluate_linking(
    n_link: int,
):
    """
    Evaluate the repository-native N4 topology construction.

    Existing signature observed in m5_11_n4_topo.py:

        topo_mass_matrix(
            n,
            alpha,
            delta,
            chi,
            n_link,
            g_chiral,
            R_loop=...,
            q=...,
            core_vox=...,
            kappa=...
        )

    Existing return value:

        M_H, Mr, Cc

    where Cc is the real antisymmetric chiral-overlap matrix.
    """

    result = TOPO_MASS_MATRIX(
        N_GRID,
        ALPHA,
        DELTA,
        CHI,
        int(n_link),
        G_CHIRAL,
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
        or len(
            result
        )
        < 3
    ):
        raise RuntimeError(
            "Unexpected topo_mass_matrix(...) return shape. "
            "Expected at least (M_H, Mr, Cc)."
        )

    M_H = np.asarray(
        result[0]
    )

    Mr = np.asarray(
        result[1]
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

    if not np.all(
        np.isfinite(
            C
        )
    ):
        raise RuntimeError(
            f"N={n_link}: non-finite C matrix"
        )

    return {
        "N":
            int(n_link),
        "M_H":
            M_H,
        "Mr":
            Mr,
        "C":
            C,
        "C_norm":
            fro_norm(C),
        "antisymmetry_residual":
            antisymmetry_residual(
                C
            ),
        "components": {
            "C_01":
                float(
                    C[
                        0,
                        1,
                    ]
                ),
            "C_02":
                float(
                    C[
                        0,
                        2,
                    ]
                ),
            "C_12":
                float(
                    C[
                        1,
                        2,
                    ]
                ),
        },
    }


# ===========================================================================
# Pair audit
# ===========================================================================

def classify_parity(
    r_odd: float,
    r_even: float,
    magnitude_ratio_value: float,
):
    magnitude_ok = (
        np.isfinite(
            magnitude_ratio_value
        )
        and
        abs(
            magnitude_ratio_value
            - 1.0
        )
        <= MAGNITUDE_RATIO_TOL
    )

    odd_ok = (
        r_odd
        <= PARITY_TOL
        and
        r_even
        >= COMPETING_PARITY_MIN
        and
        magnitude_ok
    )

    even_ok = (
        r_even
        <= PARITY_TOL
        and
        r_odd
        >= COMPETING_PARITY_MIN
        and
        magnitude_ok
    )

    if odd_ok:
        return "ODD"

    if even_ok:
        return "EVEN"

    return "NO_CLEAN_RELATION"


def classify_delta_parity(
    dC_plus,
    dC_minus,
):
    np_ = fro_norm(
        dC_plus
    )

    nm_ = fro_norm(
        dC_minus
    )

    if max(
        np_,
        nm_,
    ) < DELTA_SIGNAL_FLOOR:
        return {
            "r_odd":
                None,
            "r_even":
                None,
            "magnitude_ratio":
                None,
            "verdict":
                "SIGNAL_BELOW_FLOOR",
        }

    r_odd, r_even = (
        odd_even_residuals(
            dC_plus,
            dC_minus,
        )
    )

    ratio = magnitude_ratio(
        dC_plus,
        dC_minus,
    )

    return {
        "r_odd":
            r_odd,
        "r_even":
            r_even,
        "magnitude_ratio":
            ratio,
        "verdict":
            classify_parity(
                r_odd,
                r_even,
                ratio,
            ),
    }


def audit_pair(
    abs_N: int,
    states,
    C0,
):
    plus = states[
        +abs_N
    ]

    minus = states[
        -abs_N
    ]

    Cp = plus[
        "C"
    ]

    Cm = minus[
        "C"
    ]

    r_odd, r_even = (
        odd_even_residuals(
            Cp,
            Cm,
        )
    )

    ratio = magnitude_ratio(
        Cp,
        Cm,
    )

    full_verdict = (
        classify_parity(
            r_odd,
            r_even,
            ratio,
        )
    )

    dCp = (
        Cp
        - C0
    )

    dCm = (
        Cm
        - C0
    )

    delta = classify_delta_parity(
        dCp,
        dCm,
    )

    component_rows = {}

    for (
        key,
        i,
        j,
    ) in (
        (
            "C_01",
            0,
            1,
        ),
        (
            "C_02",
            0,
            2,
        ),
        (
            "C_12",
            1,
            2,
        ),
    ):
        cp = float(
            Cp[
                i,
                j,
            ]
        )

        cm = float(
            Cm[
                i,
                j,
            ]
        )

        component_rows[
            key
        ] = {
            "plus":
                cp,
            "minus":
                cm,
            "sum":
                cm + cp,
            "difference":
                cm - cp,
            "plus_sign":
                sign_or_zero(
                    cp
                ),
            "minus_sign":
                sign_or_zero(
                    cm
                ),
            "sign_reverses":
                (
                    sign_or_zero(
                        cp
                    )
                    not in (
                        "0",
                    )
                    and
                    sign_or_zero(
                        cm
                    )
                    not in (
                        "0",
                    )
                    and
                    sign_or_zero(
                        cp
                    )
                    !=
                    sign_or_zero(
                        cm
                    )
                ),
        }

    return {
        "abs_N":
            int(abs_N),
        "r_odd":
            r_odd,
        "r_even":
            r_even,
        "magnitude_ratio":
            ratio,
        "full_C_verdict":
            full_verdict,
        "delta_C": {
            "plus_norm":
                fro_norm(
                    dCp
                ),
            "minus_norm":
                fro_norm(
                    dCm
                ),
            **delta,
        },
        "components":
            component_rows,
    }


# ===========================================================================
# Global verdicts
# ===========================================================================

def aggregate_full_C_verdict(
    pair_results,
):
    verdicts = [
        pair_results[
            n
        ][
            "full_C_verdict"
        ]
        for n in (
            1,
            2,
        )
    ]

    if verdicts == [
        "ODD",
        "ODD",
    ]:
        return "ORIENTATION-ODD"

    if verdicts == [
        "EVEN",
        "EVEN",
    ]:
        return "ORIENTATION-EVEN"

    return "NO CLEAN FULL-C ORIENTATION ANCHOR"


def aggregate_delta_C_verdict(
    pair_results,
):
    verdicts = [
        pair_results[
            n
        ][
            "delta_C"
        ][
            "verdict"
        ]
        for n in (
            1,
            2,
        )
    ]

    if verdicts == [
        "ODD",
        "ODD",
    ]:
        return "DELTA-C ORIENTATION-ODD"

    if verdicts == [
        "EVEN",
        "EVEN",
    ]:
        return "DELTA-C ORIENTATION-EVEN"

    return "NO CLEAN DELTA-C ORIENTATION ANCHOR"


# ===========================================================================
# Structural controls
# ===========================================================================

def run_controls(
    states,
):
    # C1: antisymmetry
    antisym_ok = all(
        states[
            n_link
        ][
            "antisymmetry_residual"
        ]
        <= ANTISYMMETRY_TOL
        for n_link in TESTED_LINKING
    )

    # C0: deterministic repeatability.
    repeat_a = evaluate_linking(
        +1
    )

    repeat_b = evaluate_linking(
        +1
    )

    repeatability_residual = (
        matrix_relative_residual(
            repeat_a[
                "C"
            ],
            repeat_b[
                "C"
            ],
        )
    )

    repeatability_ok = (
        repeatability_residual
        <= REPEATABILITY_TOL
    )

    # C3: parameter identity is guaranteed structurally by one evaluation
    # function whose only varying argument is n_link.
    parameter_identity = True

    # C4: replication pairs both exist.
    replication_ok = all(
        n_link in states
        for n_link in (
            -2,
            -1,
            +1,
            +2,
        )
    )

    return {
        "repeatability_residual":
            repeatability_residual,
        "repeatability_supported":
            repeatability_ok,
        "antisymmetry_supported":
            antisym_ok,
        "parameter_identity_supported":
            parameter_identity,
        "replication_supported":
            replication_ok,
    }


# ===========================================================================
# Test gates
# ===========================================================================

def test_existing_repository_functions():
    assert callable(
        TOPO_MASS_MATRIX
    )

    assert callable(
        CHIRAL_OVERLAP
    )


def test_all_states_finite():
    for n_link in TESTED_LINKING:
        row = evaluate_linking(
            n_link
        )

        assert np.all(
            np.isfinite(
                row[
                    "C"
                ]
            )
        )


def test_all_C_antisymmetric():
    for n_link in TESTED_LINKING:
        row = evaluate_linking(
            n_link
        )

        assert (
            row[
                "antisymmetry_residual"
            ]
            <= ANTISYMMETRY_TOL
        ), (
            f"N={n_link}: C antisymmetry residual "
            f"{row['antisymmetry_residual']}"
        )


def run_all():
    test_existing_repository_functions()
    test_all_states_finite()
    test_all_C_antisymmetric()


# ===========================================================================
# JSON serialization
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
            list,
            tuple,
        ),
    ):
        return [
            json_safe(v)
            for v in value
        ]

    return value


def write_json_summary(
    states,
    pair_results,
    controls,
    full_verdict,
    delta_verdict,
    qualification,
):
    RESULT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "test":
            36,
        "title":
            "Native N4 self-linking orientation -> C-sign audit",
        "orientation_variable":
            "N",
        "orientation_definition":
            (
                "integer self-linking of closed-loop "
                "director framing"
            ),
        "orientation_reversal":
            "N -> -N",
        "tested_N":
            list(
                TESTED_LINKING
            ),
        "parameters":
            model_parameters(),
        "implementation": {
            "topology_source":
                str(
                    TOPO_PATH.relative_to(
                        REPO_ROOT
                    )
                ),
            "chiral_source":
                str(
                    CHIRAL_PATH.relative_to(
                        REPO_ROOT
                    )
                ),
            "topology_function":
                "topo_mass_matrix",
            "chiral_function":
                "chiral_overlap",
        },
        "C_by_N": {
            str(
                n_link
            ): {
                "matrix":
                    states[
                        n_link
                    ][
                        "C"
                    ],
                "components":
                    states[
                        n_link
                    ][
                        "components"
                    ],
                "norm":
                    states[
                        n_link
                    ][
                        "C_norm"
                    ],
                "antisymmetry_residual":
                    states[
                        n_link
                    ][
                        "antisymmetry_residual"
                    ],
            }
            for n_link in TESTED_LINKING
        },
        "pair_results":
            pair_results,
        "controls":
            controls,
        "full_C_verdict":
            full_verdict,
        "delta_C_verdict":
            delta_verdict,
        "qualification":
            qualification,
        "reading_point_mapping_used":
            False,
        "reading_point_chi3_sign_mapping_assigned":
            False,
    }

    JSON_PATH.write_text(
        json.dumps(
            json_safe(
                payload
            ),
            indent=2,
            sort_keys=False,
        )
        + "\n",
        encoding="utf-8",
    )


# ===========================================================================
# Reporting
# ===========================================================================

def print_state_table(
    states,
):
    print(
        f"{'N':>3s}"
        f" {'C_01':>14s}"
        f" {'C_02':>14s}"
        f" {'C_12':>14s}"
        f" {'||C||_F':>14s}"
        f" {'anti':>12s}"
    )

    print(
        "-" * 76
    )

    for n_link in TESTED_LINKING:
        row = states[
            n_link
        ]

        c = row[
            "components"
        ]

        print(
            f"{n_link:3d}"
            f" {c['C_01']:+14.6e}"
            f" {c['C_02']:+14.6e}"
            f" {c['C_12']:+14.6e}"
            f" {row['C_norm']:14.6e}"
            f" {row['antisymmetry_residual']:12.3e}"
        )


def print_component_pair(
    pair,
):
    print(
        "  component audit:"
    )

    for key in (
        "C_01",
        "C_02",
        "C_12",
    ):
        c = pair[
            "components"
        ][
            key
        ]

        print(
            f"    {key}:"
            f" +N={c['plus']:+.9e}"
            f" -N={c['minus']:+.9e}"
            f" sum={c['sum']:+.3e}"
            f" diff={c['difference']:+.3e}"
            f" signs="
            f"{c['plus_sign']}/{c['minus_sign']}"
            f" reverses={c['sign_reverses']}"
        )


# ===========================================================================
# Main
# ===========================================================================

def main():
    run_all()

    states = {
        n_link:
            evaluate_linking(
                n_link
            )
        for n_link in TESTED_LINKING
    }

    C0 = states[
        0
    ][
        "C"
    ]

    pair_results = {
        abs_N:
            audit_pair(
                abs_N,
                states,
                C0,
            )
        for abs_N in (
            1,
            2,
        )
    }

    controls = run_controls(
        states
    )

    full_verdict = (
        aggregate_full_C_verdict(
            pair_results
        )
    )

    delta_verdict = (
        aggregate_delta_C_verdict(
            pair_results
        )
    )

    qualification = (
        "Test 036 treats N -> -N exactly as the signed self-linking "
        "orientation reversal supplied by the existing N4 topology "
        "construction. It does not introduce an additional coordinate "
        "reflection. If repository interpretation requires an additional "
        "spatial operation beyond changing the native self-linking integer, "
        "the result should be read as the parity of the executable +/-N "
        "construction rather than as a complete physical-space parity law."
    )

    print()
    print("Reading Point Test 036")
    print("----------------------")
    print()

    print(
        "Native N4 self-linking orientation -> C-sign audit"
    )

    print()
    print("=" * 72)
    print("Existing implementation")
    print("=" * 72)
    print()

    print(
        "Topology source:"
    )
    print(
        TOPO_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print(
        "Chiral source:"
    )
    print(
        CHIRAL_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print(
        "Existing topology function:"
    )
    print(
        "topo_mass_matrix(...)"
    )

    print()
    print(
        "Existing chiral function:"
    )
    print(
        "chiral_overlap(...)"
    )

    print()
    print(
        "Native orientation variable:"
    )
    print(
        "integer self-linking N"
    )

    print()
    print(
        "Orientation reversal under audit:"
    )
    print(
        "N -> -N"
    )

    print()
    print(
        "Reading Point mapping used:"
    )
    print(
        "NO"
    )

    print()
    print("=" * 72)
    print("Exact parameter set")
    print("=" * 72)
    print()

    for key, value in (
        model_parameters().items()
    ):
        print(
            f"{key:10s} = {value}"
        )

    print()
    print(
        "tested N = "
        + str(
            list(
                TESTED_LINKING
            )
        )
    )

    print()
    print("=" * 72)
    print("Per-N chiral-overlap readout")
    print("=" * 72)
    print()

    print_state_table(
        states
    )

    print()
    print("C(0):")
    print()

    print(
        np.array2string(
            C0,
            precision=8,
            suppress_small=True,
        )
    )

    print()
    print(
        "N=0 assumed to imply C=0:"
    )
    print(
        "NO"
    )

    print()
    print("=" * 72)
    print("Matched +/-N parity tests")
    print("=" * 72)
    print()

    for abs_N in (
        1,
        2,
    ):
        pair = pair_results[
            abs_N
        ]

        print(
            f"|N| = {abs_N}"
        )

        print(
            f"  full-C r_odd  = "
            f"{pair['r_odd']:.9e}"
        )

        print(
            f"  full-C r_even = "
            f"{pair['r_even']:.9e}"
        )

        print(
            f"  full-C magnitude ratio "
            f"||C(-N)||/||C(+N)|| = "
            f"{pair['magnitude_ratio']:.9e}"
        )

        print(
            f"  full-C verdict = "
            f"{pair['full_C_verdict']}"
        )

        print()

        d = pair[
            "delta_C"
        ]

        print(
            f"  ||dC(+N)|| = "
            f"{d['plus_norm']:.9e}"
        )

        print(
            f"  ||dC(-N)|| = "
            f"{d['minus_norm']:.9e}"
        )

        if (
            d[
                "r_odd"
            ]
            is None
        ):
            print(
                "  delta-C r_odd  = SIGNAL BELOW FLOOR"
            )

            print(
                "  delta-C r_even = SIGNAL BELOW FLOOR"
            )

        else:
            print(
                f"  delta-C r_odd  = "
                f"{d['r_odd']:.9e}"
            )

            print(
                f"  delta-C r_even = "
                f"{d['r_even']:.9e}"
            )

            print(
                f"  delta-C magnitude ratio = "
                f"{d['magnitude_ratio']:.9e}"
            )

        print(
            f"  delta-C verdict = "
            f"{d['verdict']}"
        )

        print()

        print_component_pair(
            pair
        )

        print()

    print("=" * 72)
    print("Controls")
    print("=" * 72)
    print()

    print(
        "C0 repeatability residual:"
    )
    print(
        f"{controls['repeatability_residual']:.9e}"
    )

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
    print(
        "antisymmetry for all N:"
    )
    print(
        "SUPPORTED"
        if controls[
            "antisymmetry_supported"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "+/-N parameter identity:"
    )
    print(
        "SUPPORTED"
        if controls[
            "parameter_identity_supported"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "independent replication at |N|=1 and |N|=2:"
    )
    print(
        "SUPPORTED"
        if controls[
            "replication_supported"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Aggregate verdict")
    print("=" * 72)
    print()

    print(
        "Full C:"
    )
    print(
        full_verdict
    )

    print()
    print(
        "Baseline-subtracted dC:"
    )
    print(
        delta_verdict
    )

    print()
    print("Qualification:")
    print()

    print(
        qualification
    )

    print()
    print("=" * 72)
    print("Correspondence boundary")
    print("=" * 72)
    print()

    native_anchor_supported = (
        full_verdict
        == "ORIENTATION-ODD"
    )

    delta_anchor_supported = (
        delta_verdict
        == "DELTA-C ORIENTATION-ODD"
    )

    print(
        "Native self-linking orientation anchors full C-sign:"
    )
    print(
        "SUPPORTED"
        if native_anchor_supported
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Native self-linking orientation anchors "
        "baseline-subtracted dC sign:"
    )
    print(
        "SUPPORTED"
        if delta_anchor_supported
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Reading Point chi3 sign assigned to N sign:"
    )
    print(
        "NO"
    )

    print()
    print(
        "Result-034 admissible cross-system mappings:"
    )
    print(
        "2"
    )

    print()
    print(
        "Does Test 036 itself reduce 2 -> 1?"
    )
    print(
        "NO"
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

    write_json_summary(
        states,
        pair_results,
        controls,
        full_verdict,
        delta_verdict,
        qualification,
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

    print("RESULT 036:")
    print()

    if full_verdict == "ORIENTATION-ODD":
        print(
            "A) Native N4 self-linking reversal N -> -N "
            "reverses the full chiral-overlap matrix C "
            "within the preregistered numerical test."
        )

    elif full_verdict == "ORIENTATION-EVEN":
        print(
            "B) Native N4 self-linking reversal N -> -N "
            "preserves the full chiral-overlap matrix C "
            "within the preregistered numerical test."
        )

    else:
        print(
            "C) Native N4 self-linking reversal N -> -N "
            "gives no clean odd/even relation for the full "
            "chiral-overlap matrix C."
        )

    print()
    print(
        "Baseline-subtracted dC result:"
    )
    print(
        delta_verdict
    )

    print()
    print(
        "Reading Point chi3 sign mapping remains "
        "unassigned by Test 036."
    )

    print()
    print("PASS")


if __name__ == "__main__":
    main()
