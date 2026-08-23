#!/usr/bin/env python3
"""
Reading Point Test 031
======================

Native M5 1+2 quotient partition from existing full-frame norms.

Result 030 established a Reading Point-side intrinsic partition of the
three nonidentity quotient classes:

    unique:
        {11,29}       parent-order profile (2,2)

    paired:
        {7,13}
        {17,23}       parent-order profile (4,4)

Thus the Reading Point nonidentity labeling has the structure

    1 + 2.

Result 031 asks whether an independently defined existing M5 observable
produces the same abstract 1+2 partition on

    Txbar
    Tzbar
    TxTzbar

without using Reading Point residue labels.

Candidate observables:

    ||G||_F
        norm of the existing full-eigenframe connection-vector field

    ||R||_F
        norm of the existing full-eigenframe curvature-vector field

These are the same existing geometric quantities evaluated in Result 026:

    M -> O(M) -> Gamma_i -> G_i -> R_ij.

For either observable to be admissible on the Result-027 quotient it must
first descend through the kernel <Ty>:

    f(I)       ~= f(Ty)
    f(Tx)      ~= f(TxTy)
    f(Tz)      ~= f(TyTz)
    f(TxTz)    ~= f(TxTyTz)

Only after descent is established is the induced partition of the three
nonidentity quotient classes examined.

No Reading Point residue assignment is imposed.
No numerical threshold is fitted from the desired partition.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util
import sys

import numpy as np


# ===========================================================================
# Paths
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

FULLF_PATH = (
    M5_SCRIPTS
    / "m5_22_4_a_fullf.py"
)


# ===========================================================================
# Existing N3/N4 machinery
# ===========================================================================

from m5_11_n3_mass_matrix import rot_axis  # noqa: E402
from m5_11_n3_theta13 import (  # noqa: E402
    seed_loop_biaxial,
    biaxial_vacuum,
)


# ===========================================================================
# Geometry
# ===========================================================================

N = 40
DX = 1.0

ALPHA = 0.6
DELTA = 0.1
CHI = 0.6
Q = 0.5

R_LOOP = 9.0
CORE_VOX = 2.0


# ===========================================================================
# Tolerances
# ===========================================================================

# Equality of scalar norms after a symmetry operation.
NORM_EQUIV_TOL = 1e-10

# Distinct quotient levels must differ by more than this relative amount.
NORM_DISTINCT_TOL = 1e-4


# ===========================================================================
# Existing full-frame implementation
# ===========================================================================

def load_fullf_module():
    if not FULLF_PATH.exists():
        raise FileNotFoundError(
            f"Existing source missing: {FULLF_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "m5_22_4_a_fullf_for_rp031",
        FULLF_PATH,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load m5_22_4_a_fullf.py"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


FULLF = load_fullf_module()

FULL_FRAME = getattr(
    FULLF,
    "full_frame",
)

GAMMA_VECS = getattr(
    FULLF,
    "gamma_vecs",
)


# ===========================================================================
# Helpers
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


def scalar_relative_error(a, b):
    return float(
        abs(
            float(a)
            - float(b)
        )
        / max(
            abs(float(a)),
            abs(float(b)),
            1.0,
        )
    )


# ===========================================================================
# Flavour fields
# ===========================================================================

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


def displacement_to_spatial_M(dM):
    Mvac = biaxial_vacuum(
        N,
        DELTA,
    )

    M = (
        dM
        + Mvac
    )

    return M[
        ...,
        1:4,
        1:4,
    ]


# ===========================================================================
# Result-023 transformations
# ===========================================================================

def reflection_matrix(axis):
    S = np.eye(3)
    S[axis, axis] = -1.0

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

NONIDENTITY = (
    "Txbar",
    "Tzbar",
    "TxTzbar",
)


# ===========================================================================
# Existing M -> O -> G -> R route
# ===========================================================================

def geometry_for_field(
    dM,
):
    Msp = displacement_to_spatial_M(
        dM
    )

    frame_result = FULL_FRAME(
        Msp
    )

    if isinstance(
        frame_result,
        tuple,
    ):
        O = frame_result[0]
    else:
        O = frame_result

    O = np.asarray(
        O
    )

    if (
        O.shape[-2:]
        != (3, 3)
    ):
        raise RuntimeError(
            f"unexpected frame shape {O.shape}"
        )

    if not np.all(
        np.isfinite(
            O
        )
    ):
        raise RuntimeError(
            "non-finite full eigenframe"
        )

    G = GAMMA_VECS(
        O,
        DX,
    )

    if not isinstance(
        G,
        (list, tuple),
    ):
        G = np.asarray(
            G
        )

        G = [
            G[0],
            G[1],
            G[2],
        ]

    Gx, Gy, Gz = [
        np.asarray(
            x
        )
        for x in G
    ]

    Rxy = np.cross(
        Gx,
        Gy,
    )

    Rxz = np.cross(
        Gx,
        Gz,
    )

    Ryz = np.cross(
        Gy,
        Gz,
    )

    Gstack = np.stack(
        [
            Gx,
            Gy,
            Gz,
        ],
        axis=0,
    )

    Rstack = np.stack(
        [
            Rxy,
            Rxz,
            Ryz,
        ],
        axis=0,
    )

    return {
        "G_norm":
            norm(
                Gstack
            ),
        "R_norm":
            norm(
                Rstack
            ),
    }


def geometry_for_triplet(
    fields,
):
    rows = [
        geometry_for_field(
            F
        )
        for F in fields
    ]

    # Same observable convention as Result 026:
    # retain the ordered flavour triplet as one geometric object.
    #
    # Frobenius norm of stacked fields is equivalent to sqrt(sum norms^2).
    G_norm = float(
        np.sqrt(
            sum(
                row[
                    "G_norm"
                ] ** 2
                for row in rows
            )
        )
    )

    R_norm = float(
        np.sqrt(
            sum(
                row[
                    "R_norm"
                ] ** 2
                for row in rows
            )
        )
    )

    return {
        "G_norm":
            G_norm,
        "R_norm":
            R_norm,
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

        states[
            name
        ] = geometry_for_triplet(
            fields
        )

    return states


# ===========================================================================
# Quotient descent
# ===========================================================================

def descent_for_observable(
    states,
    observable,
):
    errors = {}

    for qname, members in (
        QUOTIENT_CLASSES.items()
    ):
        a, b = members

        errors[
            qname
        ] = scalar_relative_error(
            states[
                a
            ][
                observable
            ],
            states[
                b
            ][
                observable
            ],
        )

    max_error = max(
        errors.values()
    )

    return {
        "errors":
            errors,
        "max_error":
            max_error,
        "descends":
            (
                max_error
                <= NORM_EQUIV_TOL
            ),
    }


def quotient_value(
    states,
    observable,
    qname,
):
    a, b = QUOTIENT_CLASSES[
        qname
    ]

    return (
        states[
            a
        ][
            observable
        ]
        + states[
            b
        ][
            observable
        ]
    ) / 2.0


# ===========================================================================
# 1 + 2 partition
# ===========================================================================

def nonidentity_partition(
    states,
    observable,
):
    values = {
        qname:
            quotient_value(
                states,
                observable,
                qname,
            )
        for qname in NONIDENTITY
    }

    pair_errors = {}

    for i in range(
        len(
            NONIDENTITY
        )
    ):
        for j in range(
            i + 1,
            len(
                NONIDENTITY
            ),
        ):
            a = NONIDENTITY[i]
            b = NONIDENTITY[j]

            pair_errors[
                (
                    a,
                    b,
                )
            ] = scalar_relative_error(
                values[a],
                values[b],
            )

    equivalent_pairs = [
        pair
        for pair, error in (
            pair_errors.items()
        )
        if (
            error
            <= NORM_EQUIV_TOL
        )
    ]

    if len(
        equivalent_pairs
    ) == 1:
        pair = set(
            equivalent_pairs[0]
        )

        singleton = [
            x
            for x in NONIDENTITY
            if x not in pair
        ]

        if len(
            singleton
        ) == 1:
            s = singleton[0]

            distinct_from_pair = all(
                scalar_relative_error(
                    values[s],
                    values[p],
                )
                > NORM_DISTINCT_TOL
                for p in pair
            )

            if distinct_from_pair:
                return {
                    "supported":
                        True,
                    "singleton":
                        s,
                    "pair":
                        tuple(
                            sorted(
                                pair
                            )
                        ),
                    "values":
                        values,
                    "pair_errors":
                        pair_errors,
                }

    return {
        "supported":
            False,
        "singleton":
            None,
        "pair":
            None,
        "values":
            values,
        "pair_errors":
            pair_errors,
    }


# ===========================================================================
# Structural tests
# ===========================================================================

def test_existing_functions():
    assert callable(
        FULL_FRAME
    )

    assert callable(
        GAMMA_VECS
    )


def test_all_norms_finite():
    states = evaluate_states()

    for row in (
        states.values()
    ):
        assert np.isfinite(
            row[
                "G_norm"
            ]
        )

        assert np.isfinite(
            row[
                "R_norm"
            ]
        )


def run_all():
    test_existing_functions()
    test_all_norms_finite()


# ===========================================================================
# Main
# ===========================================================================

def main():
    run_all()

    states = evaluate_states()

    observables = (
        "G_norm",
        "R_norm",
    )

    print()
    print("Reading Point Test 031")
    print("----------------------")
    print()

    print(
        "Native M5 1+2 quotient partition "
        "from existing full-frame norms"
    )

    print()
    print("Existing route:")
    print()
    print(
        "M -> O(M) -> Gamma_i -> G_i -> R_ij"
    )

    print()
    print("Candidate observables:")
    print()
    print(
        "||G||_F"
    )
    print(
        "||R||_F"
    )

    print()
    print("Per-transformation values:")
    print()

    for name in (
        CLOSURE_WORDS
    ):
        print(
            f"{name:8s}"
            f" ||G||={states[name]['G_norm']:.9e}"
            f" ||R||={states[name]['R_norm']:.9e}"
        )

    results = {}

    for observable in (
        observables
    ):
        print()
        print("=" * 72)
        print(observable)
        print("=" * 72)
        print()

        descent = (
            descent_for_observable(
                states,
                observable,
            )
        )

        print("Quotient descent:")
        print()

        for qname in (
            QUOTIENT_CLASSES
        ):
            print(
                f"{qname:10s}"
                f" error="
                f"{descent['errors'][qname]:.6e}"
            )

        print()
        print(
            f"max descent error = "
            f"{descent['max_error']:.6e}"
        )

        print(
            f"descends through <Ty> = "
            f"{descent['descends']}"
        )

        partition = None

        if descent[
            "descends"
        ]:
            partition = (
                nonidentity_partition(
                    states,
                    observable,
                )
            )

            print()
            print(
                "Nonidentity quotient values:"
            )
            print()

            for qname in NONIDENTITY:
                print(
                    f"{qname:10s}"
                    f" {partition['values'][qname]:.9e}"
                )

            print()
            print(
                "Nonidentity pair errors:"
            )
            print()

            for (
                a,
                b,
            ), error in (
                partition[
                    "pair_errors"
                ].items()
            ):
                print(
                    f"{a:10s} vs "
                    f"{b:10s}: "
                    f"{error:.6e}"
                )

            print()
            print(
                "Native 1+2 partition:"
            )

            if partition[
                "supported"
            ]:
                print(
                    "SUPPORTED"
                )

                print(
                    "singleton = "
                    + partition[
                        "singleton"
                    ]
                )

                print(
                    "pair = {"
                    + ", ".join(
                        partition[
                            "pair"
                        ]
                    )
                    + "}"
                )

            else:
                print(
                    "NOT ESTABLISHED"
                )

        results[
            observable
        ] = {
            "descent":
                descent,
            "partition":
                partition,
        }

    successful = [
        observable
        for observable, row in (
            results.items()
        )
        if (
            row[
                "descent"
            ][
                "descends"
            ]
            and row[
                "partition"
            ]
            is not None
            and row[
                "partition"
            ][
                "supported"
            ]
        )
    ]

    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print()

    print(
        "Existing norm observables "
        "with native 1+2 quotient partition:"
    )

    if successful:
        for observable in (
            successful
        ):
            print(
                observable
            )
    else:
        print(
            "NONE"
        )

    consistent = False

    if len(
        successful
    ) >= 2:
        first = results[
            successful[0]
        ][
            "partition"
        ]

        consistent = all(
            results[
                observable
            ][
                "partition"
            ][
                "singleton"
            ]
            == first[
                "singleton"
            ]
            and
            set(
                results[
                    observable
                ][
                    "partition"
                ][
                    "pair"
                ]
            )
            == set(
                first[
                    "pair"
                ]
            )
            for observable in (
                successful[1:]
            )
        )

    elif len(
        successful
    ) == 1:
        consistent = True

    print()
    print(
        "Consistent native M5 1+2 partition:"
    )
    print(
        "SUPPORTED"
        if (
            successful
            and consistent
        )
        else "NOT ESTABLISHED"
    )

    if (
        successful
        and consistent
    ):
        p = results[
            successful[0]
        ][
            "partition"
        ]

        print()
        print(
            "M5 singleton:"
        )
        print(
            p[
                "singleton"
            ]
        )

        print()
        print(
            "M5 equivalent pair:"
        )
        print(
            "{"
            + ", ".join(
                p[
                    "pair"
                ]
            )
            + "}"
        )

    print()
    print(
        "Reading Point native 1+2 partition "
        "(Result 030):"
    )
    print()
    print(
        "singleton = {11,29}"
    )
    print(
        "pair = {{7,13}, {17,23}}"
    )

    print()
    print(
        "Cross-system partition compatibility:"
    )

    partition_match = (
        bool(
            successful
        )
        and consistent
    )

    print(
        "SUPPORTED"
        if partition_match
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Result-028 abstract isomorphisms:"
    )
    print(
        "6"
    )

    print()
    print(
        "Partition-preserving isomorphisms:"
    )

    if partition_match:
        print(
            "2"
        )
    else:
        print(
            "6"
        )

    print()
    print(
        "Residual correspondence freedom:"
    )

    if partition_match:
        print(
            "C2 / exchange of the two paired classes"
        )
    else:
        print(
            "S3"
        )

    print()
    print("Interpretation:")
    print()

    print(
        "Result 030 supplied an independently defined "
        "Reading Point 1+2 partition using parent-element "
        "orders in (Z/30Z)^*."
    )

    print()
    print(
        "Result 031 asks whether existing M5 full-frame "
        "geometric norms independently produce the same "
        "abstract singleton-plus-pair structure."
    )

    if partition_match:
        print()
        print(
            "The M5 and Reading Point quotient label structures "
            "both have one distinguished nonidentity class and "
            "one indistinguishable pair."
        )

        print()
        print(
            "Therefore an isomorphism that preserves the independently "
            "established label partitions must map the M5 singleton "
            "to {11,29}, leaving only the swap of {7,13} and {17,23}."
        )

        print()
        print(
            "This reduces the structurally admissible correspondence "
            "count from 6 to 2."
        )

        print()
        print(
            "It still does not distinguish which member of the remaining "
            "M5 pair maps to {7,13} versus {17,23}."
        )

    else:
        print()
        print(
            "No independently defined matching M5 1+2 partition "
            "was established, so the sixfold correspondence "
            "ambiguity remains."
        )

    print()
    print(
        "Reading Point residue-pair -> "
        "M5 quotient-class assignment:"
    )

    if partition_match:
        print(
            "PARTIALLY ESTABLISHED AT PARTITION LEVEL"
        )
    else:
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
