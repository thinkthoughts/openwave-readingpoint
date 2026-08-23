# readingpoint/tests/test_013_m5_chiral_operator_compatibility.py

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

N1 = (
    REPO_ROOT
    / "openwave"
    / "xperiments"
    / "m5_liquid_crystal"
    / "research"
    / "scripts"
    / "m5_11_n1_precision_method.py"
)


def read(path):
    return path.read_text(encoding="utf-8")


def test_required_sources_exist():
    for path in (P2, N4, N1):
        assert path.exists(), f"Missing source: {path}"


def test_p2_is_field_times_one_derivative():
    text = read(P2)

    assert "def chiral_energy_np" in text
    assert "2.0 * q0 * Lc" in text

    # P2 uses Msp itself contracted with one spatial derivative.
    assert re.search(
        r"Msp\[\.\.\.,\s*pi\s*-\s*1,\s*:\]",
        text,
    )

    assert re.search(
        r"g\[\.\.\.,\s*pl\s*-\s*1,\s*:\]",
        text,
    )


def test_p2_uses_spatial_3x3_tensor():
    text = read(P2)

    assert "M_np[..., 1:4, 1:4]" in text


def test_p2_has_explicit_dx_scaling_and_volume():
    text = read(P2)

    assert "1.0 / (2.0 * dx)" in text
    assert "dx ** 3" in text


def test_n4_is_gradient_times_gradient():
    text = read(N4)

    assert "def chiral_overlap" in text

    assert "_sdot(Ax, By)" in text
    assert "_sdot(Ay, Bx)" in text
    assert "_sdot(Ay, Bz)" in text
    assert "_sdot(Az, By)" in text
    assert "_sdot(Az, Bx)" in text
    assert "_sdot(Ax, Bz)" in text


def test_n4_uses_engine_signed_inner_product():
    text = read(N1)

    assert "def _sdot" in text
    assert "SIGN_MAT * A * B" in text


def test_n4_gradients_default_to_dx_one():
    text = read(N1)

    assert re.search(
        r"def _grads\(F,\s*dx=1\.0\)",
        text,
    )

    assert "1.0 / (2.0 * dx)" in text


def test_n4_overlap_has_no_explicit_volume_factor():
    text = read(N4)

    start = text.index("def chiral_overlap")
    end = text.index("def real_overlap")

    block = text[start:end]

    assert "np.sum(c)" in block
    assert "dx ** 3" not in block
    assert "dV" not in block


def test_direct_operator_identity_is_not_present():
    """
    The two implemented objects differ in differential order,
    tensor contraction, and normalization.

    This does not prove no effective reduction can relate them.
    It establishes that they are not directly identical as coded.
    """

    p2 = read(P2)
    n4 = read(N4)

    assert "Msp[..., pi - 1, :]" in p2
    assert "_sdot(Ax, By)" in n4


if __name__ == "__main__":
    test_required_sources_exist()
    test_p2_is_field_times_one_derivative()
    test_p2_uses_spatial_3x3_tensor()
    test_p2_has_explicit_dx_scaling_and_volume()
    test_n4_is_gradient_times_gradient()
    test_n4_uses_engine_signed_inner_product()
    test_n4_gradients_default_to_dx_one()
    test_n4_overlap_has_no_explicit_volume_factor()
    test_direct_operator_identity_is_not_present()

    print("Reading Point Test 013")
    print("----------------------")
    print()

    print("P2 chiral operator:")
    print("Q x dQ  (one derivative)")

    print()
    print("P2 tensor scope:")
    print("spatial 3x3 block")

    print()
    print("P2 normalization:")
    print("explicit dx in gradient + explicit dx^3 volume factor")

    print()
    print("N4 chiral operator:")
    print("dA x dB  (gradient-gradient bilinear)")

    print()
    print("N4 tensor contraction:")
    print("full field with engine SIGN_MAT signed inner product")

    print()
    print("N4 normalization:")
    print("central differences default dx=1; summed without explicit dx^3")

    print()
    print("Direct P2 Lifshitz == N4 C operator identity:")
    print("NOT SUPPORTED")

    print()
    print("Additional effective reduction required:")
    print("YES")

    print()
    print("Interpretation:")
    print(
        "The implemented P2 Lifshitz functional and N4 chiral overlap "
        "differ in differential order, tensor contraction, and explicit "
        "normalization."
    )
    print(
        "Therefore g_chiral cannot be identified directly with "
        "2*q0*Lc from the existing code definitions."
    )
    print(
        "A P2 -> N4 provenance bridge would require an independently "
        "defined projection, reduction, integration-by-parts argument, "
        "or effective-theory derivation."
    )

    print()
    print("Reading Point -> M5 physical mapping:")
    print("NOT ESTABLISHED")
