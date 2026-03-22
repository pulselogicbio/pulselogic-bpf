# PulseLogic BPF

Canonical public repository for the Biomarker Probability Fusion (BPF) pipeline, reproducibility framework, and benchmark artifacts.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ORCiD](https://img.shields.io/badge/ORCiD-0009--0008--5690--3723-brightgreen.svg)](https://orcid.org/0009-0008-5690-3723)

---

## Manuscript

This repository contains the code and benchmark artifacts for:

> Dowden, C.B. (2026). "A stability-governed, tuning-free framework for feature selection
> in high-dimensional transcriptomic biomarker discovery."
> *Bioinformatics* (submitted). bioRxiv: [DOI upon posting]

**If you are a reviewer or reader looking to verify manuscript results, go directly to [`benchmark/REPRODUCIBILITY.md`](benchmark/REPRODUCIBILITY.md).**

---

## Repository structure

```
pulselogic-bpf/
  src/bpf/                  ← Installable BPF Python package
  benchmark/
    bpf_benchmark_v2_3.py   ← Benchmark runner script (manuscript v2.3)
    splits/                 ← Frozen CV split files (23 cohorts, seed=42)
    checkpoints/            ← Per-cohort fold-level result checkpoints
    results/                ← Pre-computed outputs (Tables 1–4 source data)
    reports/                ← Per-cohort benchmark report files
    REPRODUCIBILITY.md      ← Maps every manuscript number to a file
  configs/                  ← Pipeline configuration files
  examples/                 ← Runnable demo scripts
  tests/                    ← Unit tests
  outputs/                  ← Demo output artifacts
  requirements.txt
  pyproject.toml
```

---

## Manuscript benchmark results

All numerical results in the manuscript are pre-computed and available in `benchmark/results/`:

| File | Manuscript table |
|---|---|
| `benchmark_results.csv` | Table 1 — Per-cohort mean AUC (23 cohorts) |
| `benchmark_summary.csv` | Table 3 — Cross-tier aggregate AUC |
| `benchmark_comparisons.csv` | W/L/T comparison summary |
| `benchmark_long.csv` | Full fold-level AUC data |
| `benchmark_figure_data.json` | Figure 1–3 source data |

Frozen cross-validation splits (seed=42, 5×5 repeated stratified k-fold) are in `benchmark/splits/`, one JSON file per cohort.

---

## Benchmark design

| Parameter | Value |
|---|---|
| CV design | 5×5 repeated stratified k-fold (25 folds per cohort) |
| Random seed | 42 (globally fixed; splits frozen before any method runs) |
| Downstream classifier | RandomForest(n_estimators=100, max_depth=6, random_state=42) |
| Gene pre-filter | Top 10,000 by variance (per training fold) |
| Methods compared | BPF, LASSO, ElasticNet, RF_Importance, RF_native |
| Primary metric | Mean AUC across 25 held-out test folds |
| Stability metric | Mean Jaccard similarity across all C(25,2) fold pairs |
| Cohorts | 23 independent cohorts across METABRIC, GEO, and ICGC |
| Total patients | 19,038 |
| Cancer types | 19 |

---

## Running the benchmark

> ⚠️ Full re-run is computationally intensive.
> LASSO and ElasticNet require 6–37 hours per cohort.
> BPF requires 5–9 minutes per cohort.
> Pre-computed results in `benchmark/results/` match the manuscript exactly.

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Single cohort, all methods
python benchmark/bpf_benchmark_v2_3.py \
  --data-dir /path/to/expression/data \
  --cohorts METABRIC \
  --skip-mrmr \
  --max-input-genes 10000

# All cohorts with resume support (recommended for full run)
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

The `--resume` flag loads completed cohorts from checkpoints and skips them, enabling safe restart after interruption.

---

## Data sources

All expression datasets are publicly available. Raw data are not redistributed in this repository.

| Tier | Cohorts | Source |
|---|---|---|
| METABRIC | 1 cohort, n=1,979 | [EGA: EGAS00000000083](https://ega-archive.org/studies/EGAS00000000083) |
| GEO | 5 cohorts | [NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/) — accessions GSE68465, GSE15459, GSE37745, GSE31684, GSE2990 |
| ICGC | 17 cohorts | [ICGC Data Portal](https://dcc.icgc.org/) |

To reproduce results: download expression matrices from the sources above, align sample identifiers to the frozen split indices in `benchmark/splits/`, and run the benchmark script.

---

## Environment

```
Python 3.11
scikit-learn==1.3.0
numpy==1.24.0
pandas==2.0.0
scipy>=1.12
```

---

## BPF pipeline (public prototype)

This repository also includes an installable Python package demonstrating the core BPF pipeline architecture:

- Univariate feature ranking by ROC AUC
- Adaptive top-feature selection
- Deterministic configuration defaults
- Audit and checkpoint artifact generation
- Unit tests for ranking, fusion, determinism, and compliance utilities

### Install

```bash
pip install -r requirements.txt
pip install -e .
```

### Demo

```bash
python examples/run_demo.py
```

Demo outputs are written to `outputs/`.

---

## What this repository does not include

This repository is public-safe by design and does **not** include:

- Raw expression matrices (publicly available at sources above)
- Proprietary WRF methodology internals
- Disease-specific commercial biomarker panels
- Internal research assets or private validation corpora

---

## Citation

If you use this code or benchmark in your research, please cite:

```bibtex
@article{dowden2026bpf,
  title={A stability-governed, tuning-free framework for feature selection
         in high-dimensional transcriptomic biomarker discovery},
  author={Dowden, Christopher B.},
  journal={Bioinformatics},
  year={2026},
  note={submitted}
}
```

---

## Author

**Christopher B. Dowden**
Founder & CEO, PulseLogic Biosciences Inc.
ceo@pulselogic.bio
ORCiD: [0009-0008-5690-3723](https://orcid.org/0009-0008-5690-3723)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

## Design principles

- Deterministic execution
- Canonical versioning
- Auditability
- Reproducibility
- Public-safe disclosure
