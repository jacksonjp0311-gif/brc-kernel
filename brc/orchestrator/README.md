# Orchestrator

## Overview
Canonical execution pipeline: propose → measure → gate → ledger → emit.

## Mini Directory
- cli.py — entry point
- run.py — main loop

## Sequence of Events
1. RUN_START event
1. for step in steps: propose → compute stats → gate → append → emit
1. RUN_END event

## Interlinking Notes
- Orchestrator is the only supported entry
- No side-effects outside state/ledger/artifacts

