# readingpoint/tests/test_010_m5_self_linking_baseline.py

from pathlib import Path
import json
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]

M5_SCRIPT = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_11_n4_topo.py"
)

M5_SUMMARY = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "data"
    / "m5_11_n4_topo_summary.json"
)


def run_upstream():
    completed = subprocess.run(
        [sys.executable, str(M5_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed


def parse_scan(stdout):
    rows = {}

    pattern = re.compile(
        r"^\s*(-?\d+)\s+"
        r"([0-9.]+)\s+"
        r"([0-9.]+)\s+"
        r"([0-9.]+)\s+"
        r"(-?[0-9.]+)\s+"
        r"(-?[0-9.eE+-]+)\s+"
        r"([0-9.eE+-]+)\s*$",
        flags=re.MULTILINE,
    )

    for match in pattern.finditer(stdout):
        N = int(match.group(1))
        rows[N] = {
            "theta12": float(match.group(2)),
            "theta23": float(match.group(3)),
            "theta13": float(match.group(4)),
            "delta_CP": float(match.group(5)),
            "J": float(match.group(6)),
            "C_norm": float(match.group(7)),
        }

    return rows


def test_upstream_script_runs():
    completed = run_upstream()
    assert completed.returncode == 0, completed.stderr


def test_self_linking_scan_contains_expected_N_values():
    completed = run_upstream()
    rows = parse_scan(completed.stdout)

    assert set(rows) == {-2, -1, 0, 1, 2}


def test_n0_keeps_clean_structure():
    completed = run_upstream()
    rows = parse_scan(completed.stdout)

    n0 = rows[0]

    assert abs(n0["theta12"] - 35.264) < 0.5
    assert abs(n0["theta23"] - 45.0) < 0.5
    assert abs(abs(n0["delta_CP"]) - 90.0) < 1.0


def test_nonzero_N_breaks_tbm_baseline():
    completed = run_upstream()
    rows = parse_scan(completed.stdout)

    for N in (-2, -1, 1, 2):
        row = rows[N]

        keeps_tbm = (
            abs(row["theta12"] - 35.264) < 0.5
            and abs(row["theta23"] - 45.0) < 0.5
        )

        assert keeps_tbm is False


def test_delta_cp_not_cleanly_antisymmetric_under_N_flip():
    completed = run_upstream()
    rows = parse_scan(completed.stdout)

    for N in (1, 2):
        antisym = abs(
            rows[N]["delta_CP"]
            + rows[-N]["delta_CP"]
        ) < 1.0

        assert antisym is False


def test_upstream_verdict_is_negative_inconclusive():
    completed = run_upstream()

    assert (
        "N4 topo: INCONCLUSIVE / NEGATIVE "
        "for clean topological quantization."
        in completed.stdout
    )


if __name__ == "__main__":
    completed = run_upstream()

    test_upstream_script_runs()
    test_self_linking_scan_contains_expected_N_values()
    test_n0_keeps_clean_structure()
    test_nonzero_N_breaks_tbm_baseline()
    test_delta_cp_not_cleanly_antisymmetric_under_N_flip()
    test_upstream_verdict_is_negative_inconclusive()

    rows = parse_scan(completed.stdout)

    print("Reading Point Test 010")
    print("----------------------")
    print()
    print("M5 self-linking baseline reproduction")
    print()

    for N in (-2, -1, 0, 1, 2):
        row = rows[N]

        print(
            f"N={N:+d}"
            f"  theta12={row['theta12']:.3f}"
            f"  theta23={row['theta23']:.3f}"
            f"  theta13={row['theta13']:.3f}"
            f"  delta_CP={row['delta_CP']:.2f}"
        )

    print()
    print("N=0 clean TBM/maximal-CP structure: PASS")
    print("N!=0 preserves TBM baseline: NO")
    print("delta_CP antisymmetric under N -> -N: NO")
    print()
    print(
        "M5 self-linking handedness observable: DEFINED"
    )
    print(
        "Clean topological quantization from naive N*s construction: "
        "NOT SUPPORTED"
    )
    print(
        "Orientation bridge for Result 009: NOT ESTABLISHED"
    )
    print()
    print("Interpretation:")
    print(
        "M5 already defines an integer, reflection-odd self-linking "
        "candidate N, but the current naive azimuthal N*s framing "
        "fails its own physics-preservation test."
    )
    print(
        "A mu-tau-respecting self-linking construction remains open."
    )
