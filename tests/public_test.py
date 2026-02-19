from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from brc.kernel.brc import BRC
from brc.ledger.verify import verify_chain_hash

print("")
print("=== BRC PUBLIC TEST (DETERMINISM) ===")

ROOT = Path(".")
RID = "seed42_steps5"
LEDGER_DIR = ROOT / "ledger" / "runs"
LEDGER = LEDGER_DIR / f"{RID}.jsonl"
HASH = LEDGER_DIR / f"{RID}.hash"
META = LEDGER_DIR / f"{RID}.meta.json"

def rm_seed42():
    for p in [LEDGER, HASH, META]:
        if p.exists():
            p.unlink()

def run_once():
    subprocess.run(
        ["python", "-m", "brc.orchestrator.cli", "--steps", "5", "--seed", "42"],
        check=True,
    )

# Kernel sanity (stable)
class ZeroMetric:
    def distance(self, a, b):
        return 0.0

k = BRC(ZeroMetric())
kernel_result = k.evaluate({"x": 1}, {"x": 1}, {"x": 1})
print("Kernel result:", kernel_result)

# Determinism proof: two clean runs, compare .hash
rm_seed42()
run_once()
h1 = HASH.read_text(encoding="utf-8").strip()

rm_seed42()
run_once()
h2 = HASH.read_text(encoding="utf-8").strip()

print("HASH1:", h1)
print("HASH2:", h2)
det_ok = (h1 == h2)
print("Determinism:", "OK" if det_ok else "FAIL")

# Ledger verification (recompute hash from ledger using canonical rules)
ok, actual, expected = verify_chain_hash(str(LEDGER), str(HASH))
print("Ledger verification:", "OK" if ok else "FAIL")
print("Chain hash actual:", actual)
print("Chain hash expected:", expected)

summary = {
    "kernel_result": kernel_result,
    "determinism_ok": det_ok,
    "hash1": h1,
    "hash2": h2,
    "ledger_ok": ok,
    "chain_hash_actual": actual,
    "chain_hash_expected": expected,
    "run_id": RID,
    "steps": 5,
    "seed": 42,
}

os.makedirs("benchmarks/results", exist_ok=True)
with open("benchmarks/results/latest_test.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, sort_keys=True)

print("Test summary written to benchmarks/results/latest_test.json")
print("")