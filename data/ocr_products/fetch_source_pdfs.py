"""
fetch_source_pdfs.py
====================

Automated fetch recipe for the source PDFs underlying the OCR work products
in this directory:

* The single Khanna PFD (doc_id 8221318) bundled here as
  `khanna_pfd_8221318_OCR.txt` + `khanna_pfd_8221318_P0[1-5].png`.
* The 114 Khanna PTR PDFs (2017-2026) cited via `khanna_ptr_corpus.json`,
  driving the Count 1 late-filing audit and the per-tx claims in Counts
  2 / 3 / 6 / 7. The structured per-tx rows derived from these PDFs live
  at `../occ/ptr_filing_audit_khanna_2026_05_02.json`.

The PDFs are publicly hosted at the House Clerk public disclosure portal:

    PFD: https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf
    PTR: https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf

This script extracts every source URL referenced by the bundled OCR work
products and downloads them to a local cache directory. A reviewer can then
run their own OCR / extraction pipeline against the cached PDFs and compare
to the bundled JSON / CSV / OCR text.

USAGE:
    pip install requests pymupdf
    python fetch_source_pdfs.py                          # 1 PFD only (~3 MB)
    python fetch_source_pdfs.py --include-ptr-corpus     # + 114 Khanna PTRs (~30-50 MB)
    python fetch_source_pdfs.py --render-pages           # also render each fetched PDF
                                                         # to 300-DPI PNGs (one per page)
    python fetch_source_pdfs.py --include-ptr-corpus --render-pages
                                                         # full reviewer kit: 115 PDFs +
                                                         # ~300-500 page renders ready for
                                                         # grep / browse / independent-OCR
    python fetch_source_pdfs.py --cache-dir ./_source_pdfs

EXPECTED PAYLOAD:
    --default                              ~3 MB    (1 Khanna PFD doc_id 8221318)
    --include-ptr-corpus                  ~30-50 MB (+ 114 Khanna PTR PDFs 2017-2026)
    --render-pages (PFD only)             ~5-15 MB  (5-page PFD × 300-DPI PNG ~1-3 MB/page)
    --render-pages --include-ptr-corpus  ~150-400 MB (~300-500 page renders @ 300 DPI)

NOTES:
- clerk.house.gov serves these directly with no authentication; rate is
  friendly but the script paces at 1 req/s by default.
- If a PDF returns 404, that PTR has been amended-superseded and the
  superseding PDF will be at a different doc_id. The bundled
  `khanna_ptr_corpus.json` reflects the as-of-2026-05-02 lake snapshot.

Substrate-verification dig-deeper discipline (per the OCC campaign's
central instruction): if a fetched PDF disagrees with the bundled OCR /
structured output, the default disposition is PROBE DEEPER (different
OCR pipeline, page-mis-numbering, amendment-cascade chain not yet
followed), not "the bundled work product is wrong."
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


# ---------- the 1 cited PFD ----------

KHANNA_PFD_DOCS = [
    # (doc_id, year, label)
    ("8221318", "2024", "Khanna TY2024 PFD — Counts 3 + 7 (Goldman SP margin scaffold + Schedule A asset enumeration)"),
]


# ---------- helpers ----------

def fetch_one(url: str, target: Path, *, sleep_s: float = 1.0) -> bool:
    """Fetch a single PDF; return True on success."""
    if target.exists() and target.stat().st_size > 1024:
        return True
    target.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={
        "User-Agent": "occ-khanna-complaint-reproducibility-kit/1.0",
    })
    try:
        with urlopen(req, timeout=60) as r:
            data = r.read()
    except HTTPError as e:
        print(f"  [{e.code}] {url}")
        return False
    except Exception as e:
        print(f"  [ERR] {url}: {e}")
        return False
    target.write_bytes(data)
    print(f"  [{len(data):>9,}b] {target.name}")
    time.sleep(sleep_s)
    return True


def render_pdf_pages(pdf_path: Path, out_dir: Path, *, dpi: int = 300) -> int:
    """Render every page of pdf_path to a 300-DPI PNG under out_dir/{stem}_P{NN}.png.

    Skips re-rendering if every expected output already exists (idempotent).
    Returns the count of pages rendered (or pre-existing). Returns 0 on
    fitz.open failure (unreadable PDF) so the caller can keep going on the
    other PDFs without aborting the batch.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("  [SKIP] PyMuPDF not installed; pip install pymupdf to enable --render-pages")
        return 0
    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        print(f"  [render-ERR] {pdf_path.name}: {e}")
        return 0
    n_pages = len(doc)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = pdf_path.stem
    pad = max(2, len(str(n_pages)))  # at least 2 digits; 3 if 100+ pages
    mat = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    n_rendered = 0
    n_existing = 0
    for i in range(n_pages):
        out_png = out_dir / f"{stem}_P{str(i + 1).zfill(pad)}.png"
        if out_png.exists() and out_png.stat().st_size > 1024:
            n_existing += 1
            continue
        try:
            pix = doc[i].get_pixmap(matrix=mat)
            out_png.write_bytes(pix.tobytes("png"))
            n_rendered += 1
        except Exception as e:
            print(f"  [render-ERR] {out_png.name}: {e}")
    doc.close()
    if n_rendered or n_existing:
        msg = f"  [rendered {n_rendered}/{n_pages} pages @ {dpi} DPI"
        if n_existing:
            msg += f"; {n_existing} cached"
        msg += f"] {stem}/"
        print(msg)
    return n_pages


def collect_ptr_corpus_urls(json_path: Path) -> list[tuple[str, str]]:
    """Pull (doc_id, pdf_url) tuples from khanna_ptr_corpus.json."""
    if not json_path.exists():
        return []
    d = json.loads(json_path.read_text(encoding="utf-8"))
    out = []
    for r in d.get("rows", []):
        doc_id = r.get("doc_id")
        url = r.get("pdf_url")
        if doc_id and url:
            out.append((doc_id, url))
    return out


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(
        description="Fetch source PDFs underlying the OCR work products in this directory",
    )
    ap.add_argument(
        "--cache-dir", default="./_source_pdfs",
        help="local cache directory (default ./_source_pdfs)",
    )
    ap.add_argument(
        "--include-ptr-corpus", action="store_true",
        help="also fetch every Khanna PTR PDF (114 docs, ~30-50 MB)",
    )
    ap.add_argument(
        "--sleep-s", type=float, default=1.0,
        help="seconds between requests (default 1.0)",
    )
    ap.add_argument(
        "--render-pages", action="store_true",
        help="after fetching each PDF, render every page to a PNG at --render-dpi DPI "
             "via PyMuPDF (one PNG per page; idempotent across re-runs). Lets reviewers "
             "browse / grep / re-OCR each page with their preferred engine.",
    )
    ap.add_argument(
        "--render-dpi", type=int, default=300,
        help="DPI for --render-pages output (default 300; matches the bundled "
             "khanna_pfd_8221318_P0[1-5].png renders).",
    )
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    cache = Path(args.cache_dir)
    if not cache.is_absolute():
        cache = (base / args.cache_dir).resolve()
    cache.mkdir(parents=True, exist_ok=True)

    print(f"=== fetch_source_pdfs.py ===")
    print(f"cache: {cache}")
    print()

    # 1. The 1 cited PFD
    print("[1/2] Khanna PFD (Count 3 + 7 anchor) ...")
    n_ok = 0
    pfd_targets: list[Path] = []
    for doc_id, year, label in KHANNA_PFD_DOCS:
        url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf"
        target = cache / "khanna_pfd" / f"{doc_id}.pdf"
        print(f"  {doc_id} ({year}): {label[:70]}")
        if fetch_one(url, target, sleep_s=args.sleep_s):
            n_ok += 1
            pfd_targets.append(target)
    print(f"  fetched {n_ok}/{len(KHANNA_PFD_DOCS)}")

    if args.render_pages and pfd_targets:
        print()
        print(f"[1b/2] Rendering Khanna PFD pages @ {args.render_dpi} DPI ...")
        for tgt in pfd_targets:
            render_pdf_pages(tgt, cache / "khanna_pfd_renders", dpi=args.render_dpi)

    # 2. PTR corpus (--include-ptr-corpus only)
    if args.include_ptr_corpus:
        print()
        print("[2/2] Khanna PTR corpus (Count 1 late-filing audit + Counts 2/3/6/7 per-tx) ...")
        urls = collect_ptr_corpus_urls(base / "khanna_ptr_corpus.json")
        print(f"  {len(urls)} PTR PDFs to fetch (~{len(urls) * 350 // 1000} MB at typical PTR size)")
        n_ok = 0
        ptr_targets: list[Path] = []
        for doc_id, url in urls:
            year = url.split("/")[-2]
            target = cache / "khanna_ptr" / f"{year}_{doc_id}.pdf"
            if fetch_one(url, target, sleep_s=args.sleep_s):
                n_ok += 1
                ptr_targets.append(target)
        print(f"  fetched {n_ok}/{len(urls)}")

        if args.render_pages and ptr_targets:
            print()
            print(f"[2b/2] Rendering Khanna PTR pages @ {args.render_dpi} DPI ...")
            print(f"  ({len(ptr_targets)} PDFs; ~{len(ptr_targets) * 3} pages typical; "
                  f"~{len(ptr_targets) * 3 * 1500 // 1000} MB @ {args.render_dpi} DPI)")
            n_pages_total = 0
            for tgt in ptr_targets:
                n_pages_total += render_pdf_pages(tgt, cache / "khanna_ptr_renders", dpi=args.render_dpi)
            print(f"  rendered {n_pages_total} total pages across {len(ptr_targets)} PTR PDFs")
    else:
        print()
        print("[2/2] Khanna PTR corpus skipped (pass --include-ptr-corpus to fetch the 114 PTR PDFs)")

    print()
    print(f"Source PDFs available at: {cache}")
    if args.render_pages:
        print(f"Page renders available at: {cache}/khanna_pfd_renders/", end="")
        if args.include_ptr_corpus:
            print(f" + {cache}/khanna_ptr_renders/")
        else:
            print()
    print()
    print("Next step: run your preferred OCR + structured-extraction pipeline against the")
    print("cached PDFs (or the per-page PNGs if --render-pages was passed) and compare your")
    print("output to the bundled work products in this directory")
    print("(`khanna_pfd_8221318_OCR.txt`, `khanna_pfd_schedule_a_assets.csv`).")
    print()
    print("For the late-filing audit reproducibility chain, also see:")
    print("  ../occ/ptr_filing_audit_khanna_2026_05_02.json — frozen per-tx audit")
    print("  ../../REPRODUCIBILITY_METHODOLOGY_OCC.md §1.4 — canonical-view dedup discipline")
    print("  ../../REPRODUCIBILITY_METHODOLOGY_OCC.md §6 — worked HUMANA 358d end-to-end")


if __name__ == "__main__":
    main()
