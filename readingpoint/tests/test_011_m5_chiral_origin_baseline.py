# readingpoint/tests/test_011_m5_chiral_origin_baseline.py

from pathlib import Path
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
    / "m5_11_n4b_chiral_origin.py"
)

M5_SUMMARY = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "data"
    / "m5_11_n4b_chiral_origin_summary.json"
)


_BASELINE_CACHE = None


def parse_scan(stdout):
    rows = {}

    pattern = re.compile(
        r"^\s*"
        r"([0-9.]+)\s+"
        r"([0-9.eE+-]+)\s+"
        r"(-?[0-9.]+)\s+"
        r"([0-9.]+)\s+"
        r"([0-9.eE+-]+)\s*$",
        flags=re.MULTILINE,
    )

    for match in pattern.finditer(stdout):
        g = float(match.group(1))

        rows[g] = {
            "C_norm": float(match.group(2)),
            "delta_CP": float(match.group(3)),
            "theta13": float(match.group(4)),
            "dE_handedness": float(match.group(5)),
        }

    return rows


def run_upstream_once():
    """
    Run the expensive upstream M5 chiral-origin scan once.

    The upstream script writes m5_11_n4b_chiral_origin_summary.json.
    Preserve that file exactly and restore it after the run so this
    Reading Point test leaves no persistent change in upstream OpenWave.
    """

    global _BASELINE_CACHE

    if _BASELINE_CACHE is not None:
        return _BASELINE_CACHE

    if not M5_SCRIPT.exists():
        raise FileNotFoundError(
            f"Upstream M5 script not found: {M5_SCRIPT}"
        )

    summary_existed = M5_SUMMARY.exists()

    if summary_existed:
        original_summary = M5_SUMMARY.read_bytes()
    else:
        original_summary = None

    try:
        completed = subprocess.run(
            [sys.executable, str(M5_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        rows = parse_scan(completed.stdout)

        _BASELINE_CACHE = {
            "completed": completed,
            "rows": rows,
        }

    finally:
        if summary_existed:
            M5_SUMMARY.write_bytes(original_summary)
        elif M5_SUMMARY.exists():
            M5_SUMMARY.unlink()

    return _BASELINE_CACHE


def baseline():
    return run_upstream_once()


def test_upstream_script_exists():
    assert M5_SCRIPT.exists()


def test_upstream_script_runs():
    result = baseline()
    completed = result["completed"]

    assert completed.returncode == 0, (
        "M5 chiral-origin baseline returned a nonzero exit code.\n"
        f"STDOUT:\n{completed.stdout}\n"
        f"STDERR:\n{completed.stderr}"
    )


def test_scan_contains_expected_g_values():
    rows = baseline()["rows"]

    expected = {0.0, 0.3, 0.6, 0.94, 1.5}
    assert set(rows) == expected


def test_geometric_chiral_overlap_is_constant():
    rows = baseline()["rows"]

    values = [row["C_norm"] for row in rows.values()]

    assert max(values) - min(values) < 1e-6


def test_achiral_energy_is_handedness_degenerate():
    rows = baseline()["rows"]

    for row in rows.values():
        assert abs(row["dE_handedness"]) < 1e-12


def test_g0_is_cp_conserving():
    rows = baseline()["rows"]
    g0 = rows[0.0]

    assert abs(g0["delta_CP"]) < 1.0
    assert abs(g0["theta13"]) < 0.1


def test_g094_turns_cp_on():
    rows = baseline()["rows"]
    g = rows[0.94]

    assert abs(abs(g["delta_CP"]) - 90.0) < 1.0
    assert g["theta13"] > 1.0


def test_upstream_conclusion_present():
    stdout = baseline()["completed"].stdout

    assert (
        "the achiral M5 LdG does NOT prefer a handedness"
        in stdout
    )

    assert (
        "the SIGN of g_chiral selects delta_CP's sign"
        in stdout
    )


def test_upstream_summary_restored():
    assert M5_SUMMARY.exists()


if __name__ == "__main__":
    result = baseline()
    rows = result["rows"]

    test_upstream_script_exists()
    test_upstream_script_runs()
    test_scan_contains_expected_g_values()
    test_geometric_chiral_overlap_is_constant()
    test_achiral_energy_is_handedness_degenerate()
    test_g0_is_cp_conserving()
    test_g094_turns_cp_on()
    test_upstream_conclusion_present()
    test_upstream_summary_restored()

    print("Reading Point Test 011")
    print("----------------------")
    print()
    print("M5 chiral-origin baseline reproduction")
    print()

    for g in (0.0, 0.3, 0.6, 0.94, 1.5):
        row = rows[g]

        print(
            f"g_chiral={g:>4.2f}"
            f"  |C|={row['C_norm']:.4f}"
            f"  delta_CP={row['delta_CP']:.1f}"
            f"  theta13={row['theta13']:.3f}"
            f"  dE_hand={row['dE_handedness']:.3e}"
        )

    print()
    print("Geometric chiral overlap:")
    print("SUPPORTED")

    print()
    print("Achiral handedness degeneracy:")
    print("SUPPORTED")

    print()
    print("g_chiral = 0:")
    print("CP CONSERVING")

    print()
    print("g_chiral = 0.94:")
    print("CP ON")

    print()
    print("Achiral physical orientation selector:")
    print("ABSENT IN TESTED MODEL")

    print()
    print("Chiral orientation selector:")
    print("CONDITIONAL ON g_chiral")

    print()
    print("Result 009 orientation requirement:")
    print("NOT YET SATISFIED BY ACHIRAL M5")

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")

    print()
    print("Interpretation:")
    print(
        "The loop geometry carries a nonzero chiral overlap C that is "
        "independent of g_chiral."
    )
    print(
        "However, the achiral M5 LdG energy remains exactly degenerate "
        "between +chi and -chi in the reproduced scan."
    )
    print(
        "The tested model therefore contains geometric chiral structure "
        "without an achiral energetic preference for handedness."
    )
    print(
        "A handedness selector appears only after introducing the "
        "chiral coupling g_chiral, whose substrate origin remains an "
        "upstream M5 question."
    )

    print()
    print("Upstream repository side effects:")
    print("NONE — generated summary restored after the baseline run")

    raise SystemExit(0)
