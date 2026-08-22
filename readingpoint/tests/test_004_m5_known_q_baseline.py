# readingpoint/tests/test_004_m5_known_q_baseline.py

from pathlib import Path
import json
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]

M5_BASELINE_SCRIPT = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_20_1_b_seeds.py"
)


def run_m5_baseline():
    if not M5_BASELINE_SCRIPT.exists():
        raise FileNotFoundError(
            f"M5 baseline script not found: {M5_BASELINE_SCRIPT}"
        )

    completed = subprocess.run(
        [sys.executable, str(M5_BASELINE_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    return completed


def parse_gate_results(stdout: str):
    gates = {}

    for gate in ("B0", "B0b", "B1", "B2"):
        match = re.search(
            rf"^\[{re.escape(gate)}\]\s+(PASS|FAIL)\s*$",
            stdout,
            flags=re.MULTILINE,
        )

        if match:
            gates[gate] = match.group(1) == "PASS"

    return gates


def parse_json_summary(stdout: str):
    start = stdout.rfind("{")

    if start == -1:
        return None

    candidate = stdout[start:].strip()

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def test_m5_baseline_script_exists():
    assert M5_BASELINE_SCRIPT.exists()


def test_m5_baseline_exits_successfully():
    completed = run_m5_baseline()

    assert completed.returncode == 0, (
        "M5 baseline script returned a nonzero exit code.\n"
        f"STDOUT:\n{completed.stdout}\n"
        f"STDERR:\n{completed.stderr}"
    )


def test_m5_known_q_gate_b1_passes():
    completed = run_m5_baseline()
    gates = parse_gate_results(completed.stdout)

    assert "B1" in gates, (
        "Could not locate B1 output in the M5 baseline run.\n"
        f"STDOUT:\n{completed.stdout}"
    )

    assert gates["B1"] is True


def test_all_reported_m5_seed_gates_pass():
    completed = run_m5_baseline()
    gates = parse_gate_results(completed.stdout)

    expected = {
        "B0": True,
        "B0b": True,
        "B1": True,
        "B2": True,
    }

    assert gates == expected


def test_json_summary_agrees_with_gate_output():
    completed = run_m5_baseline()

    gates = parse_gate_results(completed.stdout)
    summary = parse_json_summary(completed.stdout)

    assert summary is not None, (
        "Could not parse trailing JSON summary from M5 baseline output."
    )

    assert summary == gates


if __name__ == "__main__":
    completed = run_m5_baseline()

    print("Reading Point Test 004")
    print("----------------------")
    print()

    print("Upstream artifact:")
    print(
        "  openwave/xperiments/m5_liquid_crystal/"
        "research/scripts/m5_20_1_b_seeds.py"
    )
    print()

    print("Upstream output:")
    print(completed.stdout.rstrip())
    print()

    gates = parse_gate_results(completed.stdout)
    summary = parse_json_summary(completed.stdout)

    baseline_supported = (
        completed.returncode == 0
        and gates.get("B1") is True
        and gates == {
            "B0": True,
            "B0b": True,
            "B1": True,
            "B2": True,
        }
        and summary == gates
    )

    print("Reading Point interpretation:")
    print(
        "M5 known-q winding instrument: "
        f"{'SUPPORTED' if baseline_supported else 'NOT SUPPORTED'}"
    )
    print("B1 synthetic known-q gate:", "PASS" if gates.get("B1") else "FAIL")
    print("Reading Point mapping: NOT YET TESTED")
    print()
    print("Scope:")
    print(
        "This test reproduces the existing OpenWave M5 instrument gate."
    )
    print(
        "It does not identify mod-30 residues with quaternion classes."
    )
    print(
        "It establishes only that the upstream known-q measurement "
        "baseline is runnable and passes in this fork."
    )

    raise SystemExit(0 if baseline_supported else 1)
