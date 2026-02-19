# BRC — Bounded Recursive Coherence

Public release kernel for stability-first recursive systems.

BRC formalizes a simple but strict stability contract:

- Retention: R_k = 1 - d(Γ_k, Γ_0)
- Drift:      Δ_k = d(Γ_k, Γ_{k-1})
- Stability:  S_k = R_k - Δ_k
- Gate: accept if ΔS >= 0, or if ΔS >= -ε (bounded exploration)

## Repository Layout

    brc/        Python package (kernel + plugins + orchestrator)
    docs/       Theory + architecture (LaTeX)
    config/     Runtime thresholds (epsilon, etc.)
    state/      Run/baseline storage
    ledger/     Append-only run log (source of truth)
    artifacts/  Derived outputs (reports/manifests/hashes)

## Mini-README System

Every folder contains a local README.md that acts as the **contract** for that scope:

- Overview (what this folder is for)
- Mini directory (key files)
- Sequence of events (how it is used)
- Interlinking notes (what not to bypass)

### Human workflow
1. Navigate into the folder you need to modify.
2. Read that folder README.md first.
3. Follow the file links and sequence rules.

### AI workflow
- Treat each folder README.md as the local contract before edits.
- Preserve orchestrator ordering and ledger append-only rules.
- Never introduce hidden state or bypass gates.

## Run

    cd C:\Users\jacks\OneDrive\Desktop\BRC
    python -m brc.orchestrator.cli --root . --steps 25

## Docs

- Theory: docs/theory/BRC_v1.6.tex
- Architecture: docs/architecture/BRC_architecture.tex

