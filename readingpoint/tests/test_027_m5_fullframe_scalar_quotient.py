#!/usr/bin/env python3
"""
Reading Point Test 027
======================

Existing full-frame scalar instruments -> natural quotient search.

Result 026 established that the existing M5 route

    M -> O(M) -> Gamma_i -> G_i -> R_ij

resolves all eight Result-023 field transformations:

    I
    Tx
    Ty
    Tz
    TxTy
    TxTz
    TyTz
    TxTyTz

The full normalized G and R fields therefore retain the complete
C2^3-like field-level distinction.

The next question is NOT whether another discriminator exists.

It is:

    Does an EXISTING M5 scalar geometric instrument naturally reduce
    those eight resolved states to four composition-compatible classes
    of size two?

The scalar candidates are taken directly from
m5_22_4_a_fullf.py.

That implementation defines the existing reads:

    comp3
        internal long-axis component of the full curvature;
        verified there against the basic longest-axis instrument.

    comp2
        internal middle-axis curvature component.

    comp1
        internal short-axis curvature component.

    norm3
        sign(comp3) * ||Rvec||.

    basic
        the calibrated longest-axis Mermin-Ho instrument.

Each is already evaluated through cube_flux at:

    half6
    half12
    half18

Result 027 does not define a new scalar observable.

For each closure transformation and each repository-native scalar read,
the test records the ordered flavour triplet:

    (read_e, read_mu, read_tau).

It then clusters the eight transformations using each individual existing
scalar instrument separately.

A candidate four-state quotient is reported only if:

  1. the scalar read gives exactly four classes;
  2. every class contains exactly two transformations;
  3. the measured equivalence relation respects the Result-023
     C2^3-like composition law;
  4. the partition is produced by the existing scalar read itself,
     without hand-selecting pairs or fitting a classifier.

No V4 subgroup is chosen in advance.
No Reading Point labels enter the construction.
No Q8 quotient is assumed.
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
    sys.path.insert(0, str(M5_SCRIPTS))


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

# Fixed numerical equivalence tolerance for scalar triplets.
#
# The comparison is relative:
#
#     ||a-b|| / max(||a||, ||b||, 1)
#
# so near-zero scalar reads are compared with an absolute floor of 1.
#
# This tolerance is preregistered and is not fitted to the observed
# partitions.
SCALAR_EQUIV_TOL = 1e-8

ANTISYM_TOL = 1e-10
SYM_TOL = 1e-10


# ===========================================================================
# Load existing full-F implementation
# ===========================================================================

def load_fullf_module():
    if not FULLF_PATH.exists():
        raise FileNotFoundError(
            f"Expected existing source not found: {FULLF_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "m5_22_4_a_fullf_for_rp027",
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


# Existing objects used by the repository-native instrument.
INS = getattr(
    FULLF,
    "INS",
)

W2_T2 = getattr(
    FULLF,
    "W2_T2",
)


# ===========================================================================
# Existing scalar candidates
# ===========================================================================

READ_NAMES = (
    "comp3",
    "comp2",
    "comp1",
    "norm3",
    "basic",
)

HALF_KEYS = (
    "half6",
    "half12",
    "half18",
)


# ===========================================================================
# Generic helpers
# ===========================================================================

def frobenius_norm(A):
    return float(
        np.linalg.norm(A)
    )


def relative_error(A, B):
    den = max(
        frobenius_norm(A),
        frobenius_norm(B),
        1.0,
    )

    return float(
        frobenius_norm(
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


# ===========================================================================
# N4 flavour fields
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
    """
    Reconstruct the full N3/N4 field, then return the spatial 3x3 block
    consumed by the existing M5 full-frame electric instrument.
    """

    Mvac = biaxial_vacuum(
        N,
        DELTA,
    )

    M = dM + Mvac

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
            f"expected spatial 3x3 field; got {Msp.shape}"
        )

    if not np.all(
        np.isfinite(Msp)
    ):
        raise RuntimeError(
            "spatial M field contains non-finite values"
        )

    return Msp


# ===========================================================================
# Result-023 transformations
# ===========================================================================

def reflection_matrix(axis):
    S = np.eye(3)
    S[axis, axis] = -1.0

    return S


def reflect_field(F, axis):
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


def T(fields, axis):
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


WORD_BITS = {
    "I": (0, 0, 0),
    "Tx": (1, 0, 0),
    "Ty": (0, 1, 0),
    "Tz": (0, 0, 1),
    "TxTy": (1, 1, 0),
    "TxTz": (1, 0, 1),
    "TyTz": (0, 1, 1),
    "TxTyTz": (1, 1, 1),
}


BITS_TO_NAME = {
    bits: name
    for name, bits
    in WORD_BITS.items()
}


def group_product_name(a, b):
    ba = WORD_BITS[a]
    bb = WORD_BITS[b]

    bc = tuple(
        x ^ y
        for x, y
        in zip(ba, bb)
    )

    return BITS_TO_NAME[bc]


# ===========================================================================
# Existing C and Mr controls
# ===========================================================================

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

            K[a, b] = K[b, a] = kab
            P[a, b] = P[b, a] = pab

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
# Repository-native full-F configuration
# ===========================================================================

def fullf_cfg():
    """
    Use the existing M5 full-F instrument configuration rather than
    constructing a new scalar integration rule.
    """

    cfg = INS.base_cfg(
        term="T2",
        stencil="sym",
        eps=0.0,
        w2=W2_T2,
        n=N,
        delta=DELTA,
        bc="pinned",
    )

    return cfg


CFG = fullf_cfg()


# ===========================================================================
# Existing scalar reads
# ===========================================================================

def scalar_reads_for_field(
    dM,
):
    """
    Run the existing m5_22_4_a_fullf.reads() instrument on one flavour
    field.

    No new scalar observable is introduced.
    """

    Msp = displacement_to_spatial_M(
        dM
    )

    row = READS(
        Msp,
        CFG,
    )

    out = {}

    for read_name in READ_NAMES:
        if read_name not in row:
            raise RuntimeError(
                f"existing read '{read_name}' missing from full-F output"
            )

        for half_key in HALF_KEYS:
            if (
                half_key
                not in row[read_name]
            ):
                raise RuntimeError(
                    f"existing scalar {read_name}.{half_key} missing"
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
                    f"non-finite scalar read {read_name}.{half_key}"
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
    Preserve the ordered flavour triplet for every existing scalar
    instrument:

        (read_e, read_mu, read_tau)

    This retains the already-defined flavour ordering without introducing
    a new flavour-space contraction.
    """

    flavour_rows = [
        scalar_reads_for_field(
            F
        )
        for F in fields
    ]

    out = {}

    for read_name in READ_NAMES:
        for half_key in HALF_KEYS:
            key = (
                read_name,
                half_key,
            )

            out[key] = np.asarray(
                [
                    flavour_rows[0][key],
                    flavour_rows[1][key],
                    flavour_rows[2][key],
                ],
                dtype=float,
            )

    return out


# ===========================================================================
# Evaluate all eight transformations
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
            "fields": fields,
            "C": C,
            "Mr": Mr,
            "scalars": scalars,
            "C_anti":
                antisymmetry_error(C),
            "Mr_sym":
                symmetry_error(Mr),
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
# Scalar equivalence / clustering
# ===========================================================================

def scalar_distance(
    sig_a,
    sig_b,
):
    return relative_error(
        sig_a,
        sig_b,
    )


def scalar_equivalent(
    name_a,
    name_b,
    states,
    key,
):
    A = states[
        name_a
    ][
        "scalars"
    ][key]

    B = states[
        name_b
    ][
        "scalars"
    ][key]

    return (
        scalar_distance(
            A,
            B,
        )
        <= SCALAR_EQUIV_TOL
    )


def cluster_for_scalar(
    states,
    key,
):
    names = list(
        CLOSURE_WORDS.keys()
    )

    reps = []
    class_of = {}

    for name in names:
        assigned = False

        for idx, rep in enumerate(
            reps
        ):
            if scalar_equivalent(
                name,
                rep,
                states,
                key,
            ):
                class_of[
                    name
                ] = idx

                assigned = True
                break

        if not assigned:
            class_of[
                name
            ] = len(
                reps
            )

            reps.append(
                name
            )

    classes = {}

    for name, cls in (
        class_of.items()
    ):
        classes.setdefault(
            cls,
            [],
        ).append(
            name
        )

    return (
        class_of,
        classes,
    )


# ===========================================================================
# Composition compatibility
# ===========================================================================

def quotient_compatibility(
    class_of,
):
    names = list(
        CLOSURE_WORDS.keys()
    )

    violations = []

    for a in names:
        for ap in names:
            if (
                class_of[a]
                != class_of[ap]
            ):
                continue

            for b in names:
                for bp in names:
                    if (
                        class_of[b]
                        != class_of[bp]
                    ):
                        continue

                    ab = group_product_name(
                        a,
                        b,
                    )

                    apbp = group_product_name(
                        ap,
                        bp,
                    )

                    if (
                        class_of[ab]
                        != class_of[apbp]
                    ):
                        violations.append(
                            (
                                a,
                                ap,
                                b,
                                bp,
                                ab,
                                apbp,
                            )
                        )

    return (
        len(
            violations
        )
        == 0,
        violations,
    )


def four_balanced_classes(
    classes,
):
    if len(
        classes
    ) != 4:
        return False

    sizes = sorted(
        len(members)
        for members in (
            classes.values()
        )
    )

    return (
        sizes
        == [2, 2, 2, 2]
    )


# ===========================================================================
# Structural controls
# ===========================================================================

def test_existing_reads_available():
    assert callable(
        READS
    )

    for read_name in (
        READ_NAMES
    ):
        assert isinstance(
            read_name,
            str,
        )


def test_all_scalar_reads_finite():
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
    test_all_scalar_reads_finite()
    test_C_and_Mr_symmetry_classes()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    states = evaluate_states()

    names = list(
        CLOSURE_WORDS.keys()
    )

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
    print("Reading Point Test 027")
    print("----------------------")
    print()

    print(
        "Existing full-frame scalar "
        "instruments -> natural quotient search"
    )

    print()
    print("Source:")
    print(
        FULLF_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print("Existing scalar reads:")
    print(
        ", ".join(
            READ_NAMES
        )
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
        f"n={CFG['n']}"
        f"  delta={CFG['delta']}"
        f"  h={CFG['h']}"
    )

    print()
    print("Result-023 field closure:")
    print(
        "C2^3-like, 8 transformations"
    )

    print()
    print("Per-transformation C sign:")
    print()

    for name in names:
        print(
            f"{name:8s}"
            f" C="
            f"{states[name]['C_sign']['label']}"
        )

    print()
    print("Repository-native scalar triplets:")
    print()

    for key in candidate_keys:
        read_name, half_key = key

        print(
            f"[{read_name}.{half_key}]"
        )

        for name in names:
            sig = states[
                name
            ][
                "scalars"
            ][key]

            print(
                f"{name:8s} "
                f"["
                f"{sig[0]:+.9e}, "
                f"{sig[1]:+.9e}, "
                f"{sig[2]:+.9e}"
                f"]"
            )

        print()

    print(
        "Per-scalar class analysis:"
    )
    print()

    candidate_results = {}

    for key in candidate_keys:
        read_name, half_key = key

        (
            class_of,
            classes,
        ) = cluster_for_scalar(
            states,
            key,
        )

        quotient_ok, violations = (
            quotient_compatibility(
                class_of
            )
        )

        balanced_four = (
            four_balanced_classes(
                classes
            )
        )

        candidate_results[
            key
        ] = {
            "class_of":
                class_of,
            "classes":
                classes,
            "quotient_ok":
                quotient_ok,
            "violations":
                violations,
            "balanced_four":
                balanced_four,
        }

        print(
            f"{read_name}.{half_key}:"
        )

        print(
            f"  class_count="
            f"{len(classes)}"
        )

        print(
            "  class_sizes="
            + str(
                sorted(
                    len(x)
                    for x
                    in classes.values()
                )
            )
        )

        print(
            f"  composition_compatible="
            f"{quotient_ok}"
        )

        print(
            f"  violations="
            f"{len(violations)}"
        )

        print(
            f"  four_classes_of_two="
            f"{balanced_four}"
        )

        for cls in sorted(
            classes
        ):
            print(
                f"    class {cls}: "
                + ", ".join(
                    classes[
                        cls
                    ]
                )
            )

        print()

    successful = [
        key
        for key, row in (
            candidate_results.items()
        )
        if (
            row[
                "balanced_four"
            ]
            and row[
                "quotient_ok"
            ]
        )
    ]

    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print()

    print(
        "Existing scalar instruments tested:"
    )
    print(
        len(
            candidate_keys
        )
    )

    print()
    print(
        "Natural four-class "
        "composition-compatible candidates:"
    )

    if successful:
        for read_name, half_key in (
            successful
        ):
            print(
                f"{read_name}.{half_key}"
            )
    else:
        print(
            "NONE"
        )

    print()
    print(
        "Natural four-state reduction:"
    )

    if successful:
        print(
            "SUPPORTED BY EXISTING "
            "FULL-F SCALAR INSTRUMENT(S)"
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Interpretation:")
    print()

    print(
        "Result 026 established that the full eigenframe "
        "connection/curvature fields distinguish all eight "
        "tested C2^3-like field states."
    )

    print()
    print(
        "Result 027 tests only scalar instruments already "
        "defined by the M5 full-F implementation: comp1, "
        "comp2, comp3, norm3, and basic cube-flux reads."
    )

    print()
    print(
        "Each candidate scalar is evaluated independently. "
        "No four-state pairing is selected before measurement."
    )

    if successful:
        print()
        print(
            "At least one existing scalar instrument produces "
            "four measured classes of size two whose equivalence "
            "relation respects the established composition law."
        )

        print()
        print(
            "This supports a natural four-class geometric quotient "
            "candidate. Identification of that quotient with V4, "
            "Q8/{+1,-1}, or Reading Point still requires a separate "
            "structural correspondence test."
        )

    else:
        print()
        print(
            "None of the tested existing full-F scalar instruments "
            "produces a four-class composition-compatible reduction "
            "under the preregistered equivalence rule."
        )

        print()
        print(
            "Therefore the repository-native full-F scalars do not "
            "yet select a unique four-state reduction from the "
            "eight-state geometric structure."
        )

    print()
    print("Unique V4 selection:")
    print(
        "NOT ESTABLISHED"
    )

    print()
    print(
        "Q8/{+1,-1} identification:"
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
