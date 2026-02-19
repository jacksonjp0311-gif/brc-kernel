# Ledger

## Overview
Append-only decision history. Source of truth for run provenance.

## Mini Directory
- brc_ledger.jsonl — append-only run log
- brc_ledger.hash — optional rolling hash file

## Sequence of Events
1. Each step appends an entry
1. Optional hash verification checks immutability

## Interlinking Notes
- Never rewrite ledger lines
- If you need compaction, write a separate tool

