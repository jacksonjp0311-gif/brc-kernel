import json
import os
import hashlib

def compute_chain_hash(path: str) -> str:
    chain = ""
    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            obj = json.loads(line)
            prev = chain

            obj.pop("timestamp", None)
            obj.pop("chain", None)

            if "run_ID" in obj and "run_id" not in obj:
                obj["run_id"] = obj.pop("run_ID")

            obj["prev_chain"] = prev
            obj["ledger_version"] = int(obj.get("ledger_version", 1))

            payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
            chain = hashlib.sha256((prev + payload).encode("utf-8")).hexdigest()

    return chain


def verify_chain_hash(ledger_path: str, hash_path: str):
    expected = ""
    if os.path.exists(hash_path):
        with open(hash_path, "r", encoding="utf-8") as f:
            expected = f.read().strip()

    actual = compute_chain_hash(ledger_path)
    return actual == expected, actual, expected