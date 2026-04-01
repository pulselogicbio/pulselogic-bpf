# Biomarker Probability Fusion (BPF)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19342790.svg)](https://doi.org/10.5281/zenodo.19342790)
[![License](https://img.shields.io/badge/License-See%20LICENSE-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0008--5690--3723-brightgreen.svg)](https://orcid.org/0009-0008-5690-3723)

**A disease-agnostic biomarker discovery and risk stratification framework for precision medicine.**

Developed by [PulseLogic Biosciences Inc.](https://pulselogic.bio) under the discipline of Computational Bio-AI Engineering (CBAE).

---

## Overview

Biomarker Probability Fusion (BPF) is a deterministic, auditable pipeline for multi-modal biomarker fusion and patient risk stratification. BPF performs:

1. **Univariate biomarker ranking** â€” AUC-based discriminative power assessment with direction tracking for each gene/feature
2. **Adaptive gene selection** â€” Statistical filtering (AUC threshold + p-value) with configurable panel size
3. **Weighted score fusion** â€” AUC-weighted z-score composition with direction correction
4. **Risk stratification** â€” Probabilistic patient scoring with bootstrap confidence intervals
5. **Cross-validation** â€” 5Ã—5 repeated stratified k-fold with complete within-fold feature selection (no information leakage)

BPF is disease-agnostic: the same algorithm and parameters have been validated across oncology, Alzheimer's disease, and Parkinson's disease without domain-specific modifications.

## Validation Summary

| Domain | Training | External Datasets | External Patients | External AUC |
|--------|----------|-------------------|-------------------|--------------|
| Oncology | TCGA (39 cohorts) | 41 | 14,498 | 0.8029 |
| Alzheimer's Disease | ADNI | 7 | 2,892 | ~0.81 |
| Parkinson's Disease | PPMI | 8 | 753 | 0.793 |
| **Total** | | **56** | **18,143** | |

56 independent external datasets. 18,143 patients. Three disease domains. 100% statistically significant.

## Repository Structure

```
bpf-pipeline/
â”œâ”€â”€ README.md
â”œâ”€â”€ LICENSE
â”œâ”€â”€ CITATION.cff
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ setup.py
â”‚
â”œâ”€â”€ bpf/                          # Core BPF pipeline
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ pipeline.py               # BPF v1.0.0 locked canonical pipeline
â”‚   â”œâ”€â”€ pipeline_v2.py            # BPF v2.0 (full dataset, no CV)
â”‚   â”œâ”€â”€ ranking.py                # Univariate AUC ranking with direction tracking
â”‚   â”œâ”€â”€ selection.py              # Adaptive gene selection
â”‚   â”œâ”€â”€ fusion.py                 # AUC-weighted z-score fusion
â”‚   â”œâ”€â”€ evaluation.py             # Bootstrap CI, risk stratification
â”‚   â””â”€â”€ utils.py                  # Preprocessing, I/O, gene mapping
â”‚
â”œâ”€â”€ scripts/                      # Execution scripts
â”‚   â”œâ”€â”€ run_single_cohort.py      # Process a single dataset
â”‚   â”œâ”€â”€ run_batch.py              # Batch processing across multiple datasets
â”‚   â””â”€â”€ run_cross_validation.py   # 5Ã—5 repeated stratified k-fold
â”‚
â”œâ”€â”€ configs/                      # Parameter configurations
â”‚   â”œâ”€â”€ default_params.yaml       # Default BPF parameters
â”‚   â”œâ”€â”€ oncology_params.yaml      # Phase 1 oncology configuration
â”‚   â”œâ”€â”€ alzheimer_params.yaml     # Phase 2 AD configuration
â”‚   â””â”€â”€ parkinson_params.yaml     # Phase 3 PD configuration
â”‚
â”œâ”€â”€ data/                         # Sample data for testing
â”‚   â””â”€â”€ sample_expression.csv     # Small synthetic dataset for CI/CD
â”‚
â”œâ”€â”€ tests/                        # Unit and integration tests
â”‚   â”œâ”€â”€ test_ranking.py
â”‚   â”œâ”€â”€ test_selection.py
â”‚   â”œâ”€â”€ test_fusion.py
â”‚   â”œâ”€â”€ test_pipeline.py
â”‚   â””â”€â”€ test_reproducibility.py   # Determinism verification (seed=42)
â”‚
â”œâ”€â”€ results/                      # Output directory (gitignored except examples)
â”‚   â””â”€â”€ example_output/
â”‚       â”œâ”€â”€ DATA.json
â”‚       â”œâ”€â”€ DETAILED_STATS.txt
â”‚       â”œâ”€â”€ EXECUTIVE_SUMMARY.txt
â”‚       â”œâ”€â”€ FULL_AUC_RANKING.txt
â”‚       â”œâ”€â”€ GENE_PANEL.txt
â”‚       â””â”€â”€ SAMPLES.txt
â”‚
â””â”€â”€ docs/
    â”œâ”€â”€ METHODS.md                # Detailed methodology documentation
    â”œâ”€â”€ PARAMETERS.md             # Parameter reference
    â”œâ”€â”€ OUTPUT_FORMAT.md          # Output file specifications
    â””â”€â”€ VALIDATION.md             # External validation summary
```

## Installation

```bash
git clone https://github.com/pulselogicbio/bpf-pipeline.git
cd bpf-pipeline
pip install -r requirements.txt
```

### Requirements

- Python >= 3.11
- NumPy â‰¥ 1.21
- Pandas â‰¥ 1.3
- Scikit-learn â‰¥ 1.0
- SciPy â‰¥ 1.7
- XGBoost â‰¥ 1.5 (optional, for ML-optimized weights)

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

# Load expression data (genes Ã— samples) and binary outcome
X, y = pipeline.load_data("expression_matrix.tsv", "clinical_data.tsv")

# Run full pipeline
results = pipeline.run(X, y, cohort_name="MY_COHORT")

# Run with cross-validation
cv_results = pipeline.run_cv(X, y, n_splits=5, n_repeats=5)

# Save all 6 output files
pipeline.save_results(results, output_dir="results/MY_COHORT/")
```

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_auc` | 0.55 | Minimum univariate AUC for gene inclusion |
| `pvalue_threshold` | 0.05 | Maximum Mann-Whitney p-value for gene inclusion |
| `max_genes` | 100 | Maximum genes in the fusion panel |
| `variance_threshold` | 0.01 | Minimum variance for gene retention |
| `seed` | 42 | Random seed for reproducibility |
| `n_splits` | 5 | Number of CV folds |
| `n_repeats` | 5 | Number of CV repeats |
| `n_bootstrap` | 1000 | Bootstrap resamples for confidence intervals |

## Output Files

Each BPF run produces 6 standardized output files:

| File | Description |
|------|-------------|
| `DATA.json` | Complete results in machine-readable format |
| `DETAILED_STATS.txt` | Full statistical report |
| `EXECUTIVE_SUMMARY.txt` | One-page summary with key metrics |
| `FULL_AUC_RANKING.txt` | All genes ranked by univariate AUC |
| `GENE_PANEL.txt` | Selected biomarker panel with directions |
| `SAMPLES.txt` | Per-patient BPF scores and risk groups |

## Reproducibility

BPF is fully deterministic. Given the same input data, parameters, and seed, the pipeline produces identical results. This is verified by `test_reproducibility.py` which checks bit-for-bit output consistency.

The locked canonical pipeline (`BPF_LOCKED_PIPELINE_v1.py`) is version-controlled and hash-verified via `PIPELINE_AUDIT.json`.
## Citation

Please cite this work as:
```bibtex
@article{dowden2026bpf,
  title={A stability-governed, tuning-free framework for feature selection in high-dimensional transcriptomic biomarker discovery},
  author={Dowden, Christopher B.},
  journal={Bioinformatics},
  year={2026},
  note={Submitted. Manuscript ID: BIOINF-2026-0795}
}
```

**Software citation (for reproducibility artifacts):**
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

Alternatively, click the **"Cite this repository"** button (top-right of this GitHub page) to auto-generate citations from CITATION.cff.
