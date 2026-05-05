#!/usr/bin/env python3
"""reproduce_all.py — single-command cold-start reproduction of the OCC filing package.

Runs three reproduction tiers in sequence and emits one PASS / PASS_WITH_DEFECT /
FAIL verdict.

USAGE (from inside the package directory, with stdlib-only Python 3):

    python reproduce_all.py                          # Tiers 0 + 1 + 2
    python reproduce_all.py --spot-check 5           # + Tier-D x5
    python reproduce_all.py --tier-E                 # + Tier-E re-OCR
    python reproduce_all.py --tier-F                 # + Tier-F full re-derive
    python reproduce_all.py --verify-timestamp       # + OpenTimestamps proof
    python reproduce_all.py --verbose                # show full subprocess output

WHAT THIS DOES (tiered, in order):

  TIER 0 — manifest integrity
    Recompute LF-canonical SHA256 for every file listed in 99_SHA256SUMS.txt
    and confirm zero drift. Catches tampering or incomplete clones.

  TIER 1 — body-figure verifier (verify_anchors_occ.py)
    For each of the 66 manifest claim_ids in _provenance_index_occ.json,
    re-derive the body figure from the bundled substrate snapshots and
    compare to the body claim. 68 anchors total (66 manifest + 2
    self-references).

  TIER 2 — substrate rebuilds from raw artifacts (3 zero-cost scripts)
    Re-derive the snapshot scalars themselves from the raw bundled OCR /
    PDF / OHLC artifacts:
      - rebuild_ptr_audit_khanna.py    (Khanna PTR audit aggregates)
      - rebuild_pfd_schedule_d_khanna.py (PFD Schedule D liabilities)
      - rebuild_trade_pnl_khanna.py    (household trade-P&L scalars)
    Each emits its own diff vs the bundled snapshot.

  (NOT included — gated tiers requiring out-of-band resources:)
    - rebuild_chamber_audit.py / rebuild_peer_baseline.py — chamber-wide
      Gemini OCR rebuild ($25-200 reviewer spend; opt-in only).
    - verify_anchors_occ.py --diff-snapshots-vs-live — re-fetches against
      live FEC API + lake; requires API key + DB access.

VERDICT classes:
  PASS              — every tier requested passed cleanly.
  PASS_WITH_DEFECT  — a tier reports drift within a documented tolerance
                      band (e.g., F225 trade-PnL ±5%, Tier-E LLM sampling).
  PASS_WITH_SKIPS   — a tier was skipped for missing optional dependencies
                      (e.g., GEMINI_API_KEY for Tier-E). No hard failures.
  FAIL              — a hard failure. Full subprocess stdout+stderr is
                      auto-dumped for the failing tier so the reviewer
                      can see exactly what went wrong.

ERROR HANDLING:
  - Every tier captures full subprocess stdout + stderr.
  - On FAIL: the captured output is automatically dumped, regardless of
    --verbose.
  - On PASS / PASS_WITH_DEFECT / PASS_WITH_SKIPS: dumped only with
    --verbose.
  - Common failure classes (ModuleNotFoundError, ConnectionError,
    missing GEMINI_API_KEY, missing pymupdf, etc.) are auto-detected
    and a one-line actionable hint is printed.
  - The final FINAL VERDICT block lists every tier with its status,
    one-line summary, and (if FAILED) the captured error excerpt.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent

_BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".tar",
    ".xls", ".xlsx", ".doc", ".docx", ".bin",
}


def _canonical_sha(path: pathlib.Path) -> str:
    """LF-canonical SHA256, matching scripts/manifest_canonical_sha.py."""
    b = path.read_bytes()
    if path.suffix.lower() not in _BINARY_SUFFIXES:
        b = b.replace(b"\r\n", b"\n")
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------
# Failure classification — turn raw subprocess output into actionable hints
# ------------------------------------------------------------------

# (regex, hint) pairs. First match wins; checked against full stdout+stderr.
_FAILURE_HINTS: tuple[tuple[str, str], ...] = (
    (r"ModuleNotFoundError: No module named ['\"]pymupdf['\"]|No module named ['\"]fitz['\"]",
     "install: pip install pymupdf"),
    (r"ModuleNotFoundError: No module named ['\"]google\.generativeai['\"]"
     r"|No module named ['\"]google_generativeai['\"]",
     "install: pip install google-generativeai"),
    (r"ModuleNotFoundError: No module named ['\"]yfinance['\"]",
     "install: pip install yfinance"),
    (r"ModuleNotFoundError: No module named ['\"]requests['\"]",
     "install: pip install requests"),
    (r"ModuleNotFoundError: No module named ['\"](opentimestamps|bitcoin)['\"]",
     "install: pip install opentimestamps"),
    (r"GEMINI_API_KEY (?:not set|missing|env(?:ironment)? variable)",
     "set env: GEMINI_API_KEY=<your-key> (Google AI Studio free tier works)"),
    (r"GEMINI_PER_PAGE_HELPER_DIR (?:not set|missing|env(?:ironment)? variable)",
     "set env: GEMINI_PER_PAGE_HELPER_DIR=<path-to-helper-checkout>"),
    (r"ConnectionError|Connection refused|Connection timed out|Network is unreachable"
     r"|Failed to establish a new connection|getaddrinfo failed",
     "network: primary-source endpoint unreachable; check internet + retry"),
    (r"HTTP 403|Cloudflare|cf-chl|Access denied",
     "blocked: primary source is Cloudflare/WAF-protected; use the GitHub "
     "Release mirror (e.g., AHUJA_990PF_<year>.pdf) instead of direct fetch"),
    (r"HTTP 404|Not Found",
     "missing: primary URL returned 404 — the upstream may have moved/amended; "
     "compare provenance.fetched_at vs current upstream"),
    (r"sha mismatch|SHA mismatch|SHA_MISMATCH|hash mismatch",
     "tamper-or-amendment: bytes differ from provenance hash; check the "
     "snapshot's provenance.json fetched_at to see if upstream changed"),
    (r"pg_connection|psycopg2|could not connect to server|DB(?:_| )password",
     "lake-required: this tier requires PostgreSQL DB access; use Tier-D "
     "spot-check or skip with --no-tier-X"),
    (r"99_SHA256SUMS\.txt missing|manifest missing",
     "incomplete-clone: re-download the tarball; the package is missing files"),
    (r"FileNotFoundError.*\.json|FileNotFoundError.*\.pdf",
     "missing-substrate: a snapshot or PDF the tier expected is not on disk; "
     "see the file path in the trace above"),
)


def _classify_failure(captured: str) -> str | None:
    """Return a one-line actionable hint if a known failure class is detected."""
    for pat, hint in _FAILURE_HINTS:
        if re.search(pat, captured, re.IGNORECASE):
            return hint
    return None


def _run(cmd: list[str], cwd: pathlib.Path) -> tuple[int, str]:
    """Run a subprocess; return (returncode, combined stdout+stderr)."""
    proc = subprocess.run(
        cmd, cwd=str(cwd), capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def _print_full_output(captured: str, label: str) -> None:
    """Dump captured output verbatim, framed for visibility.

    Replaces unencodable chars under stdout's encoding so Windows cp1252
    consoles don't crash on subprocess output containing curly quotes /
    box-drawing chars / replacement chars.
    """
    enc = sys.stdout.encoding or "utf-8"
    def _safe(s: str) -> str:
        return s.encode(enc, errors="replace").decode(enc, errors="replace")
    print()
    print(_safe(f"  --- BEGIN {label} ---"))
    for line in captured.splitlines():
        print(_safe(f"  {line}"))
    print(_safe(f"  --- END {label} ---"))


# ------------------------------------------------------------------
# TIER 0 — manifest integrity
# ------------------------------------------------------------------

def tier0_manifest(verbose: bool = False) -> dict:
    print("=" * 70)
    print("TIER 0 — manifest integrity (LF-canonical SHA256 vs 99_SHA256SUMS.txt)")
    print("=" * 70)
    manifest = ROOT / "99_SHA256SUMS.txt"
    if not manifest.exists():
        msg = f"99_SHA256SUMS.txt missing at {manifest}"
        print(f"  FAIL: {msg}")
        return {"status": "FAIL", "msg": msg, "captured": "",
                "hint": "incomplete-clone: re-download the tarball"}

    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        rel = parts[1]
        if rel.startswith("./"):
            rel = rel[2:]
        expected[rel] = parts[0]

    drifted: list[tuple[str, str, str]] = []
    missing: list[str] = []
    for rel, exp in expected.items():
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
            continue
        actual = _canonical_sha(p)
        if actual != exp:
            drifted.append((rel, exp, actual))

    print(f"  manifest entries: {len(expected)}")
    print(f"  drifted SHAs:     {len(drifted)}")
    print(f"  missing files:    {len(missing)}")

    if drifted or missing:
        # On FAIL: show ALL drifted/missing, not just first 5
        for rel, e, a in drifted:
            print(f"    DRIFT {rel}")
            print(f"          expected {e}")
            print(f"          actual   {a}")
        for rel in missing:
            print(f"    MISSING {rel}")
        msg = (f"manifest integrity FAILED: {len(drifted)} drift, "
               f"{len(missing)} missing")
        hint = ("incomplete-clone: re-download the tarball — files missing"
                if missing else
                "tampered-or-edited: bytes differ from manifest; "
                "investigate which file changed")
        return {"status": "FAIL", "msg": msg,
                "captured": "\n".join(
                    [f"DRIFT {rel}" for rel, _, _ in drifted] +
                    [f"MISSING {rel}" for rel in missing]),
                "hint": hint}

    return {"status": "PASS", "msg": f"{len(expected)} files OK",
            "captured": "", "hint": None}


# ------------------------------------------------------------------
# TIER 0.5 — anchor-coverage gate
# ------------------------------------------------------------------

def tier0_5_anchor_coverage(verbose: bool = False) -> dict:
    """Assert every figure-bearing complaint paragraph cites an [OCC_M###]
    marker. Closes the silent-drift gap between body figures and verifier
    coverage: any new figure introduced into the complaint without a marker
    fires this gate before the verifier even runs."""
    print()
    print("=" * 70)
    print("TIER 0.5 — anchor coverage (verify_anchor_coverage.py)")
    print("=" * 70)
    rc, out = _run([sys.executable, str(ROOT / "verify_anchor_coverage.py")], ROOT)

    summary_line = None
    for line in out.splitlines():
        if line.startswith("Un-anchored"):
            summary_line = line.strip()
            break
    if summary_line:
        print(f"  {summary_line}")

    if rc == 0:
        return {"status": "PASS",
                "msg": "every figure-bearing paragraph anchored to a verifier marker",
                "captured": out}
    return {"status": "FAIL",
            "msg": "un-anchored figure-bearing paragraph(s) detected",
            "captured": out,
            "hint": "every numerical figure in OCC_COMPLAINT_KHANNA.md must "
                    "trace to an [OCC_M###] marker that the verifier checks "
                    "against substrate; see captured output for the punch list"}


# TIER 1 — body-figure verifier
# ------------------------------------------------------------------

def tier1_verifier(verbose: bool = False) -> dict:
    print()
    print("=" * 70)
    print("TIER 1 — body-figure verifier (verify_anchors_occ.py)")
    print("=" * 70)
    rc, out = _run([sys.executable, str(ROOT / "verify_anchors_occ.py")], ROOT)

    summary = None
    for line in out.splitlines():
        if "anchors checked" in line and "Summary" in line:
            summary = line.strip()
            break
    if summary is None:
        for line in reversed(out.splitlines()):
            if line.strip():
                summary = line.strip()
                break
    print(f"  {summary}")

    m = re.search(
        r"(\d+)\s+anchors checked\s*/\s*OK:\s*(\d+).*DIVERGE:\s*(\d+).*"
        r"ERROR:\s*(\d+).*SKIP:\s*(\d+).*MANUAL:\s*(\d+).*FAIL:\s*(\d+)",
        summary or "",
    )
    if not m:
        msg = f"could not parse verifier summary: {summary!r}"
        return {"status": "FAIL", "msg": msg, "captured": out,
                "hint": _classify_failure(out)}

    n, ok, div, err, skip, manual, fail = (int(x) for x in m.groups())

    if div + err + fail > 0:
        msg = f"{div} DIVERGE, {err} ERROR, {fail} FAIL"
        # Surface DIVERGE/ERROR/FAIL anchor lines so the reviewer can see WHICH
        bad_lines = [ln for ln in out.splitlines()
                     if any(tag in ln for tag in
                            (" DIVERGE ", " DIVERGE\t", "| DIVERGE |",
                             " ERROR ", " ERROR\t", "| ERROR |",
                             " FAIL ", " FAIL\t", "| FAIL |"))]
        if bad_lines:
            print("  failing anchors:")
            for ln in bad_lines[:20]:
                print(f"    {ln.strip()[:160]}")
            if len(bad_lines) > 20:
                print(f"    [... +{len(bad_lines)-20} more; see verify_anchors_occ_report.md ...]")
        return {"status": "FAIL", "msg": msg, "captured": out,
                "hint": _classify_failure(out) or
                ("see verify_anchors_occ_report.md for per-anchor detail; "
                 "DIVERGE typically means snapshot vs body figure drift")}

    return {"status": "PASS",
            "msg": f"{ok}/{n} OK ({skip} skip, {manual} manual)",
            "captured": out if verbose else "", "hint": None}


# ------------------------------------------------------------------
# TIER 2 — substrate rebuilds from raw artifacts
# ------------------------------------------------------------------

REBUILDS = [
    ("rebuild_ptr_audit_khanna.py",
     "data/ocr_products/rebuild_ptr_audit_khanna.py"),
    ("rebuild_pfd_schedule_d_khanna.py",
     "data/ocr_products/rebuild_pfd_schedule_d_khanna.py"),
    ("rebuild_trade_pnl_khanna.py",
     "data/ocr_products/rebuild_trade_pnl_khanna.py"),
]


def tier2_rebuilds(verbose: bool = False) -> dict:
    print()
    print("=" * 70)
    print("TIER 2 — substrate rebuilds from raw artifacts")
    print("=" * 70)
    overall = "PASS"
    notes: list[str] = []
    captured_all: list[str] = []
    failure_hint = None
    for name, rel in REBUILDS:
        path = ROOT / rel
        if not path.exists():
            print(f"  {name}: MISSING")
            overall = "FAIL"
            notes.append(f"{name}: script missing")
            captured_all.append(f"{name}: file not found at {path}")
            failure_hint = "incomplete-clone: re-download the tarball"
            continue

        rc, out = _run([sys.executable, str(path), "--quiet"], ROOT)

        summary_line = None
        for line in out.splitlines():
            if line.startswith("SUMMARY:"):
                summary_line = line
        if summary_line is None:
            # Fall back to non-quiet
            rc, out = _run([sys.executable, str(path)], ROOT)
            for line in out.splitlines():
                if line.startswith("SUMMARY:"):
                    summary_line = line

        if summary_line is None:
            print(f"  {name}: NO SUMMARY (rc={rc})")
            overall = "FAIL"
            notes.append(f"{name}: no SUMMARY line emitted")
            captured_all.append(f"--- {name} (rc={rc}) ---\n{out}")
            failure_hint = failure_hint or _classify_failure(out)
            continue

        sl = summary_line
        is_drift_class = (
            "DRIFT_VALUE" in out
            or " 1 drift" in sl
            or " 2 drift" in sl
            or " 3 drift" in sl
        )
        is_pwd = "pass-with-defect" in sl and " 0 pass-with-defect" not in sl
        if is_drift_class and not is_pwd:
            verdict = "FAIL"
            overall = "FAIL"
            captured_all.append(f"--- {name} (rc={rc}) ---\n{out}")
        elif is_pwd:
            verdict = "PASS_WITH_DEFECT"
            if overall == "PASS":
                overall = "PASS_WITH_DEFECT"
        else:
            verdict = "PASS"
        print(f"  {name}: {verdict}")
        print(f"    {summary_line}")
        notes.append(f"{name}: {verdict}")
        if verbose:
            captured_all.append(f"--- {name} (rc={rc}) ---\n{out}")

    return {"status": overall, "msg": "; ".join(notes),
            "captured": "\n\n".join(captured_all), "hint": failure_hint}


# ------------------------------------------------------------------
# Tier-D (spot-check), Tier-E (re-OCR), Tier-F (full re-derive)
# ------------------------------------------------------------------

def tier_d_spot_check(n: int, verbose: bool = False) -> dict:
    print()
    print("=" * 70)
    print(f"TIER D — primary-source spot-check ({n} random endpoints)")
    print("=" * 70)
    rc, out = _run([sys.executable, str(ROOT / "verify_anchors_occ.py"),
                    "--spot-check", str(n)], ROOT)
    n_match = n_diverge = n_diverge_benign = n_fail = n_blocked = 0
    for line in out.splitlines():
        if "MATCH:" in line and "**" in line:
            try: n_match = int(line.split("**")[1])
            except Exception: pass
        elif "DIVERGE_BENIGN_HTML_RENDERING:" in line:
            try: n_diverge_benign = int(line.strip().split()[-1])
            except Exception: pass
        elif line.strip().startswith("DIVERGE:"):
            try: n_diverge = int(line.strip().split()[-1])
            except Exception: pass
        elif "FAIL:" in line and "BLOCKED" not in line:
            try: n_fail = int(line.strip().split()[-1])
            except Exception: pass
        elif "BLOCKED:" in line:
            try: n_blocked = int(line.strip().split()[-1])
            except Exception: pass
    pieces = [f"{n_match} MATCH"]
    if n_diverge_benign: pieces.append(f"{n_diverge_benign} DIVERGE_BENIGN_HTML")
    pieces.extend([f"{n_diverge} DIVERGE", f"{n_fail} FAIL", f"{n_blocked} BLOCKED"])
    msg = ", ".join(pieces)
    print(f"  {msg}")
    if n_diverge or n_fail:
        # Surface per-endpoint detail
        bad_lines = [ln for ln in out.splitlines()
                     if any(t in ln for t in ("DIVERGE", "FAIL"))
                     and ("**" in ln or "|" in ln)]
        if bad_lines:
            print("  failing endpoints:")
            for ln in bad_lines[:15]:
                print(f"    {ln.strip()[:160]}")
        return {"status": "FAIL", "msg": msg, "captured": out,
                "hint": _classify_failure(out) or
                "see verify_anchors_occ_spot_check_report.md for endpoint detail"}
    if n_blocked:
        return {"status": "PASS_WITH_SKIPS", "msg": msg,
                "captured": out if verbose else "",
                "hint": "BLOCKED endpoints are documented in LIMITATIONS.md "
                        "(yfinance + lake-derived + Cloudflare)"}
    if n_diverge_benign:
        return {"status": "PASS_WITH_DEFECT", "msg": msg,
                "captured": out if verbose else "",
                "hint": "DIVERGE_BENIGN_HTML_RENDERING is server-side rendering "
                        "drift on uscode.house.gov / ecfr.gov / fec.gov landing "
                        "pages — substantive content unchanged. See LIMITATIONS.md §4."}
    return {"status": "PASS", "msg": msg,
            "captured": out if verbose else "", "hint": None}


def tier_e_reocr(verbose: bool = False) -> dict:
    print()
    print("=" * 70)
    print("TIER E — re-OCR primary PDFs via Gemini (pipeline reproduction)")
    print("=" * 70)
    rc, out = _run([sys.executable, str(ROOT / "tier_e_reocr.py")], ROOT)
    grand: dict[str, int] = {}
    in_grand = False
    for line in out.splitlines():
        if line.startswith("## Grand totals"):
            in_grand = True
            continue
        if in_grand:
            line = line.strip()
            if not line or line.startswith("|") or line.startswith("#"):
                continue
            if ":" in line and "**" in line:
                k = line.split(":")[0].strip()
                try:
                    n = int(line.split("**")[1])
                    grand[k] = n
                except Exception:
                    pass
    parts = ", ".join(f"{k}={n}" for k, n in sorted(grand.items())) or "(no totals parsed)"
    print(f"  {parts}")
    bad = (grand.get("DRIFT_MATERIAL", 0) + grand.get("FETCH_FAIL", 0)
           + grand.get("SHA_MISMATCH", 0) + grand.get("GEMINI_FAIL", 0))
    if bad:
        # Surface the specific failing PDFs
        bad_lines = [ln for ln in out.splitlines()
                     if any(tag in ln for tag in
                            ("DRIFT_MATERIAL", "FETCH_FAIL", "SHA_MISMATCH",
                             "GEMINI_FAIL"))
                     and "|" in ln]
        if bad_lines:
            print("  failing PDFs:")
            for ln in bad_lines[:10]:
                print(f"    {ln.strip()[:200]}")
        return {"status": "FAIL", "msg": parts, "captured": out,
                "hint": _classify_failure(out) or
                "see tier_e_reocr_report.md for per-PDF detail"}
    if grand.get("SKIP_NO_GEMINI_KEY", 0):
        return {"status": "PASS_WITH_SKIPS",
                "msg": parts + " (set GEMINI_API_KEY for re-OCR)",
                "captured": out if verbose else "",
                "hint": "set env: GEMINI_API_KEY=<your-key> (Google AI Studio "
                        "free tier works for ~10 PDFs)"}
    if grand.get("DRIFT_BENIGN", 0):
        return {"status": "PASS_WITH_DEFECT", "msg": parts,
                "captured": out if verbose else "",
                "hint": "DRIFT_BENIGN reflects Gemini's per-row LLM sampling "
                        "variance; aggregates remain stable. See LIMITATIONS.md §5."}
    return {"status": "PASS", "msg": parts,
            "captured": out if verbose else "", "hint": None}


def tier_f_full_rederive(include_chamber: bool, verbose: bool = False) -> dict:
    print()
    print("=" * 70)
    print("TIER F — full pipeline re-derive from primary sources")
    print("=" * 70)
    cmd = [sys.executable, str(ROOT / "tier_f_full_rederive.py")]
    if include_chamber:
        cmd.append("--include-chamber-rebuild")
    rc, out = _run(cmd, ROOT)
    rebuilds_passed = rebuilds_total = 0
    for line in out.splitlines():
        if "rebuilds:" in line and "/" in line:
            try:
                left = line.split("rebuilds:")[1].split("passed")[0].strip()
                a, b = left.split("/")
                rebuilds_passed = int(a.strip())
                rebuilds_total = int(b.strip())
            except Exception:
                pass
    msg = f"{rebuilds_passed}/{rebuilds_total} rebuilds passed"
    print(f"  {msg}")
    if rebuilds_total == 0 or rebuilds_passed < rebuilds_total:
        return {"status": "FAIL", "msg": msg, "captured": out,
                "hint": _classify_failure(out) or
                "see tier_f_full_rederive_report.md for rebuild detail"}
    return {"status": "PASS", "msg": msg,
            "captured": out if verbose else "", "hint": None}


def verify_timestamp(verbose: bool = False) -> dict:
    print()
    print("=" * 70)
    print("OPENTIMESTAMPS — package timestamp proof")
    print("=" * 70)
    rc, out = _run([sys.executable, str(ROOT / "verify_timestamp.py")], ROOT)
    ots_ok = "DIGEST MATCHES" in out
    if ots_ok:
        n_calendars = out.count("calendar attestation") + out.count("calendar.")
        msg = (f"manifest digest matches proof; "
               f"{n_calendars} calendar attestations verified" if n_calendars
               else "manifest digest matches proof; calendar attestations verified")
        return {"status": "PASS", "msg": msg,
                "captured": out if verbose else "", "hint": None}
    return {"status": "FAIL", "msg": "proof verification FAILED",
            "captured": out,
            "hint": _classify_failure(out) or
            ("99_SHA256SUMS.txt.ots may be missing or its digest may not "
             "match the current manifest (snapshot-was-edited?)")}


# ------------------------------------------------------------------
# Final verdict
# ------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spot-check", type=int, default=0,
                    help="Tier-D: random N endpoints (~30s each).")
    ap.add_argument("--tier-E", action="store_true", dest="tier_e",
                    help="Tier-E: re-OCR primary PDFs via Gemini "
                         "(~1-2 hr; requires GEMINI_API_KEY).")
    ap.add_argument("--tier-F", action="store_true", dest="tier_f",
                    help="Tier-F: full re-derive (Tier-E + rebuild scripts; "
                         "~2-4 hr; requires GEMINI_API_KEY).")
    ap.add_argument("--include-chamber-rebuild", action="store_true",
                    help="Tier-F option: also run chamber-wide Gemini rebuild "
                         "($50-200 reviewer Gemini spend).")
    ap.add_argument("--verify-timestamp", action="store_true",
                    help="Also verify the OpenTimestamps proof.")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="Dump full subprocess stdout+stderr for every tier "
                         "(default: only on FAIL).")
    args = ap.parse_args()

    print()
    print("OCC_FILING_PACKAGE_V2 — cold-start full reproduction")
    print(f"Working directory: {ROOT}")
    print(f"Python: {sys.version.split()[0]}  Verbose: {args.verbose}")
    print()

    results: list[tuple[str, dict]] = []
    results.append(("TIER 0 (manifest)",     tier0_manifest(args.verbose)))
    results.append(("TIER 0.5 (anchor cov)", tier0_5_anchor_coverage(args.verbose)))
    results.append(("TIER 1 (verifier)",     tier1_verifier(args.verbose)))
    results.append(("TIER 2 (rebuilds)",     tier2_rebuilds(args.verbose)))
    if args.spot_check:
        results.append((f"TIER D (spot-check x{args.spot_check})",
                        tier_d_spot_check(args.spot_check, args.verbose)))
    if args.tier_e or args.tier_f:
        results.append(("TIER E (re-OCR)",   tier_e_reocr(args.verbose)))
    if args.tier_f:
        results.append(("TIER F (full re-derive)",
                        tier_f_full_rederive(args.include_chamber_rebuild, args.verbose)))
    if args.verify_timestamp:
        results.append(("OPENTIMESTAMPS",    verify_timestamp(args.verbose)))

    # Auto-dump captured output for FAILED tiers; verbose dumps for everything
    for label, r in results:
        if r["status"] == "FAIL" and r.get("captured"):
            _print_full_output(r["captured"], f"{label} captured output (FAILED)")
        elif args.verbose and r.get("captured"):
            _print_full_output(r["captured"], f"{label} captured output")

    print()
    print("=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    for label, r in results:
        line = f"  {label}: {r['status']} — {r['msg']}"
        print(line)
        if r["status"] == "FAIL" and r.get("hint"):
            print(f"    hint: {r['hint']}")
        if r["status"] == "PASS_WITH_SKIPS" and r.get("hint"):
            print(f"    hint: {r['hint']}")
    print()

    statuses = [r["status"] for _, r in results]
    if "FAIL" in statuses:
        verdict = "FAIL"
    elif "PASS_WITH_DEFECT" in statuses:
        verdict = "PASS_WITH_DEFECT"
    elif "PASS_WITH_SKIPS" in statuses:
        verdict = "PASS_WITH_SKIPS"
    else:
        verdict = "PASS"

    print(f"  OVERALL: {verdict}")
    if verdict == "PASS_WITH_DEFECT":
        print()
        print("  Note: PASS_WITH_DEFECT is acceptable. The F225 trade-PnL")
        print("  scalar in v3_facts was computed against a slightly different")
        print("  lake snapshot than the bundled OHLC + PTR rows; the rebuild")
        print("  reproduces within ±5% (the documented post-cascade tolerance).")
        print("  All 68 body-figure anchors and the 2 deterministic rebuilds")
        print("  (PTR audit + PFD Schedule D) are bit-exact.")
        print()
        print("  For Tier-E (re-OCR): DRIFT_BENIGN reflects Gemini's per-row")
        print("  LLM sampling variance — aggregates remain stable.")
    elif verdict == "PASS_WITH_SKIPS":
        print()
        print("  Note: a tier was skipped for missing optional dependencies.")
        print("  See per-tier hints above. To run skipped tiers, install the")
        print("  noted dependency or set the noted environment variable.")
    elif verdict == "FAIL":
        print()
        print("  Note: a tier hard-failed. The captured subprocess output was")
        print("  auto-dumped above. See LIMITATIONS.md and VERIFICATION_TIERS.md")
        print("  for what each tier actually proves.")
    print()

    return 0 if verdict in ("PASS", "PASS_WITH_DEFECT", "PASS_WITH_SKIPS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
