# BRC Package

## Overview
Python package implementing the BRC kernel + plugins + orchestrator.

## Mini Directory
- kernel/ — stability function + gating
- plugins/ — genome/metric/proposal modules
- orchestrator/ — run loop + CLI
- ledger/ — append + verify
- monitoring/ — truth events

## Sequence of Events
1. Invoke via python -m brc.orchestrator.cli
1. Orchestrator owns the sequence

## Interlinking Notes
- Do not bypass orchestrator
- Keep kernel/ledger/monitoring contracts tight

