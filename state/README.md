# State

## Overview
Runtime state storage for runs/baselines.

## Mini Directory
- runs/ — run outputs
- baselines/ — baseline snapshots

## Sequence of Events
1. Orchestrator writes run outputs here
1. Keep deterministic folder naming

## Interlinking Notes
- State is output-only unless explicitly versioned
- Do not mix experiments with canonical runs

