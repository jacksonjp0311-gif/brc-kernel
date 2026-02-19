import json
import os
import hashlib
from datetime import datetime

from brc.kernel.gating import gate
from brc.ledger.append import append_ledger
from brc.monitoring.emit import emit_event

def _hash(obj):
    s = json.dumps(obj, sort_keys=True).encode()
    return hashlib.sha256(s).hexdigest()

def run(root, base, proposer, metric, steps=25):
    ledger_path = os.path.join(root, "ledger", "brc_ledger.jsonl")
    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)

    gamma = base
    prev_S = 0

    emit_event("RUN_START", {"steps": steps})

    for k in range(steps):
        cand = proposer.propose(gamma, k)

        stats = metric.compute(gamma, cand, base)

        accepted, reason = gate(prev_S, stats["S"])

        if accepted:
            gamma = cand
            prev_S = stats["S"]

        entry = {
            "step": k,
            "accepted": accepted,
            "reason": reason,
            "stats": stats,
            "hash": _hash(cand.to_dict()),
            "timestamp": datetime.utcnow().isoformat()
        }

        append_ledger(ledger_path, entry)
        emit_event("GATE", entry)

    emit_event("RUN_END", {"final_S": prev_S})
