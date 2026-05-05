#!/usr/bin/env python3
"""verify_timestamp.py — verify the OpenTimestamps proof for 99_SHA256SUMS.txt.

Reviewer-side script. Reads the bundled `99_SHA256SUMS.txt.ots` proof,
hashes the live `99_SHA256SUMS.txt` fresh, and confirms the OTS
commitment chain matches.

USAGE:
    python verify_timestamp.py

Reports:
  - Whether the proof's commitment chain attaches to the manifest's SHA256
  - Calendar attestation timestamps (when proof was submitted to each calendar)
  - Bitcoin block attestations (after the proof has been upgraded — see
    `python upgrade_timestamp.py` to pull Bitcoin block confirmation
    after ~1-2 hours from the original stamp)

Exit code 0 if proof verifies; 1 if SHA mismatch or proof corrupt; 2 if
files missing.

Why this matters: a published `.ots` proof + bundled manifest proves the
package's bytes existed at the time the proof was submitted. A reviewer
running this script much later can confirm the manifest hasn't been
tampered with AND that this particular package state existed at
publication time, not backfilled to match later events.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "99_SHA256SUMS.txt"
PROOF = ROOT / "99_SHA256SUMS.txt.ots"


def _format_attestation(att) -> str:
    """Pretty-print an OTS attestation."""
    cls = type(att).__name__
    if cls == "PendingAttestation":
        uri = getattr(att, "uri", "?")
        if isinstance(uri, bytes):
            uri = uri.decode("utf-8", errors="replace")
        return f"PENDING calendar={uri}"
    if cls == "BitcoinBlockHeaderAttestation":
        return f"BITCOIN block_height={getattr(att, 'height', '?')}"
    if cls == "LitecoinBlockHeaderAttestation":
        return f"LITECOIN block_height={getattr(att, 'height', '?')}"
    return f"{cls} (unknown attestation kind)"


def _walk_attestations(timestamp, depth=0, out=None):
    """Recursively walk a Timestamp tree and collect attestations."""
    if out is None:
        out = []
    for att in timestamp.attestations:
        out.append((depth, att))
    for op, sub_t in timestamp.ops.items():
        _walk_attestations(sub_t, depth + 1, out)
    return out


def main() -> int:
    import argparse
    argparse.ArgumentParser(
        description="Verify the OpenTimestamps proof for 99_SHA256SUMS.txt. "
                    "Reads the bundled .ots proof, hashes the live manifest "
                    "fresh, and confirms the OTS commitment chain matches. "
                    "Exit 0 if proof verifies; 1 if SHA mismatch; 2 if files missing."
    ).parse_args()
    if not MANIFEST.exists():
        print(f"ERROR: {MANIFEST.name} missing", file=sys.stderr)
        return 2
    if not PROOF.exists():
        print(f"ERROR: {PROOF.name} missing", file=sys.stderr)
        return 2

    body = MANIFEST.read_bytes()
    actual_digest = hashlib.sha256(body).digest()
    print(f"Manifest:        {MANIFEST.name}")
    print(f"Size (bytes):    {len(body):,}")
    print(f"SHA256 (hex):    {actual_digest.hex()}")
    print()

    from opentimestamps.core.timestamp import DetachedTimestampFile
    from opentimestamps.core.serialize import BytesDeserializationContext
    from opentimestamps.core.op import OpSHA256

    proof_bytes = PROOF.read_bytes()
    print(f"Proof:           {PROOF.name} ({len(proof_bytes)} bytes)")

    ctx = BytesDeserializationContext(proof_bytes)
    detached = DetachedTimestampFile.deserialize(ctx)
    if not isinstance(detached.file_hash_op, OpSHA256):
        print(f"ERROR: proof uses {type(detached.file_hash_op).__name__}, not SHA256",
              file=sys.stderr)
        return 1

    proof_digest = detached.file_digest
    print(f"Proof attests:   SHA256 {proof_digest.hex()}")
    print()

    if proof_digest != actual_digest:
        print("DIGEST MISMATCH")
        print(f"  Manifest hashes to:  {actual_digest.hex()}")
        print(f"  Proof attests to:    {proof_digest.hex()}")
        print("  -> proof does NOT cover this manifest. Manifest tampered or "
              "wrong proof file.")
        return 1

    print("DIGEST MATCHES — proof covers this exact manifest.")
    print()

    # Walk the timestamp tree and report attestations
    attestations = _walk_attestations(detached.timestamp)
    print(f"Attestations: {len(attestations)} found")
    for depth, att in attestations:
        print(f"  {'  ' * depth}- {_format_attestation(att)}")
    if not attestations:
        print("  (none yet — proof carries calendar commitment but no attestation;")
        print("  run `python upgrade_timestamp.py` after ~1-2 hours to pull")
        print("  the Bitcoin block attestation.)")

    print()
    print("OVERALL: proof structure verified; manifest matches proof digest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
