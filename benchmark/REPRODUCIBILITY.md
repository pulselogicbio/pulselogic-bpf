# BPF Benchmark — Reproducibility Guide

**Manuscript:** "A stability-governed, tuning-free framework for feature selection  
in high-dimensional transcriptomic biomarker discovery"  
**Author:** Christopher B. Dowden, PulseLogic Biosciences Inc.  
**ORCiD:** 0009-0008-5690-3723  
**Contact:** ceo@pulselogic.bio

---

## Purpose of this document

This guide maps every numerical result in the manuscript to the exact file(s)
in this repository that produced it. A reviewer or reader should be able to
verify any reported number by following the steps below.

---

## Directory structure

```
benchmark/
  bpf_benchmark_v2_3.py    ← Benchmark runner (use this to re-run)
  splits/                  ← Frozen CV split files (one JSON per cohort, 23 total)
  results/                 ← Pre-computed outputs matching manuscript tables
  checkpoints/             ← Per-cohort result checkpoints (one JSON per cohort)
  reports/                 ← Per-cohort human-readable report files
  REPRODUCIBILITY.md       ← This file
```

---

## Pre-computed results (manuscript tables)

All results are in `benchmark/results/`. These files were generated from the
23 verified checkpoint files in `benchmark/checkpoints/`.

| File | Manuscript element | Key columns |
|---|---|---|
| `benchmark_results.csv` | Table 1 — Per-cohort AUC | `cohort, method, auc_mean, auc_std, ci_lower, ci_upper, stability, time_s` |
| `benchmark_summary.csv` | Table 3 — Cross-tier aggregate | `method, mean_auc, std_auc, mean_stability, n_cohorts` |
| `benchmark_comparisons.csv` | W/L/T summary | `cohort, vs, bpf_auc, other_auc, advantage` |
| `benchmark_long.csv` | Fold-level AUC data | `cohort, method, fold, auc` |
| `benchmark_figure_data.json` | Figure 1–3 source data | cohort × method × auc/ci/stability/time |

---

## Verifying manuscript numbers

### Table 1 — Per-cohort mean AUC

Source file: `benchmark/results/benchmark_results.csv`

```python
import pandas as pd
df = pd.read_csv("benchmark/results/benchmark_results.csv")

# Verify BPF AUC on METABRIC
row = df[(df.cohort == "METABRIC") & (df.method == "BPF (RF-fixed)")]
print(row["auc_mean"].values)
# Expected: 0.6676

# Verify LASSO AUC on ICGC_STAD-US
row = df[(df.cohort == "ICGC_STAD-US") & (df.method == "LASSO (RF-fixed)")]
print(row["auc_mean"].values)
# Expected: 0.6942
```

**Method names used in files:**
- `BPF (RF-fixed)`
- `LASSO (RF-fixed)`
- `ElasticNet (RF-fixed)`
- `RF_Importance (RF-fixed)`
- `RF (native)`

### Table 2 — Jaccard stability

Stability values are in the `stability` column of `benchmark_results.csv`:

```python
df = pd.read_csv("benchmark/results/benchmark_results.csv")

# Verify BPF stability on METABRIC
row = df[(df.cohort == "METABRIC") & (df.method == "BPF (RF-fixed)")]
print(row["stability"].values)
# Expected: 0.498

# Verify LASSO stability on METABRIC
row = df[(df.cohort == "METABRIC") & (df.method == "LASSO (RF-fixed)")]
print(row["stability"].values)
# Expected: 0.174
```

### Table 3 — Cross-tier aggregate

Source file: `benchmark/results/benchmark_summary.csv`

```python
df = pd.read_csv("benchmark/results/benchmark_summary.csv")
print(df[["method", "mean_auc", "mean_stability", "n_cohorts"]])
```

### Table 4 — Runtime

Runtime values are in the `time_s` column of `benchmark_results.csv`
(in seconds). Convert to hours by dividing by 3600.

```python
df = pd.read_csv("benchmark/results/benchmark_results.csv")

# BPF runtime on METABRIC
row = df[(df.cohort == "METABRIC") & (df.method == "BPF (RF-fixed)")]
print(f"BPF: {row['time_s'].values[0]/60:.1f} minutes")

# LASSO runtime on METABRIC
row = df[(df.cohort == "METABRIC") & (df.method == "LASSO (RF-fixed)")]
print(f"LASSO: {row['time_s'].values[0]/3600:.1f} hours")
```

---

## Frozen splits

All cross-validation splits were generated **once** before any method ran,
using `RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)`.
Split files are in `benchmark/splits/`, one JSON per cohort, each containing
exactly 25 fold definitions with `train` and `test` sample indices.

The same split file was used for all five methods on each cohort, ensuring
that any observed performance difference reflects feature selection quality
rather than sampling variation.

**Split files (23 cohorts):**
```
METABRIC_splits.json
GSE68465_LUAD_splits.json    GSE15459_STAD_splits.json
GSE37745_LUNG_splits.json    GSE31684_BLCA_splits.json
GSE2990_BRCA_splits.json
ICGC_BLCA-US_splits.json     ICGC_BRCA-US_splits.json
ICGC_CESC-US_splits.json     ICGC_COAD-US_splits.json
ICGC_GBM-US_splits.json      ICGC_KIRP-US_splits.json
ICGC_LAML-US_splits.json     ICGC_LGG-US_splits.json
ICGC_LIHC-US_splits.json     ICGC_LUAD-US_splits.json
ICGC_LUSC-US_splits.json     ICGC_OV-US_splits.json
ICGC_PAAD-US_splits.json     ICGC_SKCM-US_splits.json
ICGC_STAD-US_splits.json     ICGC_THCA-US_splits.json
ICGC_UCEC-US_splits.json
```

---

## Re-running the benchmark

> ⚠️ Full re-run is computationally intensive.
> LASSO and ElasticNet require 6–37 hours per cohort.
> BPF requires 5–9 minutes per cohort.
> Pre-computed results in `benchmark/results/` match the manuscript exactly.

### Step 1 — Obtain expression data

Download expression matrices from their public sources (see main README).
Raw data are not included in this repository.

### Step 2 — Run single cohort

```bash
python benchmark/bpf_benchmark_v2_3.py \
  --data-dir /path/to/expression/data \
  --cohorts METABRIC \
  --skip-mrmr \
  --max-input-genes 10000
```

### Step 3 — Run all 23 cohorts with resume support

```bash
python benchmark/bpf_benchmark_v2_3.py \
  --data-dir /path/to/expression/data \
  --cohorts METABRIC GSE68465 GSE15459 GSE37745 GSE31684 GSE2990 \
            BLCA-US BRCA-US CESC-US COAD-US GBM-US KIRP-US LAML-US \
            LGG-US LIHC-US LUAD-US LUSC-US OV-US PAAD-US SKCM-US \
            STAD-US THCA-US UCEC-US \
  --skip-mrmr \
  --max-input-genes 10000 \
  --resume
```

The `--resume` flag loads completed cohorts from `benchmark/checkpoints/`
and skips them, enabling safe restart after interruption.

### Step 4 — Verify against pre-computed results

```python
import pandas as pd
import numpy as np

ref = pd.read_csv("benchmark/results/benchmark_results.csv")
new = pd.read_csv("benchmark_output/benchmark_results.csv")  # your re-run output

merged = ref.merge(new, on=["cohort","method"], suffixes=("_ref","_new"))
merged["diff"] = (merged.auc_mean_ref - merged.auc_mean_new).abs()
print(merged[merged["diff"] > 0.001][["cohort","method","auc_mean_ref","auc_mean_new","diff"]])
# Should be empty — any rows indicate a configuration mismatch
```

---

## Checkpoint files

Each JSON in `benchmark/checkpoints/` contains the complete results for one
cohort across all 5 methods, including fold-level AUC scores used to compute
confidence intervals and Jaccard stability. These are the source of truth for
all numbers in the manuscript.

**Note on ICGC_OV-US.json:** This checkpoint was reconstructed from the
per-cohort report file (`benchmark/reports/ICGC_OV-US_report.txt`) after
the original checkpoint was found incomplete. Summary statistics match the
manuscript exactly. Fold-level AUC data for BPF, LASSO, ElasticNet, and
RF_Importance are not available for this cohort; only RF (native) fold-level
data is included.

---

## What is and is not in this repository

| Included | Not included |
|---|---|
| Frozen CV split indices — 23 JSON files | Raw expression matrices (publicly available) |
| Pre-computed results — 5 CSV/JSON files | Proprietary WRF methodology internals |
| Per-cohort checkpoints — 23 JSON files | Disease-specific commercial panels |
| Per-cohort report files — 23 TXT files | Internal research assets |
| Benchmark runner script (v2.3) | |

---

## Determinism guarantee

Given identical inputs (expression matrix, frozen split file) and the
reference environment (Python 3.11, scikit-learn 1.3, numpy 1.24, pandas 2.0),
BPF results are exactly reproducible to floating-point precision. LASSO and
ElasticNet results depend additionally on the LAPACK/BLAS implementation and
may show negligible numerical variation across platforms while remaining
statistically identical.

---

## Version

Benchmark pipeline: v2.3
Splits generated: March 2026
Seed: 42
Archive ID: BPF-BENCH-2026-v2.3
