#!/usr/bin/env python3
"""
Reading Point Test 024 — second independent observable from the N3/N4
real-overlap sector.

Result 023 established that the field-level transformations

    T_x = P o R_x
    T_y = P o R_y
    T_z = P o R_z

generate eight distinct commuting involutions, giving a C2^3-like closure:

    I
    T_x
    T_y
    T_z
    T_x T_y
    T_x T_z
    T_y T_z
    T_x T_y T_z

The existing N4 chiral matrix C supplies only a non-faithful binary sign
readout:

    four transformations -> +C
    four transformations -> -C

Therefore C alone cannot select a four-state quotient or a unique embedded
V4 subgroup.

Result 024 asks whether an ALREADY EXISTING, independently defined N3/N4
observable supplies additional discrimination.

Primary preregistered observable:

    real_overlap(dA, dB)

which gives the real N3/N4 flavour-space sector

    K_ab = <grad dM_a, grad dM_b>_s
    P_ab = <dM_a, dM_b>_s

and

    Mr = K + kappa P.

For the current N4 baseline:

    kappa = 0

so

    Mr = K.

The test recomputes both C and Mr directly from every transformed field
configuration.

It then asks:

  1. Does Mr remain real symmetric?
  2. Does C remain antisymmetric?
  3. Does normalized Mr distinguish transformations that C identifies?
  4. How many joint signatures (sign(C), normalized Mr) occur?
  5. If exactly four joint classes occur, do those classes define a
     composition-compatible quotient of the already established C2^3-like
     field closure?

No classifier is fitted.
No subgroup is selected in advance.
No new effective observable is invented.
No Reading Point or Q8 identification is introduced.
"""

from pathlib import Path
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
from m5_11_n4_chiral import (  # noqa: E402
    chiral_overlap,
    real_overlap,
)


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

# Current N4 baseline.
KAPPA = 0.0

ANTISYM_TOL = 1e-10
SYMMETRY_TOL = 1e-10

C_SIGN_TOL = 1e-4

# Pre-registered numerical equivalence threshold for normalized Mr.
# This is not fitted from the observed separations.
MR_EQUIV_TOL = 1e-4


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def frobenius_norm(A):
    return float(
        np.linalg.norm(A)
    )


def normalized_matrix(A):
    n = frobenius_norm(A)

    if not np.isfinite(n) or n <= 1e-30:
        raise ValueError(
            "zero or non-finite matrix norm"
        )

    return A / n


def relative_matrix_error(A, B):
    den = max(
        frobenius_norm(B),
        1e-30,
    )

    return float(
        frobenius_norm(A - B)
        / den
    )


def antisymmetry_error(C):
    scale = max(
        float(np.max(np.abs(C))),
        1.0,
    )

    return float(
        np.max(np.abs(C + C.T))
        / scale
    )


def symmetry_error(M):
    scale = max(
        float(np.max(np.abs(M))),
        1.0,
    )

    return float(
        np.max(np.abs(M - M.T))
        / scale
    )


# ----------------------------------------------------------------------
# Original N4 flavour fields
# ----------------------------------------------------------------------

def build_displacements():
    """
    Standard N4 reference family:

        e   = reference
        mu  = +alpha
        tau = -alpha

    Both mu and tau carry +CHI.
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


# ----------------------------------------------------------------------
# T_x, T_y, T_z field transformations
# ----------------------------------------------------------------------

def reflection_matrix(axis):
    S = np.eye(3)
    S[axis, axis] = -1.0
    return S


def reflect_field(F, axis):
    """
    Actual coordinate reflection plus rank-2 tensor transformation.
    """

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
    """
    T_axis = P o R_axis.
    """

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


# ----------------------------------------------------------------------
# C2^3-like closure from Result 023
# ----------------------------------------------------------------------

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


# Binary-vector representation of the established commuting involutions.
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
    for name, bits in WORD_BITS.items()
}


def group_product_name(a, b):
    """
    Product in the already established C2^3-like field closure:
    componentwise XOR of generator exponents.
    """

    ba = WORD_BITS[a]
    bb = WORD_BITS[b]

    bc = tuple(
        x ^ y
        for x, y in zip(
            ba,
            bb,
        )
    )

    return BITS_TO_NAME[bc]


# ----------------------------------------------------------------------
# Existing observables
# ----------------------------------------------------------------------

def chiral_matrix(fields):
    """
    Recompute N4 C directly from transformed fields.
    """

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


def real_matrices(fields):
    """
    Recompute the existing real N3/N4 overlap sector directly.

    real_overlap returns:

        K = gradient overlap
        P = field overlap

    Mr = K + KAPPA * P
    """

    K = np.zeros(
        (3, 3),
        dtype=float,
    )

    Pmat = np.zeros(
        (3, 3),
        dtype=float,
    )

    for a in range(3):
        for b in range(a, 3):
            kab, pab = real_overlap(
                fields[a],
                fields[b],
            )

            K[a, b] = kab
            K[b, a] = kab

            Pmat[a, b] = pab
            Pmat[b, a] = pab

    Mr = (
        K
        + KAPPA * Pmat
    )

    return Mr, K, Pmat


def classify_C_sign(Ct, C0):
    even_error = relative_matrix_error(
        Ct,
        C0,
    )

    odd_error = relative_matrix_error(
        Ct,
        -C0,
    )

    if even_error < C_SIGN_TOL:
        label = "+"
    elif odd_error < C_SIGN_TOL:
        label = "-"
    else:
        label = "?"

    return {
        "label": label,
        "even_error": even_error,
        "odd_error": odd_error,
    }


# ----------------------------------------------------------------------
# Evaluate all eight field transformations
# ----------------------------------------------------------------------

def evaluate_states():
    original = build_displacements()

    states = {}

    for name, word in closure_words().items():
        fields = apply_word(
            original,
            word,
        )

        C = chiral_matrix(
            fields
        )

        Mr, K, Pmat = real_matrices(
            fields
        )

        states[name] = {
            "fields": fields,
            "C": C,
            "Mr": Mr,
            "K": K,
            "P": Pmat,
            "Mr_hat": normalized_matrix(Mr),
            "Mr_norm": frobenius_norm(Mr),
            "K_norm": frobenius_norm(K),
            "P_norm": frobenius_norm(Pmat),
            "C_antisym_error":
                antisymmetry_error(C),
            "Mr_sym_error":
                symmetry_error(Mr),
            "K_sym_error":
                symmetry_error(K),
            "P_sym_error":
                symmetry_error(Pmat),
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


# ----------------------------------------------------------------------
# Mr discrimination
# ----------------------------------------------------------------------

def mr_distance(A, B):
    """
    Frobenius distance between normalized Mr matrices.
    """

    return float(
        frobenius_norm(
            A["Mr_hat"]
            - B["Mr_hat"]
        )
    )


def pairwise_mr_distances(states):
    names = list(
        closure_words().keys()
    )

    out = {}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]

            out[
                f"{a}-{b}"
            ] = mr_distance(
                states[a],
                states[b],
            )

    return out


def same_C_sign_pairs(states):
    names = list(
        closure_words().keys()
    )

    rows = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]

            sa = states[a][
                "C_sign"
            ]["label"]

            sb = states[b][
                "C_sign"
            ]["label"]

            if (
                sa in ("+", "-")
                and sa == sb
            ):
                rows.append(
                    (
                        a,
                        b,
                        sa,
                        mr_distance(
                            states[a],
                            states[b],
                        ),
                    )
                )

    return rows


# ----------------------------------------------------------------------
# Joint signature clustering
# ----------------------------------------------------------------------

def joint_equivalent(
    name_a,
    name_b,
    states,
):
    """
    Two transformations have the same tested joint signature iff:

      - they have the same C sign;
      - normalized Mr differs by at most MR_EQUIV_TOL.
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
        mr_distance(
            states[name_a],
            states[name_b],
        )
        <= MR_EQUIV_TOL
    )


def cluster_joint_signatures(states):
    """
    Greedy clustering using the preregistered joint-equivalence rule.

    With only eight exact named transformations, every member is also
    checked against the representative of its assigned class.
    """

    names = list(
        closure_words().keys()
    )

    reps = []
    class_of = {}

    for name in names:
        assigned = False

        for idx, rep in enumerate(reps):
            if joint_equivalent(
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

    for name, idx in class_of.items():
        classes.setdefault(
            idx,
            [],
        ).append(name)

    return reps, class_of, classes


# ----------------------------------------------------------------------
# Quotient compatibility
# ----------------------------------------------------------------------

def quotient_compatibility(
    class_of,
):
    """
    Test whether the measured equivalence relation is compatible with the
    established C2^3-like group multiplication.

    For an equivalence relation to define a quotient group:

        a ~ a'
        b ~ b'

    must imply:

        ab ~ a'b'

    for all representatives.

    Returns:
        compatible
        violations
        induced multiplication table between measured classes
    """

    names = list(
        closure_words().keys()
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

    compatible = (
        len(violations) == 0
    )

    # Build an induced class multiplication table only if well-defined.
    table = {}

    if compatible:
        class_ids = sorted(
            set(
                class_of.values()
            )
        )

        representative = {}

        for cls in class_ids:
            representative[cls] = next(
                name
                for name in names
                if class_of[name] == cls
            )

        for ca in class_ids:
            for cb in class_ids:
                a = representative[ca]
                b = representative[cb]

                product = group_product_name(
                    a,
                    b,
                )

                table[
                    (ca, cb)
                ] = class_of[product]

    return (
        compatible,
        violations,
        table,
    )


# ----------------------------------------------------------------------
# Structural tests
# ----------------------------------------------------------------------

def test_C_remains_antisymmetric():
    states = evaluate_states()

    for row in states.values():
        assert (
            row["C_antisym_error"]
            < ANTISYM_TOL
        )


def test_real_sector_remains_symmetric():
    states = evaluate_states()

    for row in states.values():
        assert (
            row["Mr_sym_error"]
            < SYMMETRY_TOL
        )

        assert (
            row["K_sym_error"]
            < SYMMETRY_TOL
        )

        assert (
            row["P_sym_error"]
            < SYMMETRY_TOL
        )


def test_all_observables_finite_nonzero():
    states = evaluate_states()

    for row in states.values():
        for key in (
            "C",
            "Mr",
            "K",
            "P",
        ):
            assert np.all(
                np.isfinite(
                    row[key]
                )
            )

        assert (
            frobenius_norm(
                row["C"]
            )
            > 1e-8
        )

        assert (
            row["Mr_norm"]
            > 1e-8
        )


def run_all():
    test_C_remains_antisymmetric()
    test_real_sector_remains_symmetric()
    test_all_observables_finite_nonzero()


# ----------------------------------------------------------------------
# Main report
# ----------------------------------------------------------------------

def main():
    run_all()

    states = evaluate_states()

    mr_pairs = pairwise_mr_distances(
        states
    )

    same_sign = same_C_sign_pairs(
        states
    )

    (
        reps,
        class_of,
        classes,
    ) = cluster_joint_signatures(
        states
    )

    joint_count = len(
        classes
    )

    (
        quotient_ok,
        quotient_violations,
        quotient_table,
    ) = quotient_compatibility(
        class_of
    )

    print("Reading Point Test 024")
    print("----------------------")
    print()

    print(
        "Second independent observable "
        "for C2^3-like closure"
    )
    print()

    print("Primary observable:")
    print(
        "existing N3/N4 real overlap sector"
    )

    print()
    print(
        "Mr = K + kappa P"
    )
    print(
        f"kappa = {KAPPA}"
    )

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
    print("Field closure:")
    print(
        "C2^3-like, 8 transformations "
        "(Result 023)"
    )

    print()
    print("Per-transformation observables:")
    print()

    for name in closure_words():
        row = states[name]

        cs = row[
            "C_sign"
        ]

        print(
            f"{name:8s}"
            f"  C_sign={cs['label']}"
            f"  C_even_err={cs['even_error']:.3e}"
            f"  C_odd_err={cs['odd_error']:.3e}"
            f"  ||Mr||={row['Mr_norm']:.6e}"
            f"  Mr_sym={row['Mr_sym_error']:.3e}"
            f"  C_anti={row['C_antisym_error']:.3e}"
        )

    print()
    print("Normalized Mr matrices:")
    print()

    for name in closure_words():
        print(name)

        print(
            np.array2string(
                states[name]["Mr_hat"],
                precision=6,
                suppress_small=True,
            )
        )

        print()

    print("Pairwise normalized-Mr distances:")
    print()

    for key, value in mr_pairs.items():
        print(
            f"{key}: {value:.6e}"
        )

    print()
    print(
        "Mr discrimination inside equal-C-sign sectors:"
    )
    print()

    separated_same_sign = 0

    for a, b, sign, distance in same_sign:
        separated = (
            distance
            > MR_EQUIV_TOL
        )

        if separated:
            separated_same_sign += 1

        print(
            f"{a:8s} vs {b:8s}"
            f"  C_sign={sign}"
            f"  Mr_dist={distance:.6e}"
            f"  separated={separated}"
        )

    print()
    print(
        "Equal-C-sign pairs separated by Mr:"
    )
    print(
        f"{separated_same_sign}"
        f"/{len(same_sign)}"
    )

    print()
    print("Joint signature rule:")
    print(
        "same C sign AND "
        f"normalized-Mr distance <= {MR_EQUIV_TOL:.1e}"
    )

    print()
    print("Joint signature classes:")
    print(
        f"class count = {joint_count}"
    )

    for cls in sorted(classes):
        members = classes[cls]

        print(
            f"class {cls}: "
            + ", ".join(
                members
            )
        )

    print()
    print("Quotient compatibility:")
    print(
        "Does the measured equivalence respect "
        "the Result-023 C2^3-like composition law?"
    )

    print()

    if quotient_ok:
        print("SUPPORTED")
    else:
        print("NOT SUPPORTED")

    print(
        f"violations = "
        f"{len(quotient_violations)}"
    )

    if quotient_ok:
        print()
        print(
            "Induced class multiplication table:"
        )

        class_ids = sorted(
            classes.keys()
        )

        header = (
            "      "
            + " ".join(
                f"{c:>3d}"
                for c in class_ids
            )
        )

        print(header)

        for ca in class_ids:
            cells = []

            for cb in class_ids:
                cells.append(
                    quotient_table[
                        (ca, cb)
                    ]
                )

            print(
                f"{ca:>3d}: "
                + " ".join(
                    f"{x:>3d}"
                    for x in cells
                )
            )

    print()
    print("Observable status:")
    print()

    if separated_same_sign == 0:
        print(
            "Mr ADDS NO INDEPENDENT "
            "DISCRIMINATION WITHIN C-SIGN SECTORS"
        )
    elif joint_count == 4 and quotient_ok:
        print(
            "JOINT FOUR-STATE QUOTIENT "
            "SUPPORTED IN TESTED CONFIGURATION"
        )
    elif joint_count == 8 and quotient_ok:
        print(
            "JOINT EIGHT-STATE READOUT "
            "SUPPORTED IN TESTED CONFIGURATION"
        )
    else:
        print(
            "Mr ADDS SOME DISCRIMINATION, "
            "BUT NO FOUR-STATE QUOTIENT "
            "IS ESTABLISHED"
        )

    print()
    print("Interpretation:")
    print(
        "The real overlap sector is independently defined "
        "in the existing N3/N4 machinery and is recomputed "
        "directly from every transformed field configuration."
    )
    print(
        "The test asks whether it resolves transformations "
        "that the binary C-sign observable identifies."
    )
    print(
        "No V4 subgroup or four-state partition is imposed "
        "before measurement."
    )
    print(
        "If a measured partition is composition-compatible, "
        "that is reported explicitly as a quotient property "
        "of the already established C2^3-like field closure."
    )

    print()
    print("Unique V4 selection:")
    if (
        joint_count == 4
        and quotient_ok
    ):
        print(
            "A FOUR-CLASS QUOTIENT IS OBSERVED, "
            "BUT IDENTIFICATION WITH V4/Q8 STILL "
            "REQUIRES SEPARATE STRUCTURAL CHECK"
        )
    else:
        print(
            "NOT ESTABLISHED"
        )

    print()
    print("Q8/{+1,-1} identification:")
    print("NOT ESTABLISHED")

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    return True


if __name__ == "__main__":
    raise SystemExit(
        0 if main() else 1
    )
