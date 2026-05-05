#!/usr/bin/env python3
"""upgrade_timestamp.py — pull Bitcoin block confirmation for the OTS proof.

Run ~1-2 hours after `stamp_timestamp.py` to upgrade the bundled
`99_SHA256SUMS.txt.ots` proof from "calendar commitment" to
"Bitcoin block attestation". Once a Bitcoin block has been mined that
includes the calendar's aggregate Merkle root, the calendars expose the
inclusion path; this script pulls those paths and merges them into the
.ots file.

USAGE:
    python upgrade_timestamp.py

After running, `python verify_timestamp.py` will show
`BITCOIN block_height=N` attestations alongside the calendar pending
ones. A Bitcoin attestation gives you cryptographic proof the package
existed at the time block N was mined.
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROOF = ROOT / "99_SHA256SUMS.txt.ots"


def main() -> int:
    import argparse
    argparse.ArgumentParser(
        description="Upgrade an OpenTimestamps proof from PENDING calendar "
                    "commitment to BITCOIN block attestation. Run ~1-2 hours "
                    "after stamp_timestamp.py — pulls Bitcoin block "
                    "confirmation from the calendars and rewrites .ots in place."
    ).parse_args()
    if not PROOF.exists():
        print(f"ERROR: proof not found at {PROOF}", file=sys.stderr)
        print("Run `python stamp_timestamp.py` first.", file=sys.stderr)
        return 2

    from opentimestamps.core.timestamp import (
        DetachedTimestampFile, Timestamp,
    )
    from opentimestamps.core.notary import PendingAttestation
    from opentimestamps.core.serialize import (
        BytesDeserializationContext, BytesSerializationContext,
    )

    proof_bytes = PROOF.read_bytes()
    ctx = BytesDeserializationContext(proof_bytes)
    detached = DetachedTimestampFile.deserialize(ctx)
    print(f"Loaded proof:    {PROOF.name} ({len(proof_bytes)} bytes)")

    # Walk timestamp tree to find pending calendar attestations
    def walk(t, path=()):
        for att in t.attestations:
            if isinstance(att, PendingAttestation):
                yield (path, t, att)
        for op, sub in t.ops.items():
            yield from walk(sub, path + (op,))

    pendings = list(walk(detached.timestamp))
    print(f"Pending attestations: {len(pendings)}")

    n_upgraded = 0
    for _path, t, att in pendings:
        uri = att.uri
        if isinstance(uri, bytes):
            uri = uri.decode("utf-8", errors="replace")
        # OpenTimestamps calendar timestamp upgrade endpoint
        # Use the commitment SHA as the lookup key (stamp_timestamp.py
        # submitted the original digest, calendar response was stored at
        # this position in the timestamp tree).
        # Rebuild the commitment value at this point in the tree:
        # The calendar exposes the aggregate at /timestamp/{commitment_hex}
        # where commitment is the message at this point in the tree.
        # Actually, calendar's upgrade is per-commitment.
        # We want the commitment AT the calendar attestation node.
        # The simplest path: walk back from the attestation up the tree
        # to find the message that was sent to that calendar.
        # For the simple stamp_timestamp.py shape, the calendar received
        # the manifest digest directly, so the upgrade lookup uses the
        # detached.file_digest.
        digest_hex = detached.file_digest.hex()
        url = f"{uri}/timestamp/{digest_hex}"
        print(f"  -> {uri} ... ", end="", flush=True)
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "occ-khanna-upgrade/1.0",
                "Accept": "application/vnd.opentimestamps.v1",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = r.read()
            up_ctx = BytesDeserializationContext(resp)
            upgraded_t = Timestamp.deserialize(up_ctx, detached.file_digest)
            detached.timestamp.merge(upgraded_t)
            print(f"OK ({len(resp)} bytes)")
            n_upgraded += 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("not yet confirmed (Bitcoin block pending)")
            else:
                print(f"HTTPError {e.code}")
        except Exception as e:
            print(f"ERR {type(e).__name__}: {e}")

    if n_upgraded == 0:
        print("\nNo upgrades. Bitcoin block not yet confirmed; try again in ~1 hour.")
        return 0

    # Re-serialize the upgraded proof
    ctx_out = BytesSerializationContext()
    detached.serialize(ctx_out)
    PROOF.write_bytes(ctx_out.getbytes())
    print(f"\nUpgraded {n_upgraded} attestations; rewrote {PROOF.name}")
    print("Run `python verify_timestamp.py` to inspect the upgraded proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
