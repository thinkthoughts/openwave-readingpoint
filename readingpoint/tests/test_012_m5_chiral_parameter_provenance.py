# readingpoint/tests/test_012_m5_chiral_parameter_provenance.py

from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]

P2 = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_11_p2_heliknoton.py"
)

N4 = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_11_n4_chiral.py"
)

N4_ORIGIN = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_11_n4b_chiral_origin.py"
)

N4_LINKING = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_11_n4_linking.py"
)


def read(path):
    return path.read_text(encoding="utf-8")


def test_required_sources_exist():
    for path in (P2, N4, N4_ORIGIN, N4_LINKING):
        assert path.exists(), f"Missing source: {path}"


def test_p2_contains_explicit_lifshitz_term():
    text = read(P2)

    assert "2.0 * q0 * Lc * chi * dV" in text
    assert "chiral Lifshitz" in text
    assert "Frank" in text


def test_p2_uses_q0_Lc_Kf_parameters():
    text = read(P2)

    assert "q0" in text
    assert "Lc" in text
    assert "Kf" in text

    # P2 explicitly locks the Frank partner to L/2 in its helix/sweep setup.
    assert re.search(r"Kf\s*=\s*L\s*/\s*2\.0", text)


def test_n4_uses_g_chiral_parameter():
    text = read(N4)

    assert "g_chiral" in text
    assert "1j * g_chiral * Cc" in text


def test_n4_origin_calls_substrate_origin_open():
    text = read(N4_ORIGIN)

    assert (
        "does the M5 Landau-de Gennes functional carry a chiral / Lifshitz"
        in text
    )

    assert (
        "The open substrate question"
        in text
    )


def test_n4_linking_calls_g_chiral_free_coupling():
    text = read(N4_LINKING)

    assert "free coupling" in text
    assert "cholesteric-pitch analogue" in text


def test_no_explicit_parameter_bridge_in_examined_sources():
    """
    This is a source-provenance test.

    It does not prove that no bridge exists anywhere in mathematics or
    elsewhere in the repository. It verifies that the examined P2/N4
    implementation files contain no explicit assignment or function
    defining g_chiral from q0, Lc, or Kf.
    """

    texts = {
        "P2": read(P2),
        "N4": read(N4),
        "N4_ORIGIN": read(N4_ORIGIN),
        "N4_LINKING": read(N4_LINKING),
    }

    bridge_patterns = (
        r"g_chiral\s*=\s*[^#\n]*(?:Lc|q0|Kf)",
        r"g_chiral\s*=\s*f\s*\(",
        r"g_chiral\s*=\s*.*q0",
        r"g_chiral\s*=\s*.*Lc",
        r"g_chiral\s*=\s*.*Kf",
    )

    hits = []

    for name, text in texts.items():
        for pattern in bridge_patterns:
            if re.search(pattern, text):
                hits.append((name, pattern))

    assert hits == [], f"Unexpected explicit parameter bridge found: {hits}"


if __name__ == "__main__":
    test_required_sources_exist()
    test_p2_contains_explicit_lifshitz_term()
    test_p2_uses_q0_Lc_Kf_parameters()
    test_n4_uses_g_chiral_parameter()
    test_n4_origin_calls_substrate_origin_open()
    test_n4_linking_calls_g_chiral_free_coupling()
    test_no_explicit_parameter_bridge_in_examined_sources()

    print("Reading Point Test 012")
    print("----------------------")
    print()

    print("P2 chiral substrate machinery:")
    print("IMPLEMENTED")

    print()
    print("P2 Lifshitz coefficient structure:")
    print("2 * q0 * Lc")

    print()
    print("P2 Frank partner:")
    print("Kf = Lc / 2  (in the tested helix/sweep construction)")

    print()
    print("N4 chiral coefficient:")
    print("g_chiral")

    print()
    print("Explicit P2 -> N4 parameter bridge:")
    print("NOT FOUND IN EXAMINED SOURCES")

    print()
    print("N4 g_chiral status:")
    print("FREE / PHENOMENOLOGICAL IN EXAMINED BRANCH")

    print()
    print("Interpretation:")
    print(
        "M5 contains an implemented chiral Lifshitz substrate term in "
        "the P2 branch."
    )
    print(
        "However, the examined N4 files do not derive g_chiral from "
        "P2's q0, Lc, or Kf."
    )
    print(
        "The current repository therefore contains chiral substrate "
        "machinery and a separate N4 chiral coupling, but no explicit "
        "provenance bridge between them in the examined implementation."
    )

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")
