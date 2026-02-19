from __future__ import annotations

import json
from typing import Any, Dict, Optional, TextIO


def append_jsonl(path: str, entry: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def append_ledger(path: str, entry: Dict[str, Any]) -> None:
    """
    Backward-compatible alias.
    """
    append_jsonl(path, entry)

