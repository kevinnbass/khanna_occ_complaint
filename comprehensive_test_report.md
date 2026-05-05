# Comprehensive test report

Generated: 2026-05-05 09:25:59 UTC
Args: network=False release=False gemini=False quick=False

| status | category | name | detail |
|---|---|---|---|
| **PASS** | A | manifest_exists |  |
| **PASS** | A | manifest_parseable | 366 entries |
| **PASS** | A | manifest_no_missing_files | 0 missing |
| **PASS** | A | manifest_all_shas_match | 0 drifted |
| **PASS** | A | manifest_exhaustive | 0 files on disk missing from manifest |
| **PASS** | A | ots_proof_exists | 646 bytes |
| **PASS** | A | script_present:welcome.py |  |
| **PASS** | A | script_present:reproduce_all.py |  |
| **PASS** | A | script_present:verify_anchors_occ.py |  |
| **PASS** | A | script_present:tier_e_reocr.py |  |
| **PASS** | A | script_present:tier_f_full_rederive.py |  |
| **PASS** | A | script_present:stamp_timestamp.py |  |
| **PASS** | A | script_present:verify_timestamp.py |  |
| **PASS** | A | script_present:upgrade_timestamp.py |  |
| **PASS** | A | script_present:build_provenance.py |  |
| **PASS** | A | script_present:fetch_substrate_occ.py |  |
| **PASS** | A | script_present:strip_markers_pre_filing.py |  |
| **PASS** | A | body_file_present:OCC_COMPLAINT_KHANNA.md |  |
| **PASS** | A | body_file_present:HOUSE_ETHICS_SUBMISSION_KHANNA.md |  |
| **PASS** | A | body_file_present:DOJ_REFERRAL_KHANNA.md |  |
| **PASS** | A | body_file_present:OCC_EXHIBIT_LIST.md |  |
| **PASS** | A | body_file_present:README.md |  |
| **PASS** | A | body_file_present:VERIFICATION_TIERS.md |  |
| **PASS** | A | body_file_present:LIMITATIONS.md |  |
| **PASS** | A | body_file_present:REPRODUCIBILITY_METHODOLOGY_OCC.md |  |
| **PASS** | A | body_file_present:_provenance_index_occ.json |  |
| **PASS** | A | snapshots_count | 13 snapshot.json + 13 provenance.json |
| **PASS** | A | snapshots_paired_with_provenance | 0 unpaired |
| **PASS** | B | all_snapshot_json_valid | 26 files; 0 invalid |
| **PASS** | B | provenance_required_fields | 13 provenance files; 0 missing fields |
| **PASS** | B | provenance_snapshot_sha_matches | 0 mismatches |
| **PASS** | B | manifest_all_shas_well_formed | 0 malformed SHAs |
| **PASS** | B | provenance_endpoint_shas_well_formed | 0 malformed |
| **PASS** | B | provenance_urls_well_formed | 0 malformed URLs |
| **PASS** | B | provenance_index_self_consistent | n_entries=64 len=64 |
| **PASS** | B | provenance_index_claim_ids_well_formed | 0 bad ids |
| **PASS** | C | body_markers_resolved_in_index | 64 body / 64 index; 0 body markers without index entry |
| **PASS** | C | index_entries_appear_in_body | 0 index entries not in body |
| **PASS** | C | exhibit_list_references_resolve | 28 unique refs; 0 unresolved |
| **PASS** | C | all_six_counts_present_in_body | found [1, 2, 3, 4, 5, 6]; missing [] |
| **PASS** | C | substrate_snapshot_references_resolve | 0 bad refs |
| **PASS** | D | no_V1_path_leaks_in_body | 0 occurrences |
| **PASS** | D | no_hardcoded_windows_paths_in_scripts | 0 occurrences |
| **PASS** | D | no_tmp_paths_in_scripts | 0 occurrences |
| **PASS** | D | no_TODO_FIXME_in_operative_filings | 0 occurrences |
| **PASS** | E | help:reproduce_all.py |  |
| **PASS** | E | help:verify_anchors_occ.py |  |
| **PASS** | E | help:tier_e_reocr.py |  |
| **PASS** | E | help:tier_f_full_rederive.py |  |
| **PASS** | E | help:stamp_timestamp.py |  |
| **PASS** | E | help:verify_timestamp.py |  |
| **PASS** | E | help:upgrade_timestamp.py |  |
| **PASS** | E | help:build_provenance.py |  |
| **PASS** | E | help:fetch_substrate_occ.py |  |
| **PASS** | E | help:strip_markers_pre_filing.py |  |
| **PASS** | E | welcome_prints_banner |  |
| **PASS** | E | welcome_skip_path_clean_exit |  |
| **PASS** | E | verify_anchors_spot_check_runs |  |
| **PASS** | E | verify_anchors_spot_check_specific_marker | coverage: [('OCC_M007', 114), ('OCC_M008', 114), ('OCC_M002', 0), ('OCC_M033', 0)] |
| **PASS** | E | reproduce_all_verbose_dumps_subprocess_output |  |
| **PASS** | F | root_python_files_parse | 13 .py files; 0 bad |
| **PASS** | F | data_ocr_products_python_files_parse | 6 .py files; 0 bad |
| **PASS** | F | data_occ_json_files_valid | 26 JSONs; 0 bad |
| **PASS** | F | provenance_index_valid_json |  |
| **PASS** | G | tier_0_pass |  |
| **PASS** | G | tier_1_pass |  |
| **PASS** | G | tier_2_pass |  |
| **PASS** | G | overall_pass |  |
| **PASS** | G | rebuild:rebuild_ptr_audit_khanna.py | SUMMARY: 10/10 fields match expected (0 drift) |
| **PASS** | G | rebuild:rebuild_pfd_schedule_d_khanna.py | SUMMARY: 20/20 fields match snapshot (0 drift) |
| **PASS** | G | rebuild:rebuild_trade_pnl_khanna.py | SUMMARY: 1/1 bit-exact, 0 pass-with-defect (<=5% post-cascade band), 0 drift, 0 error |
| **PASS** | G | verifier_all_anchors_pass | 66/66 OK; 0 FAIL |
| **PASS** | G | ots_proof_verifies |  |
| **PASS** | G | rebuild_output:ptr_filing_audit_khanna_REBUILT.json | 1,083 bytes; top-level keys=['rebuild_run_at', 'snapshot_input', 'snapshot_date'] |
| **PASS** | G | rebuild_output:pfd_schedule_d_khanna_REBUILT.json | 1,039 bytes; top-level keys=['rebuild_run_at', 'snapshot_input', 'snapshot_date'] |
| **PASS** | G | rebuild_output:trade_pnl_facts_REBUILT.json | 2,437 bytes; top-level keys=['rebuild_run_at', 'snapshot_inputs', 'snapshot_date'] |
| **PASS** | H | tier0_catches_sha_corruption | tier0_fail=True has_drift=True has_hint=True |
| **PASS** | H | tier0_catches_missing_file | tier0_fail=True has_missing=True has_hint=True |
| **PASS** | H | failure_classification_pack_correct | 6/6 ok |
| **PASS** | I | reproduce_all_deterministic | both runs: ('PASS', 66, 66) |
| **PASS** | I | rebuilds_deterministic | 3 rebuilds; 0 non-deterministic |
| **SKIP** | J | tests_skipped | --network not specified |
| **SKIP** | K | tests_skipped | --gemini not specified |

## Summary

- PASS: 81
- FAIL: 0
- SKIP: 2
- WARN: 0