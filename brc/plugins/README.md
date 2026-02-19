# Plugins

## Overview
Pluggable components: genome extraction, proposal generation, and metrics.

## Mini Directory
- genome/ — genome model + serialization
- metrics/ — distance/retention metrics
- proposal/ — mutation/proposal operators

## Sequence of Events
1. Orchestrator calls proposer
1. Metric evaluates candidate vs prev/base
1. Kernel gates candidate

## Interlinking Notes
- Plugins must be deterministic when seeded
- Keep plugin interfaces minimal and stable

