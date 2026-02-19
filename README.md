
# BRC Kernel — Bounded Recursive Coherence

**BRC** is a plugin-first Python stability kernel for **recursive / self-modifying systems** (agents, optimizers, evolving codebases).  
It enforces a strict, auditable accept/reject gate over proposed mutations, with **append-only provenance** (ledger) and **truth-only runtime events** (monitoring).

Core contract:

- **Retention:** \( R_k = 1 - d(\Gamma_k, \Gamma_0) \)
- **Drift:** \( \Delta_k = d(\Gamma_k, \Gamma_{k-1}) \)
- **Stability:** \( S_k = R_k - \Delta_k \)
- **Gate:** accept if \( \Delta S \ge 0 \), or if \( \Delta S \ge -\epsilon \) (bounded exploration)

> BRC is designed as a reusable kernel: swap in your own **genome**, **metric**, and **proposer**, keep the same gate + ledger + monitoring contracts.

---

## Status

- ✅ Canonical public layout in place (`brc/` is the real package)
- ✅ Working CLI demo (`python -m brc.orchestrator.cli`)
- ✅ Ledger append + event surface active
- 🔜 Packaging for `pip install brc-kernel` (see Roadmap)

---

## Quickstart

### 1) Clone

#### Bash (macOS/Linux/Git Bash)
```bash
git clone https://github.com/jacksonjp0311-gif/brc-kernel.git
cd brc-kernel
````

#### PowerShell (Windows)

```powershell
git clone "https://github.com/jacksonjp0311-gif/brc-kernel.git"
cd "brc-kernel"
```

### 2) Run demo pipeline

```bash
python -m brc.orchestrator.cli --root . --steps 20
```

You should see events like:

* `EVENT RUN_START`
* `EVENT GATE` (per step)
* `EVENT RUN_END`

### 3) Inspect outputs

* **Ledger (source of truth):** `ledger/brc_ledger.jsonl`
* **Docs:** `docs/theory/BRC_v1.6.tex`, `docs/architecture/BRC_architecture.tex`
* **Config:** `config/brc_config.json`

---

## How it works (pipeline)

BRC runs a canonical loop:

1. **Propose** a candidate genome (plugin)
2. **Measure** candidate vs previous/base (metric plugin)
3. **Gate** with stability rule (kernel)
4. **Append** decision to **ledger** (append-only)
5. **Emit** truth events (monitoring)

This ordering is intentional: **do not bypass orchestrator order** if you want deterministic provenance.

---

## Repository layout (canonical)

### Top-level structure

```
.
├── brc/                 # Python package (kernel + plugins + orchestrator)
├── docs/                # Theory + architecture (LaTeX)
├── config/              # Runtime thresholds
├── state/               # Run/baseline storage
├── ledger/              # Append-only run log (source of truth)
├── artifacts/           # Derived outputs (reports/manifests/hashes)
├── .gitignore
└── README.md
```

### Package structure (`brc/`)

```
brc/
├── __init__.py
├── kernel/              # Stability + gate
├── plugins/             # Genome + metrics + proposers
├── orchestrator/        # Canonical run loop + CLI
├── ledger/              # Append + verify helpers
├── monitoring/          # Truth-only event emission
└── interventions/       # Optional actions (freeze/refine/rollback)
```

---

## Mini-README contract system (important)

Every core folder contains a **local `README.md`** that serves as the contract for that scope:

* **Overview:** what it is
* **Mini directory:** key files and meaning
* **Sequence of events:** how it participates in the run
* **Interlinking notes:** what must not be bypassed

**Workflow rule:** if you modify a folder, read its local README first.

---

## Theory + Architecture

BRC’s math and architecture are documented in LaTeX:

* **Theory (BRC v1.6):** `docs/theory/BRC_v1.6.tex`
* **Architecture:** `docs/architecture/BRC_architecture.tex`

The intent is tight alignment:

* If you change gate logic or stability definition, update **theory**.
* If you change orchestration or file contracts, update **architecture**.

---

## Using BRC in your own system (implementations)

BRC is intentionally “kernel + interfaces.” To integrate with a real agent system:

### A) Define a genome object

A genome is the thing you are evolving (graph, AST, tool plan, code tree, etc.).

Minimum interface used in this demo:

* Store internal structure (e.g., edges)
* Provide a stable serialization:

  * `to_dict()` → JSON-serializable dict

Example in repo:

* `brc/plugins/genome/toy_genome.py`

### B) Define a metric

A metric measures distance / drift / retention between genomes.

In demo:

* `JaccardEdges.compute(prev, cand, base) -> {"R","Delta","S"}`

Example in repo:

* `brc/plugins/metrics/jaccard_edges.py`

> Real systems: replace this with a normalized metric on your genome space:
> AST edit distance, dependency graph divergence, unit test deltas, embedding drift, etc.
> Keep it **normalized to [0,1]** for stable gating.

### C) Define a proposer (mutation operator)

A proposer creates candidate genomes.

Example in repo:

* `brc/plugins/proposal/toy_edge_flip.py`

Real systems: proposer can be

* LLM proposal step
* heuristic mutation
* program rewrite
* constrained optimizer step

### D) Run through orchestrator

Orchestrator is the supported entry. In demo:

* `brc/orchestrator/run.py` + `brc/orchestrator/cli.py`

---

## Configuration

`config/brc_config.json` holds runtime thresholds.

Current fields:

* `epsilon` — bounded exploration allowance
* `S_min` — optional stability floor (reserved for stricter modes)

---

## Ledger (provenance)

Ledger is append-only and intended to be the **source of truth**.

* File: `ledger/brc_ledger.jsonl`
* Each line is a JSON record containing:

  * step index
  * accepted/rejected + reason
  * stats (R, Delta, S)
  * genome hash
  * timestamp

Verification helper exists:

* `brc/ledger/verify.py`

> Rule: never rewrite ledger lines. If you need compaction, write a separate tool that emits a derived summary.

---

## Monitoring (truth-only event surface)

BRC emits events designed to be consumed by:

* UI monitors
* agent supervisors
* log parsers
* pipelines

Current demo emits:

* `RUN_START`
* `GATE` (per step)
* `RUN_END`

Implementation:

* `brc/monitoring/emit.py`

---

## Interventions

Folder:

* `brc/interventions/`

These are optional action hooks (placeholders in v1.6) for:

* freeze
* refine
* rollback

Real usage: interventions become *controlled actions* triggered by gate outcomes or higher-level policy.

---

## Development notes

### Don’t paste GitHub “diff view” into PowerShell

If you copy text like `@@ -0,0 +1 @@` or “Lines changed…” into PowerShell, it will throw parser errors (that text is not PowerShell).
Use an editor (VS Code) for file content; use PowerShell only for commands.

### Clean artifacts

Recommended `.gitignore`:

* `__pycache__/`
* `*.pyc`

---

## Roadmap (next canonical upgrades)

1. **Packaging (pip)**

   * add `pyproject.toml`
   * versioning (`brc-kernel` distribution name)
   * optional console entrypoint: `brc-run`

2. **Real plugin interfaces**

   * define stable abstract interfaces for Genome/Metric/Proposer
   * seed control + determinism guarantees

3. **Ledger verification hardening**

   * rolling hash file emission
   * optional signature / chain checks

4. **Reference implementations**

   * AST genome (Python code)
   * dependency graph genome
   * test-driven stability metric
   * “LLM proposer” example (behind a flag)

5. **UI monitor**

   * read-only dashboard consuming `EVENT ...` outputs + ledger JSONL

---

## License

Add your license of choice (MIT/Apache-2.0 recommended) before broad adoption.

---

## Run (one-liner)

```bash
python -m brc.orchestrator.cli --root . --steps 20