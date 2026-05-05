#!/usr/bin/env python3
"""welcome.py — interactive guided launcher for OCC_FILING_PACKAGE_V2.

A first-time reviewer runs `python welcome.py` and is walked through
exactly what's in the package, what each verification tier proves, and
which depth they want to run. Defaults are sensible (Enter accepts
everything; the default path is fully offline + reproducible in ~30s).

For CI / scripted use, run `python reproduce_all.py` directly with flags.
This launcher just wraps it with explanations + sane prompts.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_OFF = "\033[0m"


def _supports_color() -> bool:
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        return os.environ.get("TERM") not in (None, "")
    return True


def _bold(s: str) -> str:
    return f"{ANSI_BOLD}{s}{ANSI_OFF}" if _supports_color() else s


def _dim(s: str) -> str:
    return f"{ANSI_DIM}{s}{ANSI_OFF}" if _supports_color() else s


def _ask(prompt: str, default: str = "y") -> str:
    """Read a yes/no answer; Enter accepts the default."""
    suffix = " [Y/n]" if default == "y" else " [y/N]"
    while True:
        try:
            raw = input(f"{prompt}{suffix} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(130)
        if not raw:
            return default
        if raw in ("y", "yes"):
            return "y"
        if raw in ("n", "no"):
            return "n"
        print("  please answer 'y' or 'n' (or press Enter for the default)")


def _ask_text(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        raw = input(f"{prompt}{suffix} ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(130)
    return raw or default


def _count(path: pathlib.Path, pat: str = "*") -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.glob(pat))


def banner() -> None:
    print()
    print("=" * 72)
    print(_bold("  OCC_FILING_PACKAGE_V2 — reviewer welcome"))
    print("=" * 72)
    print()
    print("  This package supports an OCC complaint regarding STOCK Act")
    print("  compliance + financial-interest conflicts by Rep. Ro Khanna")
    print("  (CA-17). Every body figure cited in OCC_COMPLAINT_KHANNA.md")
    print("  is reproducible from primary sources at four depths of trust.")
    print()


def show_inventory() -> None:
    print(_bold("Bundled in this package (the publisher's most-recent extraction):"))
    print()

    n_ptrs = _count(ROOT / "data/ocr_products/khanna_ptrs", "*/")
    n_ptr_ocrs = sum(1 for _ in (ROOT / "data/ocr_products/khanna_ptrs").rglob("*_OCR.json"))
    n_snapshots = _count(ROOT / "data/occ", "*.json") - _count(
        ROOT / "data/occ", "*.provenance.json"
    )
    n_provs = _count(ROOT / "data/occ", "*.provenance.json")
    pfd_ocr = ROOT / "data/ocr_products/khanna_pfd_8221318_OCR.txt"
    has_pfd_ocr = pfd_ocr.exists()
    has_ots = (ROOT / "99_SHA256SUMS.txt.ots").exists()

    print(f"  • {n_ptrs} per-PTR Gemini OCR JSONs ({n_ptr_ocrs} total OCR files)")
    print( "    -> data/ocr_products/khanna_ptrs/<doc_id>/<doc_id>_OCR.json")
    if has_pfd_ocr:
        sz = pfd_ocr.stat().st_size
        print(f"  • 1 PFD Tesseract OCR ({sz:,} bytes; cross-validation vs Gemini)")
        print( "    -> data/ocr_products/khanna_pfd_8221318_OCR.txt")
    print(f"  • {n_snapshots} snapshot JSONs + {n_provs} sibling provenance.json files")
    print( "    -> data/occ/*.json + *.provenance.json (every snapshot's primary URL +")
    print( "       raw-bytes SHA256 + reviewer re-fetch instructions)")
    print(f"  • 6 Ahuja Foundation 990-PF mirror PDFs (GitHub Release assets)")
    print( "    -> AHUJA_990PF_<year>.pdf (TY2016/2018/2019/2021×2/2022)")
    if has_ots:
        print(f"  • OpenTimestamps proof of publication time")
        print( "    -> 99_SHA256SUMS.txt.ots (4 calendar attestations)")
    print()


def show_tier_menu() -> None:
    print(_bold("Verification tiers (in order of effort):"))
    print()
    rows = [
        ("0", "manifest integrity",
         "<1s",  "none",  "298 LF-canonical SHA256s match"),
        ("1", "body-figure verifier",
         "~3s",  "none",  "every body figure derives from bundled snapshots"),
        ("2", "substrate rebuilds",
         "~30s", "none",  "snapshot scalars derive from raw bundled OCR/PDF/OHLC"),
        ("D", "primary-source spot-check",
         "~30s/anchor", "yes (no key)",
         "random snapshot endpoints re-fetched + bytes compared"),
        ("E", "re-OCR via Gemini",
         "~1-2 hr",  "yes + GEMINI_API_KEY",
         "re-runs the OCR pipeline you trust the publisher with"),
        ("F", "full re-derive",
         "~2-4 hr",  "yes + GEMINI_API_KEY",
         "Tier-E + rebuild scripts on re-OCR'd substrate"),
        ("OTS", "OpenTimestamps proof",
         "<1s",  "optional",
         "package existed at publication time (Bitcoin-anchored)"),
    ]
    print(f"  {_bold('Tier'):<5} {_bold('Effort'):<14} {_bold('Network'):<22} {_bold('Proves')}")
    for tier, _name, eff, net, what in rows:
        print(f"  {tier:<5} {eff:<14} {net:<22} {what}")
    print()
    print(_dim("  See VERIFICATION_TIERS.md for what each tier does NOT prove."))
    print(_dim("  See LIMITATIONS.md for documented permanent gaps (yfinance,"))
    print(_dim("  lake-derived chamber percentiles, ProPublica Cloudflare)."))
    print()


def detect_gemini_key() -> str | None:
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def detect_helper_dir() -> str | None:
    return os.environ.get("GEMINI_PER_PAGE_HELPER_DIR")


def run_main() -> int:
    banner()
    show_inventory()
    show_tier_menu()

    print(_bold("What would you like to do?"))
    print()
    print("  Default (recommended for first reviewers): Tiers 0+1+2 — fully")
    print("  offline, ~30s. Verifies every body figure derives from bundled")
    print("  snapshots and every snapshot scalar derives from bundled OCR.")
    print()

    if _ask("  Run the default verification (Tiers 0+1+2)?", "y") == "n":
        print("  Skipping. You can run any tier later via:")
        print(f"    {_bold('python reproduce_all.py [flags]')}")
        return 0

    flags: list[str] = []

    print()
    if _ask("  Also spot-check N random primary sources (Tier-D, ~30s each, "
            "needs network but no key)?", "y") == "y":
        n = _ask_text("    How many endpoints to spot-check?", "5")
        try:
            n_int = max(1, int(n))
        except ValueError:
            n_int = 5
        flags.extend(["--spot-check", str(n_int)])

    print()
    if _ask("  Also verify the OpenTimestamps publication-time proof (OTS, "
            "<1s, optional)?", "y") == "y":
        flags.append("--verify-timestamp")

    print()
    print(_bold("  Tier-E: re-OCR primary PDFs via Gemini"))
    print("  This is the most powerful trust tier — it re-runs the EXACT")
    print("  OCR pipeline the publisher used, on PDFs you fetch yourself,")
    print("  proving the bundled OCR isn't fabricated. It costs ~$5-50 in")
    print("  Gemini API spend (Google AI Studio free tier covers ~10 PDFs)")
    print("  and takes 1-2 hours.")
    print()
    print( "  Most reviewers SKIP this — the bundled OCR is the publisher's")
    print( "  authoritative output, and Tiers 0+1+2+D already cover the")
    print( "  body figures + primary-source bytes. Re-OCR is for paranoid")
    print( "  mode (regulators, opposing counsel, or a journalist who wants")
    print( "  to make a stronger statement than \"the figures verify\").")
    print()

    if _ask("  Want to run Tier-E re-OCR yourself?", "n") == "y":
        key = detect_gemini_key()
        if key:
            print(f"    -> Detected GEMINI_API_KEY in env (set, length={len(key)})")
        else:
            print( "    -> No GEMINI_API_KEY found in env.")
            print( "       Get one free at https://aistudio.google.com/apikey")
            entered = _ask_text("       Paste your GEMINI_API_KEY (or Enter to skip Tier-E)", "")
            if entered:
                os.environ["GEMINI_API_KEY"] = entered
            else:
                print( "    -> Skipping Tier-E.")
                key = None
        if key or os.environ.get("GEMINI_API_KEY"):
            helper = detect_helper_dir()
            if not helper:
                print( "    -> GEMINI_PER_PAGE_HELPER_DIR not set. This is the path")
                print( "       to a checkout of the helper repo exposing")
                print( "       src.gemini_per_page_extract. Without it Tier-E will skip.")
                entered = _ask_text("       Paste GEMINI_PER_PAGE_HELPER_DIR (or Enter to skip Tier-E)", "")
                if entered:
                    os.environ["GEMINI_PER_PAGE_HELPER_DIR"] = entered
                else:
                    print( "    -> Skipping Tier-E (helper dir missing).")
                    key = None
            if key or detect_helper_dir():
                flags.append("--tier-E")
                if _ask("    Also run Tier-F (full re-derive: Tier-E + rebuild scripts)?", "n") == "y":
                    flags.append("--tier-F")
                    if _ask("    Include chamber-wide rebuild ($50-200 Gemini spend)?", "n") == "y":
                        flags.append("--include-chamber-rebuild")

    print()
    if _ask("  Verbose mode (dump full subprocess output for every tier)?", "n") == "y":
        flags.append("--verbose")

    cmd = [sys.executable, str(ROOT / "reproduce_all.py")] + flags
    print()
    print(_bold(f"Running: {' '.join(cmd[1:])}"))
    print(_dim(f"  (you can re-run this directly via: python reproduce_all.py {' '.join(flags)})"))
    print()

    return subprocess.call(cmd, cwd=str(ROOT))


if __name__ == "__main__":
    sys.exit(run_main())
