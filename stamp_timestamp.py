#!/usr/bin/env python3
"""stamp_timestamp.py — submit 99_SHA256SUMS.txt to OpenTimestamps calendars.

Runs ONCE at release-build time on the publisher side. Submits the SHA256
of `99_SHA256SUMS.txt` to multiple public OpenTimestamps calendar servers,
collects the partial proofs, and writes a combined `.ots` file alongside
the manifest.

Why timestamp the SHA manifest (and not the tarball directly)?
  - The SHA manifest is the cryptographic root of the package's integrity.
    Every file in the tarball is hashed in the manifest. If any file
    changes, the manifest changes, the manifest's SHA changes, and the
    OTS proof breaks. So timestamping the manifest implicitly timestamps
    every file in it.
  - The tarball varies by compression level / order; the manifest is
    deterministic LF-canonical bytes.

USAGE:
    python stamp_timestamp.py
    # produces 99_SHA256SUMS.txt.ots (incomplete proof; calendar
    # commitment but no Bitcoin block yet — Bitcoin block confirmation
    # comes later via `python upgrade_timestamp.py` after ~1-2 hours)

The companion `verify_timestamp.py` reads the .ots file, hashes the
manifest fresh, and confirms the OTS commitment chain. Even before
Bitcoin block confirmation, calendar commitment proves the package
existed at submission time + survives calendar-server tampering (since
multiple calendars are queried).
"""
from __future__ import annotations

import hashlib
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "99_SHA256SUMS.txt"
PROOF = ROOT / "99_SHA256SUMS.txt.ots"

# Public OpenTimestamps calendar servers. We submit to multiple calendars
# so the proof survives any single calendar going offline.
CALENDARS = [
    "https://a.pool.opentimestamps.org",
    "https://b.pool.opentimestamps.org",
    "https://a.pool.eternitywall.com",
    "https://ots.btc.catallaxy.com",
]


def main() -> int:
    import argparse
    argparse.ArgumentParser(
        description="Submit 99_SHA256SUMS.txt to OpenTimestamps calendars + "
                    "write 99_SHA256SUMS.txt.ots proof. Run ONCE at "
                    "release-build time (publisher side); reviewers verify "
                    "via verify_timestamp.py."
    ).parse_args()
    if not MANIFEST.exists():
        print(f"ERROR: manifest not found at {MANIFEST}", file=sys.stderr)
        return 2

    # Read manifest as raw bytes (NOT LF-normalized — we want bit-for-bit)
    body = MANIFEST.read_bytes()
    digest = hashlib.sha256(body).digest()
    print(f"Manifest:        {MANIFEST.name}")
    print(f"Size (bytes):    {len(body):,}")
    print(f"SHA256 (hex):    {digest.hex()}")
    print()

    # Lazy import — opentimestamps lib bypasses the broken otsclient.cmds
    # path on Windows (python-bitcoinlib OpenSSL load failure).
    from opentimestamps.core.timestamp import Timestamp
    from opentimestamps.core.serialize import (
        BytesDeserializationContext,
        BytesSerializationContext,
    )

    # Build a fresh Timestamp object for the manifest digest
    timestamp = Timestamp(digest)

    # Submit to each calendar; merge the returned partial proofs
    n_ok = n_fail = 0
    for cal_url in CALENDARS:
        url = cal_url + "/digest"
        print(f"  -> {cal_url}", end=" ... ", flush=True)
        try:
            req = urllib.request.Request(
                url, data=digest, method="POST",
                headers={
                    "Content-Type": "application/octet-stream",
                    "User-Agent": "occ-khanna-stamp/1.0",
                    "Accept": "application/vnd.opentimestamps.v1",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = r.read()
            ctx = BytesDeserializationContext(resp)
            cal_t = Timestamp.deserialize(ctx, digest)
            timestamp.merge(cal_t)
            print(f"OK ({len(resp)} bytes)")
            n_ok += 1
        except urllib.error.HTTPError as e:
            print(f"HTTPError {e.code}")
            n_fail += 1
        except Exception as e:
            print(f"ERR {type(e).__name__}: {e}")
            n_fail += 1

    if n_ok == 0:
        print("\nERROR: no calendars accepted the digest. Network issue?", file=sys.stderr)
        return 1

    # Serialize the combined timestamp proof to .ots format
    # The .ots file format is: magic header + version + digest_op + serialized_timestamp
    from opentimestamps.core.notary import PendingAttestation  # noqa: F401
    from opentimestamps.core.timestamp import DetachedTimestampFile
    from opentimestamps.core.op import OpSHA256
    detached = DetachedTimestampFile(OpSHA256(), timestamp)
    ctx = BytesSerializationContext()
    detached.serialize(ctx)
    proof_bytes = ctx.getbytes()
    PROOF.write_bytes(proof_bytes)

    print()
    print(f"Calendars OK: {n_ok}/{len(CALENDARS)}")
    print(f"Proof:        {PROOF.name} ({len(proof_bytes)} bytes)")
    print()
    print("This .ots proof attests that the SHA256 of 99_SHA256SUMS.txt was")
    print("submitted to the named OpenTimestamps calendars at the time of")
    print(f"submission ({n_ok} independent calendars). Bitcoin block")
    print("confirmation will land within ~1-2 hours; until then the proof is a")
    print("calendar commitment chain. Use `python upgrade_timestamp.py` later")
    print("to upgrade the proof to a full Bitcoin attestation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
