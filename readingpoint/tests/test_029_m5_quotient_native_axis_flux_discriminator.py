#!/usr/bin/env python3
"""
Reading Point Test 029
======================

Native M5 axis/flux labels on the Result-027 quotient.

Result 027 established the repository-native quotient

    C2^3 / <Ty>

with four cosets

    Ibar      = {I, Ty}
    Txbar     = {Tx, TxTy}
    Tzbar     = {Tz, TyTz}
    TxTzbar   = {TxTz, TxTyTz}

selected by the existing M5 `basic` longest-axis / Mermin-Ho instrument.

Result 028 then established

    C2^3/<Ty>
      ~= (Z/30Z)^*/{1,19}
      ~= Q8/{+1,-1}
      ~= V4

at the abstract quotient level, while leaving six equally valid
correspondences among the three nonidentity classes.

The unresolved question is now narrower:

    Does existing M5 geometry itself supply intrinsic labels for

        Txbar
        Tzbar
        TxTzbar

    that are well-defined on the Result-027 quotient?

Repository-native candidates come from m5_22_4_a_fullf.py:

    comp1   short-axis full-F curvature component
    comp2   middle-axis full-F curvature component
    comp3   long-axis full-F curvature component
    norm3   sign(comp3) * ||Rvec||
    basic   calibrated longest-axis / Mermin-Ho instrument

at the existing cube-flux scales:

    half6
    half12
    half18

CRITICAL RULE
-------------

An observable f may label the quotient only if it DESCENDS through the
Result-027 kernel <Ty>.

That requires, for each Result-027 coset,

    f(I)       ~= f(Ty)
    f(Tx)      ~= f(TxTy)
    f(Tz)      ~= f(TyTz)
    f(TxTz)    ~= f(TxTyTz)

under the preregistered numerical equivalence rule.

Only after that descent condition is satisfied do we ask whether the
resulting quotient signatures distinguish the three nonidentity classes.

This test does NOT:

  * assign Reading Point residue pairs to M5 classes;
  * assign quaternion labels i,j,k;
  * choose a correspondence after seeing the values;
  * combine non-descending reads into a synthetic classifier;
  * invent a new scalar observable.

A successful native M5 quotient label does not by itself solve the
Reading Point correspondence. It only reduces the ambiguity on the M5 side.

Run:

    python3 readingpoint/tests/test_029_m5_quotient_native_axis_flux_discriminator.py
"""

from __future__ import annotations

from pathlib import Path
import importlib.util
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
from m5_11_n4_chiral import (  # noqa: E402
    chiral_overlap,
    real_overlap,
)


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

KAPPA = 0.0


# ===========================================================================
# Numerical tolerances
# ===========================================================================

C_SIGN_TOL = 1e-4

# Same relative-equivalence convention used for the Result-027 scalar
# quotient search.
SCALAR_EQUIV_TOL = 1e-8

ANTISYM_TOL = 1e-10
SYM_TOL = 1e-10


# ===========================================================================
# Existing full-F implementation
# ===========================================================================

def load_fullf_module():
    if not FULLF_PATH.exists():
        raise FileNotFoundError(
            f"Expected existing source not found: {FULLF_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "m5_22_4_a_fullf_for_rp029",
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


def require_existing_function(name):
    fn = getattr(
        FULLF,
        name,
        None,
    )

    if not callable(fn):
        raise RuntimeError(
            f"Expected existing function {name}() "
            f"not found in {FULLF_PATH}"
        )

    return fn


READS = require_existing_function(
    "reads"
)

INS = getattr(
    FULLF,
    "INS",
)

W2_T2 = getattr(
    FULLF,
    "W2_T2",
)


# ===========================================================================
# Existing scalar instruments
# ===========================================================================

READ_NAMES = (
    "comp1",
    "comp2",
    "comp3",
    "norm3",
    "basic",
)

READ_ROLES = {
    "comp1":
        "short-axis full-F curvature component",
    "comp2":
        "middle-axis full-F curvature component",
    "comp3":
        "long-axis full-F curvature component",
    "norm3":
        "signed full-curvature magnitude",
    "basic":
        "longest-axis / Mermin-Ho basic instrument",
}

HALF_KEYS = (
    "half6",
    "half12",
    "half18",
)


# ===========================================================================
# Generic helpers
# ===========================================================================

def vec_norm(A):
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
        vec_norm(A),
        vec_norm(B),
        1.0,
    )

    return float(
        vec_norm(
            A - B
        )
        / den
    )


def symmetry_error(A):
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
                A - A.T
            )
        )
        / scale
    )


def antisymmetry_error(A):
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


def equivalent(A, B):
    return (
        relative_error(
            A,
            B,
        )
        <= SCALAR_EQUIV_TOL
    )


# ===========================================================================
# N3/N4 flavour fields
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

    Msp = M[
        ...,
        1:4,
        1:4,
    ]

    if (
        Msp.shape[-2:]
        != (3, 3)
    ):
        raise RuntimeError(
            f"expected spatial 3x3 M field; got {Msp.shape}"
        )

    if not np.all(
        np.isfinite(
            Msp
        )
    ):
        raise RuntimeError(
            "non-finite spatial M field"
        )

    return Msp


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

NONIDENTITY_QUOTIENT_CLASSES = (
    "Txbar",
    "Tzbar",
    "TxTzbar",
)


# ===========================================================================
# Existing C / Mr controls
# ===========================================================================

def chiral_matrix(fields):
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


def real_matrix(fields):
    K = np.zeros(
        (3, 3),
        dtype=float,
    )

    P = np.zeros(
        (3, 3),
        dtype=float,
    )

    for a in range(3):
        for b in range(
            a,
            3,
        ):
            kab, pab = real_overlap(
                fields[a],
                fields[b],
            )

            K[
                a,
                b,
            ] = (
                K[
                    b,
                    a,
                ]
            ) = kab

            P[
                a,
                b,
            ] = (
                P[
                    b,
                    a,
                ]
            ) = pab

    return (
        K
        + KAPPA * P
    )


def classify_C_sign(
    Ct,
    C0,
):
    even_err = relative_error(
        Ct,
        C0,
    )

    odd_err = relative_error(
        Ct,
        -C0,
    )

    if even_err < C_SIGN_TOL:
        label = "+"

    elif odd_err < C_SIGN_TOL:
        label = "-"

    else:
        label = "?"

    return {
        "label": label,
        "even_error": even_err,
        "odd_error": odd_err,
    }


# ===========================================================================
# Existing full-F configuration
# ===========================================================================

def fullf_cfg():
    return INS.base_cfg(
        term="T2",
        stencil="sym",
        eps=0.0,
        w2=W2_T2,
        n=N,
        delta=DELTA,
        bc="pinned",
    )


CFG = fullf_cfg()


# ===========================================================================
# Existing scalar reads
# ===========================================================================

def scalar_reads_for_field(
    dM,
):
    Msp = displacement_to_spatial_M(
        dM
    )

    row = READS(
        Msp,
        CFG,
    )

    out = {}

    for read_name in (
        READ_NAMES
    ):
        if (
            read_name
            not in row
        ):
            raise RuntimeError(
                f"existing read '{read_name}' missing"
            )

        for half_key in (
            HALF_KEYS
        ):
            if (
                half_key
                not in row[
                    read_name
                ]
            ):
                raise RuntimeError(
                    f"missing "
                    f"{read_name}.{half_key}"
                )

            value = float(
                row[
                    read_name
                ][
                    half_key
                ]
            )

            if not np.isfinite(
                value
            ):
                raise RuntimeError(
                    f"non-finite "
                    f"{read_name}.{half_key}"
                )

            out[
                (
                    read_name,
                    half_key,
                )
            ] = value

    return out


def scalar_triplets(
    fields,
):
    """
    Preserve the existing flavour ordering:

        (e, mu, tau)

    for each repository-native scalar read.
    """

    rows = [
        scalar_reads_for_field(
            F
        )
        for F in fields
    ]

    out = {}

    for read_name in (
        READ_NAMES
    ):
        for half_key in (
            HALF_KEYS
        ):
            key = (
                read_name,
                half_key,
            )

            out[key] = np.asarray(
                [
                    rows[0][key],
                    rows[1][key],
                    rows[2][key],
                ],
                dtype=float,
            )

    return out


# ===========================================================================
# Evaluate all 8 states
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

        Mr = real_matrix(
            fields
        )

        scalars = scalar_triplets(
            fields
        )

        states[name] = {
            "fields":
                fields,
            "C":
                C,
            "Mr":
                Mr,
            "scalars":
                scalars,
            "C_anti":
                antisymmetry_error(
                    C
                ),
            "Mr_sym":
                symmetry_error(
                    Mr
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
            "C_sign"
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

def descent_diagnostics(
    states,
    key,
):
    """
    For a scalar observable f, test whether it is constant on every
    Result-027 coset.

    Returns per-coset errors and the maximum descent error.
    """

    errors = {}

    for qname, pair in (
        QUOTIENT_CLASSES.items()
    ):
        a, b = pair

        A = states[
            a
        ][
            "scalars"
        ][key]

        B = states[
            b
        ][
            "scalars"
        ][key]

        errors[
            qname
        ] = relative_error(
            A,
            B,
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
                <= SCALAR_EQUIV_TOL
            ),
    }


def quotient_signature(
    states,
    key,
    qname,
):
    """
    For a descended observable, use the arithmetic mean of the two
    numerically equivalent representatives as the quotient signature.

    This is not a new physical observable; it is only a symmetric numerical
    representative of a class whose two values already passed the descent
    test.
    """

    a, b = QUOTIENT_CLASSES[
        qname
    ]

    A = states[
        a
    ][
        "scalars"
    ][key]

    B = states[
        b
    ][
        "scalars"
    ][key]

    return (
        A
        + B
    ) / 2.0


# ===========================================================================
# Quotient discrimination
# ===========================================================================

def quotient_pairwise_distances(
    states,
    key,
):
    sigs = {
        qname:
            quotient_signature(
                states,
                key,
                qname,
            )
        for qname in (
            QUOTIENT_CLASSES
        )
    }

    distances = {}

    names = list(
        QUOTIENT_CLASSES.keys()
    )

    for i in range(
        len(names)
    ):
        for j in range(
            i + 1,
            len(names),
        ):
            a = names[i]
            b = names[j]

            distances[
                (
                    a,
                    b,
                )
            ] = relative_error(
                sigs[a],
                sigs[b],
            )

    return (
        sigs,
        distances,
    )


def nonidentity_discrimination(
    states,
    key,
):
    sigs = {
        qname:
            quotient_signature(
                states,
                key,
                qname,
            )
        for qname in (
            NONIDENTITY_QUOTIENT_CLASSES
        )
    }

    pairs = (
        (
            "Txbar",
            "Tzbar",
        ),
        (
            "Txbar",
            "TxTzbar",
        ),
        (
            "Tzbar",
            "TxTzbar",
        ),
    )

    distances = {}

    separated = {}

    for a, b in pairs:
        d = relative_error(
            sigs[a],
            sigs[b],
        )

        distances[
            (
                a,
                b,
            )
        ] = d

        separated[
            (
                a,
                b,
            )
        ] = (
            d
            > SCALAR_EQUIV_TOL
        )

    all_distinct = all(
        separated.values()
    )

    return {
        "signatures":
            sigs,
        "distances":
            distances,
        "separated":
            separated,
        "all_three_distinct":
            all_distinct,
    }


# ===========================================================================
# Structural checks
# ===========================================================================

def test_existing_reads_available():
    assert callable(
        READS
    )

    for name in (
        READ_NAMES
    ):
        assert isinstance(
            name,
            str,
        )


def test_all_values_finite():
    states = evaluate_states()

    for row in (
        states.values()
    ):
        for sig in (
            row[
                "scalars"
            ].values()
        ):
            assert np.all(
                np.isfinite(
                    sig
                )
            )


def test_C_and_Mr_symmetry_classes():
    states = evaluate_states()

    for row in (
        states.values()
    ):
        assert (
            row[
                "C_anti"
            ]
            < ANTISYM_TOL
        )

        assert (
            row[
                "Mr_sym"
            ]
            < SYM_TOL
        )


def run_all():
    test_existing_reads_available()
    test_all_values_finite()
    test_C_and_Mr_symmetry_classes()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    states = evaluate_states()

    candidate_keys = [
        (
            read_name,
            half_key,
        )
        for read_name in (
            READ_NAMES
        )
        for half_key in (
            HALF_KEYS
        )
    ]

    print()
    print("Reading Point Test 029")
    print("----------------------")
    print()

    print(
        "Native M5 axis/flux discriminator "
        "on the Result-027 quotient"
    )

    print()
    print("Source:")
    print(
        FULLF_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print("Result-027 quotient:")
    print()
    print(
        "C2^3 / <Ty>"
    )

    print()
    print("Quotient classes:")
    print()

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
    print("Existing M5 candidate reads:")
    print()

    for name in READ_NAMES:
        print(
            f"{name:7s} : "
            f"{READ_ROLES[name]}"
        )

    print()
    print("Existing flux scales:")
    print(
        ", ".join(
            HALF_KEYS
        )
    )

    print()
    print("Full-F native configuration:")
    print(
        f"n={CFG['n']}  "
        f"delta={CFG['delta']}  "
        f"h={CFG['h']}"
    )

    print()
    print(
        "Preregistered scalar equivalence tolerance:"
    )
    print(
        f"{SCALAR_EQUIV_TOL:.1e}"
    )

    print()
    print("=" * 76)
    print("Quotient-descent audit")
    print("=" * 76)
    print()

    results = {}

    for key in candidate_keys:
        read_name, half_key = key

        descent = descent_diagnostics(
            states,
            key,
        )

        row = {
            "descent":
                descent,
            "discrimination":
                None,
        }

        print(
            f"{read_name}.{half_key}"
        )

        print(
            f"  role = "
            f"{READ_ROLES[read_name]}"
        )

        for qname in (
            QUOTIENT_CLASSES
        ):
            print(
                f"  {qname:10s}"
                f" descent_error="
                f"{descent['errors'][qname]:.6e}"
            )

        print(
            f"  max_descent_error="
            f"{descent['max_error']:.6e}"
        )

        print(
            f"  descends_to_quotient="
            f"{descent['descends']}"
        )

        if descent[
            "descends"
        ]:
            discr = (
                nonidentity_discrimination(
                    states,
                    key,
                )
            )

            row[
                "discrimination"
            ] = discr

            print(
                "  nonidentity quotient signatures:"
            )

            for qname in (
                NONIDENTITY_QUOTIENT_CLASSES
            ):
                sig = discr[
                    "signatures"
                ][
                    qname
                ]

                print(
                    f"    {qname:10s} "
                    f"["
                    f"{sig[0]:+.9e}, "
                    f"{sig[1]:+.9e}, "
                    f"{sig[2]:+.9e}"
                    f"]"
                )

            print(
                "  nonidentity pair distances:"
            )

            for (
                a,
                b,
            ), d in (
                discr[
                    "distances"
                ].items()
            ):
                print(
                    f"    {a:10s} vs "
                    f"{b:10s}: "
                    f"{d:.6e}"
                )

            print(
                f"  all_three_nonidentity_classes_distinct="
                f"{discr['all_three_distinct']}"
            )

        else:
            print(
                "  quotient discrimination:"
            )
            print(
                "    INADMISSIBLE — observable "
                "does not descend through <Ty>"
            )

        print()

        results[
            key
        ] = row

    # -----------------------------------------------------------------------
    # Summary sets
    # -----------------------------------------------------------------------

    descended = [
        key
        for key, row in (
            results.items()
        )
        if row[
            "descent"
        ][
            "descends"
        ]
    ]

    intrinsically_labels_three = [
        key
        for key, row in (
            results.items()
        )
        if (
            row[
                "descent"
            ][
                "descends"
            ]
            and
            row[
                "discrimination"
            ]
            is not None
            and
            row[
                "discrimination"
            ][
                "all_three_distinct"
            ]
        )
    ]

    axis_fullF_descended = [
        key
        for key in (
            descended
        )
        if key[0] in (
            "comp1",
            "comp2",
            "comp3",
            "norm3",
        )
    ]

    basic_descended = [
        key
        for key in (
            descended
        )
        if key[0] == "basic"
    ]

    print("=" * 76)
    print("Summary")
    print("=" * 76)
    print()

    print(
        "Repository-native candidate observables tested:"
    )
    print(
        len(
            candidate_keys
        )
    )

    print()
    print(
        "Observables that descend through <Ty>:"
    )

    if descended:
        for read_name, half_key in (
            descended
        ):
            print(
                f"{read_name}.{half_key}"
            )
    else:
        print("NONE")

    print()
    print(
        "Full-F axis/component reads that descend:"
    )

    if axis_fullF_descended:
        for read_name, half_key in (
            axis_fullF_descended
        ):
            print(
                f"{read_name}.{half_key}"
            )
    else:
        print("NONE")

    print()
    print(
        "Basic longest-axis reads that descend:"
    )

    if basic_descended:
        for read_name, half_key in (
            basic_descended
        ):
            print(
                f"{read_name}.{half_key}"
            )
    else:
        print("NONE")

    print()
    print(
        "Descending observables that distinguish "
        "all three nonidentity quotient classes:"
    )

    if intrinsically_labels_three:
        for read_name, half_key in (
            intrinsically_labels_three
        ):
            print(
                f"{read_name}.{half_key}"
            )
    else:
        print("NONE")

    print()
    print(
        "Native M5 quotient labeling:"
    )

    if intrinsically_labels_three:
        print(
            "SUPPORTED"
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Interpretation:")
    print()

    print(
        "A repository-native observable can label the "
        "Result-027 quotient only if it is invariant under "
        "the kernel <Ty>."
    )

    print()
    print(
        "Reads that distinguish members inside a Result-027 "
        "coset contain valid eight-state information, but they "
        "are not themselves observables on C2^3/<Ty>."
    )

    print()
    print(
        "Only descended observables are therefore admitted as "
        "intrinsic labels of Ibar, Txbar, Tzbar, and TxTzbar."
    )

    if axis_fullF_descended:
        print()
        print(
            "At least one full-F axis/component read descends "
            "through <Ty>, so the ordered eigenframe geometry "
            "supplies quotient-level information."
        )
    else:
        print()
        print(
            "The tested full-F axis/component reads do not "
            "supply quotient-level labels unless they pass "
            "the descent condition."
        )

    if intrinsically_labels_three:
        print()
        print(
            "At least one existing descended M5 observable "
            "distinguishes Txbar, Tzbar, and TxTzbar."
        )

        print()
        print(
            "This gives the M5 quotient intrinsic numerical/"
            "geometric labels without using Reading Point "
            "residue classes."
        )

        print()
        print(
            "However, this alone does not select which intrinsic "
            "M5 label corresponds to {7,13}, {11,29}, or {17,23}."
        )

        print()
        print(
            "The sixfold cross-system ambiguity from Result 028 "
            "can be reduced only by an independently defined "
            "corresponding structure on the Reading Point side."
        )

    else:
        print()
        print(
            "No tested existing M5 scalar both descends through "
            "<Ty> and distinguishes all three nonidentity quotient "
            "classes."
        )

        print()
        print(
            "Therefore the sixfold Result-028 correspondence "
            "ambiguity remains unresolved by these native reads."
        )

    print()
    print(
        "Result-028 admissible M5 -> Reading Point mappings:"
    )
    print(
        "6"
    )

    print()
    print(
        "Reading Point residue-pair -> M5 quotient-class assignment:"
    )
    print(
        "NOT ESTABLISHED"
    )

    print()
    print(
        "Physical Q8/{+1,-1} identification:"
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
