#!/usr/bin/env python3
"""
Reading Point Test 038
======================

Native M5 signed Mermin-Ho / topological-flux orientation -> C-sign audit.

Purpose
-------

Results 035-037 tested three existing M5/N4 sign or orientation structures:

    035  right-handed full eigenframe
    036  integer self-linking N
    037  g_chiral / chi signs

None supplied an independently implemented sign anchor for the geometric
N4 chiral-overlap matrix C used in Result 032.

Result 038 tests the strongest remaining field-derived candidate already
present in the repository:

    the signed longest-axis / Mermin-Ho "basic" flux instrument

implemented in:

    openwave/xperiments/m5_liquid_crystal/research/scripts/
        m5_22_4_a_fullf.py

This is not a new observable.

Result 027 already established that, at half6, half12, and half18, this
native scalar instrument descends exactly through

    <Ty> = {I, Ty}

and produces the four quotient classes

    Ibar      = {I, Ty}
    Txbar     = {Tx, TxTy}
    Tzbar     = {Tz, TyTz}
    TxTzbar   = {TxTz, TxTyTz}.

Result 029 further showed that the full signed flavour-triplet values
distinguish all three nonidentity quotient classes.

Question
--------

Does the SIGN information carried by this existing Mermin-Ho / topological
flux read provide a native orientation anchor for the residual M5 pair

    Tzbar
    TxTzbar

whose N4 C-sign labels are

    Tzbar      -> +C
    TxTzbar    -> -C ?

Critical distinction
--------------------

A numerical flux vector can distinguish two quotient classes without giving
them opposite topological signs.

Therefore Test 038 separates:

    A. quotient descent
    B. numerical quotient discrimination
    C. signed orientation discrimination
    D. relation to C-sign

No Reading Point residue or chi3 value enters this test.


Existing implementation
-----------------------

Reuse:

    m5_22_4_a_fullf.py

and specifically its already-defined:

    full_frame(...)
    full_F(...)
    reads(...)

The native `reads(...)` routine constructs:

    e3 = oriented longest eigen-axis
    basic = mermin_B(e3, h)

and evaluates signed cube flux at:

    half6
    half12
    half18.

Reuse the exact Result-023/026 eight-state field closure.

Do not invent a new contraction of the Mermin-Ho field.


Preregistered quotient
----------------------

    Ibar      = {I, Ty}
    Txbar     = {Tx, TxTy}
    Tzbar     = {Tz, TyTz}
    TxTzbar   = {TxTz, TxTyTz}

Kernel:

    <Ty> = {I, Ty}


Preregistered C labels
----------------------

From Result 032:

    Ibar      -> +
    Txbar     -> -
    Tzbar     -> +
    TxTzbar   -> -

These labels may be used only AFTER the independent Mermin-Ho readout has
been evaluated.


Native signed readout
---------------------

For every transformation and every flux scale, evaluate the ordered flavour
triplet:

    B_s(state) = (
        basic_e.half_s,
        basic_mu.half_s,
        basic_tau.half_s
    )

for:

    s in {6, 12, 18}.

Also report these preregistered sign summaries:

1. component sign tuple

       sign(B_s)
       =
       (sign B_e, sign B_mu, sign B_tau)

2. net signed flux

       B_net = B_e + B_mu + B_tau

3. net-flux sign

       sign(B_net)

4. orientation-insensitive magnitude control

       ||B_s||_2

Do not select a component or linear combination after seeing the result.


Quotient descent
----------------

For every quotient class and every scale, compare its two representatives.

The complete triplet is considered descended if

    ||B(a) - B(b)||_2 <= DESCENT_TOL

with preregistered:

    DESCENT_TOL = 1e-8

consistent with Results 027/029.

Also separately test whether:

    component sign tuple
    net sign

descend through the same quotient.


Residual-pair orientation test
------------------------------

The target pair is:

    Tzbar
    TxTzbar.

For each scale compare the quotient-level signed reads.

Possible outcomes:

A. OPPOSITE NATIVE SIGN

    A preregistered sign summary that descends through <Ty> gives opposite
    values on Tzbar and TxTzbar, consistently across all three scales.

B. SAME NATIVE SIGN

    All descended preregistered sign summaries give the same sign on Tzbar
    and TxTzbar, even if their numerical triplets differ.

C. MIXED / NO CLEAN SIGN RELATION

    Sign relations vary across scales or summaries.

Only outcome A supplies a candidate native topological sign anchor for the
Result-032 residual pair.


Relation to C
-------------

Only after the Mermin-Ho sign audit is complete compare with:

    Tzbar      -> +C
    TxTzbar    -> -C.

Report:

    ALIGNED
        native topological sign and C-sign distinguish the pair in the same
        binary orientation

    REVERSED
        both distinguish the pair, but with opposite orientation

    NONE
        native topological sign does not distinguish the pair

    MIXED
        no stable scale-independent relation.

Do NOT compare to Reading Point chi3 in this test.


Known limitation
----------------

The `basic` instrument is an ordered three-flavour signed-flux read.

A permutation of the mu/tau entries can numerically distinguish Tzbar and
TxTzbar while preserving the same component-sign tuple and net sign.

Such a result counts as:

    quotient discrimination: SUPPORTED
    orientation-sign anchor: NOT SUPPORTED

This distinction is central to Test 038.


Required output
---------------

Print:

1. existing implementation and exact parameter set;
2. all eight signed basic-flux triplets at half6/half12/half18;
3. quotient descent errors;
4. quotient-level component sign tuples;
5. net flux and net sign;
6. residual Tzbar vs TxTzbar numerical distances;
7. whether a native signed binary discriminator exists;
8. relation, if any, to Result-032 C-sign;
9. correspondence boundary.

Write:

    readingpoint/results/
        test_038_m5_mermin_ho_orientation_anchor/
            audit.json

A negative orientation result is still PASS if all controls and preregistered
audits execute correctly.


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

FULLF_PATH = (
    M5_SCRIPTS
    / "m5_22_4_a_fullf.py"
)

RESULT_DIR = (
    REPO_ROOT
    / "readingpoint"
    / "results"
    / "test_038_m5_mermin_ho_orientation_anchor"
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
# Load an existing Result-026 implementation for the established closure
# ===========================================================================

RESULT_026_CANDIDATES = (
    HERE
    / "test_026_m5_fullframe_connection_discriminator.py",

    HERE
    / "test_026_m5_fullframe_connection_discriminator_fixed.py",
)


def load_module(
    name: str,
    path: Path,
):
    if not path.exists():
        raise FileNotFoundError(
            f"Required source not found: {path}"
        )

    spec = importlib.util.spec_from_file_location(
        name,
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


def find_result_026():
    for path in RESULT_026_CANDIDATES:
        if path.exists():
            return path

    raise FileNotFoundError(
        "Could not find an existing Result-026 test. "
        "Expected one of:\n"
        + "\n".join(
            str(x)
            for x in RESULT_026_CANDIDATES
        )
    )


RESULT_026_PATH = (
    find_result_026()
)

R026 = load_module(
    "rp026_for_rp038",
    RESULT_026_PATH,
)

FULLF = load_module(
    "m5_22_4_a_fullf_for_rp038",
    FULLF_PATH,
)


# ===========================================================================
# Required existing interfaces
# ===========================================================================

def require_callable(
    module,
    name,
):
    fn = getattr(
        module,
        name,
        None,
    )

    if not callable(fn):
        raise RuntimeError(
            f"Expected callable {name}() "
            f"not found in {module}"
        )

    return fn


BUILD_DISPLACEMENTS = (
    require_callable(
        R026,
        "build_displacements",
    )
)

APPLY_WORD = (
    require_callable(
        R026,
        "apply_word",
    )
)

CHIRAL_MATRIX = (
    require_callable(
        R026,
        "chiral_matrix",
    )
)

CLASSIFY_C_SIGN = (
    require_callable(
        R026,
        "classify_C_sign",
    )
)

DISPLACEMENT_TO_FULL_M = (
    require_callable(
        R026,
        "displacement_to_full_M",
    )
)

FULLF_READS = (
    require_callable(
        FULLF,
        "reads",
    )
)


# ===========================================================================
# Established constants
# ===========================================================================

N = int(
    getattr(
        R026,
        "N",
        40,
    )
)

DELTA = float(
    getattr(
        R026,
        "DELTA",
        0.1,
    )
)

CLOSURE_WORDS = dict(
    getattr(
        R026,
        "CLOSURE_WORDS",
    )
)

EXPECTED_NAMES = (
    "I",
    "Tx",
    "Ty",
    "Tz",
    "TxTy",
    "TxTz",
    "TyTz",
    "TxTyTz",
)

if tuple(
    CLOSURE_WORDS.keys()
) != EXPECTED_NAMES:
    if set(
        CLOSURE_WORDS.keys()
    ) != set(
        EXPECTED_NAMES
    ):
        raise RuntimeError(
            "Result-026 closure does not contain "
            "the expected eight Result-023 states"
        )


# ===========================================================================
# Preregistered quotient
# ===========================================================================

QUOTIENT = {
    "Ibar":
        (
            "I",
            "Ty",
        ),

    "Txbar":
        (
            "Tx",
            "TxTy",
        ),

    "Tzbar":
        (
            "Tz",
            "TyTz",
        ),

    "TxTzbar":
        (
            "TxTz",
            "TxTyTz",
        ),
}

RESIDUAL_PAIR = (
    "Tzbar",
    "TxTzbar",
)

RESULT_032_C_SIGN = {
    "Ibar":
        +1,

    "Txbar":
        -1,

    "Tzbar":
        +1,

    "TxTzbar":
        -1,
}


# ===========================================================================
# Flux configuration
# ===========================================================================

FLUX_SCALES = (
    "half6",
    "half12",
    "half18",
)

DESCENT_TOL = 1.0e-8

ZERO_SIGN_TOL = 1.0e-10


def make_fullf_cfg():
    """
    Construct the same native full-F configuration used in Results 027/029.

    m5_22_4_a_fullf.py exposes its own INS and W2_T2 implementation.
    """

    INS = getattr(
        FULLF,
        "INS",
        None,
    )

    W2_T2 = getattr(
        FULLF,
        "W2_T2",
        None,
    )

    if (
        INS is None
        or W2_T2 is None
        or not hasattr(
            INS,
            "base_cfg",
        )
    ):
        raise RuntimeError(
            "Existing full-F configuration machinery "
            "INS.base_cfg / W2_T2 not found"
        )

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


CFG = make_fullf_cfg()


# ===========================================================================
# Generic helpers
# ===========================================================================

def norm(
    x,
):
    return float(
        np.linalg.norm(
            np.asarray(
                x,
                dtype=float,
            )
        )
    )


def sign_label(
    x,
    tol=ZERO_SIGN_TOL,
):
    x = float(x)

    if abs(x) <= tol:
        return "0"

    return (
        "+"
        if x > 0
        else "-"
    )


def sign_value(
    x,
    tol=ZERO_SIGN_TOL,
):
    x = float(x)

    if abs(x) <= tol:
        return 0

    return (
        +1
        if x > 0
        else -1
    )


def sign_tuple(
    values,
):
    return tuple(
        sign_value(x)
        for x in values
    )


def sign_tuple_label(
    values,
):
    return tuple(
        sign_label(x)
        for x in values
    )


# ===========================================================================
# Existing basic / Mermin-Ho read on one flavour field
# ===========================================================================

def basic_reads_for_displacement(
    dM,
):
    """
    Result-026 displacement -> actual M -> spatial 3x3 M -> existing reads().

    No new topological observable is introduced here.
    """

    M = DISPLACEMENT_TO_FULL_M(
        dM
    )

    Msp = np.asarray(
        M[
            ...,
            1:4,
            1:4,
        ],
        dtype=float,
    )

    if (
        Msp.shape[-2:]
        != (3, 3)
    ):
        raise RuntimeError(
            f"Expected spatial 3x3 M field; got {Msp.shape}"
        )

    if not np.all(
        np.isfinite(
            Msp
        )
    ):
        raise RuntimeError(
            "Non-finite spatial M field"
        )

    row = FULLF_READS(
        Msp,
        CFG,
    )

    if "basic" not in row:
        raise RuntimeError(
            "Existing full-F reads() returned no 'basic' instrument"
        )

    basic = row[
        "basic"
    ]

    out = {}

    for scale in FLUX_SCALES:
        if scale not in basic:
            raise RuntimeError(
                f"Existing basic read missing {scale}"
            )

        out[
            scale
        ] = float(
            basic[
                scale
            ]
        )

    return out


# ===========================================================================
# Evaluate eight-state closure
# ===========================================================================

def evaluate_states():
    original = (
        BUILD_DISPLACEMENTS()
    )

    states = {}

    for name in EXPECTED_NAMES:
        fields = APPLY_WORD(
            original,
            CLOSURE_WORDS[
                name
            ],
        )

        C = CHIRAL_MATRIX(
            fields
        )

        flavour_reads = [
            basic_reads_for_displacement(
                F
            )
            for F in fields
        ]

        basic_triplets = {}

        for scale in FLUX_SCALES:
            triplet = np.array(
                [
                    flavour_reads[0][scale],
                    flavour_reads[1][scale],
                    flavour_reads[2][scale],
                ],
                dtype=float,
            )

            basic_triplets[
                scale
            ] = {
                "triplet":
                    triplet,

                "norm":
                    norm(
                        triplet
                    ),

                "net":
                    float(
                        np.sum(
                            triplet
                        )
                    ),

                "net_sign":
                    sign_value(
                        np.sum(
                            triplet
                        )
                    ),

                "component_signs":
                    sign_tuple(
                        triplet
                    ),
            }

        states[
            name
        ] = {
            "fields":
                fields,

            "C":
                C,

            "basic":
                basic_triplets,
        }

    C0 = states[
        "I"
    ][
        "C"
    ]

    for name in EXPECTED_NAMES:
        states[
            name
        ][
            "C_sign"
        ] = CLASSIFY_C_SIGN(
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
    out = {}

    for qname, (
        a,
        b,
    ) in QUOTIENT.items():
        out[
            qname
        ] = {}

        for scale in FLUX_SCALES:
            A = states[
                a
            ][
                "basic"
            ][
                scale
            ]

            B = states[
                b
            ][
                "basic"
            ][
                scale
            ]

            triplet_error = norm(
                A[
                    "triplet"
                ]
                -
                B[
                    "triplet"
                ]
            )

            component_signs_equal = (
                A[
                    "component_signs"
                ]
                ==
                B[
                    "component_signs"
                ]
            )

            net_sign_equal = (
                A[
                    "net_sign"
                ]
                ==
                B[
                    "net_sign"
                ]
            )

            out[
                qname
            ][
                scale
            ] = {
                "representatives":
                    (
                        a,
                        b,
                    ),

                "triplet_error":
                    triplet_error,

                "triplet_descends":
                    (
                        triplet_error
                        <= DESCENT_TOL
                    ),

                "component_signs_equal":
                    component_signs_equal,

                "net_sign_equal":
                    net_sign_equal,

                "component_signs_descend":
                    component_signs_equal,

                "net_sign_descends":
                    net_sign_equal,
            }

    return out


def all_triplets_descend(
    descent,
):
    return all(
        descent[
            qname
        ][
            scale
        ][
            "triplet_descends"
        ]
        for qname in QUOTIENT
        for scale in FLUX_SCALES
    )


# ===========================================================================
# Quotient-level representative values
# ===========================================================================

def quotient_values(
    states,
    descent,
):
    out = {}

    for qname, (
        a,
        b,
    ) in QUOTIENT.items():
        out[
            qname
        ] = {}

        for scale in FLUX_SCALES:
            d = descent[
                qname
            ][
                scale
            ]

            if not d[
                "triplet_descends"
            ]:
                raise RuntimeError(
                    f"{qname}.{scale} does not descend; "
                    "quotient-level value is inadmissible"
                )

            # Mean is used only to suppress machine-level representative
            # differences after descent has already been established.
            A = states[
                a
            ][
                "basic"
            ][
                scale
            ][
                "triplet"
            ]

            B = states[
                b
            ][
                "basic"
            ][
                scale
            ][
                "triplet"
            ]

            v = (
                A + B
            ) / 2.0

            out[
                qname
            ][
                scale
            ] = {
                "triplet":
                    v,

                "norm":
                    norm(v),

                "net":
                    float(
                        np.sum(v)
                    ),

                "net_sign":
                    sign_value(
                        np.sum(v)
                    ),

                "component_signs":
                    sign_tuple(v),
            }

    return out


# ===========================================================================
# Residual-pair audit
# ===========================================================================

def residual_pair_audit(
    qvalues,
):
    qa, qb = RESIDUAL_PAIR

    out = {}

    for scale in FLUX_SCALES:
        A = qvalues[
            qa
        ][
            scale
        ]

        B = qvalues[
            qb
        ][
            scale
        ]

        triplet_distance = norm(
            A[
                "triplet"
            ]
            -
            B[
                "triplet"
            ]
        )

        component_sign_relation = (
            "OPPOSITE"
            if tuple(
                -x
                for x in A[
                    "component_signs"
                ]
            )
            ==
            B[
                "component_signs"
            ]
            else
            (
                "SAME"
                if A[
                    "component_signs"
                ]
                ==
                B[
                    "component_signs"
                ]
                else
                "MIXED"
            )
        )

        net_sign_relation = (
            "OPPOSITE"
            if (
                A[
                    "net_sign"
                ]
                != 0
                and
                B[
                    "net_sign"
                ]
                ==
                -A[
                    "net_sign"
                ]
            )
            else
            (
                "SAME"
                if A[
                    "net_sign"
                ]
                ==
                B[
                    "net_sign"
                ]
                else
                "MIXED"
            )
        )

        out[
            scale
        ] = {
            "triplet_distance":
                triplet_distance,

            "numerically_distinct":
                (
                    triplet_distance
                    > DESCENT_TOL
                ),

            "component_sign_relation":
                component_sign_relation,

            "net_sign_relation":
                net_sign_relation,

            qa:
                {
                    "triplet":
                        A[
                            "triplet"
                        ],

                    "component_signs":
                        A[
                            "component_signs"
                        ],

                    "net":
                        A[
                            "net"
                        ],

                    "net_sign":
                        A[
                            "net_sign"
                        ],
                },

            qb:
                {
                    "triplet":
                        B[
                            "triplet"
                        ],

                    "component_signs":
                        B[
                            "component_signs"
                        ],

                    "net":
                        B[
                            "net"
                        ],

                    "net_sign":
                        B[
                            "net_sign"
                        ],
                },
        }

    return out


# ===========================================================================
# Aggregate orientation verdict
# ===========================================================================

def aggregate_orientation(
    pair_audit,
):
    component_relations = [
        pair_audit[
            scale
        ][
            "component_sign_relation"
        ]
        for scale in FLUX_SCALES
    ]

    net_relations = [
        pair_audit[
            scale
        ][
            "net_sign_relation"
        ]
        for scale in FLUX_SCALES
    ]

    numerical_distinction = all(
        pair_audit[
            scale
        ][
            "numerically_distinct"
        ]
        for scale in FLUX_SCALES
    )

    component_opposite = all(
        x == "OPPOSITE"
        for x in component_relations
    )

    net_opposite = all(
        x == "OPPOSITE"
        for x in net_relations
    )

    component_same = all(
        x == "SAME"
        for x in component_relations
    )

    net_same = all(
        x == "SAME"
        for x in net_relations
    )

    if (
        component_opposite
        or
        net_opposite
    ):
        signed_binary = True

        if (
            component_opposite
            and
            net_opposite
        ):
            verdict = (
                "OPPOSITE_NATIVE_TOPOLOGICAL_SIGN"
            )

        else:
            verdict = (
                "PARTIAL_NATIVE_TOPOLOGICAL_SIGN"
            )

    elif (
        component_same
        and
        net_same
    ):
        signed_binary = False

        verdict = (
            "SAME_NATIVE_TOPOLOGICAL_SIGN"
        )

    else:
        signed_binary = False

        verdict = (
            "NO_CLEAN_NATIVE_TOPOLOGICAL_SIGN_RELATION"
        )

    return {
        "numerical_quotient_discrimination":
            numerical_distinction,

        "component_relations":
            component_relations,

        "net_relations":
            net_relations,

        "component_opposite_all_scales":
            component_opposite,

        "net_opposite_all_scales":
            net_opposite,

        "component_same_all_scales":
            component_same,

        "net_same_all_scales":
            net_same,

        "native_signed_binary_discriminator":
            signed_binary,

        "verdict":
            verdict,
    }


# ===========================================================================
# Relation to Result-032 C sign
# ===========================================================================

def relation_to_C_sign(
    qvalues,
    orientation,
):
    if not orientation[
        "native_signed_binary_discriminator"
    ]:
        return {
            "relation":
                "NONE",

            "reason":
                (
                    "The native Mermin-Ho sign summaries do not supply "
                    "an opposite binary sign on Tzbar and TxTzbar."
                ),
        }

    # Determine a stable topological sign from net sign first if it is
    # opposite across all scales. Otherwise use component-sign orientation.
    #
    # No arbitrary post-hoc scalar is introduced.
    if orientation[
        "net_opposite_all_scales"
    ]:
        topo_signs = {}

        for qname in RESIDUAL_PAIR:
            values = [
                qvalues[
                    qname
                ][
                    scale
                ][
                    "net_sign"
                ]
                for scale in FLUX_SCALES
            ]

            if len(
                set(values)
            ) != 1:
                return {
                    "relation":
                        "MIXED",

                    "reason":
                        (
                            "Net topological sign varies across scales."
                        ),
                }

            topo_signs[
                qname
            ] = values[0]

        cA = RESULT_032_C_SIGN[
            RESIDUAL_PAIR[0]
        ]

        cB = RESULT_032_C_SIGN[
            RESIDUAL_PAIR[1]
        ]

        tA = topo_signs[
            RESIDUAL_PAIR[0]
        ]

        tB = topo_signs[
            RESIDUAL_PAIR[1]
        ]

        if (
            tA == cA
            and
            tB == cB
        ):
            relation = "ALIGNED"

        elif (
            tA == -cA
            and
            tB == -cB
        ):
            relation = "REVERSED"

        else:
            relation = "MIXED"

        return {
            "relation":
                relation,

            "topological_signs":
                topo_signs,

            "C_signs":
                {
                    q:
                        RESULT_032_C_SIGN[q]
                    for q in RESIDUAL_PAIR
                },

            "reader":
                "net_signed_flux",
        }

    # Component-sign tuple can establish opposite orientation as a tuple, but
    # it does not produce a scalar +1/-1 without choosing an arbitrary axis.
    return {
        "relation":
            "BINARY_TUPLE_ONLY",

        "reason":
            (
                "Component sign tuples are opposite but no native scalar "
                "orientation sign is available without choosing a component."
            ),
    }


# ===========================================================================
# Controls
# ===========================================================================

def run_controls(
    states,
    descent,
):
    C_signs = {
        name:
            states[
                name
            ][
                "C_sign"
            ][
                "label"
            ]
        for name in EXPECTED_NAMES
    }

    expected_C = {
        "I": "+",
        "Tx": "-",
        "Ty": "+",
        "Tz": "+",
        "TxTy": "-",
        "TxTz": "-",
        "TyTz": "+",
        "TxTyTz": "-",
    }

    return {
        "all_fields_finite":
            all(
                np.all(
                    np.isfinite(
                        states[
                            name
                        ][
                            "basic"
                        ][
                            scale
                        ][
                            "triplet"
                        ]
                    )
                )
                for name in EXPECTED_NAMES
                for scale in FLUX_SCALES
            ),

        "C_sign_pattern_matches_result_023_032":
            (
                C_signs
                ==
                expected_C
            ),

        "all_basic_triplets_descend":
            all_triplets_descend(
                descent
            ),

        "fullf_h":
            float(
                CFG[
                    "h"
                ]
            ),
    }


# ===========================================================================
# Test gates
# ===========================================================================

def test_existing_interfaces():
    assert callable(
        BUILD_DISPLACEMENTS
    )

    assert callable(
        APPLY_WORD
    )

    assert callable(
        FULLF_READS
    )


def test_flux_scales_present():
    states = evaluate_states()

    for name in EXPECTED_NAMES:
        for scale in FLUX_SCALES:
            assert scale in states[
                name
            ][
                "basic"
            ]


def test_quotient_descent():
    states = evaluate_states()

    descent = quotient_descent(
        states
    )

    assert all_triplets_descend(
        descent
    ), (
        "Existing basic Mermin-Ho triplet did not descend through "
        "<Ty> at the preregistered tolerance"
    )


def run_all():
    test_existing_interfaces()
    test_flux_scales_present()
    test_quotient_descent()


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
        tuple,
    ):
        return [
            json_safe(x)
            for x in value
        ]

    if isinstance(
        value,
        list,
    ):
        return [
            json_safe(x)
            for x in value
        ]

    if isinstance(
        value,
        dict,
    ):
        return {
            str(k):
                json_safe(v)
            for k, v in value.items()
        }

    return value


def write_json(
    states,
    descent,
    qvalues,
    pair_audit,
    orientation,
    C_relation,
    controls,
):
    RESULT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "test":
            38,

        "title":
            (
                "Native M5 signed Mermin-Ho / topological-flux "
                "orientation -> C-sign audit"
            ),

        "implementation": {
            "fullf_source":
                str(
                    FULLF_PATH.relative_to(
                        REPO_ROOT
                    )
                ),

            "closure_source":
                str(
                    RESULT_026_PATH.relative_to(
                        REPO_ROOT
                    )
                ),

            "native_reader":
                "reads(...)[basic]",

            "flux_scales":
                list(
                    FLUX_SCALES
                ),

            "native_configuration": {
                "n":
                    N,
                "delta":
                    DELTA,
                "h":
                    float(
                        CFG[
                            "h"
                        ]
                    ),
            },
        },

        "quotient":
            QUOTIENT,

        "result_032_C_sign":
            RESULT_032_C_SIGN,

        "state_reads": {
            name: {
                scale:
                    states[
                        name
                    ][
                        "basic"
                    ][
                        scale
                    ]
                for scale in FLUX_SCALES
            }
            for name in EXPECTED_NAMES
        },

        "descent":
            descent,

        "quotient_values":
            qvalues,

        "residual_pair_audit":
            pair_audit,

        "aggregate_orientation":
            orientation,

        "relation_to_C_sign":
            C_relation,

        "controls":
            controls,

        "reading_point_mapping_used":
            False,

        "chi3_used":
            False,

        "result_034_mapping_count_before":
            2,

        "result_038_mapping_count_after":
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
# Reporting
# ===========================================================================

def format_triplet(
    v,
):
    return (
        "["
        + ", ".join(
            f"{float(x):+.9e}"
            for x in v
        )
        + "]"
    )


def format_sign_tuple(
    s,
):
    symbol = {
        -1: "-",
        0: "0",
        +1: "+",
    }

    return (
        "("
        + ",".join(
            symbol[
                int(x)
            ]
            for x in s
        )
        + ")"
    )


def main():
    run_all()

    states = evaluate_states()

    descent = quotient_descent(
        states
    )

    qvalues = quotient_values(
        states,
        descent,
    )

    pair_audit = residual_pair_audit(
        qvalues
    )

    orientation = aggregate_orientation(
        pair_audit
    )

    C_relation = relation_to_C_sign(
        qvalues,
        orientation,
    )

    controls = run_controls(
        states,
        descent,
    )

    print()
    print("Reading Point Test 038")
    print("----------------------")
    print()

    print(
        "Native M5 signed Mermin-Ho / "
        "topological-flux orientation -> C-sign audit"
    )

    print()
    print("=" * 72)
    print("Existing implementation")
    print("=" * 72)
    print()

    print("Full-F source:")
    print(
        FULLF_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print("Closure source:")
    print(
        RESULT_026_PATH.relative_to(
            REPO_ROOT
        )
    )

    print()
    print("Existing native reader:")
    print(
        "reads(...)[basic]"
    )

    print()
    print("Existing interpretation:")
    print(
        "longest-axis / Mermin-Ho signed cube flux"
    )

    print()
    print("Reading Point mapping used:")
    print("NO")

    print()
    print("chi3 used:")
    print("NO")

    print()
    print("=" * 72)
    print("Native configuration")
    print("=" * 72)
    print()

    print(
        f"n      = {N}"
    )

    print(
        f"delta  = {DELTA}"
    )

    print(
        f"h      = {CFG['h']}"
    )

    print()
    print(
        "flux scales = half6, half12, half18"
    )

    print()
    print("=" * 72)
    print("Per-transformation signed basic reads")
    print("=" * 72)
    print()

    for scale in FLUX_SCALES:
        print(
            f"[basic.{scale}]"
        )

        for name in EXPECTED_NAMES:
            row = states[
                name
            ][
                "basic"
            ][
                scale
            ]

            print(
                f"{name:8s} "
                f"{format_triplet(row['triplet'])} "
                f"signs={format_sign_tuple(row['component_signs'])} "
                f"net={row['net']:+.9e} "
                f"net_sign={sign_label(row['net'])}"
            )

        print()

    print("=" * 72)
    print("Quotient descent through <Ty>")
    print("=" * 72)
    print()

    for qname in QUOTIENT:
        print(
            qname
        )

        for scale in FLUX_SCALES:
            d = descent[
                qname
            ][
                scale
            ]

            print(
                f"  {scale}: "
                f"triplet_error={d['triplet_error']:.9e} "
                f"triplet_descends={d['triplet_descends']} "
                f"component_signs_descend="
                f"{d['component_signs_descend']} "
                f"net_sign_descends={d['net_sign_descends']}"
            )

        print()

    print(
        "All basic triplets descend through <Ty>:"
    )

    print(
        "SUPPORTED"
        if controls[
            "all_basic_triplets_descend"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Quotient-level native signed reads")
    print("=" * 72)
    print()

    for scale in FLUX_SCALES:
        print(
            f"[{scale}]"
        )

        for qname in QUOTIENT:
            row = qvalues[
                qname
            ][
                scale
            ]

            print(
                f"{qname:10s} "
                f"{format_triplet(row['triplet'])} "
                f"signs={format_sign_tuple(row['component_signs'])} "
                f"net={row['net']:+.9e} "
                f"net_sign={sign_label(row['net'])}"
            )

        print()

    print("=" * 72)
    print("Residual-pair orientation audit")
    print("=" * 72)
    print()

    print(
        "Target pair:"
    )

    print(
        "Tzbar"
    )

    print(
        "TxTzbar"
    )

    print()
    print(
        "Result-032 C labels withheld until "
        "after native topological readout:"
    )

    print(
        "Tzbar    -> +C"
    )

    print(
        "TxTzbar  -> -C"
    )

    print()

    for scale in FLUX_SCALES:
        row = pair_audit[
            scale
        ]

        A = row[
            "Tzbar"
        ]

        B = row[
            "TxTzbar"
        ]

        print(
            scale
        )

        print(
            f"  triplet distance = "
            f"{row['triplet_distance']:.9e}"
        )

        print(
            f"  numerically distinct = "
            f"{row['numerically_distinct']}"
        )

        print(
            f"  component-sign relation = "
            f"{row['component_sign_relation']}"
        )

        print(
            f"  net-sign relation = "
            f"{row['net_sign_relation']}"
        )

        print(
            f"  Tzbar signs = "
            f"{format_sign_tuple(A['component_signs'])}, "
            f"net_sign={sign_label(A['net'])}"
        )

        print(
            f"  TxTzbar signs = "
            f"{format_sign_tuple(B['component_signs'])}, "
            f"net_sign={sign_label(B['net'])}"
        )

        print()

    print("=" * 72)
    print("Aggregate native orientation verdict")
    print("=" * 72)
    print()

    print(
        "Mermin-Ho triplet numerically distinguishes "
        "the residual quotient pair:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "numerical_quotient_discrimination"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Opposite component-sign tuples "
        "at all scales:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "component_opposite_all_scales"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Opposite net signed flux "
        "at all scales:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "net_opposite_all_scales"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Same component-sign tuples "
        "at all scales:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "component_same_all_scales"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Same net sign at all scales:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "net_same_all_scales"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Native signed binary discriminator:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "native_signed_binary_discriminator"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Native orientation verdict:"
    )

    print(
        orientation[
            "verdict"
        ]
    )

    print()
    print("=" * 72)
    print("Relation to Result-032 C-sign")
    print("=" * 72)
    print()

    print(
        "Relation:"
    )

    print(
        C_relation[
            "relation"
        ]
    )

    if "reason" in C_relation:
        print()

        print(
            C_relation[
                "reason"
            ]
        )

    print()
    print("=" * 72)
    print("Controls")
    print("=" * 72)
    print()

    print(
        "All signed basic reads finite:"
    )

    print(
        "SUPPORTED"
        if controls[
            "all_fields_finite"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "C-sign pattern reproduces Results 023/032:"
    )

    print(
        "SUPPORTED"
        if controls[
            "C_sign_pattern_matches_result_023_032"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Existing basic triplet quotient descent:"
    )

    print(
        "SUPPORTED"
        if controls[
            "all_basic_triplets_descend"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print("=" * 72)
    print("Correspondence boundary")
    print("=" * 72)
    print()

    anchor_supported = (
        orientation[
            "native_signed_binary_discriminator"
        ]
        and
        C_relation[
            "relation"
        ]
        in (
            "ALIGNED",
            "REVERSED",
        )
    )

    print(
        "Native Mermin-Ho/topological sign "
        "anchors Result-032 C-sign:"
    )

    print(
        "SUPPORTED"
        if anchor_supported
        else "NOT ESTABLISHED"
    )

    print()
    print(
        "Numerical Mermin-Ho quotient labeling:"
    )

    print(
        "SUPPORTED"
        if orientation[
            "numerical_quotient_discrimination"
        ]
        else "NOT SUPPORTED"
    )

    print()
    print(
        "Does numerical distinction alone establish "
        "orientation sign?"
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
        "Result-038 admissible mappings:"
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
        descent,
        qvalues,
        pair_audit,
        orientation,
        C_relation,
        controls,
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

    print(
        "RESULT 038:"
    )

    print()

    if anchor_supported:
        print(
            "The existing signed Mermin-Ho/topological-flux "
            "instrument supplies a native orientation sign that "
            f"is {C_relation['relation'].lower()} with the "
            "Result-032 C-sign on the residual M5 quotient pair."
        )

    elif orientation[
        "numerical_quotient_discrimination"
    ]:
        print(
            "The existing Mermin-Ho/topological-flux instrument "
            "numerically distinguishes the residual M5 quotient pair, "
            "but its preregistered signed summaries do not supply an "
            "opposite binary orientation sign for that pair."
        )

    else:
        print(
            "The existing signed Mermin-Ho/topological-flux instrument "
            "does not provide a clean native orientation discriminator "
            "for the residual M5 quotient pair."
        )

    print()
    print(
        "Reading Point chi3 sign mapping remains "
        "unassigned by Test 038."
    )

    print()
    print("PASS")


if __name__ == "__main__":
    main()
