import os, hashlib

def _sha(x):
    return hashlib.sha256(x.encode()).hexdigest()

def verify(root):
    ledger=os.path.join(root,"ledger","brc_ledger.jsonl")
    hfile=os.path.join(root,"ledger","brc_ledger.hash")

    if not os.path.exists(ledger):
        return True

    h=""
    for line in open(ledger):
        line=line.strip()
        if line:
            h=_sha(h+line)

    expected=open(hfile).read().strip() if os.path.exists(hfile) else ""

    return h==expected
