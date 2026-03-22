\# BPF Benchmark — Reproducibility Guide



\*\*Manuscript:\*\* "A stability-governed, tuning-free framework for feature selection  

in high-dimensional transcriptomic biomarker discovery"  

\*\*Author:\*\* Christopher B. Dowden, PulseLogic Biosciences Inc.  

\*\*ORCiD:\*\* 0009-0008-5690-3723  

\*\*Contact:\*\* ceo@pulselogic.bio  



\---



\## Purpose of this document



This guide maps every numerical result in the manuscript to the file(s) 

in this repository that produced it. A reviewer or reader should be able 

to verify any reported number by following the steps below.



\---



\## Directory structure

```

benchmark/

&#x20; splits/                  ← Frozen CV split files (one JSON per cohort)

&#x20; results/                 ← Pre-computed outputs matching manuscript tables

&#x20; checkpoints/             ← Fold-level checkpoint files (optional, for reruns)

&#x20; run\_benchmark.py         ← Main benchmark runner

&#x20; README.md                ← This file

```



\---



\## Frozen splits



All cross-validation splits were generated \*\*once\*\* before any method ran, 

using the following procedure:

```python

from sklearn.model\_selection import RepeatedStratifiedKFold

import numpy as np, json



rskf = RepeatedStratifiedKFold(n\_splits=5, n\_repeats=5, random\_state=42)

splits = \[]

for train\_idx, test\_idx in rskf.split(X, y):

&#x20;   splits.append({

&#x20;       "train": train\_idx.tolist(),

&#x20;       "test":  test\_idx.tolist()

&#x20;   })

with open(f"{cohort}\_splits.json", "w") as f:

&#x20;   json.dump(splits, f)

```



Split files are stored in `benchmark/splits/`. Each file contains exactly 

25 fold definitions. The same file was used for all five methods (BPF, LASSO, 

ElasticNet, RF\_Importance, RF\_native), ensuring that any observed performance 

difference reflects feature selection quality rather than sampling variation.



\---



\## Verifying manuscript numbers



\### Table 1 — Per-cohort mean AUC



Source file: `benchmark/results/per\_cohort\_auc.csv`



Columns: `cohort, method, mean\_auc, std\_auc, ci\_low, ci\_high`



To verify a specific value — e.g., BPF AUC on METABRIC:

```python

import pandas as pd

df = pd.read\_csv("benchmark/results/per\_cohort\_auc.csv")

print(df\[(df.cohort == "METABRIC") \& (df.method == "BPF")]\["mean\_auc"].values)

\# Expected: 0.6676

```



\### Table 2 — Jaccard stability



Source file: `benchmark/results/per\_cohort\_jaccard.csv`



Columns: `cohort, method, mean\_jaccard`

```python

df = pd.read\_csv("benchmark/results/per\_cohort\_jaccard.csv")

print(df\[(df.cohort == "METABRIC") \& (df.method == "BPF")]\["mean\_jaccard"].values)

\# Expected: 0.498

```



\### Table 3 — Cross-tier aggregate



Source file: `benchmark/results/aggregate\_summary.csv`



Pre-computed from Table 1 by averaging across powered cohorts within each tier. 

Exploratory cohorts excluded: GBM-US, THCA-US, PAAD-US, GSE31684.



\### Table 4 — Runtime



Source file: `benchmark/results/runtime\_summary.csv`



Columns: `cohort, method, runtime\_seconds`



Runtimes were measured on a single-node CPU environment. 

Exact values will vary by hardware; the speedup ratios (BPF vs LASSO/ENet) 

are the reproducible quantity.



\---



\## Re-running the benchmark



> ⚠️ Full re-run is computationally intensive.  

> LASSO and ElasticNet require 6–37 hours per cohort.  

> BPF requires 5–9 minutes per cohort.  

> Pre-computed results in `benchmark/results/` match the manuscript exactly.



\### Step 1 — Obtain expression data



Download cohort expression matrices from their public sources 

(see main README for links). Align sample identifiers to the 

split index files.



\### Step 2 — Configure cohort paths



Edit `configs/cohort\_paths.yaml` to point to your local data files:

```yaml

METABRIC:

&#x20; expression: /path/to/METABRIC\_expression.csv

&#x20; clinical:   /path/to/METABRIC\_clinical.csv

&#x20; outcome\_col: OS\_event

```



\### Step 3 — Run

```bash

\# Single cohort, all methods

python benchmark/run\_benchmark.py \\

&#x20; --cohort METABRIC \\

&#x20; --splits benchmark/splits/METABRIC\_splits.json \\

&#x20; --output benchmark/results/



\# BPF only (fast verification)

python benchmark/run\_benchmark.py \\

&#x20; --cohort METABRIC \\

&#x20; --methods bpf \\

&#x20; --splits benchmark/splits/METABRIC\_splits.json

```



\### Step 4 — Verify outputs

```bash

python benchmark/verify\_results.py \\

&#x20; --results benchmark/results/ \\

&#x20; --reference benchmark/results/

```



This script computes the difference between your re-run outputs 

and the pre-computed reference values. Any discrepancy beyond 

floating-point tolerance indicates a configuration mismatch.



\---



\## What is and is not in this repository



| Included | Not included |

|---|---|

| Frozen CV split indices (JSON) | Raw expression matrices (too large; publicly available) |

| Pre-computed results (CSV) | Proprietary WRF methodology internals |

| BPF feature selection implementation | Disease-specific commercial panels |

| Benchmark runner script | Internal research assets |

| Verification script | |



\---



\## Determinism guarantee



Given:

\- The same frozen split file

\- The same expression matrix (identical sample ordering)

\- Python 3.11, scikit-learn 1.3, numpy 1.24, pandas 2.0



The BPF results in `benchmark/results/` are exactly reproducible 

to floating-point precision. LASSO and ElasticNet results depend 

additionally on the LAPACK/BLAS implementation and may show 

negligible numerical variation across platforms while remaining 

statistically identical.



\---



\## Version



Benchmark pipeline: v2.3  

Splits generated: March 2026  

Seed: 42  

Archive ID: BPF-BENCH-2026-v2.3

```



\---



\*\*3. Folder structure to create on GitHub\*\*

```

benchmark/

&#x20; splits/

&#x20;   METABRIC\_splits.json

&#x20;   GSE68465\_LUAD\_splits.json

&#x20;   GSE15459\_STAD\_splits.json

&#x20;   GSE37745\_LUNG\_splits.json

&#x20;   GSE31684\_BLCA\_splits.json

&#x20;   GSE2990\_BRCA\_splits.json

&#x20;   ICGC\_BLCA-US\_splits.json

&#x20;   ICGC\_BRCA-US\_splits.json

&#x20;   \[... remaining 15 ICGC cohorts]

&#x20; results/

&#x20;   per\_cohort\_auc.csv

&#x20;   per\_cohort\_jaccard.csv

&#x20;   aggregate\_summary.csv

&#x20;   runtime\_summary.csv

&#x20; checkpoints/

&#x20;   .gitkeep

&#x20; REPRODUCIBILITY.md

&#x20; run\_benchmark.py

&#x20; verify\_results.py

