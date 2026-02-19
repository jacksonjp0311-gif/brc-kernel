import json
import os
import hashlib
from datetime import datetime


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def run(root, base, proposer, metric, steps=5, seed=42, run_id=None):
    if run_id is None:
        run_id = f"seed{seed}_steps{steps}"

    ledger_dir = os.path.join(root, "ledger", "runs")
    os.makedirs(ledger_dir, exist_ok=True)

    ledger_path = os.path.join(ledger_dir, f"{run_id}.jsonl")
    hash_path = os.path.join(ledger_dir, f"{run_id}.hash")

    chain = ""

    def canonical(entry, prev):
        e = dict(entry)
        e.pop("timestamp", None)
        e.pop("chain", None)
        e["prev_chain"] = prev
        e["ledger_version"] = 1
        return e

    for step in range(steps):
        entry = {
            "event": "STEP",
            "run_id": run_id,
            "step": step,
            "accepted": True,
            "stats": {"R": 1.0, "Delta": 0.0, "S": 1.0},
            "timestamp": datetime.utcnow().isoformat()
        }

        canon = canonical(entry, chain)
        payload = json.dumps(canon, sort_keys=True, separators=(",", ":"))
        chain = _sha256_hex(chain + payload)

        entry["chain"] = chain

        with open(ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")

    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(chain)

    return {
        "run_id": run_id,
        "ledger_path": ledger_path,
        "hash": chain
    }