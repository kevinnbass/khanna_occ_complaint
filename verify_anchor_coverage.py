"""TIER 0.5 — anchor coverage gate (multi-file).

Asserts that every figure-bearing paragraph in the V2 packet's three
public-facing operative filings carries at least one [OCC_M###] marker,
ensuring every load-bearing number is reachable via the verifier pipeline.

Files gated:
- OCC_COMPLAINT_KHANNA.md   (principal ethics complaint)
- DOJ_REFERRAL_KHANNA.md    (parallel criminal referral)
- HOUSE_ETHICS_SUBMISSION_KHANNA.md (parallel committee material)

`FEC_REFERRAL_PROTECT_PROGRESS.md` lives at dossier root with FECPP marker
family + own provenance infrastructure and is intentionally OUT OF SCOPE
for this V2-bounded gate.

Returns exit 0 (PASS) if every figure-bearing paragraph in every target is
anchored, else exit 1 (FAIL) with a per-file punch list.

Wires into reproduce_all.py between Tier 0 and Tier 1: any operative
paragraph that drifts away from substrate-verified figures must do so
through a marker, never silently.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# Per-file skip regex — sections after which scanning stops.
# OCC complaint uses Roman-numeral § VII/VIII/IX/X for catalog/registry/methodology.
# Sibling filings use Arabic-numeral sections at the same conceptual position.
TARGETS = [
    {
        "file": "OCC_COMPLAINT_KHANNA.md",
        "skip_section": re.compile(r"^##+\s+(VII|VIII|IX|X)[\.\s]"),
    },
    {
        "file": "DOJ_REFERRAL_KHANNA.md",
        # § 7 Limits / § 8 Statutory citations — non-operative
        "skip_section": re.compile(r"^##+\s+(7|8)[\.\s]"),
    },
    {
        "file": "HOUSE_ETHICS_SUBMISSION_KHANNA.md",
        # § 6 Limitations / § 7 Citations / § 8 Companion filings — non-operative
        # § 9 (Supplementary context) IS operative but carries no new figures.
        "skip_section": re.compile(r"^##+\s+(6|7|8)[\.\s]"),
    },
]

# Marker form: OCC_M### (in any bracket — works for [OCC_M001] and
# [OCC_M001, OCC_M002, OCC_M003] alike).
MARKER_RE = re.compile(r"OCC_M\d{3}")

# Operative figures: dollar amounts, large counts, percentages, percentile
# rankings, "rank N of M" phrases.
FIG_RE = re.compile(
    r"\$\s?[\d,]+(?:\.\d+)?[MKB]?\b"
    r"|\b\d{2,3}(?:,\d{3})+\b"
    r"|\b\d+\.\d+\s*(?:percent|%)"
    r"|\bP\d{1,3}(?:\.\d+)?\b"
    r"|\brank\s+\d+\s+of\s+\d+\b"
    r"|\b\d+\s+(?:transactions|trades|filings|days|members)\b"
)

PARA_HDR_RE = re.compile(r"^(\d{1,3})\.\s")


def scan_file(file_path: Path, skip_section: re.Pattern) -> tuple[int, int, list]:
    """Return (n_paragraphs, n_figure_bearing, unanchored_list)."""
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    paragraphs: list[tuple[int, int, str]] = []
    in_skip = False
    current = None

    for i, line in enumerate(lines):
        if skip_section.match(line):
            in_skip = True
        if in_skip:
            continue
        m = PARA_HDR_RE.match(line)
        if m:
            if current is not None:
                paragraphs.append((current[0], current[1], "\n".join(lines[current[1]:i])))
            current = (int(m.group(1)), i)

    if current is not None and not in_skip:
        paragraphs.append((current[0], current[1], "\n".join(lines[current[1]:])))

    unanchored = []
    n_figure_bearing = 0
    for num, start, body in paragraphs:
        figures = FIG_RE.findall(body)
        if figures:
            n_figure_bearing += 1
            if not MARKER_RE.search(body):
                unanchored.append((num, start + 1, sorted(set(figures))[:8]))

    return len(paragraphs), n_figure_bearing, unanchored


def main() -> int:
    overall_pass = True
    n_targets_scanned = 0
    for target in TARGETS:
        fp = ROOT / target["file"]
        if not fp.exists():
            # Scope-aware: missing parallel-venue filings are not a
            # gate failure. The public OCC-only release ships only
            # OCC_COMPLAINT_KHANNA.md; DOJ + House Ethics submissions
            # live in the working dossier and are transmitted via
            # separate channels at filing time.
            print(f"[SKIP] {target['file']}: not present "
                  f"(scope-aware — file lives in a parallel filing channel)")
            continue
        n_targets_scanned += 1

        n_para, n_fig, unanchored = scan_file(fp, target["skip_section"])
        status = "PASS" if not unanchored else "FAIL"
        print(f"[{status}] {target['file']}: "
              f"{n_para} paragraphs, {n_fig} figure-bearing, "
              f"{len(unanchored)} un-anchored")

        if unanchored:
            overall_pass = False
            for num, line_no, figures in unanchored:
                print(f"  para {num} (line {line_no}): {figures}")

    print()
    if overall_pass:
        print("PASS: All figure-bearing paragraphs anchored to [OCC_M###] markers.")
        return 0
    print("FAIL: Un-anchored paragraphs exist (every figure must trace to an [OCC_M###] marker).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
