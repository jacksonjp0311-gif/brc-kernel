from __future__ import annotations

import hashlib
import json
import os
import random
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from brc.kernel.brc import BRC
from brc.kernel.gating import gate
from brc.ledger.append import append_jsonl
from brc.monitoring.emit import emit_event


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _stable_obj_hash(obj: Any) -> str:
    s = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(s).hexdigest()


def _run_id(seed: int) -> str:
    # deterministic identifier prefix + timestamp for uniqueness
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}_seed{seed}"


def _call_proposer(proposer: Any, genome: Any, step: int, rng: random.Random):
    """
    Preferred proposer signature:
      propose(genome, step, rng)
    Backward compatible:
      propose(genome, step)
    """
    try:
        return proposer.propose(genome, step, rng)
    except TypeError:
        return proposer.propose(genome, step)


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

    chain = ""  # rolling chain hash over JSONL lines

    # --- RUN_START (ledger + event) ---
    start_entry = {
        "event": "RUN_START",
        "run_id": rid,
        "seed": int(seed),
        "steps": int(steps),
        "timestamp": _utc_now_iso(),
    }
    start_line = json.dumps(start_entry, sort_keys=True)
    chain = _sha256_hex(chain + start_line)
    start_entry["chain"] = chain

    append_jsonl(ledger_path, start_entry)
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

        step_line = json.dumps(step_entry, sort_keys=True)
        chain = _sha256_hex(chain + step_line)
        step_entry["chain"] = chain

        append_jsonl(ledger_path, step_entry)
        emit_event("GATE", step_entry)

    # --- RUN_END (ledger + event) ---
    end_entry = {
        "event": "RUN_END",
        "run_id": rid,
        "final_S": float(prev_S),
        "ledger_chain_hash": chain,
        "timestamp": _utc_now_iso(),
    }
    end_line = json.dumps(end_entry, sort_keys=True)
    chain = _sha256_hex(chain + end_line)
    end_entry["chain"] = chain

    append_jsonl(ledger_path, end_entry)

    # write final expected hash (final chain state)
    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(chain)

    # metadata for tooling / UI
    meta = {
        "run_id": rid,
        "seed": int(seed),
        "steps": int(steps),
        "ledger_path": ledger_path.replace("\\", "/"),
        "hash_path": hash_path.replace("\\", "/"),
        "created_utc": _utc_now_iso(),
        "final_S": float(prev_S),
        "ledger_chain_hash": chain,
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    # also write "latest" pointers for convenience
    latest_meta = os.path.join(root, "ledger", "latest.meta.json")
    latest_ledger = os.path.join(root, "ledger", "latest.jsonl")
    latest_hash = os.path.join(root, "ledger", "latest.hash")

    try:
        with open(latest_meta, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, sort_keys=True)
        # store copies (not links) for Windows friendliness
        import shutil
        shutil.copyfile(ledger_path, latest_ledger)
        shutil.copyfile(hash_path, latest_hash)
    except Exception:
        # non-fatal
        pass

    emit_event("RUN_END", {"run_id": rid, "final_S": float(prev_S), "ledger_hash": chain})
    return meta
