# Monitoring (Package)

## Overview
Truth-only runtime events for UI/agents/logging.

## Mini Directory
- emit.py — prints EVENT name + payload

## Sequence of Events
1. Emit RUN_START
1. Emit GATE per step
1. Emit RUN_END

## Interlinking Notes
- Events must be stable schemas
- No unbounded payloads

