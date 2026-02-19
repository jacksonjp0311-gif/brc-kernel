import hashlib, pathlib

ledger = pathlib.Path("ledger/latest.jsonl")
h = hashlib.sha256()

for line in ledger.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line:
        h.update(line.encode())

digest = h.hexdigest()
pathlib.Path("ledger/latest.hash").write_text(digest)

print("NEW HASH:", digest)
