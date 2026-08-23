# readingpoint/tests/test_015_m5_connection_to_n4_provenance.py

from pathlib import Path
import re


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

M5_5_1 = M5_SCRIPTS / "m5_5_1_evolution_symbolic.py"
M5_31 = M5_SCRIPTS / "m5_31_coupling_curvature_field.py"

N3 = M5_SCRIPTS / "m5_11_n3_mass_matrix.py"
N4 = M5_SCRIPTS / "m5_11_n4_chiral.py"

N4_LINKING = M5_SCRIPTS / "m5_11_n4_linking.py"
N4_TOPO = M5_SCRIPTS / "m5_11_n4_topo.py"
N4_ORIGIN = M5_SCRIPTS / "m5_11_n4b_chiral_origin.py"
N4_POTENTIAL = M5_SCRIPTS / "m5_11_n4b_potential.py"
N4_RESIDUAL = M5_SCRIPTS / "m5_11_n4b_residual.py"

EXAMINED = (
    M5_5_1,
    M5_31,
    N3,
    N4,
    N4_LINKING,
    N4_TOPO,
    N4_ORIGIN,
    N4_POTENTIAL,
    N4_RESIDUAL,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_required_sources_exist():
    for path in EXAMINED:
        assert path.exists(), f"Missing source: {path}"


def test_m5_symbolic_connection_is_defined():
    text = read(M5_5_1)

    assert "Gamma = [O0.T * O0.diff(c) for c in coords]" in text
    assert "antisymmetric" in text
    assert "so(3) connection" in text


def test_m5_field_connection_and_curvature_are_defined():
    text = read(M5_31)

    assert "def connection(" in text
    assert "q0[..., None] * dq - dq0[..., None] * q" in text
    assert "np.cross(q, dq)" in text

    assert "def curvature_magnitude" in text
    assert "np.cross(gamma[i], gamma[j])" in text


def test_n3_uses_energy_hessian_flavour_reduction():
    text = read(N3)

    assert "ENERGY HESSIAN" in text
    assert "projected onto the three flavour" in text
    assert "M_mass = K + kappa P" in text


def test_n4_builds_C_from_chiral_overlap():
    text = read(N4)

    assert "def chiral_overlap" in text
    assert "Cc[a, b] = cab" in text
    assert "Cc[b, a] = -cab" in text
    assert "1j * g_chiral * Cc" in text


def test_examined_n4_descendants_reuse_chiral_overlap():
    descendants = (
        N4_LINKING,
        N4_TOPO,
        N4_ORIGIN,
        N4_POTENTIAL,
        N4_RESIDUAL,
    )

    for path in descendants:
        text = read(path)

        assert "chiral_overlap" in text, (
            f"{path.name} does not reuse chiral_overlap as expected"
        )


def test_no_connection_to_C_projection_found_in_examined_sources():
    """
    Source-provenance boundary.

    We are looking for an explicit implemented path from the M5
    connection/curvature objects (Gamma_i, R_ij, connection(), curvature)
    to the N4 flavour-space antisymmetric matrix C / Cc.

    This test is intentionally conservative: it does not prove that no such
    derivation can exist elsewhere. It verifies only that the examined
    implementation files do not contain an explicit bridge.
    """

    texts = {
        path.name: read(path)
        for path in EXAMINED
    }

    bridge_patterns = (
        r"chiral_overlap\s*\(\s*Gamma",
        r"chiral_overlap\s*\(\s*gamma",
        r"chiral_overlap\s*\(\s*R_",
        r"chiral_overlap\s*\(\s*curvature",
        r"Cc\s*=.*Gamma",
        r"Cc\s*=.*gamma",
        r"Cc\s*=.*R_",
        r"Cc\s*=.*curvature",
        r"Gamma.*Cc",
        r"gamma.*Cc",
        r"curvature.*Cc",
        r"connection.*Cc",
        r"Gamma.*chiral_overlap",
        r"connection.*chiral_overlap",
        r"curvature.*chiral_overlap",
    )

    hits = []

    for name, text in texts.items():
        for pattern in bridge_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                hits.append((name, pattern))

    assert hits == [], (
        "Unexpected explicit connection/curvature -> N4 C bridge found: "
        f"{hits}"
    )


def test_n4_C_is_constructed_directly_from_loop_field_derivatives():
    """
    Confirm that the current N4 implementation gets C from derivatives of
    the flavour-loop displacements, rather than importing the M5
    connection/curvature machinery.
    """

    text = read(N4)

    start = text.index("def chiral_overlap")
    end = text.index("def real_overlap")

    block = text[start:end]

    assert "_grads(dA)" in block
    assert "_grads(dB)" in block
    assert "_sdot(Ax, By)" in block

    assert "Gamma" not in block
    assert "connection(" not in block
    assert "curvature" not in block


if __name__ == "__main__":
    test_required_sources_exist()
    test_m5_symbolic_connection_is_defined()
    test_m5_field_connection_and_curvature_are_defined()
    test_n3_uses_energy_hessian_flavour_reduction()
    test_n4_builds_C_from_chiral_overlap()
    test_examined_n4_descendants_reuse_chiral_overlap()
    test_no_connection_to_C_projection_found_in_examined_sources()
    test_n4_C_is_constructed_directly_from_loop_field_derivatives()

    print("Reading Point Test 015")
    print("----------------------")
    print()

    print("M5 non-Hessian connection machinery:")
    print("IMPLEMENTED")

    print()
    print("Symbolic connection:")
    print("Gamma_i = O^T d_i O")

    print()
    print("Connection symmetry class:")
    print("ANTISYMMETRIC so(3)")

    print()
    print("Field-level connection:")
    print(
        "Gamma_i = q0 d_i q - (d_i q0) q + q x d_i q"
    )

    print()
    print("Curvature:")
    print("R_ij = Gamma_i x Gamma_j")

    print()
    print("N3 flavour-space reduction:")
    print("ENERGY-HESSIAN PROJECTION")

    print()
    print("N4 CP-odd flavour structure:")
    print("i * g_chiral * C")

    print()
    print("N4 C construction:")
    print("chiral_overlap(dA, dB)")

    print()
    print("Examined N4 descendants reuse chiral_overlap:")
    print("SUPPORTED")

    print()
    print("Connection/curvature -> N4 C implementation:")
    print("NOT FOUND IN EXAMINED SOURCES")

    print()
    print("Candidate non-Hessian geometric structure:")
    print("EXISTS")

    print()
    print("Candidate identified with N4 C:")
    print("NO")

    print()
    print("Result 014 structural obstruction bypassed by existing code:")
    print("NO")

    print()
    print("Additional effective projection / derivation:")
    print("REQUIRED")

    print()
    print("Interpretation:")
    print(
        "M5 contains independently implemented antisymmetric connection "
        "and curvature machinery."
    )
    print(
        "This supplies a genuine non-Hessian geometric structure of the "
        "kind that could participate in an antisymmetric effective sector."
    )
    print(
        "However, the examined repository does not project Gamma_i or "
        "R_ij onto the three N3/N4 flavour configurations."
    )
    print(
        "The N4 branch and the examined N4 descendants instead construct "
        "their antisymmetric matrix C directly through "
        "chiral_overlap(dA, dB)."
    )
    print(
        "Therefore M5 contains a candidate geometric ingredient for the "
        "additional structure required by Result 014, but no implemented "
        "provenance bridge establishes that ingredient as the origin of "
        "N4 C."
    )

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")
