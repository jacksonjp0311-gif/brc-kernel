from brc.kernel.brc import BRC
from brc.ledger.verify import verify_chain_hash
import json
import os

print("")
print("=== BRC PUBLIC TEST ===")

class ZeroMetric:
    def distance(self, a, b):
        return 0.0

k = BRC(ZeroMetric())
result = k.evaluate({"x":1},{"x":1},{"x":1})

print("Kernel result:", result)

ok, actual, expected = verify_chain_hash("ledger/latest.jsonl","ledger/latest.hash")

print("Ledger verification:", "OK" if ok else "FAIL")
print("Chain hash:", actual)

summary = {
    "kernel_result": result,
    "ledger_ok": ok,
    "chain_hash": actual
}

os.makedirs("benchmarks/results", exist_ok=True)

with open("benchmarks/results/latest_test.json","w",encoding="utf-8") as f:
    json.dump(summary,f,indent=2)

print("Test summary written to benchmarks/results/latest_test.json")
print("")
