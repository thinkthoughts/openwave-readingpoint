#!/usr/bin/env python3
"""
Reading Point Test 035
======================

M5 right-handed full-frame orientation anchor -> N4 C-sign audit.

Background
----------

Result 034 reduced the Reading Point <-> M5 bridge to two equally valid
partition-preserving quotient isomorphisms:

    Mapping A:
        C-sign = chi3

    Mapping B:
        C-sign = -chi3

No independent cross-system sign convention selected one.

A repository search then identified an existing M5 orientation convention
in:

    m5_22_4_a_fullf.py

The full eigenframe is constructed as

    e3 = oriented long axis
    e1 = oriented short axis
    e2 = e3 x e1
    O  = [e1, e2, e3]

and is explicitly right-handed by construction.

Question
--------

Does this pre-existing right-handed M5 frame convention provide an
orientation anchor for the N4 chiral-overlap sign C?

Important implementation rule
-----------------------------

We must NOT test this by merely swapping columns of O after C has already
been computed.

That would alter a derived frame label without applying a transformation
to the underlying tensor fields.

Instead this test applies an ACTUAL IMPROPER SPATIAL TRANSFORMATION to
the underlying N3/N4 rank-2 M fields:

    R_x:
        x -> -x

        M_sp'(x) = S_x M_sp(S_x x) S_x^T

        S_x = diag(-1,+1,+1)

with det(S_x) = -1.

Then we recompute, independently:

    1. the existing full eigenframe O(M');
    2. det(O);
    3. the existing N4 chiral-overlap matrix C.

This asks whether:

    spatial orientation reversal
        ->
    a definite change in C-sign

while the M5 full-frame implementation re-establishes its native
right-handed frame convention.

Controls
--------

A. Native fields

B. Actual x-reflected underlying fields

For each flavour field:

    det(O_native)
    det(O_reflected)

should remain approximately +1 if full_frame() enforces the repository's
right-handed convention.

The C observable is then compared directly:

    even error:
        ||C_ref - C|| / ||C||

    odd error:
        ||C_ref + C|| / ||C||

Success criterion for a C-sign anchor
-------------------------------------

A right-handed full-frame orientation anchor for C would require that the
actual improper spatial transformation induce a reproducible C-sign
reversal tied to the frame orientation convention.

Specifically:

    full frames remain right-handed;
    AND
    C_ref ~= -C.

If instead:

    full frames remain right-handed;
    AND
    C_ref ~= +C,

then the right-handed full-frame convention does NOT determine C-sign.

That outcome would reproduce and sharpen Result 020:

    direct spatial parity of C is approximately even

and would show that the C-sign used in Result 032 is associated with the
composite orientation/flavour transformation rather than with the
right-handed M5 full-frame convention alone.

No Reading Point chi3 value is used anywhere in this test.
No cross-system sign assignment is imposed.
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

DET_TOL = 1.0e-10

C_SIGN_TOL = 1.0e-4

ANTISYM_TOL = 1.0e-10


# ===========================================================================
# Existing full-frame implementation
# ===========================================================================

def load_fullf_module():
    if not FULLF_PATH.exists():
        raise FileNotFoundError(
            f"Expected existing full-frame source not found: "
            f"{FULLF_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "m5_22_4_a_fullf_for_rp035",
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
    None,
)

if not callable(
    FULL_FRAME
):
    raise RuntimeError(
        "Existing full_frame(M) function not found"
    )


# ===========================================================================
# Generic helpers
# ===========================================================================

def matrix_norm(A):
    return float(
        np.linalg.norm(
            np.asarray(
                A,
                dtype=float,
            )
        )
    )


def relative_error(
    A,
    B,
):
    A = np.asarray(
        A,
        dtype=float,
    )

    B = np.asarray(
        B,
        dtype=float,
    )

    den = max(
        matrix_norm(A),
        matrix_norm(B),
        1.0,
    )

    return float(
        matrix_norm(
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
# N3/N4 reference flavour geometry
# ===========================================================================

def build_displacements():
    """
    Same reference geometry used throughout Results 018-034.
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
# Convert N3/N4 displacement field -> M5 spatial M
# ===========================================================================

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
            f"Expected 3x3 spatial tensor field, "
            f"got {Msp.shape}"
        )

    if not np.all(
        np.isfinite(
            Msp
        )
    ):
        raise RuntimeError(
            "Non-finite spatial M field"
        )

    return Msp


# ===========================================================================
# Actual spatial reflection
# ===========================================================================

def reflection_matrix_x():
    """
    Improper spatial transformation:

        x -> -x

    det(Sx) = -1.
    """

    return np.diag(
        [
            -1.0,
            +1.0,
            +1.0,
        ]
    )


def reflect_field_x(F):
    """
    Apply the same actual spatial reflection used in Result 020.

        M_sp'(x) = S M_sp(Sx) S^T

    The x lattice axis is reversed, and the spatial rank-2 tensor
    components are transformed covariantly.
    """

    S = reflection_matrix_x()

    # N3/N4 field shape is expected to be:
    #
    #     (Nx, Ny, Nz, 4, 4)
    #
    # Reverse the x coordinate.
    Fr = F[
        ::-1,
        ...,
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


def reflect_fields_x(fields):
    return [
        reflect_field_x(
            F
        )
        for F in fields
    ]


# ===========================================================================
# Existing N4 C
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


# ===========================================================================
# Full-frame diagnostics
# ===========================================================================

def full_frame_for_field(dM):
    Msp = displacement_to_spatial_M(
        dM
    )

    result = FULL_FRAME(
        Msp
    )

    if isinstance(
        result,
        tuple,
    ):
        O = result[0]

        extras = result[1:]
    else:
        O = result
        extras = ()

    O = np.asarray(
        O,
        dtype=float,
    )

    if (
        O.shape[-2:]
        != (3, 3)
    ):
        raise RuntimeError(
            f"Unexpected full-frame shape: {O.shape}"
        )

    if not np.all(
        np.isfinite(
            O
        )
    ):
        raise RuntimeError(
            "Non-finite full eigenframe"
        )

    dets = np.linalg.det(
        O
    )

    if not np.all(
        np.isfinite(
            dets
        )
    ):
        raise RuntimeError(
            "Non-finite full-frame determinants"
        )

    return {
        "O":
            O,
        "determinants":
            dets,
        "det_min":
            float(
                np.min(
                    dets
                )
            ),
        "det_mean":
            float(
                np.mean(
                    dets
                )
            ),
        "det_max":
            float(
                np.max(
                    dets
                )
            ),
        "max_abs_det_minus_one":
            float(
                np.max(
                    np.abs(
                        dets - 1.0
                    )
                )
            ),
        "extra":
            extras,
    }


def full_frame_triplet(fields):
    return [
        full_frame_for_field(
            F
        )
        for F in fields
    ]


# ===========================================================================
# Orientation-reversed frame-only negative control
# ===========================================================================

def reverse_frame_orientation(O):
    """
    Derived control only.

    Swap e1 and e2 after the full frame has been constructed:

        O_rev = [e2,e1,e3]

    This produces det(O_rev) = -det(O).

    IMPORTANT:

    This control is NOT used to recompute C.

    It exists only to verify that determinant sign behaves as expected
    under a literal frame-orientation reversal. Since C is defined from
    the underlying tensor fields rather than O, changing O alone would
    not constitute a physical/tensor transformation.
    """

    O = np.asarray(
        O,
        dtype=float,
    )

    Orev = O.copy()

    Orev[
        ...,
        :,
        0,
    ] = O[
        ...,
        :,
        1,
    ]

    Orev[
        ...,
        :,
        1,
    ] = O[
        ...,
        :,
        0,
    ]

    return Orev


# ===========================================================================
# Structural tests
# ===========================================================================

def test_reflection_matrix_is_improper():
    S = reflection_matrix_x()

    assert abs(
        np.linalg.det(S)
        + 1.0
    ) < DET_TOL


def test_native_full_frames_right_handed():
    fields = build_displacements()

    frames = full_frame_triplet(
        fields
    )

    for row in frames:
        assert (
            row[
                "max_abs_det_minus_one"
            ]
            < DET_TOL
        )


def test_reflected_full_frames_right_handed():
    fields = build_displacements()

    reflected = reflect_fields_x(
        fields
    )

    frames = full_frame_triplet(
        reflected
    )

    for row in frames:
        assert (
            row[
                "max_abs_det_minus_one"
            ]
            < DET_TOL
        )


def test_frame_swap_flips_determinant():
    fields = build_displacements()

    frames = full_frame_triplet(
        fields
    )

    for row in frames:
        O = row[
            "O"
        ]

        Orev = reverse_frame_orientation(
            O
        )

        det_native = np.linalg.det(
            O
        )

        det_reversed = np.linalg.det(
            Orev
        )

        err = np.max(
            np.abs(
                det_reversed
                + det_native
            )
        )

        assert (
            err
            < DET_TOL
        )


def test_C_antisymmetric_native_and_reflected():
    fields = build_displacements()

    reflected = reflect_fields_x(
        fields
    )

    C = chiral_matrix(
        fields
    )

    Cref = chiral_matrix(
        reflected
    )

    assert (
        antisymmetry_error(
            C
        )
        < ANTISYM_TOL
    )

    assert (
        antisymmetry_error(
            Cref
        )
        < ANTISYM_TOL
    )


def run_all():
    test_reflection_matrix_is_improper()
    test_native_full_frames_right_handed()
    test_reflected_full_frames_right_handed()
    test_frame_swap_flips_determinant()
    test_C_antisymmetric_native_and_reflected()


# ===========================================================================
# Main report
# ===========================================================================

def main():
    run_all()

    fields = build_displacements()

    reflected = reflect_fields_x(
        fields
    )

    native_frames = full_frame_triplet(
        fields
    )

    reflected_frames = full_frame_triplet(
        reflected
    )

    C = chiral_matrix(
        fields
    )

    Cref = chiral_matrix(
        reflected
    )

    even_error = relative_error(
        Cref,
        C,
    )

    odd_error = relative_error(
        Cref,
        -C,
    )

    C_even = (
        even_error
        <= C_SIGN_TOL
    )

    C_odd = (
        odd_error
        <= C_SIGN_TOL
    )

    S = reflection_matrix_x()

    print()
    print("Reading Point Test 035")
    print("----------------------")
    print()

    print(
        "M5 right-handed full-frame orientation "
        "anchor -> N4 C-sign audit"
    )

    print()
    print("Candidate M5 orientation anchor:")
    print()

    print(
        "m5_22_4_a_fullf.py"
    )

    print()
    print(
        "e3 = oriented long axis"
    )

    print(
        "e1 = oriented short axis"
    )

    print(
        "e2 = e3 x e1"
    )

    print(
        "O  = [e1,e2,e3]"
    )

    print()
    print(
        "Declared frame convention:"
    )
    print(
        "RIGHT-HANDED BY CONSTRUCTION"
    )

    print()
    print("=" * 72)
    print("Improper spatial transformation")
    print("=" * 72)
    print()

    print(
        "R_x:"
    )

    print(
        "x -> -x"
    )

    print(
        "M_sp'(x) = S_x M_sp(S_x x) S_x^T"
    )

    print()
    print(
        "S_x ="
    )

    print(
        S
    )

    print()
    print(
        "det(S_x):"
    )

    print(
        f"{np.linalg.det(S):+.12f}"
    )

    print()
    print(
        "Improper transformation:"
    )

    print(
        "SUPPORTED"
        if abs(
            np.linalg.det(S)
            + 1.0
        ) < DET_TOL
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Native full-frame handedness")
    print("=" * 72)
    print()

    flavour_names = (
        "e",
        "mu",
        "tau",
    )

    for name, row in zip(
        flavour_names,
        native_frames,
    ):
        print(
            f"{name:4s}"
            f" det_min={row['det_min']:+.12e}"
            f" det_mean={row['det_mean']:+.12e}"
            f" det_max={row['det_max']:+.12e}"
            f" max|det-1|="
            f"{row['max_abs_det_minus_one']:.3e}"
        )

    native_right_handed = all(
        row[
            "max_abs_det_minus_one"
        ]
        < DET_TOL
        for row in native_frames
    )

    print()
    print(
        "Native full frames right-handed:"
    )

    print(
        "SUPPORTED"
        if native_right_handed
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Reflected-field full-frame handedness")
    print("=" * 72)
    print()

    for name, row in zip(
        flavour_names,
        reflected_frames,
    ):
        print(
            f"{name:4s}"
            f" det_min={row['det_min']:+.12e}"
            f" det_mean={row['det_mean']:+.12e}"
            f" det_max={row['det_max']:+.12e}"
            f" max|det-1|="
            f"{row['max_abs_det_minus_one']:.3e}"
        )

    reflected_right_handed = all(
        row[
            "max_abs_det_minus_one"
        ]
        < DET_TOL
        for row in reflected_frames
    )

    print()
    print(
        "Reflected-field full frames right-handed:"
    )

    print(
        "SUPPORTED"
        if reflected_right_handed
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Interpretation:"
    )
    print()

    print(
        "The underlying tensor fields experienced an "
        "orientation-reversing spatial transformation."
    )

    print()
    print(
        "The existing full_frame implementation then "
        "reconstructed a right-handed eigenframe from "
        "the transformed tensors."
    )

    print()
    print("=" * 72)
    print("Derived frame-reversal control")
    print("=" * 72)
    print()

    frame_flip_errors = []

    reversed_det_ranges = []

    for name, row in zip(
        flavour_names,
        native_frames,
    ):
        O = row[
            "O"
        ]

        Orev = reverse_frame_orientation(
            O
        )

        det_native = np.linalg.det(
            O
        )

        det_reversed = np.linalg.det(
            Orev
        )

        err = float(
            np.max(
                np.abs(
                    det_reversed
                    + det_native
                )
            )
        )

        frame_flip_errors.append(
            err
        )

        reversed_det_ranges.append(
            (
                float(
                    np.min(
                        det_reversed
                    )
                ),
                float(
                    np.mean(
                        det_reversed
                    )
                ),
                float(
                    np.max(
                        det_reversed
                    )
                ),
            )
        )

        print(
            f"{name:4s}"
            f" reversed_det_min="
            f"{np.min(det_reversed):+.12e}"
            f" reversed_det_mean="
            f"{np.mean(det_reversed):+.12e}"
            f" reversed_det_max="
            f"{np.max(det_reversed):+.12e}"
            f" sign_flip_error="
            f"{err:.3e}"
        )

    print()
    print(
        "Literal e1<->e2 frame swap flips det(O):"
    )

    print(
        "SUPPORTED"
        if max(
            frame_flip_errors
        )
        < DET_TOL
        else "NOT SUPPORTED"
    )

    print()
    print(
        "This frame-only control is NOT used to compute C."
    )

    print()
    print(
        "It verifies the determinant convention only."
    )

    print()
    print("=" * 72)
    print("N4 C response to actual spatial reflection")
    print("=" * 72)
    print()

    print("Native C:")
    print()

    print(
        np.array2string(
            C,
            precision=6,
            suppress_small=True,
        )
    )

    print()
    print("Reflected C:")
    print()

    print(
        np.array2string(
            Cref,
            precision=6,
            suppress_small=True,
        )
    )

    print()
    print(
        "C antisymmetry:"
    )

    print(
        f"native="
        f"{antisymmetry_error(C):.3e}"
        f" reflected="
        f"{antisymmetry_error(Cref):.3e}"
    )

    print()
    print(
        "evenness error "
        "||C_ref-C|| / ||C||:"
    )

    print(
        f"{even_error:.6e}"
    )

    print()
    print(
        "oddness error "
        "||C_ref+C|| / ||C||:"
    )

    print(
        f"{odd_error:.6e}"
    )

    print()
    print(
        "C invariant under actual spatial reflection:"
    )

    print(
        "SUPPORTED"
        if C_even
        else "NOT SUPPORTED"
    )

    print()
    print(
        "C sign-reversing under actual spatial reflection:"
    )

    print(
        "SUPPORTED"
        if C_odd
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Orientation-anchor verdict")
    print("=" * 72)
    print()

    anchor_supported = (
        native_right_handed
        and
        reflected_right_handed
        and
        C_odd
    )

    anchor_rejected = (
        native_right_handed
        and
        reflected_right_handed
        and
        C_even
        and
        not C_odd
    )

    print(
        "Native M5 right-handed frame convention:"
    )

    print(
        "SUPPORTED"
        if (
            native_right_handed
            and reflected_right_handed
        )
        else "NOT SUPPORTED"
    )

    print()
    print(
        "C sign anchored by that full-frame handedness:"
    )

    if anchor_supported:
        print(
            "SUPPORTED"
        )

    elif anchor_rejected:
        print(
            "NOT SUPPORTED"
        )

    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Interpretation:")
    print()

    if anchor_supported:
        print(
            "The actual orientation-reversing spatial "
            "transformation reverses C while the existing "
            "full-frame machinery restores its native "
            "right-handed frame convention."
        )

        print()
        print(
            "This supports a link between the native M5 "
            "orientation convention and the Result-032 C sign."
        )

    elif anchor_rejected:
        print(
            "The actual orientation-reversing spatial "
            "transformation leaves C approximately invariant, "
            "even though the underlying spatial transformation "
            "has determinant -1."
        )

        print()
        print(
            "The full_frame implementation reconstructs a "
            "right-handed frame both before and after reflection."
        )

        print()
        print(
            "Therefore the repository's right-handed full-frame "
            "convention does not by itself determine the sign "
            "of the Result-032 C discriminator."
        )

        print()
        print(
            "This is consistent with the earlier finding that "
            "C sign reversal belongs to the composite "
            "orientation/flavour operation rather than to "
            "direct spatial parity alone."
        )

    else:
        print(
            "The tested relation does not establish a clean "
            "C-sign anchor from the full-frame handedness."
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
        "Does Result 035 license C-sign = chi3?"
    )
    print(
        "NO"
    )

    print()
    print(
        "Does Result 035 license C-sign = -chi3?"
    )
    print(
        "NO"
    )

    print()
    print(
        "Result-035 cross-system correspondence count:"
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

    print()
    print("PASS")


if __name__ == "__main__":
    main()
