from __future__ import annotations

import hashlib
import json
import os
import random
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from brc.kernel.brc import BRC
from brc.kernel.gating import gate
from brc.monitoring.emit import emit_event


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _stable_obj_hash(obj: Any) -> str:
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _run_id(seed: int) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}_seed{seed}"


def _call_proposer(proposer: Any, genome: Any, step: int, rng: random.Random):
    try:
        return proposer.propose(genome, step, rng)
    except TypeError:
        return proposer.propose(genome, step)


def _append_with_chain(path: str, entry: Dict[str, Any], chain: str) -> str:
    """
    Compute next chain from canonical payload (without 'chain'),
    then append 'chain' field and write full JSON line.
    Returns updated chain.
    """
    payload = json.dumps(entry, sort_keys=True)
    chain = _sha256_hex(chain + payload)

    entry["chain"] = chain
    final_line = json.dumps(entry, sort_keys=True)

    with open(path, "a", encoding="utf-8") as f:
        f.write(final_line + "\n")

    return chain


def run(
    root: str,
    base: Any,
    proposer: Any,
    metric: Any,
    steps: int = 25,
    seed: int = 0,
    run_id: Optional[str] = None,
) -> Dict[str, Any]:

    rng = random.Random(int(seed))
    rid = run_id or _run_id(int(seed))

    ledger_dir = os.path.join(root, "ledger", "runs")
    os.makedirs(ledger_dir, exist_ok=True)

    ledger_path = os.path.join(ledger_dir, f"{rid}.jsonl")
    hash_path = os.path.join(ledger_dir, f"{rid}.hash")
    meta_path = os.path.join(ledger_dir, f"{rid}.meta.json")

    kernel = BRC(metric)

    gamma = base
    prev_S = 0.0
    chain = ""

    # RUN_START
    start_entry = {
        "event": "RUN_START",
        "run_id": rid,
        "seed": int(seed),
        "steps": int(steps),
        "timestamp": _utc_now_iso(),
    }

    chain = _append_with_chain(ledger_path, start_entry, chain)
    emit_event("RUN_START", {"run_id": rid, "steps": steps, "seed": seed})

    for k in range(int(steps)):
        cand = _call_proposer(proposer, gamma, k, rng)

        stats = kernel.evaluate(gamma, cand, base)
        accepted, reason = gate(prev_S, float(stats["S"]))

        if accepted:
            gamma = cand
            prev_S = float(stats["S"])

        step_entry = {
            "event": "STEP",
            "run_id": rid,
            "step": int(k),
            "accepted": bool(accepted),
            "reason": str(reason),
            "stats": stats,
            "genome_hash": _stable_obj_hash(cand.to_dict()),
            "timestamp": _utc_now_iso(),
        }

        chain = _append_with_chain(ledger_path, step_entry, chain)
        emit_event("GATE", step_entry)

    # RUN_END
    end_entry = {
        "event": "RUN_END",
        "run_id": rid,
        "final_S": float(prev_S),
        "timestamp": _utc_now_iso(),
    }

    chain = _append_with_chain(ledger_path, end_entry, chain)

    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(chain)

    meta = {
        "run_id": rid,
        "seed": int(seed),
        "steps": int(steps),
        "ledger_path": ledger_path.replace("\\", "/"),
        "hash_path": hash_path.replace("\\", "/"),
        "final_S": float(prev_S),
        "ledger_chain_hash": chain,
        "created_utc": _utc_now_iso(),
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    emit_event("RUN_END", {"run_id": rid, "final_S": float(prev_S), "ledger_hash": chain})

    return meta
