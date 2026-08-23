result: "015"
title: "M5 connection/curvature to N4 provenance"
status: "SUPPORTED"

claim:
  tested: >
    Whether existing M5 non-Hessian connection or curvature machinery
    provides an implemented provenance bridge to the antisymmetric
    flavour-space matrix C used by the N4 chiral sector.
  outcome: >
    M5 contains independently implemented antisymmetric connection and
    curvature machinery, but no examined implementation projects that
    machinery onto the N3/N4 flavour configurations to produce N4 C.

m5_connection_machinery:
  status: "IMPLEMENTED"
  symbolic_connection: "Gamma_i = O^T d_i O"
  symmetry_class: "antisymmetric so(3)"
  field_level_connection: >
    Gamma_i = q0 d_i q - (d_i q0) q + q x d_i q
  curvature: "R_ij = Gamma_i x Gamma_j"

n3_reduction:
  prescription: "ENERGY-HESSIAN PROJECTION"

n4_chiral_sector:
  effective_structure: "i * g_chiral * C"
  C_construction: "chiral_overlap(dA, dB)"
  antisymmetric: true
  descendants_reuse_chiral_overlap: true

provenance_test:
  connection_or_curvature_to_n4_C_implementation: "NOT FOUND IN EXAMINED SOURCES"
  candidate_non_hessian_geometric_structure: "EXISTS"
  candidate_identified_with_n4_C: false
  result_014_obstruction_bypassed_by_existing_code: false
  additional_effective_projection_or_derivation: "REQUIRED"

interpretation: >
  M5 contains independently implemented antisymmetric connection and
  curvature machinery. This supplies a genuine non-Hessian geometric
  structure of the kind that could participate in an antisymmetric
  effective sector. However, the examined repository does not project
  Gamma_i or R_ij onto the three N3/N4 flavour configurations. The N4
  branch and the examined N4 descendants instead construct their
  antisymmetric matrix C directly through chiral_overlap(dA, dB).
  Therefore M5 contains a candidate geometric ingredient for the
  additional structure required by Result 014, but no implemented
  provenance bridge establishes that ingredient as the origin of N4 C.

reading_point_to_m5_physical_mapping: "NOT ESTABLISHED"

relation_to_previous_results:
  result_012: >
    P2 contains implemented chiral substrate machinery, but no explicit
    P2-to-N4 parameter bridge was found.
  result_013: >
    The implemented P2 Lifshitz operator and N4 chiral_overlap are
    different operators.
  result_014: >
    The N3 scalar-energy Hessian projection produces a symmetric
    flavour-space Hessian and therefore cannot by itself generate the
    nonzero antisymmetric N4 C.
  result_015: >
    M5 contains non-Hessian connection and curvature geometry, but no
    existing implementation was found that reduces it to N4 C.

next_reading_point: >
  Characterize chiral_overlap(dA,dB) directly as an effective N4
  operator. Test whether C is geometrically reproducible and stable
  under controlled changes of numerical resolution and loop geometry
  before proposing any additional provenance mechanism.

script:
  path: "readingpoint/tests/test_015_m5_connection_to_n4_provenance.py"
