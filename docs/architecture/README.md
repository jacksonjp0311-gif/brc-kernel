# Architecture Overview

## Mini Directory

BRC_architecture.tex — implementation spec  
Defines kernel → plugins → ledger flow  


## Sequence of Events
1. Folder is loaded by orchestrator.
2. Contracts are validated.
3. Artifacts emitted deterministically.

## Interlinking Notes
- Do not bypass orchestrator.
- Maintain deterministic ordering.
- All outputs must be ledger-tracked.
