#!/usr/bin/env python3
"""
Reading Point Test 015 — M5 connection/curvature -> N4 provenance.

Result 014 established a structural obstruction:

    the N3 flavour-space prescription is an energy-Hessian projection,
    so projecting the scalar P2 Lifshitz energy through that prescription
    produces a symmetric Hessian, whereas N4 uses a nonzero real
    antisymmetric matrix C.

The next question is therefore narrower:

    Does the existing M5 repository already contain a non-Hessian
    connection/curvature structure, and is that structure explicitly
    used to construct N4 C?

The repository contains connection/curvature machinery, including

    Gamma_i = O^T d_i O

and the field-level construction

    Gamma_i = q0 d_i q - (d_i q0) q + q x d_i q

with curvature represented through Gamma_i x Gamma_j.

This test establishes repository provenance only. It does NOT derive
N4 C from that machinery and does NOT claim that such a derivation is
impossible.

The tested questions are:

  1. Is M5 connection machinery implemented?
  2. Is M5 curvature machinery implemented?
  3. Does N3 define its flavour mass matrix through an energy-Hessian
     projection?
  4. Does N4 construct C directly through chiral_overlap(dA, dB)?
  5. Do examined N4 descendants continue to reuse chiral_overlap?
  6. Do those N4 files explicitly import/call the examined M5
     connection/curvature machinery in constructing their CP-odd sector?

Expected result:

    candidate non-Hessian geometric structure: EXISTS
    explicit connection/curvature -> N4 C implementation:
        NOT FOUND IN EXAMINED SOURCES

This leaves an independently derived effective projection/reduction as
an open requirement.

No Reading Point residue-to-M5 mapping is introduced here.
"""

from pathlib import Path


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

# Connection / curvature sources examined.
M5_5_1 = M5_SCRIPTS / "m5_5_1_evolution_symbolic.py"
M5_31 = M5_SCRIPTS / "m5_31_coupling_curvature_field.py"

# N3/N4 effective flavour machinery.
N3 = M5_SCRIPTS / "m5_11_n3_mass_matrix.py"
N4 = M5_SCRIPTS / "m5_11_n4_chiral.py"

# Examined N4 descendants.
N4_LINKING = M5_SCRIPTS / "m5_11_n4_linking.py"
N4_TOPO = M5_SCRIPTS / "m5_11_n4_topo.py"
N4_ORIGIN = M5_SCRIPTS / "m5_11_n4b_chiral_origin.py"
N4_POTENTIAL = M5_SCRIPTS / "m5_11_n4b_potential.py"
N4_RESIDUAL = M5_SCRIPTS / "m5_11_n4b_residual.py"

CONNECTION_SOURCES = (
    M5_5_1,
    M5_31,
)

N4_FAMILY = (
    N4,
    N4_LINKING,
    N4_TOPO,
    N4_ORIGIN,
    N4_POTENTIAL,
    N4_RESIDUAL,
)

EXAMINED = (
    *CONNECTION_SOURCES,
    N3,
    *N4_FAMILY,
)


def read(path: Path) -> str:
    """Read one examined source as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def test_required_sources_exist():
    """All sources used for the provenance result must exist."""
    for path in EXAMINED:
        assert path.exists(), f"Missing source: {path}"


def test_m5_symbolic_connection_is_defined():
    """
    M5.5.1 explicitly constructs the frame connection

        Gamma_i = O^T d_i O

    and checks that it is antisymmetric, i.e. so(3)-valued.
    """
    text = read(M5_5_1)

    assert "Gamma = [O0.T * O0.diff(c) for c in coords]" in text
    assert "antisymmetric" in text
    assert "so(3) connection" in text


def test_m5_field_connection_is_defined():
    """
    The field-level Faber/hedgehog branch implements

        Gamma_i =
            q0 d_i q
            - (d_i q0) q
            + q x d_i q.
    """
    text = read(M5_31)

    assert "def connection(" in text
    assert "q0[..., None] * dq - dq0[..., None] * q" in text
    assert "np.cross(q, dq)" in text


def test_m5_curvature_is_defined():
    """
    The same field-level branch constructs curvature from pairwise
    cross products of the connection components.
    """
    text = read(M5_31)

    assert "def curvature_magnitude" in text
    assert "np.cross(gamma[i], gamma[j])" in text


def test_n3_uses_energy_hessian_flavour_reduction():
    """
    N3 states the effective flavour mass prescription explicitly as the
    energy Hessian projected onto the three flavour field displacements.
    """
    text = read(N3)

    assert "ENERGY HESSIAN" in text
    assert "projected onto the three flavour" in text
    assert "M_mass = K + kappa P" in text


def test_n4_builds_C_from_chiral_overlap():
    """
    N4 constructs a real antisymmetric Cc from chiral_overlap and inserts
    it into the complex Hermitian effective matrix as i*g_chiral*Cc.
    """
    text = read(N4)

    assert "def chiral_overlap" in text
    assert "cab = chiral_overlap(d[a], d[b])" in text
    assert "Cc[a, b] = cab" in text
    assert "Cc[b, a] = -cab" in text
    assert "1j * g_chiral * Cc" in text


def test_examined_n4_descendants_reuse_chiral_overlap():
    """
    The examined N4 descendants retain the same chiral_overlap machinery
    rather than replacing it with the separate connection/curvature API.
    """
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


def test_no_connection_to_C_implementation_found():
    """
    Repository-provenance boundary.

    Look specifically for concrete dependencies on the examined M5
    connection/curvature machinery inside the N4 family.

    This deliberately avoids loose regexes such as "R_" because ordinary
    N4 variables such as R_loop, Rmu, and Rtau would create false
    positives.

    Absence here means only:

        no explicit dependency was found in THESE examined sources.

    It does not establish that no theoretical bridge can exist.
    """

    # Modules/files containing the examined connection/curvature machinery.
    forbidden_module_references = (
        "m5_5_1_evolution_symbolic",
        "m5_31_coupling_curvature_field",
    )

    # Concrete APIs from the field-level connection/curvature implementation.
    forbidden_api_calls = (
        "connection(",
        "curvature_magnitude(",
        "regularized_hedgehog(",
        "analytic_curvature_magnitude(",
        "analytic_proxy(",
        "analytic_log_slope(",
        "shell_profile(",
    )

    hits = []

    for path in N4_FAMILY:
        text = read(path)

        for token in forbidden_module_references:
            if token in text:
                hits.append(
                    (
                        path.name,
                        f"references connection/curvature module {token}",
                    )
                )

        for token in forbidden_api_calls:
            if token in text:
                hits.append(
                    (
                        path.name,
                        f"calls connection/curvature API {token}",
                    )
                )

    assert hits == [], (
        "Explicit connection/curvature -> N4 dependency found: "
        f"{hits}"
    )


def test_n4_C_is_direct_loop_derivative_construction():
    """
    Inspect chiral_overlap itself.

    The current N4 C operator is built from first derivatives of the two
    flavour-loop displacement fields and signed bilinear contractions.

    It does not call the separate M5 connection/curvature implementation.
    """
    text = read(N4)

    start = text.index("def chiral_overlap")
    end = text.index("def real_overlap")

    block = text[start:end]

    assert "_grads(dA)" in block
    assert "_grads(dB)" in block

    assert "_sdot(Ax, By)" in block
    assert "_sdot(Ay, Bx)" in block

    assert "_sdot(Ay, Bz)" in block
    assert "_sdot(Az, By)" in block

    assert "_sdot(Az, Bx)" in block
    assert "_sdot(Ax, Bz)" in block

    assert "connection(" not in block
    assert "curvature_magnitude(" not in block
    assert "regularized_hedgehog(" not in block


def run_all():
    """Run the provenance checks without requiring pytest."""
    test_required_sources_exist()
    test_m5_symbolic_connection_is_defined()
    test_m5_field_connection_is_defined()
    test_m5_curvature_is_defined()
    test_n3_uses_energy_hessian_flavour_reduction()
    test_n4_builds_C_from_chiral_overlap()
    test_examined_n4_descendants_reuse_chiral_overlap()
    test_no_connection_to_C_implementation_found()
    test_n4_C_is_direct_loop_derivative_construction()


def main():
    run_all()

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

    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
