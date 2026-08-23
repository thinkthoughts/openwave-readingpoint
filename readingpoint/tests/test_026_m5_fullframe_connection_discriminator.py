#!/usr/bin/env python3
"""
Reading Point Test 026
======================

Existing M -> eigenframe -> connection/curvature discriminator.

Result 025 reached a stopping boundary for the specifically examined path

    M -> (q0, q) -> Gamma/R

because no implemented M -> (q0,q) projection was found.

A subsequent repository-wide search found a different existing M5 route:

    m5_22_4_a_fullf.py

which explicitly constructs

    O(x) = oriented full eigenframe of M(x)

and then

    Gamma_i = O^T d_i O

with rotation-vector representation

    G_i = ((Gamma_i)_32, (Gamma_i)_13, (Gamma_i)_21)

and curvature-vector structure

    R_ij = G_i x G_j.

Thus Result 026 does NOT invent an M -> q projection.

It tests the independently implemented route

    M -> O(M) -> Gamma -> G -> R

on the eight Result-023 flavour-field transformations:

    I
    Tx
    Ty
    Tz
    TxTy
    TxTz
    TyTz
    TxTyTz

Result 024 left two unresolved effective classes:

    K+ = {I, Ty, Tz, TyTz}
    K- = {Tx, TxTy, TxTz, TxTyTz}

The question is:

    Does the existing full-eigenframe connection/curvature machinery
    distinguish states inside either four-element kernel?

Primary observables:

    normalized G field
    normalized R field

where R contains the three pair curvatures

    R_xy
    R_xz
    R_yz.

The test does not fit a classifier and does not preselect a V4 subgroup.

If connection/curvature adds discrimination, the measured joint partition
is checked against the already established C2^3-like composition law.

No Reading Point -> M5 mapping is assumed.
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
DX = 1.0

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

# Preregistered equivalence threshold for normalized connection/curvature
# fields. This is not selected from observed clustering.
GEOM_EQUIV_TOL = 1e-4

ANTISYM_TOL = 1e-10
SYM_TOL = 1e-10


# ===========================================================================
# Load existing full-frame implementation
# ===========================================================================

def load_fullf_module():
    if not FULLF_PATH.exists():
        raise FileNotFoundError(
            f"Existing full-frame source not found: {FULLF_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "m5_22_4_a_fullf_for_rp026",
        FULLF_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Could not load m5_22_4_a_fullf.py"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

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


FULL_FRAME = require_existing_function(
    "full_frame"
)

GAMMA_VECS = require_existing_function(
    "gamma_vecs"
)


# ===========================================================================
# Generic helpers
# ===========================================================================

def frobenius_norm(A):
    return float(
        np.linalg.norm(A)
    )


def normalized_field(A):
    n = frobenius_norm(A)

    if (
        not np.isfinite(n)
        or n <= 1e-30
    ):
        raise ValueError(
            "zero or non-finite field norm"
        )

    return A / n


def relative_error(A, B):
    den = max(
        frobenius_norm(B),
        1e-30,
    )

    return float(
        frobenius_norm(A - B)
        / den
    )


def symmetry_error(A):
    scale = max(
        float(np.max(np.abs(A))),
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
        float(np.max(np.abs(A))),
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
# Original N4 flavour fields
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


def reflect_fields(fields, axis):
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


def apply_word(fields, word):
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
# N4 C and Mr
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

    Mr = K + KAPPA * P

    return Mr


def classify_C_sign(Ct, C0):
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
# M -> full eigenframe -> Gamma vectors
# ===========================================================================

def displacement_to_full_M(dM):
    """
    full_frame() expects an M field, not a displacement.

    The N4 displacement fields are defined relative to the same vacuum.
    Reconstruct the actual field before extracting its eigenframe.
    """

    Mvac = biaxial_vacuum(
        N,
        DELTA,
    )

    return dM + Mvac


def connection_geometry_for_field(dM):
    """
    Existing M5 route:

        rank-2 M field
        -> spatial 3x3 block M_sp
        -> full_frame(M_sp)
        -> gamma_vecs(O, h)

    The N3/N4 field is 4x4 because index 0 carries the g/time-like
    component. m5_22_4_a_fullf.full_frame() constructs an SO(3)
    eigenframe and therefore acts on the spatial 3x3 block only.
    """

    M = displacement_to_full_M(
        dM
    )

    # The existing full-frame machinery is spatial SO(3), not the full
    # 4x4 M5 matrix. Passing the 4x4 field makes full_frame() produce
    # four-component eigenvectors, which are incompatible with np.cross().
    Msp = M[
        ...,
        1:4,
        1:4,
    ]

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

    O = np.asarray(O)

    # Explicit interface guard: the existing routine should return a field
    # of spatial 3x3 frames.
    if (
        O.ndim < 2
        or O.shape[-2:] != (3, 3)
    ):
        raise RuntimeError(
            "full_frame(M_sp) did not return a spatial 3x3 "
            f"eigenframe; got shape {O.shape}"
        )

    # Do not regularize or mask a non-finite eigenframe here. If the
    # existing full_frame() convention is undefined at degenerate cells,
    # that is a scientific/interface result to inspect rather than hide.
    if not np.all(
        np.isfinite(O)
    ):
        raise RuntimeError(
            "full_frame(M_sp) returned non-finite values; "
            "inspect eigenframe degeneracy/orientation handling before "
            "introducing any regularization"
        )

    G = GAMMA_VECS(
        O,
        DX,
    )

    # Accept the existing implementation as either a sequence of three
    # vector fields or an ndarray whose leading axis labels x,y,z.
    if isinstance(
        G,
        (list, tuple),
    ):
        if len(G) != 3:
            raise RuntimeError(
                "gamma_vecs() did not return three spatial components"
            )

        Gx, Gy, Gz = [
            np.asarray(x)
            for x in G
        ]

    else:
        G = np.asarray(G)

        if (
            G.ndim < 1
            or G.shape[0] != 3
        ):
            raise RuntimeError(
                "gamma_vecs() ndarray does not have leading size 3; "
                f"got shape {G.shape}"
            )

        Gx, Gy, Gz = (
            G[0],
            G[1],
            G[2],
        )

    # Each connection-vector field must itself be a 3-vector field.
    for label, Gi in (
        ("Gx", Gx),
        ("Gy", Gy),
        ("Gz", Gz),
    ):
        if (
            Gi.ndim < 1
            or Gi.shape[-1] != 3
        ):
            raise RuntimeError(
                f"{label} is not a 3-vector field; got shape {Gi.shape}"
            )

    # Existing curvature-vector construction:
    #
    #     R_ij = G_i x G_j
    #
    # Retain the three independent pair curvatures.
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

    if not np.all(
        np.isfinite(Gstack)
    ):
        raise RuntimeError(
            "full-frame connection contains non-finite values"
        )

    if not np.all(
        np.isfinite(Rstack)
    ):
        raise RuntimeError(
            "full-frame curvature contains non-finite values"
        )

    return {
        "O": O,
        "G": Gstack,
        "R": Rstack,
        "G_hat": normalized_field(
            Gstack
        ),
        "R_hat": normalized_field(
            Rstack
        ),
        "G_norm": frobenius_norm(
            Gstack
        ),
        "R_norm": frobenius_norm(
            Rstack
        ),
    }


def geometry_for_flavour_triplet(fields):
    """
    Evaluate each of the three flavour fields independently and retain the
    ordered flavour triplet.

    This avoids inventing a new flavour-space contraction.
    """

    rows = [
        connection_geometry_for_field(
            F
        )
        for F in fields
    ]

    G_triplet = np.stack(
        [
            row["G"]
            for row in rows
        ],
        axis=0,
    )

    R_triplet = np.stack(
        [
            row["R"]
            for row in rows
        ],
        axis=0,
    )

    return {
        "per_flavour": rows,
        "G_triplet": G_triplet,
        "R_triplet": R_triplet,
        "G_triplet_hat":
            normalized_field(
                G_triplet
            ),
        "R_triplet_hat":
            normalized_field(
                R_triplet
            ),
        "G_triplet_norm":
            frobenius_norm(
                G_triplet
            ),
        "R_triplet_norm":
            frobenius_norm(
                R_triplet
            ),
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

        Mr = real_matrix(
            fields
        )

        geom = geometry_for_flavour_triplet(
            fields
        )

        states[name] = {
            "fields": fields,
            "C": C,
            "Mr": Mr,
            "geom": geom,
            "C_anti":
                antisymmetry_error(C),
            "Mr_sym":
                symmetry_error(Mr),
        }

    C0 = states["I"]["C"]

    for name in states:
        states[name]["C_sign"] = (
            classify_C_sign(
                states[name]["C"],
                C0,
            )
        )

    return states


# ===========================================================================
# Geometry distances
# ===========================================================================

def G_distance(A, B):
    return frobenius_norm(
        A["geom"]["G_triplet_hat"]
        - B["geom"]["G_triplet_hat"]
    )


def R_distance(A, B):
    return frobenius_norm(
        A["geom"]["R_triplet_hat"]
        - B["geom"]["R_triplet_hat"]
    )


def geometric_equivalent(
    name_a,
    name_b,
    states,
):
    """
    Existing-geometry equivalence:

      same C sign
      AND normalized G distance <= threshold
      AND normalized R distance <= threshold

    Mr is omitted from the condition because Result 024 established that it
    is invariant across the tested closure.
    """

    sa = states[name_a][
        "C_sign"
    ]["label"]

    sb = states[name_b][
        "C_sign"
    ]["label"]

    if (
        sa not in ("+", "-")
        or sb not in ("+", "-")
    ):
        return False

    if sa != sb:
        return False

    return (
        G_distance(
            states[name_a],
            states[name_b],
        )
        <= GEOM_EQUIV_TOL
        and
        R_distance(
            states[name_a],
            states[name_b],
        )
        <= GEOM_EQUIV_TOL
    )


# ===========================================================================
# Joint clustering
# ===========================================================================

def cluster_joint(states):
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
            if geometric_equivalent(
                name,
                rep,
                states,
            ):
                class_of[name] = idx
                assigned = True
                break

        if not assigned:
            class_of[name] = len(
                reps
            )
            reps.append(name)

    classes = {}

    for name, cls in (
        class_of.items()
    ):
        classes.setdefault(
            cls,
            [],
        ).append(name)

    return (
        reps,
        class_of,
        classes,
    )


# ===========================================================================
# Quotient compatibility
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
        len(violations) == 0,
        violations,
    )


# ===========================================================================
# Structural tests
# ===========================================================================

def test_existing_fullframe_functions_available():
    assert callable(
        FULL_FRAME
    )

    assert callable(
        GAMMA_VECS
    )


def test_all_states_finite():
    states = evaluate_states()

    for row in states.values():
        geom = row["geom"]

        for key in (
            "G_triplet",
            "R_triplet",
            "G_triplet_hat",
            "R_triplet_hat",
        ):
            assert np.all(
                np.isfinite(
                    geom[key]
                )
            )


def test_C_and_Mr_symmetry_classes():
    states = evaluate_states()

    for row in states.values():
        assert (
            row["C_anti"]
            < ANTISYM_TOL
        )

        assert (
            row["Mr_sym"]
            < SYM_TOL
        )


def run_all():
    test_existing_fullframe_functions_available()
    test_all_states_finite()
    test_C_and_Mr_symmetry_classes()


# ===========================================================================
# Reporting
# ===========================================================================

def main():
    run_all()

    states = evaluate_states()

    names = list(
        CLOSURE_WORDS.keys()
    )

    print()
    print("Reading Point Test 026")
    print("----------------------")
    print()

    print(
        "Existing M -> full eigenframe -> "
        "connection/curvature discriminator"
    )
    print()

    print("Existing implementation:")
    print()
    print(
        "source:",
        FULLF_PATH.relative_to(
            REPO_ROOT
        ),
    )
    print(
        "full_frame(M): FOUND"
    )
    print(
        "gamma_vecs(O, h): FOUND"
    )

    print()
    print("Implemented route:")
    print()
    print(
        "M -> O(M) -> Gamma_i -> "
        "G_i -> R_ij"
    )

    print()
    print("Result-024 unresolved classes:")
    print()
    print(
        "K+ = {I, Ty, Tz, TyTz}"
    )
    print(
        "K- = {Tx, TxTy, TxTz, TxTyTz}"
    )

    print()
    print("Per-transformation readout:")
    print()

    for name in names:
        row = states[name]
        geom = row["geom"]
        cs = row["C_sign"]

        print(
            f"{name:8s}"
            f" C={cs['label']}"
            f" ||G||={geom['G_triplet_norm']:.6e}"
            f" ||R||={geom['R_triplet_norm']:.6e}"
            f" C_anti={row['C_anti']:.3e}"
            f" Mr_sym={row['Mr_sym']:.3e}"
        )

    print()
    print(
        "Pairwise normalized-G distances:"
    )
    print()

    for i in range(len(names)):
        for j in range(
            i + 1,
            len(names),
        ):
            a = names[i]
            b = names[j]

            print(
                f"{a:8s}-{b:8s}: "
                f"{G_distance(states[a], states[b]):.6e}"
            )

    print()
    print(
        "Pairwise normalized-R distances:"
    )
    print()

    for i in range(len(names)):
        for j in range(
            i + 1,
            len(names),
        ):
            a = names[i]
            b = names[j]

            print(
                f"{a:8s}-{b:8s}: "
                f"{R_distance(states[a], states[b]):.6e}"
            )

    print()
    print(
        "Discrimination inside equal-C-sign sectors:"
    )
    print()

    same_sign_pairs = 0
    G_separated = 0
    R_separated = 0
    either_separated = 0

    for i in range(len(names)):
        for j in range(
            i + 1,
            len(names),
        ):
            a = names[i]
            b = names[j]

            sa = states[a][
                "C_sign"
            ]["label"]

            sb = states[b][
                "C_sign"
            ]["label"]

            if (
                sa not in ("+", "-")
                or sa != sb
            ):
                continue

            same_sign_pairs += 1

            gd = G_distance(
                states[a],
                states[b],
            )

            rd = R_distance(
                states[a],
                states[b],
            )

            gs = (
                gd
                > GEOM_EQUIV_TOL
            )

            rs = (
                rd
                > GEOM_EQUIV_TOL
            )

            if gs:
                G_separated += 1

            if rs:
                R_separated += 1

            if gs or rs:
                either_separated += 1

            print(
                f"{a:8s} vs {b:8s}"
                f" C={sa}"
                f" G_dist={gd:.6e}"
                f" R_dist={rd:.6e}"
                f" separated={gs or rs}"
            )

    print()
    print("Equal-C-sign pair totals:")
    print()
    print(
        f"pairs = {same_sign_pairs}"
    )
    print(
        f"G separates = "
        f"{G_separated}/{same_sign_pairs}"
    )
    print(
        f"R separates = "
        f"{R_separated}/{same_sign_pairs}"
    )
    print(
        f"G or R separates = "
        f"{either_separated}/{same_sign_pairs}"
    )

    (
        reps,
        class_of,
        classes,
    ) = cluster_joint(
        states
    )

    print()
    print("Joint C + full-frame geometry classes:")
    print()
    print(
        f"class count = {len(classes)}"
    )

    for cls in sorted(
        classes
    ):
        print(
            f"class {cls}: "
            + ", ".join(
                classes[cls]
            )
        )

    quotient_ok, violations = (
        quotient_compatibility(
            class_of
        )
    )

    print()
    print("Composition compatibility:")
    print()

    if quotient_ok:
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED")

    print(
        f"violations = {len(violations)}"
    )

    print()
    print("Observable result:")
    print()

    if either_separated == 0:
        print(
            "FULL-FRAME CONNECTION/CURVATURE "
            "ADDS NO INDEPENDENT DISCRIMINATION"
        )

    elif (
        len(classes) == 4
        and quotient_ok
    ):
        print(
            "FOUR-CLASS COMPOSITION-COMPATIBLE "
            "GEOMETRIC READOUT SUPPORTED"
        )

    elif (
        len(classes) == 8
        and quotient_ok
    ):
        print(
            "EIGHT-CLASS COMPOSITION-COMPATIBLE "
            "GEOMETRIC READOUT SUPPORTED"
        )

    else:
        print(
            "GEOMETRIC SECTOR ADDS DISCRIMINATION, "
            "BUT NO SIMPLE FOUR-CLASS QUOTIENT "
            "IS ESTABLISHED"
        )

    print()
    print("Interpretation:")
    print()

    print(
        "Unlike Result 025's q0,q path, this test uses an "
        "existing M5 implementation that begins directly from M."
    )

    print()
    print(
        "The oriented full eigenframe O(M), connection vectors G_i, "
        "and curvature vectors R_ij are evaluated on the same eight "
        "Result-023 transformed N3/N4 flavour-field states."
    )

    print()
    print(
        "No M -> q conversion and no new flavour-space contraction "
        "is introduced."
    )

    print()
    print("Unique V4 selection:")
    print()

    if (
        len(classes) == 4
        and quotient_ok
    ):
        print(
            "A FOUR-CLASS GEOMETRIC QUOTIENT IS OBSERVED; "
            "IDENTIFICATION WITH A PARTICULAR V4 OR Q8 QUOTIENT "
            "REQUIRES A SEPARATE STRUCTURAL TEST"
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Q8/{+1,-1} identification:")
    print()
    print("NOT ESTABLISHED")

    print()
    print("Reading Point -> M5 physical mapping:")
    print()
    print("NOT ESTABLISHED")

    print()
    print("PASS")


if __name__ == "__main__":
    main()
