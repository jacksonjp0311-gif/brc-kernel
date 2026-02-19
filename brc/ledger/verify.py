from __future__ import annotations

import hashlib
import os
from typing import Tuple


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def compute_chain_hash(ledger_jsonl_path: str) -> str:
    """
    Rolling chain hash: h_0 = ""
    h_{i+1} = sha256(h_i + line_i)
    where line_i is the raw JSONL line (stripped).
    """
    h = ""
    if not os.path.exists(ledger_jsonl_path):
        return ""

    with open(ledger_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                h = _sha256_hex(h + line)
    return h


def verify_chain_hash(ledger_jsonl_path: str, expected_hash_path: str) -> Tuple[bool, str, str]:
    expected = ""
    if os.path.exists(expected_hash_path):
        with open(expected_hash_path, "r", encoding="utf-8") as f:
            expected = f.read().strip()

    actual = compute_chain_hash(ledger_jsonl_path)
    return (actual == expected), actual, expected
