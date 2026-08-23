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


def test_sign_reversal_is_visible():
    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]

                assert qp * qn < 0
                assert abs(qp + qn) <= TOL


if __name__ == "__main__":
    test_positive_and_negative_seeds_are_measurable()
    test_magnitude_is_preserved_for_both_signs()
    test_sign_reversal_is_visible()

    print("Reading Point Test 005")
    print("----------------------")
    print()

    all_sign_sensitive = True

    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +Q_MAG)
            negative = measure(delta, pairing, -Q_MAG)

            print(f"delta={delta}  pairing={pairing}")

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]

                sign_sensitive = (
                    np.isfinite(qp)
                    and np.isfinite(qn)
                    and qp * qn < 0
                    and abs(qp + qn) <= TOL
                )

                all_sign_sensitive = all_sign_sensitive and sign_sensitive

                print(
                    f"  r={radius:.1f}"
                    f"  q(+0.5)={qp:+.4f}"
                    f"  q(-0.5)={qn:+.4f}"
                    f"  {'PASS' if sign_sensitive else 'FAIL'}"
                )

            print()

    print(
        "M5 winding sign observable:",
        "SIGN DISTINGUISHED" if all_sign_sensitive else "SIGN NOT DISTINGUISHED",
    )
    print()
    print("Interpretation:")

    if all_sign_sensitive:
        print(
            "The M5 winding instrument retains the sign of the synthetic "
            "winding input."
        )
        print(
            "The existing B1 gate quotients the sign only in its acceptance "
            "criterion via |q_meas|."
        )
        print(
            "Therefore q ~ -q is not supplied by this numerical observable."
        )
    else:
        print(
            "The instrument did not consistently retain winding sign across "
            "the tested configurations."
        )

    print()
    print("Reading Point V4 quotient:")
    print("MATHEMATICALLY SUPPORTED")
    print("M5 operational q ~ -q identification:")
    print("NOT ESTABLISHED")

    raise SystemExit(0 if all_sign_sensitive else 1)
