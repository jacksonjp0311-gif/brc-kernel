# Kernel Overview

## Overview
Computes stability S = R − Δ and enforces acceptance gates.

## Mini Directory
- gating.py — accept/reject logic (epsilon-bounded explore)
- contracts.py — invariants/normalization guards
- brc.py — kernel evaluation utilities
- convergence.py — optional contraction estimation

## Sequence of Events
1. Given prev genome + candidate genome → compute (R,Δ,S)
1. Gate uses ΔS and epsilon
1. Return decision + reason

## Interlinking Notes
- Metric must be normalized [0,1]
- Do not change S definition without updating theory

