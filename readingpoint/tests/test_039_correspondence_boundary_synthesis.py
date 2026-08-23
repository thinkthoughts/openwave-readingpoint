#!/usr/bin/env python3
"""
Reading Point Test 039
----------------------

Evidence-ledger / correspondence-boundary synthesis.

Purpose
=======

Results 001-038 have progressively constrained the proposed
Reading Point <-> M5 correspondence.

This test does not introduce a new observable, fit a new parameter,
or impose a new cross-system sign convention.

Instead it asks:

    Given the executable evidence already established by Results
    001-038, what is the strongest Reading Point <-> M5
    correspondence currently licensed?

The relevant established ladder is:

    common V4 quotient
        ->
    six abstract quotient isomorphisms
        ->
    independently defined Reading Point and M5 1+2 partitions
        ->
    two partition-preserving isomorphisms
        ->
    complete intrinsic labeling on both sides
        ->
    unresolved cross-system orientation convention

Results 035-038 then tested several repository-native candidates for
anchoring that final orientation bit:

    035  right-handed full-frame convention
    036  N4 self-linking N -> -N
    037  chiral coupling / screw signs
    038  signed Mermin-Ho / topological flux

None licensed identification of the M5 residual C-sign with either
+chi3 or -chi3.

Therefore Test 039 is a stopping-boundary audit.

It reconstructs the relevant groups and mappings directly, records the
prior-result evidence ledger, verifies the remaining correspondence
count, and emits a machine-readable audit.

No Reading Point -> M5 physical mapping is assumed.
"""

from __future__ import annotations

import json
import os
from itertools import permutations


HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.abspath(
    os.path.join(
        HERE,
        "..",
        "results",
        "test_039_correspondence_boundary_synthesis",
    )
)
AUDIT_JSON = os.path.join(RESULT_DIR, "audit.json")


# ======================================================================
# Groups
# ======================================================================

# Result-027 M5 quotient:
#
#     C2^3 / <Ty>
#
# represented as V4 bit pairs.
#
# Txbar and Tzbar are generators; TxTzbar is their product.

M5 = {
    "Ibar": (0, 0),
    "Txbar": (1, 0),
    "Tzbar": (0, 1),
    "TxTzbar": (1, 1),
}

M5_BY_BITS = {v: k for k, v in M5.items()}


# Result-003 Reading Point quotient:
#
#     (Z/30Z)^* / {1,19}
#
# Canonical intrinsic labels from Result 033 are (chi3, chi5).
#
# We encode +1 -> 0 and -1 -> 1 so quotient multiplication becomes XOR.
#
# {1,19}  -> (+,+) -> (0,0)
# {7,13}  -> (+,-) -> (0,1)
# {11,29} -> (-,+) -> (1,0)
# {17,23} -> (-,-) -> (1,1)

RP = {
    "{1,19}": (0, 0),
    "{7,13}": (0, 1),
    "{11,29}": (1, 0),
    "{17,23}": (1, 1),
}

RP_BY_BITS = {v: k for k, v in RP.items()}

M5_ID = "Ibar"
RP_ID = "{1,19}"

M5_NONIDENTITY = ("Txbar", "Tzbar", "TxTzbar")
RP_NONIDENTITY = ("{7,13}", "{11,29}", "{17,23}")


def xor(a, b):
    return (a[0] ^ b[0], a[1] ^ b[1])


def m5_mul(a, b):
    return M5_BY_BITS[xor(M5[a], M5[b])]


def rp_mul(a, b):
    return RP_BY_BITS[xor(RP[a], RP[b])]


# ======================================================================
# Mapping audits
# ======================================================================

def is_bijection(mapping):
    return (
        set(mapping.keys()) == set(M5.keys())
        and set(mapping.values()) == set(RP.keys())
    )


def multiplication_preserving(mapping):
    for a in M5:
        for b in M5:
            lhs = mapping[m5_mul(a, b)]
            rhs = rp_mul(mapping[a], mapping[b])
            if lhs != rhs:
                return False
    return True


def all_identity_preserving_bijections():
    """
    There are 3! = 6 identity-preserving bijections between the
    nonidentity elements of two V4 groups.
    """
    out = []

    for perm in permutations(RP_NONIDENTITY):
        mapping = {M5_ID: RP_ID}
        mapping.update(dict(zip(M5_NONIDENTITY, perm)))
        out.append(mapping)

    return out


# ======================================================================
# Independently established labels
# ======================================================================

# Result 030:
#
# Reading Point parent-order / chi5 partition:
#
# singleton = {11,29}
# pair      = {{7,13}, {17,23}}

RP_SINGLETON = "{11,29}"
RP_PAIR = frozenset({"{7,13}", "{17,23}"})


# Result 031:
#
# M5 full-frame G/R norm partition:
#
# singleton = Txbar
# pair      = {Tzbar, TxTzbar}

M5_SINGLETON = "Txbar"
M5_PAIR = frozenset({"Tzbar", "TxTzbar"})


def partition_preserving(mapping):
    return (
        mapping[M5_SINGLETON] == RP_SINGLETON
        and frozenset(mapping[x] for x in M5_PAIR) == RP_PAIR
    )


# Result 032:
#
# Existing N4 C-sign distinguishes the remaining M5 pair.

M5_C_SIGN = {
    "Tzbar": +1,
    "TxTzbar": -1,
}


# Result 033:
#
# chi3 distinguishes the remaining Reading Point pair.

RP_CHI3 = {
    "{7,13}": +1,
    "{17,23}": -1,
}


def residual_sign_relation(mapping):
    """
    Compare Result-032 C-sign with Result-033 chi3 only after the
    independently established partition bridge has been imposed.

    Return:
        ALIGNED   if C = chi3
        REVERSED  if C = -chi3
        MIXED     otherwise
    """
    aligned = True
    reversed_ = True

    for m5_class in M5_PAIR:
        rp_class = mapping[m5_class]

        c = M5_C_SIGN[m5_class]
        chi3 = RP_CHI3[rp_class]

        if c != chi3:
            aligned = False

        if c != -chi3:
            reversed_ = False

    if aligned:
        return "ALIGNED"

    if reversed_:
        return "REVERSED"

    return "MIXED"


# ======================================================================
# Evidence ledger
# ======================================================================

EVIDENCE_LEDGER = [
    {
        "result": 3,
        "claim": "common V4 quotient",
        "status": "SUPPORTED",
        "role": (
            "(Z/30Z)^*/{1,19} and the abstract Q8/{+1,-1} "
            "comparison have C2 x C2 quotient structure"
        ),
    },
    {
        "result": 27,
        "claim": "repository-native M5 quotient",
        "status": "SUPPORTED",
        "role": (
            "C2^3/<Ty> supplies four composition-compatible "
            "repository-native M5 quotient classes"
        ),
    },
    {
        "result": 28,
        "claim": "abstract M5 <-> Reading Point quotient isomorphisms",
        "status": "SUPPORTED",
        "role": (
            "six identity-preserving multiplication-preserving "
            "V4 isomorphisms remain"
        ),
    },
    {
        "result": 29,
        "claim": "native M5 quotient observables",
        "status": "SUPPORTED",
        "role": (
            "existing longest-axis basic reads descend through <Ty> "
            "and distinguish the nonidentity quotient classes numerically"
        ),
    },
    {
        "result": 30,
        "claim": "Reading Point native 1+2 partition",
        "status": "SUPPORTED",
        "role": (
            "{11,29} is distinguished from the two parent-order-(4,4) "
            "classes"
        ),
    },
    {
        "result": 31,
        "claim": "M5 native 1+2 partition",
        "status": "SUPPORTED",
        "role": (
            "G_norm and R_norm distinguish Txbar from "
            "{Tzbar, TxTzbar}"
        ),
    },
    {
        "result": 32,
        "claim": "M5 residual-pair C-sign label",
        "status": "SUPPORTED",
        "role": (
            "Tzbar and TxTzbar carry opposite quotient-level "
            "N4 C signs"
        ),
    },
    {
        "result": 33,
        "claim": "Reading Point residual-pair chi3 label",
        "status": "SUPPORTED",
        "role": (
            "canonical mod-3 character distinguishes "
            "{7,13} from {17,23}"
        ),
    },
    {
        "result": 34,
        "claim": "two-bit cross-system correspondence audit",
        "status": "SUPPORTED",
        "role": (
            "two partition-preserving mappings remain; one aligns "
            "C-sign with chi3 and one reverses it"
        ),
    },
    {
        "result": 35,
        "claim": "right-handed full-frame C-sign anchor",
        "status": "NOT_SUPPORTED",
        "role": (
            "full_frame is right-handed by construction, but actual "
            "spatial reflection does not reverse C"
        ),
    },
    {
        "result": 36,
        "claim": "self-linking N -> -N C-sign anchor",
        "status": "NOT_ESTABLISHED",
        "role": (
            "native N4 self-linking reversal gives no clean full-C "
            "or baseline-subtracted dC orientation law"
        ),
    },
    {
        "result": 37,
        "claim": "native chiral-sign C anchor",
        "status": "NOT_ESTABLISHED",
        "role": (
            "g_chiral reverses g_chiral*C but not geometric C; "
            "chi sign also leaves geometric C approximately even"
        ),
    },
    {
        "result": 38,
        "claim": "Mermin-Ho/topological-flux C-sign anchor",
        "status": "NOT_ESTABLISHED",
        "role": (
            "native signed basic flux numerically distinguishes the "
            "residual pair but gives both classes the same tested sign"
        ),
    },
]


# ======================================================================
# Main audit
# ======================================================================

def main():
    print("Reading Point Test 039")
    print("----------------------")
    print()
    print("Evidence-ledger / correspondence-boundary synthesis")
    print()

    print("=" * 72)
    print("Scope")
    print("=" * 72)
    print()
    print("New M5 observable introduced:")
    print("NO")
    print()
    print("New Reading Point arithmetic label introduced:")
    print("NO")
    print()
    print("New cross-system sign convention imposed:")
    print("NO")
    print()
    print("Purpose:")
    print(
        "Reconstruct the strongest correspondence licensed by "
        "Results 001-038."
    )
    print()

    # ------------------------------------------------------------------
    # A. Reconstruct abstract V4 correspondence count
    # ------------------------------------------------------------------

    print("=" * 72)
    print("A. Abstract quotient reconstruction")
    print("=" * 72)
    print()

    candidates = all_identity_preserving_bijections()

    iso = [
        m for m in candidates
        if is_bijection(m) and multiplication_preserving(m)
    ]

    print("Identity-preserving bijections tested:")
    print(len(candidates))
    print()

    print("Multiplication-preserving V4 isomorphisms:")
    print(len(iso))
    print()

    assert len(candidates) == 6
    assert len(iso) == 6

    print("Result-028 sixfold abstract ambiguity reproduced:")
    print("SUPPORTED")
    print()

    # ------------------------------------------------------------------
    # B. Apply independently established 1+2 partitions
    # ------------------------------------------------------------------

    print("=" * 72)
    print("B. Independent 1+2 partition bridge")
    print("=" * 72)
    print()

    print("M5 partition:")
    print(f"  singleton = {M5_SINGLETON}")
    print(f"  pair      = {{{', '.join(sorted(M5_PAIR))}}}")
    print()

    print("Reading Point partition:")
    print(f"  singleton = {RP_SINGLETON}")
    print(f"  pair      = {{{', '.join(sorted(RP_PAIR))}}}")
    print()

    partition_iso = [m for m in iso if partition_preserving(m)]

    print("Partition-preserving isomorphisms:")
    print(len(partition_iso))
    print()

    assert len(partition_iso) == 2

    print("6 -> 2 structural reduction:")
    print("SUPPORTED")
    print()

    # ------------------------------------------------------------------
    # C. Display the two surviving mappings
    # ------------------------------------------------------------------

    print("=" * 72)
    print("C. Remaining quotient isomorphisms")
    print("=" * 72)
    print()

    mapping_rows = []

    for idx, mapping in enumerate(partition_iso, start=1):
        relation = residual_sign_relation(mapping)

        print(f"Mapping {idx}:")
        for key in ("Ibar", "Txbar", "Tzbar", "TxTzbar"):
            print(f"  {key:<10} -> {mapping[key]}")

        print(f"  residual C-sign / chi3 relation = {relation}")
        print()

        mapping_rows.append(
            {
                "index": idx,
                "mapping": mapping,
                "multiplication_preserving": True,
                "partition_preserving": True,
                "residual_C_chi3_relation": relation,
            }
        )

    relations = sorted(
        row["residual_C_chi3_relation"]
        for row in mapping_rows
    )

    assert relations == ["ALIGNED", "REVERSED"]

    print("One aligned mapping exists:")
    print("SUPPORTED")
    print()

    print("One reversed mapping exists:")
    print("SUPPORTED")
    print()

    # ------------------------------------------------------------------
    # D. Internal labeling status
    # ------------------------------------------------------------------

    print("=" * 72)
    print("D. Internal quotient labeling")
    print("=" * 72)
    print()

    print("Reading Point:")
    print("  first label  = chi5 / mod-5 quadratic character")
    print("  second label = chi3 / nontrivial mod-3 character")
    print("  all four quotient classes intrinsically labeled = SUPPORTED")
    print()

    print("M5:")
    print("  first label  = full-frame G/R norm partition")
    print("  second label = N4 C-sign")
    print("  all four tested quotient classes intrinsically labeled = SUPPORTED")
    print()

    print("Complete internal labeling on both sides:")
    print("SUPPORTED")
    print()

    print("Complete internal labeling implies unique cross-system mapping:")
    print("NO")
    print()

    # ------------------------------------------------------------------
    # E. Orientation-anchor evidence
    # ------------------------------------------------------------------

    print("=" * 72)
    print("E. Native orientation-anchor audit")
    print("=" * 72)
    print()

    anchors = [
        (
            35,
            "right-handed full-frame convention",
            "NO C-sign anchor",
        ),
        (
            36,
            "self-linking N -> -N",
            "NO CLEAN C-sign anchor",
        ),
        (
            37,
            "g_chiral / chi signs",
            "WEIGHTED-TERM SIGN ONLY",
        ),
        (
            38,
            "Mermin-Ho / topological-flux sign",
            "SAME RESIDUAL-PAIR SIGN",
        ),
    ]

    for number, label, verdict in anchors:
        print(f"Result {number:03d}")
        print(f"  candidate = {label}")
        print(f"  verdict   = {verdict}")
        print()

    independent_alignment_rule_found = False

    print("Independent rule establishing C-sign = chi3:")
    print("NOT FOUND")
    print()

    print("Independent rule establishing C-sign = -chi3:")
    print("NOT FOUND")
    print()

    # ------------------------------------------------------------------
    # F. Evidence ledger
    # ------------------------------------------------------------------

    print("=" * 72)
    print("F. Evidence ledger")
    print("=" * 72)
    print()

    for row in EVIDENCE_LEDGER:
        print(
            f"Result {row['result']:03d}  "
            f"{row['claim']:<52} "
            f"{row['status']}"
        )

    print()

    # ------------------------------------------------------------------
    # G. Strongest licensed correspondence
    # ------------------------------------------------------------------

    print("=" * 72)
    print("G. Strongest licensed correspondence")
    print("=" * 72)
    print()

    strongest = {
        "common_v4_quotient": "SUPPORTED",
        "repository_native_m5_quotient": "SUPPORTED",
        "readingpoint_intrinsic_labeling": "SUPPORTED",
        "m5_intrinsic_labeling": "SUPPORTED",
        "partition_level_cross_system_correspondence": "SUPPORTED",
        "abstract_isomorphism_count": 6,
        "partition_preserving_isomorphism_count": 2,
        "current_admissible_cross_system_mappings": 2,
        "independent_orientation_alignment_rule": "NOT_FOUND",
        "unique_structural_correspondence": "NOT_ESTABLISHED",
        "physical_mapping": "NOT_ESTABLISHED",
    }

    print("Common quotient structure:")
    print(strongest["common_v4_quotient"])
    print()

    print("Repository-native M5 quotient:")
    print(strongest["repository_native_m5_quotient"])
    print()

    print("Reading Point quotient intrinsically labeled:")
    print(strongest["readingpoint_intrinsic_labeling"])
    print()

    print("M5 quotient intrinsically labeled:")
    print(strongest["m5_intrinsic_labeling"])
    print()

    print("Partition-level cross-system correspondence:")
    print(strongest["partition_level_cross_system_correspondence"])
    print()

    print("Abstract quotient isomorphisms:")
    print(strongest["abstract_isomorphism_count"])
    print()

    print("Partition-preserving isomorphisms:")
    print(strongest["partition_preserving_isomorphism_count"])
    print()

    print("Currently admissible cross-system mappings:")
    print(strongest["current_admissible_cross_system_mappings"])
    print()

    print("Independent orientation-alignment rule:")
    print(strongest["independent_orientation_alignment_rule"])
    print()

    print("Unique structural correspondence:")
    print(strongest["unique_structural_correspondence"])
    print()

    print("Reading Point -> M5 physical mapping:")
    print(strongest["physical_mapping"])
    print()

    # ------------------------------------------------------------------
    # H. Stopping boundary
    # ------------------------------------------------------------------

    print("=" * 72)
    print("H. Current implementation stopping boundary")
    print("=" * 72)
    print()

    assert len(iso) == 6
    assert len(partition_iso) == 2
    assert not independent_alignment_rule_found

    stopping_boundary = True

    print("Existing executable evidence reduces 6 -> 2:")
    print("SUPPORTED")
    print()

    print("Existing executable evidence reduces 2 -> 1:")
    print("NOT SUPPORTED")
    print()

    print("Additional sign convention required for 2 -> 1:")
    print("YES")
    print()

    print("Such a convention independently established by Results 001-038:")
    print("NO")
    print()

    print("Current implementation stopping boundary:")
    print("SUPPORTED")
    print()

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    audit = {
        "test": 39,
        "name": "correspondence_boundary_synthesis",
        "scope": {
            "new_m5_observable": False,
            "new_readingpoint_label": False,
            "new_cross_system_sign_convention": False,
        },
        "abstract_quotient": {
            "identity_preserving_bijections_tested": len(candidates),
            "multiplication_preserving_isomorphisms": len(iso),
            "result_028_reproduced": len(iso) == 6,
        },
        "partition_bridge": {
            "m5_singleton": M5_SINGLETON,
            "m5_pair": sorted(M5_PAIR),
            "readingpoint_singleton": RP_SINGLETON,
            "readingpoint_pair": sorted(RP_PAIR),
            "partition_preserving_isomorphisms": len(partition_iso),
            "reduction_6_to_2": len(partition_iso) == 2,
        },
        "remaining_mappings": mapping_rows,
        "internal_labeling": {
            "readingpoint": {
                "first_label": "chi5",
                "second_label": "chi3",
                "fully_distinguished": True,
            },
            "m5": {
                "first_label": "full-frame G/R norm partition",
                "second_label": "N4 C-sign",
                "fully_distinguished": True,
            },
        },
        "orientation_anchor_audits": [
            {
                "result": number,
                "candidate": label,
                "verdict": verdict,
            }
            for number, label, verdict in anchors
        ],
        "independent_alignment_rule": {
            "C_equals_chi3": False,
            "C_equals_minus_chi3": False,
            "found": False,
        },
        "evidence_ledger": EVIDENCE_LEDGER,
        "strongest_licensed_correspondence": strongest,
        "stopping_boundary": {
            "reduction_6_to_2_supported": True,
            "reduction_2_to_1_supported": False,
            "additional_cross_system_orientation_rule_required": True,
            "such_rule_established_in_results_001_038": False,
            "current_implementation_stopping_boundary": stopping_boundary,
        },
        "conclusion": (
            "The Reading Point quotient and the repository-native M5 "
            "quotient share V4 structure and compatible independently "
            "defined singleton-plus-pair label partitions. This reduces "
            "the six abstract quotient isomorphisms to two. Both systems "
            "are internally fully labeled, but Results 035-038 do not "
            "supply an independent cross-system orientation rule that "
            "selects between the aligned and reversed residual-sign "
            "mappings. A unique Reading Point -> M5 correspondence and "
            "a physical mapping therefore remain unestablished."
        ),
        "result": "PASS",
    }

    os.makedirs(RESULT_DIR, exist_ok=True)

    with open(AUDIT_JSON, "w") as f:
        json.dump(audit, f, indent=2)

    print("JSON summary:")
    print(
        "readingpoint/results/"
        "test_039_correspondence_boundary_synthesis/audit.json"
    )
    print()

    # ------------------------------------------------------------------
    # Required final statement
    # ------------------------------------------------------------------

    print("=" * 72)
    print("Required final statement")
    print("=" * 72)
    print()

    print("RESULT 039:")
    print()
    print(
        "Results 001-038 license a shared V4 quotient and an "
        "independently supported partition-level Reading Point <-> M5 "
        "correspondence that reduces six abstract quotient isomorphisms "
        "to two."
    )
    print()
    print(
        "Both quotients are internally fully labeled, but no "
        "independently implemented cross-system orientation rule "
        "selects between the two remaining mappings."
    )
    print()
    print(
        "Unique Reading Point -> M5 correspondence: "
        "NOT ESTABLISHED"
    )
    print()
    print(
        "Reading Point -> M5 physical mapping: "
        "NOT ESTABLISHED"
    )
    print()
    print("Current implementation stopping boundary: SUPPORTED")
    print()
    print("PASS")


if __name__ == "__main__":
    main()
