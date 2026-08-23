# readingpoint/tests/test_005_m5_winding_sign.py

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

from m5_17_energy import grid_coords  # noqa: E402
from m5_20_1_b_seeds import (  # noqa: E402
    H,
    NR,
    NZ,
    loop_field_biax,
    winding_measure_biax,
)


DELTAS = (0.1, 0.3, 0.5)
PAIRINGS = ("pair_1d", "pair_d0")
RADII = (3.0, 4.0, 5.0, 6.0)

R0 = 17.0
Q_MAG = 0.5
TOL = 0.05
MIX_TOL = 0.05


def measure(delta, pairing, q):
    R, Z = grid_coords(NR, NZ, H)

    M = loop_field_biax(
        R,
        Z,
        R0,
        q,
        delta,
        pairing,
    )

    out = {}

    for radius in RADII:
        q_meas, mix = winding_measure_biax(
            M,
            NR,
            NZ,
            H,
            R0,
            0.0,
            r_w=radius,
        )

        out[radius] = {
            "q": float(q_meas),
            "mix": float(mix),
        }

    return out


def valid_reads(reads):
    return all(
        np.isfinite(item["q"])
        and np.isfinite(item["mix"])
        and item["mix"] < MIX_TOL
        for item in reads.values()
    )


def test_positive_and_negative_seeds_are_measurable():
    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            assert valid_reads(positive)
            assert valid_reads(negative)


def test_magnitude_is_preserved_for_both_signs():
    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]

                assert abs(abs(qp) - Q_MAG) <= TOL
                assert abs(abs(qn) - Q_MAG) <= TOL


def test_sign_is_identified_by_current_observable():
    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]

                assert abs(qp - qn) <= TOL


def test_measured_value_is_positive_half_winding():
    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]

                assert abs(qp - Q_MAG) <= TOL
                assert abs(qn - Q_MAG) <= TOL


if __name__ == "__main__":
    test_positive_and_negative_seeds_are_measurable()
    test_magnitude_is_preserved_for_both_signs()
    test_sign_is_identified_by_current_observable()
    test_measured_value_is_positive_half_winding()

    print("Reading Point Test 005")
    print("----------------------")
    print()

    all_sign_identified = True

    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            print(f"delta={delta}  pairing={pairing}")

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]
                mixp = positive[radius]["mix"]
                mixn = negative[radius]["mix"]

                sign_identified = (
                    np.isfinite(qp)
                    and np.isfinite(qn)
                    and abs(qp - qn) <= TOL
                    and abs(qp - Q_MAG) <= TOL
                    and abs(qn - Q_MAG) <= TOL
                    and mixp < MIX_TOL
                    and mixn < MIX_TOL
                )

                all_sign_identified = (
                    all_sign_identified and sign_identified
                )

                print(
                    f"  r={radius:.1f}"
                    f"  q(+0.5)={qp:+.4f}"
                    f"  q(-0.5)={qn:+.4f}"
                    f"  mix+={mixp:.4f}"
                    f"  mix-={mixn:.4f}"
                    f"  {'PASS' if sign_identified else 'FAIL'}"
                )

            print()

    print(
        "M5 winding sign observable:",
        "SIGN IDENTIFIED"
        if all_sign_identified
        else "SIGN NOT CONSISTENTLY IDENTIFIED",
    )
    print()

    print("Interpretation:")

    if all_sign_identified:
        print(
            "For every tested delta, pairing, and read radius, "
            "the current M5 eigenframe-winding observable returns "
            "the same +0.5 value for synthetic +0.5 and -0.5 inputs."
        )
        print(
            "The tested observable therefore does not distinguish "
            "the input winding sign in this sector."
        )
        print(
            "This operationally supports q ~ -q for this specific "
            "numerical observable and tested configuration family."
        )
        print(
            "It does not establish that the full M5 Q8 topology is "
            "physically reduced to Q8/{1,-1}."
        )
    else:
        print(
            "The tested M5 observable does not consistently identify "
            "+q and -q across the tested configuration family."
        )

    print()
    print("Reading Point Result 003 quotient:")
    print("MATHEMATICALLY SUPPORTED")
    print("M5 observable sign identification:")
    print(
        "SUPPORTED IN TESTED SECTOR"
        if all_sign_identified
        else "NOT SUPPORTED"
    )
    print("Full physical Q8/{1,-1} identification:")
    print("NOT ESTABLISHED")

    raise SystemExit(0 if all_sign_identified else 1)
