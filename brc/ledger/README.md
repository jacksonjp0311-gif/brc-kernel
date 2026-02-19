# Ledger (Package)

## Overview
Append + verify utilities. Ledger is append-only.

## Mini Directory
- append.py — append JSONL
- verify.py — rolling hash verification

## Sequence of Events
1. After gating, append entry
1. Optional verify compares rolling hash

## Interlinking Notes
- Never rewrite ledger
- If verify is enabled, always update hash deterministically

