# Config

## Overview
Runtime parameters (epsilon, thresholds). Keep small + explicit.

## Mini Directory
- brc_config.json — runtime thresholds

## Sequence of Events
1. Orchestrator loads config
1. Kernel uses epsilon for bounded exploration gate

## Interlinking Notes
- No hidden defaults
- Config changes should be reflected in docs/theory

