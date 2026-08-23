#!/usr/bin/env python3
"""
Reading Point Test 025
======================

Existing M5 connection/curvature discriminator audit.

Results 023-024 established:

    field-level closure:
        C2^3-like, 8 transformations

    N4 chiral observable C:
        non-faithful binary sign readout

    N3/N4 real overlap Mr:
        invariant across the tested closure

    joint C + Mr readout:
        2 classes

        K+ = {I, Ty, Tz, TyTz}
        K- = {Tx, TxTy, TxTz, TxTyTz}

Result 015 independently established that M5 contains non-Hessian geometric
machinery:

    Gamma_i = O^T d_i O

and, in the regularized hedgehog implementation,

    Gamma_i
      = q0 d_i q
        - (d_i q0) q
        + q x d_i q

    R_ij = Gamma_i x Gamma_j

Result 015 also found no implemented provenance bridge identifying these
objects with the N4 antisymmetric matrix C.

Test 025 asks the next narrower question:

    Does the EXISTING M5 connection/curvature code define an independently
    motivated observable that is already applicable to the same N3/N4
    transformed flavour-field states and could therefore discriminate states
    inside the four-element kernels left unresolved by C + Mr?

This is first a provenance/readout audit.

IMPORTANT
---------

This test MUST NOT invent a projection such as

    flavour field -> q
    flavour field -> Gamma
    flavour field -> R
    Gamma/R -> 3x3 flavour observable

merely to obtain additional classes.

An observable counts as an executable N4 discriminator only if the examined
repository already supplies the required mapping/readout.

Therefore both outcomes are scientifically meaningful:

    A. existing compatible readout FOUND
       -> characterize it

    B. existing compatible readout NOT FOUND
       -> record an implementation/provenance stopping boundary

The latter does not say that no connection/curvature bridge can exist.
It says that the currently examined implementation does not establish one.

LOCAL / repository audit.  No Reading Point -> M5 identification is imposed.

Run:

    python3 readingpoint/tests/test_025_m5_connection_curvature_discriminator.py
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# repository locations
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

M5_ROOT = REPO / "openwave" / "xperiments" / "m5_liquid_crystal"
SCRIPTS = M5_ROOT / "research" / "scripts"


# Files already implicated by Results 015 and the subsequent N4 audit.
#
# We intentionally inspect explicit known sources rather than grep the entire
# repository and accidentally treat comments, archived experiments, generated
# output, or unrelated M5 branches as an implemented N4 bridge.

CONNECTION_SOURCES = [
    SCRIPTS / "m5_5_1_evolution_symbolic.py",
    SCRIPTS / "m5_31_coupling_curvature_field.py",
]

N3_SOURCES = [
    SCRIPTS / "m5_11_n3_mass_matrix.py",
]

N4_SOURCE_NAMES = [
    "m5_11_n4_chiral.py",
    "m5_11_n4_linking.py",
    "m5_11_n4_topo.py",
    "m5_11_n4b_chiral_origin.py",
    "m5_11_n4b_potential.py",
    "m5_11_n4b_residual.py",
]

N4_SOURCES = [SCRIPTS / name for name in N4_SOURCE_NAMES]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def existing(paths):
    return [p for p in paths if p.exists()]


def function_names(path: Path) -> set[str]:
    """
    Return top-level and nested Python function names where the source parses.

    Failure to parse is treated conservatively: no function names are inferred.
    """
    text = read_text(path)
    if not text:
        return set()

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()

    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def normalized_code(text: str) -> str:
    """
    Remove comments and strings where possible, so provenance matching is less
    likely to be triggered solely by explanatory prose.

    If parsing fails, return the original source; all resulting hits remain
    audit candidates rather than proof of a bridge.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return text

    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            try:
                chunks.append(ast.unparse(node))
            except Exception:
                pass
        elif isinstance(node, ast.Assign):
            try:
                chunks.append(ast.unparse(node))
            except Exception:
                pass
        elif isinstance(node, ast.AnnAssign):
            try:
                chunks.append(ast.unparse(node))
            except Exception:
                pass
        elif isinstance(node, ast.Return):
            try:
                chunks.append(ast.unparse(node))
            except Exception:
                pass

    return "\n".join(chunks)


def grep_patterns(paths, patterns):
    """
    Return explicit code-level pattern hits.

    Result entries:
        (relative_path, pattern)
    """
    hits = []

    for path in existing(paths):
        code = normalized_code(read_text(path))

        for pattern in patterns:
            if re.search(pattern, code, flags=re.IGNORECASE | re.MULTILINE):
                hits.append((rel(path), pattern))

    return hits


def name_hits(paths, names):
    """
    Find explicit symbol-name occurrences in executable-code extracts.
    """
    out = []

    for path in existing(paths):
        code = normalized_code(read_text(path))

        for name in names:
            if re.search(rf"\b{re.escape(name)}\b", code):
                out.append((rel(path), name))

    return out


# ---------------------------------------------------------------------------
# Audit 1: establish the independently implemented geometric machinery
# ---------------------------------------------------------------------------

def audit_connection_machinery():
    symbolic = CONNECTION_SOURCES[0]
    field = CONNECTION_SOURCES[1]

    symbolic_text = read_text(symbolic)
    field_text = read_text(field)

    symbolic_connection = bool(
        re.search(
            r"O0?\.T\s*\*\s*O0?\.diff|O\.T\s*\*\s*O\.diff",
            symbolic_text,
        )
        or (
            "Gamma" in symbolic_text
            and "antisymmetric" in symbolic_text
            and "connection" in symbolic_text
        )
    )

    field_functions = function_names(field)

    field_connection = "connection" in field_functions
    field_curvature = "curvature_magnitude" in field_functions

    analytic_curvature = (
        "analytic_curvature_magnitude" in field_functions
        or "analytic_proxy" in field_functions
        or "shell_profile" in field_functions
    )

    return {
        "symbolic_source_exists": symbolic.exists(),
        "field_source_exists": field.exists(),
        "symbolic_connection": symbolic_connection,
        "field_connection": field_connection,
        "field_curvature": field_curvature,
        "analytic_or_shell_observable": analytic_curvature,
        "field_functions": sorted(field_functions),
    }


# ---------------------------------------------------------------------------
# Audit 2: characterize the existing curvature observables
# ---------------------------------------------------------------------------

def audit_curvature_observables():
    path = CONNECTION_SOURCES[1]
    funcs = function_names(path)

    known = [
        "regularized_hedgehog",
        "centered_difference",
        "connection",
        "curvature_magnitude",
        "analytic_curvature_magnitude",
        "analytic_proxy",
        "analytic_log_slope",
        "shell_profile",
        "coupling_interpretations",
    ]

    present = [name for name in known if name in funcs]

    return {
        "source": rel(path),
        "present": present,
        "has_regularized_hedgehog_input": "regularized_hedgehog" in funcs,
        "has_connection": "connection" in funcs,
        "has_curvature_magnitude": "curvature_magnitude" in funcs,
        "has_shell_profile": "shell_profile" in funcs,
        "has_coupling_interpretations": "coupling_interpretations" in funcs,
    }


# ---------------------------------------------------------------------------
# Audit 3: is there an implemented N3/N4 -> connection/curvature projection?
# ---------------------------------------------------------------------------

def audit_n4_to_connection_bridge():
    """
    Search N3/N4 sources for actual use of the connection/curvature machinery.

    Merely mentioning words in comments is insufficient; normalized_code()
    preferentially searches executable AST fragments.
    """

    geometric_symbols = [
        "regularized_hedgehog",
        "connection",
        "curvature_magnitude",
        "analytic_curvature_magnitude",
        "analytic_proxy",
        "analytic_log_slope",
        "shell_profile",
        "coupling_interpretations",
    ]

    symbol_hits = name_hits(N3_SOURCES + N4_SOURCES, geometric_symbols)

    explicit_patterns = [
        r"\bGamma_[a-zA-Z0-9_]*\b",
        r"\bgamma_[a-zA-Z0-9_]*\b",
        r"\bR_ij\b",
        r"\bcurvature_magnitude\s*\(",
        r"\bconnection\s*\(",
        r"\bshell_profile\s*\(",
        r"\bregularized_hedgehog\s*\(",
    ]

    pattern_hits = grep_patterns(
        N3_SOURCES + N4_SOURCES,
        explicit_patterns,
    )

    all_hits = sorted(set(symbol_hits + pattern_hits))

    return {
        "hits": all_hits,
        "found": len(all_hits) > 0,
    }


# ---------------------------------------------------------------------------
# Audit 4: does the connection code accept the N3/N4 flavour-field object?
# ---------------------------------------------------------------------------

def audit_field_compatibility():
    """
    Compare the explicit interfaces.

    N3/N4 fields are rank-2 4x4 M fields with spatial block M_sp.

    m5_31 connection() is explicitly written in terms of q0 and q.

    Unless an existing M -> (q0,q) conversion exists, calling connection()
    on N4 fields would require a new projection.
    """

    connection_path = CONNECTION_SOURCES[1]
    n3_path = N3_SOURCES[0]

    conn_text = read_text(connection_path)
    n3_text = read_text(n3_path)

    conn_funcs = function_names(connection_path)
    n3_funcs = function_names(n3_path)

    connection_accepts_q = (
        "connection" in conn_funcs
        and bool(
            re.search(
                r"def\s+connection\s*\(\s*q0\s*,\s*q",
                conn_text,
                flags=re.MULTILINE,
            )
        )
    )

    n3_builds_M_fields = (
        "seed_loop_oriented" in n3_funcs
        and "vacuum_field" in n3_funcs
        and "flavour_mass_matrix" in n3_funcs
    )

    # Search examined sources for an explicit conversion routine.
    conversion_names = [
        "M_to_q",
        "matrix_to_q",
        "field_to_q",
        "tensor_to_q",
        "M_to_quaternion",
        "matrix_to_quaternion",
        "director_to_q",
        "extract_q",
    ]

    conversion_hits = name_hits(
        CONNECTION_SOURCES + N3_SOURCES + N4_SOURCES,
        conversion_names,
    )

    # Also inspect executable code for a direct q0/q construction from M.
    conversion_patterns = [
        r"q0\s*=.*\bM\b",
        r"\bq\s*=.*\bM\b",
        r"q0\s*=.*M_sp",
        r"\bq\s*=.*M_sp",
    ]

    conversion_pattern_hits = grep_patterns(
        CONNECTION_SOURCES + N3_SOURCES + N4_SOURCES,
        conversion_patterns,
    )

    conversion_hits = sorted(
        set(conversion_hits + conversion_pattern_hits)
    )

    return {
        "connection_accepts_q0_q": connection_accepts_q,
        "n3_builds_rank2_M_fields": n3_builds_M_fields,
        "explicit_M_to_q_conversion_hits": conversion_hits,
        "explicit_M_to_q_conversion_found": len(conversion_hits) > 0,
    }


# ---------------------------------------------------------------------------
# Audit 5: does an existing observable already consume the N4 transformed
#          fields or flavour triplet?
# ---------------------------------------------------------------------------

def audit_existing_discriminator():
    """
    A valid Result-025 discriminator requires BOTH:

      1. an independently implemented connection/curvature observable;
      2. an existing mapping from the N3/N4 transformed fields into that
         observable's required input.

    This test intentionally does not create condition (2).
    """

    machinery = audit_connection_machinery()
    bridge = audit_n4_to_connection_bridge()
    compatibility = audit_field_compatibility()

    geometric_observable_exists = (
        machinery["field_connection"]
        and machinery["field_curvature"]
        and machinery["analytic_or_shell_observable"]
    )

    input_bridge_exists = (
        bridge["found"]
        or compatibility["explicit_M_to_q_conversion_found"]
    )

    executable_discriminator = (
        geometric_observable_exists
        and input_bridge_exists
    )

    return {
        "geometric_observable_exists": geometric_observable_exists,
        "input_bridge_exists": input_bridge_exists,
        "executable_discriminator": executable_discriminator,
    }


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------

def yn(value):
    return "YES" if value else "NO"


def supported(value):
    return "SUPPORTED" if value else "NOT SUPPORTED"


def print_hits(title, hits):
    print(title)

    if not hits:
        print("NONE")
        return

    for path, item in hits:
        print(f"{path}: {item}")


def main():
    print()
    print("Reading Point Test 025")
    print("----------------------")
    print()
    print("Existing M5 connection/curvature discriminator audit")
    print()

    machinery = audit_connection_machinery()
    observables = audit_curvature_observables()
    bridge = audit_n4_to_connection_bridge()
    compatibility = audit_field_compatibility()
    discriminator = audit_existing_discriminator()

    print("Result-024 unresolved effective classes:")
    print()
    print("K+ = {I, Ty, Tz, TyTz}")
    print("K- = {Tx, TxTy, TxTz, TxTyTz}")
    print()

    print("M5 non-Hessian geometric machinery:")
    print()
    print(
        "symbolic Gamma_i = O^T d_i O:",
        "IMPLEMENTED" if machinery["symbolic_connection"] else "NOT CONFIRMED",
    )
    print(
        "field-level Gamma_i(q0,q):",
        "IMPLEMENTED" if machinery["field_connection"] else "NOT CONFIRMED",
    )
    print(
        "field-level curvature:",
        "IMPLEMENTED" if machinery["field_curvature"] else "NOT CONFIRMED",
    )
    print(
        "curvature scalar/profile observable:",
        "IMPLEMENTED"
        if machinery["analytic_or_shell_observable"]
        else "NOT CONFIRMED",
    )
    print()

    print("Existing field-level geometric functions:")
    print()
    if observables["present"]:
        for name in observables["present"]:
            print(name)
    else:
        print("NONE FOUND")
    print()

    print("Connection/curvature input representation:")
    print()
    print("connection(q0, q):", yn(compatibility["connection_accepts_q0_q"]))
    print(
        "N3/N4 rank-2 M flavour fields:",
        yn(compatibility["n3_builds_rank2_M_fields"]),
    )
    print()

    print("Explicit M-field -> (q0,q) conversion:")
    print()
    print(
        "FOUND"
        if compatibility["explicit_M_to_q_conversion_found"]
        else "NOT FOUND IN EXAMINED SOURCES"
    )
    print()

    print_hits(
        "M -> q conversion audit hits:",
        compatibility["explicit_M_to_q_conversion_hits"],
    )
    print()

    print("N3/N4 -> connection/curvature executable bridge:")
    print()
    print(
        "FOUND"
        if bridge["found"]
        else "NOT FOUND IN EXAMINED SOURCES"
    )
    print()

    print_hits(
        "Executable bridge audit hits:",
        bridge["hits"],
    )
    print()

    print("Independent connection/curvature observable exists:")
    print()
    print(supported(discriminator["geometric_observable_exists"]))
    print()

    print("Existing input/projection bridge into that observable:")
    print()
    print(
        "SUPPORTED"
        if discriminator["input_bridge_exists"]
        else "NOT ESTABLISHED"
    )
    print()

    print("Existing executable discriminator for Result-024 kernel states:")
    print()
    print(
        "FOUND"
        if discriminator["executable_discriminator"]
        else "NOT FOUND"
    )
    print()

    if discriminator["executable_discriminator"]:
        print("Stopping-boundary verdict:")
        print()
        print("NOT REACHED BY PROVENANCE AUDIT")
        print()
        print(
            "An existing geometric readout path was detected. "
            "A follow-up numerical characterization is required before "
            "claiming additional state discrimination."
        )
    else:
        print("Stopping-boundary verdict:")
        print()
        print("REACHED FOR CURRENT IMPLEMENTED BRIDGE")
        print()
        print("Reason:")
        print()
        print(
            "M5 contains independently implemented connection and curvature "
            "observables, but the examined code does not establish the "
            "required projection from the N3/N4 rank-2 flavour fields into "
            "that geometric readout."
        )
        print()
        print(
            "Evaluating Gamma_i or R_ij on the Result-023 transformed flavour "
            "states would therefore require an additional derived mapping "
            "rather than merely executing an existing observable."
        )

    print()
    print("Interpretation:")
    print()
    print(
        "Result 015 established that M5 contains genuine non-Hessian "
        "connection/curvature machinery."
    )
    print()
    print(
        "Result 024 established that the existing N3/N4 real overlap sector "
        "adds no discrimination beyond the binary sign of C."
    )
    print()
    print(
        "Test 025 asks whether the independently implemented geometric sector "
        "already supplies the missing discriminator without adding a new "
        "projection."
    )
    print()

    if not discriminator["executable_discriminator"]:
        print(
            "In the examined implementation, the connection/curvature code "
            "operates on its own q0,q hedgehog representation, while the "
            "N3/N4 flavour construction operates on rank-2 M fields."
        )
        print()
        print(
            "No examined executable path establishes M -> (q0,q), "
            "Gamma/R -> flavour readout, or an equivalent connection/"
            "curvature observable on the eight Result-023 states."
        )
        print()
        print(
            "Therefore the current repository does not provide an "
            "independently implemented second discriminator for the "
            "four-element kernels left unresolved by C + Mr."
        )

    print()
    print("Unique V4 selection:")
    print()
    print("NOT ESTABLISHED")
    print()
    print("Q8/{+1,-1} identification:")
    print()
    print("NOT ESTABLISHED")
    print()
    print("Reading Point -> M5 physical mapping:")
    print()
    print("NOT ESTABLISHED")
    print()

    # ------------------------------------------------------------------
    # assertions
    #
    # These assert the pieces that make this test meaningful without
    # asserting in advance that the bridge must be absent.
    # ------------------------------------------------------------------

    assert machinery["field_source_exists"], (
        "Expected M5 field-level connection/curvature source is missing: "
        f"{CONNECTION_SOURCES[1]}"
    )

    assert machinery["field_connection"], (
        "Expected existing field-level connection() implementation was "
        "not found."
    )

    assert machinery["field_curvature"], (
        "Expected existing curvature_magnitude() implementation was "
        "not found."
    )

    assert compatibility["n3_builds_rank2_M_fields"], (
        "Expected N3 flavour-field construction was not found."
    )

    # A detected bridge is NOT an assertion failure.  It changes the
    # scientific outcome: the next step becomes numerical characterization
    # of that already-existing path.
    #
    # Likewise, no bridge is a valid Result-025 outcome.

    print("PASS")


if __name__ == "__main__":
    main()
