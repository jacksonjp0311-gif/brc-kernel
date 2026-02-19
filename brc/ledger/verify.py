from __future__ import annotations
import hashlib
import os
import json
from typing import Tuple

def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def compute_chain_hash(path: str) -> str:
    h = ""
    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            obj.pop("chain", None)
            payload = json.dumps(obj, sort_keys=True)
            h = _sha256_hex(h + payload)

    return h

def verify_chain_hash(jsonl: str, hash_path: str) -> Tuple[bool, str, str]:
    expected = ""
    if os.path.exists(hash_path):
        with open(hash_path, "r", encoding="utf-8") as f:
            expected = f.read().strip()

    actual = compute_chain_hash(jsonl)
    return (actual == expected), actual, expected
