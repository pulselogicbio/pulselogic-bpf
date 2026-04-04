# Benchmark Summary -- BPF v2.3

**PulseLogic Biosciences Inc. | BPF Benchmark v2.3**
**23 Cohorts | 19,038 Patients | 19 Cancer Types**

This file summarizes the results of BPF Benchmark v2.3, comparing BPF against
four baseline methods under frozen, identical cross-validation splits.

Manuscript: BIOINF-2026-0795 (Bioinformatics, Oxford) -- under review.

---

## Benchmark Design

| Parameter | Value |
|-----------|-------|
| Cohorts | 23 independent cohorts |
| Patients | 19,038 |
| Cancer types | 19 |
| Sources | METABRIC, 5 GEO, 17 ICGC |
| CV scheme | 5x5 repeated stratified k-fold (frozen splits) |
| Random seed | 42 (deterministic) |
| Split parity | All methods receive identical splits |
| Feature input | Identical per method |
| Execution date | February 2026 |

---

## Baseline Comparators

| Method | Type |
|--------|------|
| LASSO | L1-regularized logistic regression |
| ElasticNet | L1+L2 regularized logistic regression |
| RF_Importance | Random Forest with importance-based selection |
| RF_native | Random Forest native classifier |

All baselines use identical CV splits, identical feature input, and identical
evaluation metrics as BPF.

---

## Head-to-Head Results

| Comparison | Wins | Ties | Losses | p-value | Mean AUC Advantage |
|------------|------|------|--------|---------|-------------------|
| BPF vs. LASSO | 10 | 3 | 2 | 0.011 | +0.0255 |
| BPF vs. ElasticNet | 7 | 6 | 2 | 0.011 | +0.0209 |
| BPF vs. RF_native | 7 | 1 | 7 | 0.903 | parity |

Win = BPF exceeds baseline by >0.02 AUC.
Loss = baseline exceeds BPF by >0.02 AUC.
Tie = absolute difference <= 0.02 AUC.

BPF is statistically superior to LASSO and ElasticNet (p=0.011 each).
BPF achieves statistical parity with Random Forest (p=0.903).

---

## Gene Signature Stability

A key differentiator of BPF is gene panel stability across cross-validation folds.

| Method | Mean Jaccard Stability |
|--------|----------------------|
| BPF | 0.281 |
| LASSO | 0.164 |
| ElasticNet | 0.051 |
| RF_Importance | 0.089 |

Higher Jaccard = more consistent gene panel across folds.
BPF produces 1.7x -- 5.5x more stable gene signatures than all baselines.
Stable gene panels are essential for clinical translation and regulatory review.

---

## Runtime Comparison

| Method | Mean Runtime |
|--------|-------------|
| BPF | 5.4 minutes |
| LASSO | 5.7 minutes |
| ElasticNet | 6.2 minutes |
| RF_Importance | 11.9 hours |
| RF_native | 8.3 hours |

BPF runs in minutes, not hours. 63x faster than RF_Importance on identical hardware.
Runtime advantage scales with cohort size and feature dimensionality.

---

## Practical Significance Threshold

| Result | Definition |
|--------|------------|
| Win | BPF exceeds baseline by > 0.02 AUC |
| Loss | Baseline exceeds BPF by > 0.02 AUC |
| Tie | Absolute difference <= 0.02 AUC |

The 0.02 AUC practical significance threshold follows established biomarker
benchmarking conventions. Statistical significance alone (p-value) is insufficient
for clinical relevance assessment.

---

## Benchmark Cohorts

23 cohorts from METABRIC, GEO, and ICGC spanning 19 cancer types.
All cohorts are independent from the Phase 1 TCGA training portfolio.
Full cohort list and per-cohort results are available in the companion manuscript
(BIOINF-2026-0795).

---

## Reproducibility

All benchmark results are fully reproducible:
- Frozen CV splits serialized and archived before execution
- Random seed: 42
- All outputs hash-verified via SHA-256
- Per-cohort checkpoint files archived

---

## Manuscript Status

**Submitted:** Bioinformatics (Oxford Academic)
**Manuscript ID:** BIOINF-2026-0795
**Submitted:** March 25, 2026
**Status:** Under peer review

**Preprint:** bioRxiv accession BIORXIV/2026/713505 (in screening)

**Software DOI:** 10.5281/zenodo.19342790 (Zenodo, v1.0.1)

---

*PulseLogic Biosciences Inc. | ceo@pulselogic.bio | https://pulselogic.bio*
