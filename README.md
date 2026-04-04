# Biomarker Probability Fusion (BPF)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19342790.svg)](https://doi.org/10.5281/zenodo.19342790)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--5690--3723-green.svg)](https://orcid.org/0009-0008-5690-3723)

A disease-agnostic biomarker discovery and risk stratification framework for precision medicine.

Developed by PulseLogic Biosciences Inc. under the discipline of Computational Bio-AI Engineering (CBAE).

---

## Overview

Biomarker Probability Fusion (BPF) is a deterministic, auditable pipeline for
transcriptomic biomarker discovery and patient risk stratification. BPF performs:

- **Univariate biomarker ranking** -- AUC-based discriminative power assessment
  with direction tracking for each gene/feature
- **Adaptive gene selection** -- Statistical filtering (AUC threshold + p-value)
  with configurable panel size
- **Weighted score fusion** -- AUC-weighted z-score composition with direction correction
- **Risk stratification** -- Probabilistic patient scoring with bootstrap confidence intervals
- **Cross-validation** -- 5x5 repeated stratified k-fold with complete within-fold
  feature selection (no information leakage)

BPF is disease-agnostic: the same algorithm and parameters have been validated across
oncology, Alzheimer's disease, and Parkinson's disease without domain-specific modifications.

---

## Validation Summary

| Domain | Training | External Datasets | External Patients | External AUC |
|--------|----------|------------------|-------------------|--------------|
| Oncology | TCGA (39 cohorts) | 41 | 14,498 | 0.8029 |
| Alzheimer's Disease | ADNI | 8 | 2,972 | 0.818 |
| Parkinson's Disease | PPMI | 8 | 753 | 0.793 |
| **Total** | | **57** | **18,223** | |

57 independent external datasets. 18,223 patients. Three disease domains. 100% statistically significant.

See [BENCHMARK_SUMMARY.md](BENCHMARK_SUMMARY.md) for head-to-head benchmark results against
LASSO, ElasticNet, and Random Forest.

---

## Repository Structure

```
pulselogic-bpf/
|-- README.md
|-- LICENSE
|-- CITATION.cff
|-- BENCHMARK_SUMMARY.md       # Benchmark v2.3 results vs. baselines
|-- PUBLICATIONS_AND_IP.md     # Manuscript status, patents, DOIs
|-- requirements.txt
|-- setup.py
|
|-- bpf/                          # Core BPF pipeline
|   |-- __init__.py
|   |-- pipeline.py               # BPF v1.0.0 locked canonical pipeline
|   |-- pipeline_v2.py            # BPF v2.0 (full dataset, no CV)
|   |-- ranking.py                # Univariate AUC ranking with direction tracking
|   |-- selection.py              # Adaptive gene selection
|   |-- fusion.py                 # AUC-weighted z-score fusion
|   |-- evaluation.py             # Bootstrap CI, risk stratification
|   `-- utils.py                  # Preprocessing, I/O, gene mapping
|
|-- scripts/                      # Execution scripts
|   |-- run_single_cohort.py      # Process a single dataset
|   |-- run_batch.py              # Batch processing across multiple datasets
|   `-- run_cross_validation.py   # 5x5 repeated stratified k-fold
|
|-- configs/                      # Parameter configurations
|   |-- default_params.yaml       # Default BPF parameters
|   |-- oncology_params.yaml      # Phase 1 oncology configuration
|   |-- alzheimer_params.yaml     # Phase 2 AD configuration
|   `-- parkinson_params.yaml     # Phase 3 PD configuration
|
|-- data/                         # Sample data for testing
|   `-- sample_expression.csv     # Small synthetic dataset for CI/CD
|
|-- tests/                        # Unit and integration tests
|   |-- test_ranking.py
|   |-- test_selection.py
|   |-- test_fusion.py
|   |-- test_pipeline.py
|   `-- test_reproducibility.py   # Determinism verification (seed=42)
|
|-- results/                      # Output directory (gitignored except examples)
|   `-- example_output/
|       |-- DATA.json
|       |-- DETAILED_STATS.txt
|       |-- EXECUTIVE_SUMMARY.txt
|       |-- FULL_AUC_RANKING.txt
|       |-- GENE_PANEL.txt
|       `-- SAMPLES.txt
|
`-- docs/
    |-- METHODS.md                # Detailed methodology documentation
    |-- PARAMETERS.md             # Parameter reference
    |-- OUTPUT_FORMAT.md          # Output file specifications
    `-- VALIDATION.md             # External validation summary
```

---

## Installation

```bash
git clone https://github.com/pulselogicbio/pulselogic-bpf.git
cd pulselogic-bpf
pip install -r requirements.txt
```

### Requirements

- Python >= 3.11
- NumPy >= 1.21
- Pandas >= 1.3
- Scikit-learn >= 1.0
- SciPy >= 1.7

---

## Quick Start

```python
from bpf import BPFPipeline

# Initialize with default parameters
pipeline = BPFPipeline(
    min_auc=0.55,
    pvalue_threshold=0.05,
    max_genes=100,
    variance_threshold=0.01,
    seed=42
)

# Load expression data (genes x samples) and binary outcome
X, y = pipeline.load_data("expression_matrix.tsv", "clinical_data.tsv")

# Run full pipeline
results = pipeline.run(X, y, cohort_name="MY_COHORT")

# Run with cross-validation
cv_results = pipeline.run_cv(X, y, n_splits=5, n_repeats=5)

# Save all 6 output files
pipeline.save_results(results, output_dir="results/MY_COHORT/")
```

---

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| min_auc | 0.55 | Minimum univariate AUC for gene inclusion |
| pvalue_threshold | 0.05 | Maximum Mann-Whitney p-value for gene inclusion |
| max_genes | 100 | Maximum genes in the fusion panel |
| variance_threshold | 0.01 | Minimum variance for gene retention |
| seed | 42 | Random seed for reproducibility |
| n_splits | 5 | Number of CV folds |
| n_repeats | 5 | Number of CV repeats |
| n_bootstrap | 1000 | Bootstrap resamples for confidence intervals |

---

## Output Files

Each BPF run produces 6 standardized output files:

| File | Description |
|------|-------------|
| DATA.json | Complete results in machine-readable format |
| DETAILED_STATS.txt | Full statistical report |
| EXECUTIVE_SUMMARY.txt | One-page summary with key metrics |
| FULL_AUC_RANKING.txt | All genes ranked by univariate AUC |
| GENE_PANEL.txt | Selected biomarker panel with directions |
| SAMPLES.txt | Per-patient BPF scores and risk groups |

---

## Reproducibility

BPF is fully deterministic. Given the same input data, parameters, and seed, the
pipeline produces identical results. This is verified by `test_reproducibility.py`
which checks bit-for-bit output consistency.

The locked canonical pipeline (BPF_LOCKED_PIPELINE_v1.py) is version-controlled
and hash-verified via PIPELINE_AUDIT.json.

- **Random seed:** 42 (all stochastic operations)
- **Pipeline version:** v1.0.0 (locked February 11, 2026)
- **Input verification:** SHA-256 checksums on all expression and survival files

---

## Citation

Please cite this work as:

```bibtex
@article{dowden2026bpf,
  title={A stability-governed, tuning-free framework for feature selection
         in high-dimensional transcriptomic biomarker discovery},
  author={Dowden, Christopher B.},
  journal={Bioinformatics},
  year={2026},
  note={Submitted. Manuscript ID: BIOINF-2026-0795}
}
```

Software citation (for reproducibility artifacts):

```bibtex
@software{dowden2026bpfcode,
  title={PulseLogic BPF: Biomarker Probability Fusion Pipeline},
  author={Dowden, Christopher B.},
  year={2026},
  url={https://github.com/pulselogicbio/pulselogic-bpf},
  doi={10.5281/zenodo.19342790},
  version={1.0.1}
}
```

Alternatively, click the "Cite this repository" button (top-right of this page)
to auto-generate citations from CITATION.cff.

---

## Intellectual Property

Provisional patent: US 63/942,422 (filed December 2025) -- BPF methodology and
multi-modal fusion framework. All IP assigned to PulseLogic Biosciences Inc.
Methodology implementation is proprietary. This repository presents the research
artifact companion to the submitted manuscript.

---

## Author

**Christopher B. Dowden**
Founder & CEO, PulseLogic Biosciences Inc.
ceo@pulselogic.bio | ORCiD: 0009-0008-5690-3723

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Disclaimer

Research software. Not for clinical decision-making. Not FDA cleared or approved.
