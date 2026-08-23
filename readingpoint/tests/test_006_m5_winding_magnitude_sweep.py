# readingpoint/tests/test_006_m5_winding_magnitude_sweep.py

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

# Synthetic instrument probes only.
Q_MAGNITUDES = (0.25, 0.5, 1.0)

R0 = 17.0
MIX_TOL = 0.05
COMPARE_TOL = 0.05


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


def finite_clean(read):
    return (
        np.isfinite(read["q"])
        and np.isfinite(read["mix"])
        and read["mix"] < MIX_TOL
    )


def classify_pair(qp, qn):
    if not (np.isfinite(qp) and np.isfinite(qn)):
        return "UNREADABLE"

    if abs(qp - qn) <= COMPARE_TOL:
        return "SIGN_IDENTIFIED"

    if abs(qp + qn) <= COMPARE_TOL:
        return "SIGN_DISTINGUISHED"

    return "OTHER"


def test_reference_half_winding_still_identifies_sign():
    """
    Regression check for Result 005.
    """
    qmag = 0.5

    for delta in DELTAS:
        for pairing in PAIRINGS:
            positive = measure(delta, pairing, +qmag)
            negative = measure(delta, pairing, -qmag)

            for radius in RADII:
                qp = positive[radius]["q"]
                qn = negative[radius]["q"]

                assert finite_clean(positive[radius])
                assert finite_clean(negative[radius])
                assert abs(qp - qn) <= COMPARE_TOL


def test_sweep_runs_without_instrument_failure():
    """
    Additional q magnitudes are characterization probes.

    This test requires only that the existing M5 instrument return a
    finite, low-mixing read. It does not assume what sign behavior
    should occur away from |q| = 0.5.
    """
    for qmag in Q_MAGNITUDES:
        for delta in DELTAS:
            for pairing in PAIRINGS:
                positive = measure(delta, pairing, +qmag)
                negative = measure(delta, pairing, -qmag)

                for radius in RADII:
                    assert finite_clean(positive[radius])
                    assert finite_clean(negative[radius])


if __name__ == "__main__":
    test_reference_half_winding_still_identifies_sign()
    test_sweep_runs_without_instrument_failure()

    print("Reading Point Test 006")
    print("----------------------")
    print()
    print("M5 winding-magnitude characterization sweep")
    print()
    print(
        "NOTE: q = ±0.25 and ±1.0 are synthetic instrument probes here, "
        "not asserted physical M5 defect classes."
    )
    print()

    counts = {
        "SIGN_IDENTIFIED": 0,
        "SIGN_DISTINGUISHED": 0,
        "OTHER": 0,
        "UNREADABLE": 0,
    }

    total = 0

    for qmag in Q_MAGNITUDES:
        print(f"|q_input| = {qmag}")

        for delta in DELTAS:
            for pairing in PAIRINGS:
                positive = measure(delta, pairing, +qmag)
                negative = measure(delta, pairing, -qmag)

                print(f"  delta={delta}  pairing={pairing}")

                for radius in RADII:
                    qp = positive[radius]["q"]
                    qn = negative[radius]["q"]
                    mixp = positive[radius]["mix"]
                    mixn = negative[radius]["mix"]

                    classification = classify_pair(qp, qn)

                    counts[classification] += 1
                    total += 1

                    print(
                        f"    r={radius:.1f}"
                        f"  q(+{qmag})={qp:+.4f}"
                        f"  q(-{qmag})={qn:+.4f}"
                        f"  mix+={mixp:.4f}"
                        f"  mix-={mixn:.4f}"
                        f"  {classification}"
                    )

        print()

    print("Summary")
    print("-------")
    print(f"tested sign pairs: {total}")

    for name in (
        "SIGN_IDENTIFIED",
        "SIGN_DISTINGUISHED",
        "OTHER",
        "UNREADABLE",
    ):
        print(f"{name}: {counts[name]}")

    print()
    print("Reference Result 005:")
    print("|q| = 0.5 sign identification: SUPPORTED")
    print()
    print("Test 006 purpose:")
    print(
        "Characterize whether that sign-insensitive behavior persists, "
        "changes, aliases, or fails at other synthetic winding magnitudes."
    )
    print()
    print("Physical interpretation of additional q values:")
    print("NOT ASSUMED")
