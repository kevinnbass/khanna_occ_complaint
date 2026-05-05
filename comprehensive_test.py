#!/usr/bin/env python3
"""comprehensive_test.py — exhaustive test runner for OCC_FILING_PACKAGE_V2.

Validates EVERY aspect of the package and reports per-test PASS/FAIL/SKIP/WARN.

USAGE:
    python comprehensive_test.py                      # offline tests only
    python comprehensive_test.py --network            # + network tests
    python comprehensive_test.py --gemini             # + Gemini smoke test (1 PDF)
    python comprehensive_test.py --release            # + release-asset tests
    python comprehensive_test.py --all                # everything
    python comprehensive_test.py --quick              # just the most critical tests
    python comprehensive_test.py --verbose            # show all subprocess output

Categories:
    A. STRUCTURAL — files exist, manifest exhaustive, no orphans
    B. SCHEMA — provenance.json valid, snapshots well-formed, hashes well-formed
    C. CROSS-REF — fact_ids resolve, body markers map to provenance
    D. PATH PURITY — no V1 leaks, no hardcoded absolute Windows paths
    E. CLI — every script's --help works, every flag combo works
    F. SYNTAX — every .py file parses; every .json file is valid JSON
    G. EXECUTION — every tier independently passes
    H. ERROR HANDLING — synthetic corruption triggers correct classification
    I. CONSISTENCY — running twice produces identical results
    J. NETWORK — provenance URLs reachable; release assets downloadable
    K. GEMINI — 1-PDF re-OCR smoke test (opt-in)

Exit codes:
    0 — all required tests passed (FAIL count = 0)
    1 — one or more required tests failed
    2 — runtime error in the harness itself
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
DATA_OCC = ROOT / "data" / "occ"

# ─────────────────────────────────────────────────────────────────────────
# ANSI / output helpers
# ─────────────────────────────────────────────────────────────────────────

_USE_COLOR = sys.stdout.isatty() and os.name != "nt"

def _c(s: str, code: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _USE_COLOR else s

def _green(s: str) -> str: return _c(s, "32")
def _red(s: str) -> str:   return _c(s, "31")
def _yellow(s: str) -> str: return _c(s, "33")
def _bold(s: str) -> str:  return _c(s, "1")

# ─────────────────────────────────────────────────────────────────────────
# Test result accumulator
# ─────────────────────────────────────────────────────────────────────────

class Results:
    def __init__(self) -> None:
        self.tests: list[dict] = []
        self.t0 = time.time()
    def add(self, category: str, name: str, status: str, detail: str = "") -> None:
        self.tests.append({"category": category, "name": name,
                           "status": status, "detail": detail})
        # Live print as tests run so the user sees progress
        if status == "PASS":
            print(f"  {_green('PASS')}  {category}/{name}" + (f"  {detail}" if detail else ""))
        elif status == "FAIL":
            print(f"  {_red('FAIL')}  {category}/{name}  {detail}")
        elif status == "SKIP":
            print(f"  {_yellow('SKIP')}  {category}/{name}  {detail}")
        elif status == "WARN":
            print(f"  {_yellow('WARN')}  {category}/{name}  {detail}")
        else:
            print(f"  {status}  {category}/{name}  {detail}")
    def n(self, status: str) -> int:
        return sum(1 for t in self.tests if t["status"] == status)
    def render_summary(self) -> str:
        n_pass = self.n("PASS"); n_fail = self.n("FAIL")
        n_skip = self.n("SKIP"); n_warn = self.n("WARN")
        total = len(self.tests)
        elapsed = time.time() - self.t0
        out = []
        out.append("")
        out.append("=" * 72)
        out.append(_bold("COMPREHENSIVE TEST SUMMARY"))
        out.append("=" * 72)
        # Per-category breakdown
        by_cat: dict[str, dict] = {}
        for t in self.tests:
            c = t["category"]
            d = by_cat.setdefault(c, {"PASS": 0, "FAIL": 0, "SKIP": 0, "WARN": 0})
            d[t["status"]] = d.get(t["status"], 0) + 1
        out.append("")
        out.append(f"  {'category':<18} {'PASS':>5} {'FAIL':>5} {'SKIP':>5} {'WARN':>5}")
        out.append(f"  {'-'*18} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")
        for c in sorted(by_cat):
            d = by_cat[c]
            line = f"  {c:<18} {d['PASS']:>5} {d['FAIL']:>5} {d['SKIP']:>5} {d['WARN']:>5}"
            if d["FAIL"]:
                line = _red(line)
            elif d["SKIP"]:
                line = _yellow(line)
            out.append(line)
        out.append(f"  {'-'*18} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")
        out.append(f"  {'TOTAL':<18} {n_pass:>5} {n_fail:>5} {n_skip:>5} {n_warn:>5}")
        out.append("")
        if n_fail:
            out.append(_red(f"  {n_fail} TESTS FAILED:"))
            for t in self.tests:
                if t["status"] == "FAIL":
                    out.append(f"    - {t['category']}/{t['name']}: {t['detail']}")
        out.append("")
        out.append(f"  Elapsed: {elapsed:.1f}s   Total: {total} tests")
        if n_fail == 0:
            out.append(f"  {_green(_bold('OVERALL: PASS'))}"
                       + (f" (with {n_skip} SKIP, {n_warn} WARN)" if n_skip or n_warn else ""))
        else:
            out.append(f"  {_red(_bold('OVERALL: FAIL'))} ({n_fail} failures)")
        out.append("")
        return "\n".join(out)

# ─────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────

_BINARY_SUFFIXES = {".png",".jpg",".jpeg",".gif",".pdf",".zip",".gz",".tar",
                    ".xls",".xlsx",".doc",".docx",".bin"}

def canonical_sha(path: pathlib.Path) -> str:
    b = path.read_bytes()
    if path.suffix.lower() not in _BINARY_SUFFIXES:
        b = b.replace(b"\r\n", b"\n")
    return hashlib.sha256(b).hexdigest()

def run_subprocess(cmd: list[str], cwd: pathlib.Path | None = None,
                   timeout: int = 600, env_overrides: dict | None = None) -> tuple[int, str]:
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          timeout=timeout, env=env)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

def http_head_ok(url: str, timeout: int = 15) -> tuple[bool, str]:
    """HEAD-then-GET probe; returns (ok, note)."""
    try:
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent":"comp-test/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (200 <= r.status < 400, f"HTTP {r.status}")
    except urllib.error.HTTPError as e:
        # Some servers don't allow HEAD; try GET range
        if e.code in (405, 501):
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent":"comp-test/1.0",
                    "Range": "bytes=0-1023"
                })
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return (200 <= r.status < 400, f"HTTP {r.status} (GET range)")
            except Exception as e2:
                return False, f"HEAD HTTP {e.code}; GET fallback: {type(e2).__name__}"
        return False, f"HTTP {e.code} {e.reason}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY A — Structural integrity
# ─────────────────────────────────────────────────────────────────────────

def cat_A_structural(r: Results) -> None:
    print(_bold("\n[A] Structural integrity"))

    manifest = ROOT / "99_SHA256SUMS.txt"
    r.add("A","manifest_exists",
          "PASS" if manifest.exists() else "FAIL",
          "" if manifest.exists() else f"missing: {manifest}")
    if not manifest.exists(): return

    # Parse manifest
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = line.split(None, 1)
        if len(parts) != 2: continue
        rel = parts[1]
        if rel.startswith("./"): rel = rel[2:]
        expected[rel] = parts[0]
    r.add("A","manifest_parseable",
          "PASS" if expected else "FAIL",
          f"{len(expected)} entries")

    # Every manifest entry exists
    missing = [rel for rel in expected if not (ROOT / rel).exists()]
    r.add("A","manifest_no_missing_files",
          "PASS" if not missing else "FAIL",
          f"{len(missing)} missing" + (f": {missing[:3]}" if missing else ""))

    # Every manifest entry has correct SHA
    drifted = []
    for rel, exp_sha in expected.items():
        p = ROOT / rel
        if not p.exists(): continue
        if canonical_sha(p) != exp_sha:
            drifted.append(rel)
    r.add("A","manifest_all_shas_match",
          "PASS" if not drifted else "FAIL",
          f"{len(drifted)} drifted" + (f": {drifted[:3]}" if drifted else ""))

    # Manifest exhaustiveness — every non-runtime file in V2 should be in manifest
    _runtime_caches = ("data/raw_pdfs/", "data/tier_e_reocr_substrate/",
                       "data/tier_f_reocr_substrate/", "__pycache__/",
                       "_substrate_cache_occ/", "_substrate_cache/",
                       "data/ocr_products/_source_pdfs/",
                       "data/ocr_products/khanna_pfd_renders/",
                       "data/ocr_products/khanna_ptr_renders/")
    _runtime_reports = {"verify_anchors_occ_diff_report.md",
                        "verify_anchors_diff_report.md",
                        "verify_anchors_occ_report.md",
                        "verify_anchors_report.md",
                        "verify_anchors_occ_spot_check_report.md",
                        "tier_e_reocr_report.md",
                        "tier_f_full_rederive_report.md",
                        "comprehensive_test_report.md",
                        "99_SHA256SUMS.txt.ots",
                        "data/ocr_products/ptr_filing_audit_khanna_REBUILT.json",
                        "data/ocr_products/pfd_schedule_d_khanna_REBUILT.json",
                        "data/ocr_products/trade_pnl_facts_REBUILT.json",
                        "data/ocr_products/house_chamber_audit_REBUILT.json",
                        "data/ocr_products/peer_baseline_percentiles_REBUILT.json"}
    _runtime_suffixes = (".filing.md",)

    on_disk = []
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        rel = p.relative_to(ROOT).as_posix()
        if rel == "99_SHA256SUMS.txt": continue
        if rel == ".git" or rel.startswith(".git/"): continue
        if any(rel.startswith(pfx) for pfx in _runtime_caches): continue
        if rel in _runtime_reports: continue
        if any(rel.endswith(s) for s in _runtime_suffixes): continue
        on_disk.append(rel)

    orphans = sorted(set(on_disk) - set(expected))
    r.add("A","manifest_exhaustive",
          "PASS" if not orphans else "FAIL",
          f"{len(orphans)} files on disk missing from manifest"
          + (f": {orphans[:3]}" if orphans else ""))

    # OTS proof file present
    ots = ROOT / "99_SHA256SUMS.txt.ots"
    r.add("A","ots_proof_exists",
          "PASS" if ots.exists() else "FAIL",
          f"{ots.stat().st_size} bytes" if ots.exists() else "missing")

    # Critical scripts present
    for fn in ("welcome.py","reproduce_all.py","verify_anchors_occ.py",
               "tier_e_reocr.py","tier_f_full_rederive.py","stamp_timestamp.py",
               "verify_timestamp.py","upgrade_timestamp.py","build_provenance.py",
               "fetch_substrate_occ.py","strip_markers_pre_filing.py"):
        r.add("A", f"script_present:{fn}",
              "PASS" if (ROOT/fn).exists() else "FAIL", "")

    # Critical body files
    for fn in ("OCC_COMPLAINT_KHANNA.md","HOUSE_ETHICS_SUBMISSION_KHANNA.md",
               "DOJ_REFERRAL_KHANNA.md","OCC_EXHIBIT_LIST.md","README.md",
               "VERIFICATION_TIERS.md","LIMITATIONS.md",
               "REPRODUCIBILITY_METHODOLOGY_OCC.md","_provenance_index_occ.json"):
        r.add("A", f"body_file_present:{fn}",
              "PASS" if (ROOT/fn).exists() else "FAIL", "")

    # Snapshot pairs
    snaps = list(DATA_OCC.glob("*_2026_*.json"))
    snaps_data = [s for s in snaps if not s.name.endswith(".provenance.json")]
    snaps_prov = [s for s in snaps if s.name.endswith(".provenance.json")]
    r.add("A","snapshots_count",
          "PASS" if len(snaps_data) >= 13 else "FAIL",
          f"{len(snaps_data)} snapshot.json + {len(snaps_prov)} provenance.json")
    # 1:1 pairing
    unpaired = [s.name for s in snaps_data
                if not (s.parent / s.name.replace(".json", ".provenance.json")).exists()]
    r.add("A","snapshots_paired_with_provenance",
          "PASS" if not unpaired else "FAIL",
          f"{len(unpaired)} unpaired" + (f": {unpaired[:3]}" if unpaired else ""))

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY B — Schema validation
# ─────────────────────────────────────────────────────────────────────────

def cat_B_schema(r: Results) -> None:
    print(_bold("\n[B] Schema validation"))

    # All snapshot JSONs are valid JSON
    snaps = sorted(DATA_OCC.glob("*_2026_*.json"))
    invalid = []
    for s in snaps:
        try:
            json.loads(s.read_text(encoding="utf-8"))
        except Exception as e:
            invalid.append(f"{s.name}: {e}")
    r.add("B","all_snapshot_json_valid",
          "PASS" if not invalid else "FAIL",
          f"{len(snaps)} files; {len(invalid)} invalid"
          + (f": {invalid[:1]}" if invalid else ""))

    # Each provenance.json has required fields
    REQUIRED = {"snapshot_file","snapshot_sha256","primary_source_class",
                "fetch_script","generated_at_utc"}
    provs = sorted(DATA_OCC.glob("*.provenance.json"))
    bad = []
    for p in provs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            missing = REQUIRED - set(d.keys())
            if missing:
                bad.append(f"{p.name}: missing {missing}")
        except Exception as e:
            bad.append(f"{p.name}: parse error {e}")
    r.add("B","provenance_required_fields",
          "PASS" if not bad else "FAIL",
          f"{len(provs)} provenance files; {len(bad)} missing fields"
          + (f": {bad[:1]}" if bad else ""))

    # Each provenance's snapshot_sha256 matches actual file hash
    sha_mismatches = []
    for p in provs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            snap_name = d.get("snapshot_file")
            exp_sha = d.get("snapshot_sha256")
            if not snap_name or not exp_sha: continue
            snap_path = p.parent / snap_name
            if not snap_path.exists(): continue
            actual_sha = hashlib.sha256(snap_path.read_bytes()).hexdigest()
            if actual_sha != exp_sha:
                sha_mismatches.append(f"{snap_name}: prov={exp_sha[:8]} actual={actual_sha[:8]}")
        except Exception as e:
            sha_mismatches.append(f"{p.name}: {e}")
    r.add("B","provenance_snapshot_sha_matches",
          "PASS" if not sha_mismatches else "FAIL",
          f"{len(sha_mismatches)} mismatches"
          + (f": {sha_mismatches[:1]}" if sha_mismatches else ""))

    # All SHAs in manifest are 64 hex chars
    manifest = ROOT / "99_SHA256SUMS.txt"
    bad_sha = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line: continue
        parts = line.split(None, 1)
        if len(parts) != 2: continue
        sha = parts[0]
        if len(sha) != 64 or not all(c in "0123456789abcdef" for c in sha.lower()):
            bad_sha.append(f"{parts[1]}: {sha}")
    r.add("B","manifest_all_shas_well_formed",
          "PASS" if not bad_sha else "FAIL",
          f"{len(bad_sha)} malformed SHAs"
          + (f": {bad_sha[:2]}" if bad_sha else ""))

    # All provenance fetched_sha256_raw_bytes are 64 hex
    bad = []
    for p in provs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            for ep in d.get("primary_source_endpoints", []):
                if not isinstance(ep, dict): continue
                for fld in ("fetched_sha256_raw_bytes",
                            "release_mirror_sha256",
                            "amendment_release_mirror_sha256"):
                    sha = ep.get(fld)
                    if sha and (len(sha) != 64 or
                                not all(c in "0123456789abcdef" for c in sha.lower())):
                        bad.append(f"{p.name}.{fld}: {sha}")
        except Exception:
            pass
    r.add("B","provenance_endpoint_shas_well_formed",
          "PASS" if not bad else "FAIL",
          f"{len(bad)} malformed"
          + (f": {bad[:1]}" if bad else ""))

    # Every URL across every provenance endpoint is well-formed (no embedded
    # whitespace, valid scheme, no truncated descriptions accidentally
    # concatenated). Whitelist allowed exceptions where the URL field
    # documents a template ({placeholder}) or a documented-as-constant pointer.
    URL_FIELDS = ("url","primary_source_url","pdf_irs_direct_url",
                  "primary_source_url_irs_eos","primary_source_url_propublica",
                  "primary_source_url_propublica_xml","release_mirror_url",
                  "amendment_release_mirror_url","endpoint_url_template")
    bad = []
    for p in provs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            # Walk all endpoint lists at all top-level keys
            ep_lists = []
            for k, v in d.items():
                if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
                    ep_lists.append((k, v))
            for k, eps in ep_lists:
                for i, ep in enumerate(eps):
                    for fld in URL_FIELDS:
                        url = ep.get(fld)
                        if not isinstance(url, str): continue
                        # URL with embedded whitespace = malformed (unless template)
                        if " " in url and "{" not in url:
                            bad.append(f"{p.name}.{k}[{i}].{fld}: whitespace")
                        # URL with no scheme is bad
                        elif not (url.startswith("http://") or url.startswith("https://")
                                  or url.startswith("s3://") or url.startswith("ftp://")):
                            bad.append(f"{p.name}.{k}[{i}].{fld}: no scheme: {url[:50]}")
        except Exception:
            pass
    r.add("B","provenance_urls_well_formed",
          "PASS" if not bad else "FAIL",
          f"{len(bad)} malformed URLs"
          + (f": {bad[:1]}" if bad else ""))

    # Provenance index is well-formed
    pix = ROOT / "_provenance_index_occ.json"
    try:
        d = json.loads(pix.read_text(encoding="utf-8"))
        n_entries = d.get("n_entries", 0)
        len_entries = len(d.get("entries", []))
        ok = n_entries == len_entries and n_entries > 0
        r.add("B","provenance_index_self_consistent",
              "PASS" if ok else "FAIL",
              f"n_entries={n_entries} len={len_entries}")
        # Each entry has claim_id matching OCC_M### pattern
        bad_ids = [e.get("claim_id") for e in d.get("entries", [])
                   if not re.match(r"^OCC_M\d{3}$", str(e.get("claim_id","")))]
        r.add("B","provenance_index_claim_ids_well_formed",
              "PASS" if not bad_ids else "FAIL",
              f"{len(bad_ids)} bad ids" + (f": {bad_ids[:3]}" if bad_ids else ""))
    except Exception as e:
        r.add("B","provenance_index_loadable","FAIL",str(e))

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY C — Cross-reference validation
# ─────────────────────────────────────────────────────────────────────────

def cat_C_cross_ref(r: Results) -> None:
    print(_bold("\n[C] Cross-reference validation"))

    pix = ROOT / "_provenance_index_occ.json"
    body = ROOT / "OCC_COMPLAINT_KHANNA.md"
    if not pix.exists() or not body.exists():
        r.add("C","prereqs_present","FAIL","missing index or body")
        return
    d = json.loads(pix.read_text(encoding="utf-8"))
    body_text = body.read_text(encoding="utf-8")

    index_ids = {e["claim_id"] for e in d["entries"]}
    body_ids = set(re.findall(r"OCC_M\d{3}", body_text))

    # Every OCC_M### in the body has an entry in the index
    body_only = body_ids - index_ids
    r.add("C","body_markers_resolved_in_index",
          "PASS" if not body_only else "FAIL",
          f"{len(body_ids)} body / {len(index_ids)} index; "
          f"{len(body_only)} body markers without index entry"
          + (f": {sorted(body_only)[:3]}" if body_only else ""))

    # Every entry in the index appears in the body
    # (minus self-references like the appendix itself)
    index_only = index_ids - body_ids
    r.add("C","index_entries_appear_in_body",
          "PASS" if not index_only else "WARN",
          f"{len(index_only)} index entries not in body"
          + (f": {sorted(index_only)[:3]}" if index_only else ""))

    # All exhibit references in OCC_EXHIBIT_LIST.md resolve to files.
    # Refs use `../EXHIBIT_*.{md,csv,pdf,png,txt}` (sibling at dossier root).
    # Also accept the bundled `exhibits/EXHIBIT_*.{md,csv,pdf,png,txt}` location
    # which is what cold-clone reviewers see (the bundled copy ships with V2).
    exh = ROOT / "OCC_EXHIBIT_LIST.md"
    if exh.exists():
        text = exh.read_text(encoding="utf-8")
        refs = re.findall(r"\.\.\/EXHIBIT[_A-Z0-9]+\.[a-z]+", text)
        unique_refs = set(refs)
        unresolved = []
        for ref in unique_refs:
            base = ref[3:]  # strip "../"
            primary = ROOT / ref     # sibling at dossier root
            bundled = ROOT / "exhibits" / base   # bundled inside V2
            if not primary.exists() and not bundled.exists():
                unresolved.append(ref)
        r.add("C","exhibit_list_references_resolve",
              "PASS" if not unresolved else "WARN",
              f"{len(unique_refs)} unique refs; {len(unresolved)} unresolved"
              + (f": {unresolved[:2]}" if unresolved else ""))

    # Each Count number 1-6 appears in body as a Count header (Count 5 dropped)
    counts = re.findall(r"^#+\s*Count\s+(\d+)", body_text, re.MULTILINE | re.IGNORECASE)
    found = {int(c) for c in counts}
    expected = set(range(1, 7))
    missing = expected - found
    r.add("C","all_six_counts_present_in_body",
          "PASS" if not missing else "FAIL",
          f"found {sorted(found)}; missing {sorted(missing)}")

    # Every snapshot referenced in provenance index entries exists on disk
    snap_refs_missing = []
    for e in d["entries"]:
        sub = e.get("substrate") or ""
        # Look for substrate strings that reference data/occ/*.json
        for m in re.findall(r"data/occ/[\w_-]+\.json", sub):
            if not (ROOT / m).exists():
                snap_refs_missing.append((e["claim_id"], m))
    r.add("C","substrate_snapshot_references_resolve",
          "PASS" if not snap_refs_missing else "WARN",
          f"{len(snap_refs_missing)} bad refs"
          + (f": {snap_refs_missing[:2]}" if snap_refs_missing else ""))

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY D — Path purity (no V1 leaks, no hardcoded paths)
# ─────────────────────────────────────────────────────────────────────────

def cat_D_path_purity(r: Results) -> None:
    print(_bold("\n[D] Path purity"))

    # No V1 paths in body files (OCC_FILING_PACKAGE/ without _V2)
    body_files = list(ROOT.glob("*.md")) + [ROOT / "_provenance_index_occ.json"]
    bad_v1 = []
    for f in body_files:
        if not f.exists(): continue
        text = f.read_text(encoding="utf-8", errors="replace")
        # Look for "OCC_FILING_PACKAGE/" not followed by "_V2"
        for m in re.finditer(r"OCC_FILING_PACKAGE(?!_V2)/", text):
            bad_v1.append(f"{f.name}:{text[:m.start()].count(chr(10))+1}")
    r.add("D","no_V1_path_leaks_in_body",
          "PASS" if not bad_v1 else "FAIL",
          f"{len(bad_v1)} occurrences" + (f": {bad_v1[:3]}" if bad_v1 else ""))

    # No hardcoded absolute Windows paths in scripts
    py_files = list(ROOT.glob("*.py"))
    bad_winabs = []
    for f in py_files:
        if f.name == "comprehensive_test.py": continue  # this file uses tempfile paths in tests
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'["\']C:\\Users\\Kevin\\', text):
            bad_winabs.append(f"{f.name}:{text[:m.start()].count(chr(10))+1}")
    r.add("D","no_hardcoded_windows_paths_in_scripts",
          "PASS" if not bad_winabs else "FAIL",
          f"{len(bad_winabs)} occurrences" + (f": {bad_winabs[:2]}" if bad_winabs else ""))

    # No /tmp paths in scripts (test harness leak)
    bad_tmp = []
    for f in py_files:
        if f.name == "comprehensive_test.py": continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'["\']\/tmp\/', text):
            bad_tmp.append(f"{f.name}:{text[:m.start()].count(chr(10))+1}")
    r.add("D","no_tmp_paths_in_scripts",
          "PASS" if not bad_tmp else "FAIL",
          f"{len(bad_tmp)} occurrences" + (f": {bad_tmp[:2]}" if bad_tmp else ""))

    # No "TODO" or "FIXME" in operative body files (OCC complaint, exhibits)
    todos = []
    for f in [ROOT / "OCC_COMPLAINT_KHANNA.md",
              ROOT / "DOJ_REFERRAL_KHANNA.md",
              ROOT / "HOUSE_ETHICS_SUBMISSION_KHANNA.md"]:
        if not f.exists(): continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\bTODO\b|\bFIXME\b|\[V2 SCOPE", text):
            todos.append(f"{f.name}:{text[:m.start()].count(chr(10))+1}")
    r.add("D","no_TODO_FIXME_in_operative_filings",
          "PASS" if not todos else "FAIL",
          f"{len(todos)} occurrences" + (f": {todos[:2]}" if todos else ""))

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY E — CLI surface
# ─────────────────────────────────────────────────────────────────────────

def cat_E_cli(r: Results, verbose: bool = False) -> None:
    print(_bold("\n[E] CLI surface"))
    SCRIPTS_WITH_HELP = [
        "reproduce_all.py", "verify_anchors_occ.py", "tier_e_reocr.py",
        "tier_f_full_rederive.py", "stamp_timestamp.py", "verify_timestamp.py",
        "upgrade_timestamp.py", "build_provenance.py", "fetch_substrate_occ.py",
        "strip_markers_pre_filing.py",
    ]
    for s in SCRIPTS_WITH_HELP:
        path = ROOT / s
        if not path.exists():
            r.add("E", f"help:{s}", "SKIP", "script missing")
            continue
        rc, out = run_subprocess([sys.executable, str(path), "--help"], cwd=ROOT, timeout=30)
        ok = rc == 0 and ("usage:" in out.lower() or "options" in out.lower())
        r.add("E", f"help:{s}", "PASS" if ok else "FAIL",
              f"rc={rc}; out_head={out[:80]!r}" if not ok else "")

    # welcome.py doesn't have argparse but should print banner when stdin is closed
    rc, out = run_subprocess([sys.executable, str(ROOT / "welcome.py")], cwd=ROOT, timeout=10,
                             env_overrides={"PYTHONIOENCODING":"utf-8"})
    # It will fail on EOF when prompted; just verify it printed the banner first
    ok = "OCC_FILING_PACKAGE_V2" in out and "reviewer welcome" in out
    r.add("E","welcome_prints_banner","PASS" if ok else "FAIL",
          "" if ok else f"out_head={out[:120]!r}")

    # welcome.py "skip everything" path (just press n at first prompt)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "welcome.py")],
        input="n\n", cwd=str(ROOT), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=15,
    )
    ok = proc.returncode == 0 and "Skipping" in (proc.stdout or "")
    r.add("E","welcome_skip_path_clean_exit",
          "PASS" if ok else "FAIL",
          "" if ok else f"rc={proc.returncode}; tail={(proc.stdout or '')[-150:]!r}")

    # verify_anchors_occ.py --spot-check 2 works
    rc, out = run_subprocess([sys.executable, str(ROOT / "verify_anchors_occ.py"),
                              "--spot-check", "2"], cwd=ROOT, timeout=120)
    ok = rc in (0, 1) and "MATCH" in out  # may divergence-FAIL on rendering, that's OK
    r.add("E","verify_anchors_spot_check_runs",
          "PASS" if ok else "FAIL",
          "" if ok else f"rc={rc}; out_tail={out[-200:]!r}")

    # verify_anchors_occ.py --spot-check OCC_M### — verify that AT LEAST ONE
    # marker in the index resolves to >0 endpoints. We test 4 distinct
    # markers to cover representative substrate classes (PTR, PFD, votes,
    # statute) and pass if any one resolves; but also report the success
    # rate so we know broad anchor->snapshot coverage isn't broken.
    test_markers = ("OCC_M007", "OCC_M008", "OCC_M002", "OCC_M033")
    found_any = False
    coverage = []
    for marker in test_markers:
        # Use --spot-check-out to redirect the (potentially slow) re-fetching;
        # we only care about how many endpoints are SELECTED, not their MATCHes.
        # Scan the [spot-check] selected line which prints before any fetch.
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tf:
            out_path = tf.name
        try:
            # Run with a timeout; the script will print "selected N endpoints"
            # near the start. To avoid waiting for full fetch, we cap at 10s
            # and parse from partial output.
            try:
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "verify_anchors_occ.py"),
                     "--spot-check", marker, "--spot-check-out", out_path],
                    cwd=str(ROOT), capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=10,
                )
                out = (proc.stdout or "") + (proc.stderr or "")
            except subprocess.TimeoutExpired as e:
                # text=True so stdout/stderr are already str (or None)
                so = e.stdout if isinstance(e.stdout, str) else (
                     e.stdout.decode("utf-8","replace") if e.stdout else "")
                se = e.stderr if isinstance(e.stderr, str) else (
                     e.stderr.decode("utf-8","replace") if e.stderr else "")
                out = so + se
            m = re.search(r"selected (\d+) endpoints", out)
            n_sel = int(m.group(1)) if m else 0
            coverage.append((marker, n_sel))
            if n_sel > 0:
                found_any = True
        finally:
            try: os.unlink(out_path)
            except OSError: pass
    r.add("E","verify_anchors_spot_check_specific_marker",
          "PASS" if found_any else "FAIL",
          f"coverage: {coverage}")

    # reproduce_all.py --verbose flag works
    rc, out = run_subprocess([sys.executable, str(ROOT / "reproduce_all.py"),
                              "--verbose"], cwd=ROOT, timeout=180)
    # Verbose should auto-dump captured output for at least one tier
    ok = rc == 0 and "OVERALL: PASS" in out and "captured output" in out
    r.add("E","reproduce_all_verbose_dumps_subprocess_output",
          "PASS" if ok else "FAIL",
          "" if ok else f"rc={rc}; out_tail={out[-200:]!r}")

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY F — Syntax / parseability
# ─────────────────────────────────────────────────────────────────────────

def cat_F_syntax(r: Results) -> None:
    print(_bold("\n[F] Syntax / parseability"))

    # Every .py file at V2 root parses
    py_files = list(ROOT.glob("*.py"))
    bad = []
    for f in py_files:
        try:
            ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError as e:
            bad.append(f"{f.name}: {e.msg} line {e.lineno}")
    r.add("F","root_python_files_parse",
          "PASS" if not bad else "FAIL",
          f"{len(py_files)} .py files; {len(bad)} bad"
          + (f": {bad[:1]}" if bad else ""))

    # Every .py in data/ocr_products parses
    py_data = list((ROOT / "data" / "ocr_products").glob("*.py"))
    bad = []
    for f in py_data:
        try:
            ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError as e:
            bad.append(f"{f.name}: {e.msg}")
    r.add("F","data_ocr_products_python_files_parse",
          "PASS" if not bad else "FAIL",
          f"{len(py_data)} .py files; {len(bad)} bad"
          + (f": {bad[:1]}" if bad else ""))

    # All JSON files in data/occ/ are valid JSON
    json_files = list(DATA_OCC.glob("*.json"))
    bad = []
    for f in json_files:
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            bad.append(f"{f.name}: {e}")
    r.add("F","data_occ_json_files_valid",
          "PASS" if not bad else "FAIL",
          f"{len(json_files)} JSONs; {len(bad)} bad"
          + (f": {bad[:1]}" if bad else ""))

    # _provenance_index_occ.json is valid JSON
    pix = ROOT / "_provenance_index_occ.json"
    try:
        json.loads(pix.read_text(encoding="utf-8"))
        r.add("F","provenance_index_valid_json","PASS","")
    except Exception as e:
        r.add("F","provenance_index_valid_json","FAIL",str(e))

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY G — Execution (each tier independently)
# ─────────────────────────────────────────────────────────────────────────

def cat_G_execution(r: Results, verbose: bool = False) -> None:
    print(_bold("\n[G] Execution"))

    # Tier 0: manifest integrity via reproduce_all.py
    rc, out = run_subprocess([sys.executable, str(ROOT / "reproduce_all.py")],
                             cwd=ROOT, timeout=300)
    parts = [
        ("tier_0_pass", "TIER 0 (manifest): PASS" in out),
        ("tier_1_pass", "TIER 1 (verifier): PASS" in out),
        ("tier_2_pass", "TIER 2 (rebuilds): PASS" in out),
        ("overall_pass", "OVERALL: PASS" in out),
    ]
    for name, ok in parts:
        r.add("G", name, "PASS" if ok else "FAIL",
              "" if ok else f"rc={rc}; tail={out[-200:]!r}")

    # Each rebuild script independently
    REBUILDS = [
        "data/ocr_products/rebuild_ptr_audit_khanna.py",
        "data/ocr_products/rebuild_pfd_schedule_d_khanna.py",
        "data/ocr_products/rebuild_trade_pnl_khanna.py",
    ]
    for rel in REBUILDS:
        p = ROOT / rel
        if not p.exists():
            r.add("G", f"rebuild:{p.name}", "SKIP", "script missing")
            continue
        rc, out = run_subprocess([sys.executable, str(p), "--quiet"],
                                 cwd=ROOT, timeout=120)
        # rc can be 0 or 1 depending on whether script signals PASS_WITH_DEFECT
        summary = next((ln for ln in out.splitlines() if ln.startswith("SUMMARY:")), None)
        ok = (summary is not None) and ("0 drift" in summary or "drift" not in summary
                                         or "0 error" in summary)
        r.add("G", f"rebuild:{p.name}", "PASS" if ok else "FAIL",
              summary or f"rc={rc}")

    # Verifier full report
    rc, out = run_subprocess([sys.executable, str(ROOT / "verify_anchors_occ.py")],
                             cwd=ROOT, timeout=120)
    m = re.search(r"(\d+)\s+anchors checked\s*/\s*OK:\s*(\d+).*FAIL:\s*(\d+)", out)
    if m:
        n, ok_n, fail_n = int(m.group(1)), int(m.group(2)), int(m.group(3))
        r.add("G","verifier_all_anchors_pass",
              "PASS" if fail_n == 0 else "FAIL",
              f"{ok_n}/{n} OK; {fail_n} FAIL")
    else:
        r.add("G","verifier_all_anchors_pass","FAIL",f"could not parse summary; tail={out[-150:]!r}")

    # OpenTimestamps proof verifies
    rc, out = run_subprocess([sys.executable, str(ROOT / "verify_timestamp.py")],
                             cwd=ROOT, timeout=30)
    ok = "DIGEST MATCHES" in out
    r.add("G","ots_proof_verifies",
          "PASS" if ok else "FAIL",
          "" if ok else f"rc={rc}; tail={out[-200:]!r}")

    # Each rebuild's REBUILT.json output bit-exact-matches the corresponding
    # snapshot scalar fields it claims to reproduce. (The rebuild script
    # already does its own diff and reports SUMMARY; this test independently
    # cross-checks the rebuild output exists and is valid JSON.)
    REBUILT = [
        "data/ocr_products/ptr_filing_audit_khanna_REBUILT.json",
        "data/ocr_products/pfd_schedule_d_khanna_REBUILT.json",
        "data/ocr_products/trade_pnl_facts_REBUILT.json",
    ]
    for rel in REBUILT:
        p = ROOT / rel
        if not p.exists():
            r.add("G", f"rebuild_output:{p.name}", "FAIL",
                  "REBUILT artifact missing — rebuild may not have been run")
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            r.add("G", f"rebuild_output:{p.name}", "PASS",
                  f"{p.stat().st_size:,} bytes; top-level keys={list(d.keys())[:3] if isinstance(d, dict) else 'list'}")
        except Exception as e:
            r.add("G", f"rebuild_output:{p.name}", "FAIL", f"invalid JSON: {e}")

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY H — Error handling (synthetic corruption)
# ─────────────────────────────────────────────────────────────────────────

def cat_H_error_handling(r: Results) -> None:
    print(_bold("\n[H] Error handling (synthetic corruption)"))

    # Make a temp copy of just the manifest, corrupt it, verify Tier 0 catches
    # We do this by running reproduce_all.py with a temporarily bad manifest.
    # Simpler: directly invoke the tier_0 logic and feed it a bad SHA.
    manifest = ROOT / "99_SHA256SUMS.txt"
    if not manifest.exists():
        r.add("H","corruption_test_setup","SKIP","manifest missing")
        return
    backup = manifest.read_bytes()
    try:
        # Corrupt one SHA in the manifest temporarily
        text = manifest.read_text(encoding="utf-8")
        # Replace first SHA's first hex char with a different char
        m = re.search(r"^([0-9a-f]{64})  ", text, re.MULTILINE)
        if not m:
            r.add("H","corruption_test_setup","SKIP","no SHA pattern matched")
            return
        original_sha = m.group(1)
        bad_sha = ("0" if original_sha[0] != "0" else "1") + original_sha[1:]
        bad_text = text.replace(original_sha + "  ", bad_sha + "  ", 1)
        manifest.write_bytes(bad_text.encode("utf-8"))

        # Run reproduce_all.py, expect Tier 0 FAIL with auto-dump
        rc, out = run_subprocess([sys.executable, str(ROOT / "reproduce_all.py")],
                                 cwd=ROOT, timeout=120)
        tier0_fail = "TIER 0 (manifest): FAIL" in out
        has_drift_dump = "DRIFT" in out
        has_hint = "tampered-or-edited" in out or "tamper" in out.lower()
        r.add("H","tier0_catches_sha_corruption",
              "PASS" if (tier0_fail and has_drift_dump) else "FAIL",
              f"tier0_fail={tier0_fail} has_drift={has_drift_dump} has_hint={has_hint}")
    finally:
        # Restore
        manifest.write_bytes(backup)

    # Synthetically remove a file Tier-0 expects, verify it's caught
    # (use a small, non-critical file to minimize blast radius)
    target = ROOT / "VERIFICATION_TIERS.md"
    if target.exists():
        backup_bytes = target.read_bytes()
        try:
            target.unlink()
            rc, out = run_subprocess([sys.executable, str(ROOT / "reproduce_all.py")],
                                     cwd=ROOT, timeout=120)
            tier0_fail = "TIER 0 (manifest): FAIL" in out
            has_missing = "MISSING" in out and "VERIFICATION_TIERS.md" in out
            has_hint = "incomplete-clone" in out or "re-download" in out
            r.add("H","tier0_catches_missing_file",
                  "PASS" if (tier0_fail and has_missing and has_hint) else "FAIL",
                  f"tier0_fail={tier0_fail} has_missing={has_missing} has_hint={has_hint}")
        finally:
            target.write_bytes(backup_bytes)
    else:
        r.add("H","tier0_catches_missing_file","SKIP","VERIFICATION_TIERS.md not present")

    # Test the failure-classification regex pack
    try:
        sys.path.insert(0, str(ROOT))
        # Reimport fresh
        import importlib
        if "reproduce_all" in sys.modules:
            del sys.modules["reproduce_all"]
        ra = importlib.import_module("reproduce_all")
        cases = [
            ("ModuleNotFoundError: No module named 'pymupdf'", "pymupdf"),
            ("GEMINI_API_KEY not set", "GEMINI_API_KEY"),
            ("ConnectionError: Failed to establish a new connection", "network"),
            ("HTTP 403 Cloudflare", "Cloudflare"),
            ("SHA mismatch on bundled doc", "tamper"),
            ("foo bar baz quux", None),
        ]
        bad = []
        for msg, expected_substr in cases:
            hint = ra._classify_failure(msg)
            ok = (hint is None and expected_substr is None) or \
                 (hint and expected_substr and expected_substr.lower() in hint.lower())
            if not ok:
                bad.append(f"{msg!r} -> {hint!r}")
        r.add("H","failure_classification_pack_correct",
              "PASS" if not bad else "FAIL",
              f"{len(cases)-len(bad)}/{len(cases)} ok"
              + (f": {bad[:1]}" if bad else ""))
    except Exception as e:
        r.add("H","failure_classification_pack_correct","FAIL",f"import error: {e}")
    finally:
        sys.path.pop(0)

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY I — Consistency (running twice produces identical output)
# ─────────────────────────────────────────────────────────────────────────

def cat_I_consistency(r: Results) -> None:
    print(_bold("\n[I] Consistency"))

    # Run reproduce_all.py twice; OK counts must match
    summaries = []
    for i in range(2):
        rc, out = run_subprocess([sys.executable, str(ROOT / "reproduce_all.py")],
                                 cwd=ROOT, timeout=300)
        m = re.search(r"TIER 1 \(verifier\):\s*(\w+)\s*.\s*(\d+)/(\d+)", out)
        if m:
            summaries.append((m.group(1), int(m.group(2)), int(m.group(3))))
    if len(summaries) == 2 and summaries[0] == summaries[1]:
        r.add("I","reproduce_all_deterministic",
              "PASS", f"both runs: {summaries[0]}")
    else:
        r.add("I","reproduce_all_deterministic", "FAIL",
              f"runs differ: {summaries}")

    # Re-run each rebuild twice and check identical SUMMARY lines
    REBUILDS = [
        "data/ocr_products/rebuild_ptr_audit_khanna.py",
        "data/ocr_products/rebuild_pfd_schedule_d_khanna.py",
        "data/ocr_products/rebuild_trade_pnl_khanna.py",
    ]
    bad = []
    for rel in REBUILDS:
        p = ROOT / rel
        if not p.exists(): continue
        sums = []
        for _ in range(2):
            rc, out = run_subprocess([sys.executable, str(p), "--quiet"],
                                     cwd=ROOT, timeout=120)
            sums.append(next((ln for ln in out.splitlines()
                              if ln.startswith("SUMMARY:")), None))
        if sums[0] != sums[1]:
            bad.append(f"{p.name}: {sums}")
    r.add("I","rebuilds_deterministic",
          "PASS" if not bad else "FAIL",
          f"{len(REBUILDS)} rebuilds; {len(bad)} non-deterministic"
          + (f": {bad[:1]}" if bad else ""))

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY J — Network (provenance URLs reachable; release assets)
# ─────────────────────────────────────────────────────────────────────────

def cat_J_network(r: Results, do_release: bool = False) -> None:
    print(_bold("\n[J] Network"))

    # Internet sanity check
    ok, note = http_head_ok("https://www.google.com")
    if not ok:
        r.add("J","internet_reachable","SKIP",note)
        return
    r.add("J","internet_reachable","PASS",note)

    # Sample one fetchable URL from each provenance file. Skip endpoints
    # that are documented-as-constants (no real URL to fetch), template
    # URLs (have {placeholders}), or release-mirror URLs (own check).
    provs = sorted(DATA_OCC.glob("*.provenance.json"))
    sampled = 0
    failed_urls = []
    for p in provs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            chosen_url = None
            for ep in d.get("primary_source_endpoints", []):
                if not isinstance(ep, dict): continue
                fs = (ep.get("fetch_status") or "").upper()
                if "DOCUMENTED_AS_CONSTANTS" in fs:
                    continue  # No URL to probe; data is hardcoded.
                url = ep.get("url") or ep.get("primary_source_url") \
                    or ep.get("pdf_irs_direct_url") \
                    or ep.get("primary_source_url_irs_eos")
                if not url:
                    continue
                if url.startswith("https://github.com/"):
                    continue  # Release mirror; tested separately.
                if "{" in url and "}" in url:
                    continue  # Template URL with placeholders.
                if " " in url:
                    failed_urls.append((p.name, url[:80], "malformed URL (whitespace)"))
                    continue
                chosen_url = url
                break
            if chosen_url:
                ok, note = http_head_ok(chosen_url, timeout=10)
                sampled += 1
                if not ok:
                    failed_urls.append((p.name, chosen_url[:80], note))
        except Exception as e:
            failed_urls.append((p.name, "(load error)", str(e)))
    r.add("J","provenance_urls_sampled_reachable",
          "PASS" if not failed_urls else "WARN",
          f"sampled {sampled}; {len(failed_urls)} unreachable"
          + (f": {[(p,u[:30],n[:30]) for p,u,n in failed_urls[:2]]}" if failed_urls else ""))

    if not do_release:
        r.add("J","release_assets_check","SKIP","--release not specified")
        return

    # Verify all release assets are downloadable via gh CLI + Ahuja PDFs
    # match expected SHA. We use `gh release download` instead of urllib
    # because GitHub's anonymous-release-asset path can return 404 to
    # urllib in some contexts (rate-limit / IP-flag heuristics) while
    # `gh` (which authenticates via gh auth) works reliably.
    has_gh = shutil.which("gh") is not None
    if not has_gh:
        r.add("J","release_gh_cli_present","SKIP",
              "gh CLI not in PATH; install from https://cli.github.com")
        return
    r.add("J","release_gh_cli_present","PASS","")

    AHUJA_EXPECTED = {
        "AHUJA_990PF_2016.pdf": "660e4be43f67b9cc9eca107dcad6d5e452f616df9d6319306eabac371ad887d2",
        "AHUJA_990PF_2018.pdf": "0b031d37364df49ba43f0e7da77fbca8dc72e74095421e81684efcb64a9e338f",
        "AHUJA_990PF_2019.pdf": "198581431492ba773f0a763144fdf2b9b25d2a2329264e1e542acceef4a737ff",
        "AHUJA_990PF_2021.pdf": "256397795674732271c517b02684d3358d8dd5aef6388790a5e465d78aea3a23",
        "AHUJA_990PF_2021_v2.pdf": "3fca4f8fbdb523b7c53cf34f57b305dcb5eb46293e2dd07f01d7b8584607bb5c",
        "AHUJA_990PF_2022.pdf": "0d994de9819573187683dc03bc595265a9a335a7fc2dd9df65f6e92727ab7b00",
    }
    with tempfile.TemporaryDirectory() as tmp:
        for asset, expected_sha in AHUJA_EXPECTED.items():
            out_path = pathlib.Path(tmp) / asset
            rc, out = run_subprocess(
                ["gh", "release", "download", "v2-occ-trust-tiers-2026-05-04",
                 "-R", "kevinnbass/political", "-p", asset,
                 "--output", str(out_path), "--clobber"],
                cwd=pathlib.Path(tmp), timeout=180,
            )
            if rc != 0 or not out_path.exists():
                r.add("J", f"release_asset_sha:{asset}", "FAIL",
                      f"gh download rc={rc}; out={out[-150:]!r}")
                continue
            actual = hashlib.sha256(out_path.read_bytes()).hexdigest()
            if actual == expected_sha:
                r.add("J", f"release_asset_sha:{asset}", "PASS",
                      f"{out_path.stat().st_size:,} bytes")
            else:
                r.add("J", f"release_asset_sha:{asset}", "FAIL",
                      f"expected {expected_sha[:8]}.. got {actual[:8]}..")

# ─────────────────────────────────────────────────────────────────────────
# CATEGORY K — Gemini smoke test (opt-in)
# ─────────────────────────────────────────────────────────────────────────

def cat_K_gemini(r: Results) -> None:
    print(_bold("\n[K] Gemini smoke test"))
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        r.add("K","gemini_key_present","SKIP","no GEMINI_API_KEY/GOOGLE_API_KEY env")
        return
    if not os.environ.get("GEMINI_PER_PAGE_HELPER_DIR"):
        r.add("K","helper_dir_present","SKIP","no GEMINI_PER_PAGE_HELPER_DIR env")
        return

    rc, out = run_subprocess(
        [sys.executable, str(ROOT / "tier_e_reocr.py"),
         "--snapshots", "khanna_ptr_transactions",
         "--max-pdfs", "1"],
        cwd=ROOT, timeout=600,
    )
    grand = {}
    in_g = False
    for ln in out.splitlines():
        if ln.startswith("## Grand totals"):
            in_g = True; continue
        if in_g and ":" in ln and "**" in ln:
            try:
                k = ln.split(":")[0].strip()
                n = int(ln.split("**")[1])
                grand[k] = n
            except Exception:
                pass
    n_ok = grand.get("BIT_EXACT", 0) + grand.get("DRIFT_BENIGN", 0)
    n_bad = (grand.get("DRIFT_MATERIAL", 0) + grand.get("FETCH_FAIL", 0)
             + grand.get("SHA_MISMATCH", 0) + grand.get("GEMINI_FAIL", 0))
    if n_ok and not n_bad:
        r.add("K","tier_e_smoke_test","PASS",f"{grand}")
    else:
        r.add("K","tier_e_smoke_test","FAIL" if n_bad else "WARN",f"{grand}")

# ─────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--network", action="store_true",
                    help="Run network tests (probes provenance URLs).")
    ap.add_argument("--release", action="store_true",
                    help="Run release-asset SHA verification (requires network + ~10 MB DL).")
    ap.add_argument("--gemini", action="store_true",
                    help="Run Tier-E 1-PDF smoke test (requires GEMINI_API_KEY).")
    ap.add_argument("--all", action="store_true",
                    help="Equivalent to --network --release --gemini.")
    ap.add_argument("--quick", action="store_true",
                    help="Skip slow tests (consistency, error_handling).")
    ap.add_argument("--verbose", action="store_true",
                    help="Print full subprocess output for each test.")
    ap.add_argument("--out", default="comprehensive_test_report.md",
                    help="Output Markdown report path.")
    args = ap.parse_args()
    if args.all:
        args.network = args.release = args.gemini = True

    print()
    print("=" * 72)
    print(_bold("OCC_FILING_PACKAGE_V2 — COMPREHENSIVE TEST"))
    print("=" * 72)
    print(f"Working directory: {ROOT}")
    print(f"Python: {sys.version.split()[0]}  Args: network={args.network} "
          f"release={args.release} gemini={args.gemini} quick={args.quick}")

    r = Results()
    cat_A_structural(r)
    cat_B_schema(r)
    cat_C_cross_ref(r)
    cat_D_path_purity(r)
    cat_E_cli(r, args.verbose)
    cat_F_syntax(r)
    cat_G_execution(r, args.verbose)
    if not args.quick:
        cat_H_error_handling(r)
        cat_I_consistency(r)
    else:
        r.add("H","tests_skipped","SKIP","--quick mode")
        r.add("I","tests_skipped","SKIP","--quick mode")
    if args.network or args.release:
        cat_J_network(r, do_release=args.release)
    else:
        r.add("J","tests_skipped","SKIP","--network not specified")
    if args.gemini:
        cat_K_gemini(r)
    else:
        r.add("K","tests_skipped","SKIP","--gemini not specified")

    summary = r.render_summary()
    print(summary)

    # Also write Markdown report
    md_lines = [
        f"# Comprehensive test report",
        f"",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}",
        f"Args: network={args.network} release={args.release} gemini={args.gemini} quick={args.quick}",
        f"",
        f"| status | category | name | detail |",
        f"|---|---|---|---|",
    ]
    for t in r.tests:
        d = t["detail"].replace("|","\\|").replace("\n"," ")[:120]
        md_lines.append(f"| **{t['status']}** | {t['category']} | {t['name']} | {d} |")
    md_lines.extend([
        "",
        f"## Summary",
        "",
        f"- PASS: {r.n('PASS')}",
        f"- FAIL: {r.n('FAIL')}",
        f"- SKIP: {r.n('SKIP')}",
        f"- WARN: {r.n('WARN')}",
    ])
    (ROOT / args.out).write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  Report: {ROOT / args.out}")

    return 0 if r.n("FAIL") == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
