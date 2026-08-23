# readingpoint/tests/test_010_m5_self_linking_baseline.py

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


# Cache the expensive upstream run so every assertion uses the same result.
_BASELINE_CACHE = None


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


def run_upstream_once():
    """
    Execute the expensive upstream M5 N4 self-linking scan exactly once.

    The upstream script writes m5_11_n4_topo_summary.json. Preserve the
    repository's original version of that file and restore it immediately
    after the run so this Reading Point baseline test has no persistent
    side effect inside upstream OpenWave.
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
        # Restore the upstream-generated data artifact exactly as it was.
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
        "M5 self-linking baseline returned a nonzero exit code.\n"
        f"STDOUT:\n{completed.stdout}\n"
        f"STDERR:\n{completed.stderr}"
    )


def test_self_linking_scan_contains_expected_N_values():
    result = baseline()
    rows = result["rows"]

    assert set(rows) == {-2, -1, 0, 1, 2}


def test_n0_keeps_clean_structure():
    result = baseline()
    rows = result["rows"]

    n0 = rows[0]

    assert abs(n0["theta12"] - 35.264) < 0.5
    assert abs(n0["theta23"] - 45.0) < 0.5
    assert abs(abs(n0["delta_CP"]) - 90.0) < 1.0


def test_nonzero_N_breaks_tbm_baseline():
    result = baseline()
    rows = result["rows"]

    for N in (-2, -1, 1, 2):
        row = rows[N]

        keeps_tbm = (
            abs(row["theta12"] - 35.264) < 0.5
            and abs(row["theta23"] - 45.0) < 0.5
        )

        assert keeps_tbm is False


def test_delta_cp_not_cleanly_antisymmetric_under_N_flip():
    result = baseline()
    rows = result["rows"]

    for N in (1, 2):
        antisymmetric = (
            abs(
                rows[N]["delta_CP"]
                + rows[-N]["delta_CP"]
            )
            < 1.0
        )

        assert antisymmetric is False


def test_upstream_verdict_is_negative_inconclusive():
    result = baseline()
    stdout = result["completed"].stdout

    assert (
        "N4 topo: INCONCLUSIVE / NEGATIVE "
        "for clean topological quantization."
        in stdout
    )


def test_upstream_summary_file_restored():
    """
    The baseline wrapper should leave upstream OpenWave data unchanged.

    The exact bytes are restored inside run_upstream_once(); here we
    simply verify that the expected repository path still exists when it
    existed before the test run.
    """

    # In the current OpenWave checkout this tracked artifact exists.
    assert M5_SUMMARY.exists()


if __name__ == "__main__":
    result = baseline()
    completed = result["completed"]
    rows = result["rows"]

    test_upstream_script_exists()
    test_upstream_script_runs()
    test_self_linking_scan_contains_expected_N_values()
    test_n0_keeps_clean_structure()
    test_nonzero_N_breaks_tbm_baseline()
    test_delta_cp_not_cleanly_antisymmetric_under_N_flip()
    test_upstream_verdict_is_negative_inconclusive()
    test_upstream_summary_file_restored()

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

    print("M5 self-linking handedness candidate:")
    print("DEFINED")

    print()
    print("Clean topological quantization from naive N*s construction:")
    print("NOT SUPPORTED")

    print()
    print("Orientation bridge for Result 009:")
    print("NOT ESTABLISHED")

    print()
    print("Interpretation:")
    print(
        "M5 defines an integer, reflection-odd self-linking candidate N, "
        "but the current naive azimuthal N*s framing fails its own "
        "physics-preservation test."
    )
    print(
        "N=0 preserves the clean TBM/maximal-CP structure, while all "
        "tested nonzero N values break the TBM baseline."
    )
    print(
        "The tested delta_CP response is also not cleanly antisymmetric "
        "under N -> -N."
    )
    print(
        "A mu-tau-respecting definition of self-linking remains an "
        "open M5 requirement."
    )
    print()

    print("Upstream repository side effects:")
    print("NONE — generated summary restored after the baseline run")

    raise SystemExit(0)
