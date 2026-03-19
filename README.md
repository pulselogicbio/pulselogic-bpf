# PulseLogic BPF

Canonical public repository for the Biomarker Probability Fusion (BPF) pipeline, reproducibility framework, and audit-ready biomarker discovery workflow.

## Overview

This repository provides a public-safe prototype of the BPF pipeline architecture. It demonstrates a deterministic biomarker discovery workflow built around:

- univariate feature ranking by ROC AUC
- top-feature selection
- fused scoring across prioritized biomarkers
- logistic transformation of fused scores
- audit and checkpoint artifact generation
- deterministic configuration defaults

## What this repository includes

- installable Python package under `src/bpf/`
- canonical config for a toy public demo
- toy expression and label datasets
- runnable script and CLI entrypoint
- output artifact generation
- unit tests for ranking, fusion, determinism, and compliance utilities

## What this repository does not include

This repository is public-safe by design and does **not** include:

- confidential datasets
- proprietary disease-specific biomarker panels
- internal research assets
- private validation corpora
- undisclosed commercial implementation details

## Design principles

- deterministic execution
- canonical versioning
- auditability
- reproducibility
- public-safe disclosure

## Quickstart

### Install

```bash
pip install -r requirements.txt
pip install -e .