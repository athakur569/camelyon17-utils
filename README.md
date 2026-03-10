# camelyon17-utils

Utilities for the CAMELYON17 lymph node metastasis detection dataset: parse `stages.csv`, create center-disjoint train/val/test splits, and normalize slide-level labels.

## Features
- Parse `stages.csv` — slide-level (negative/macro/micro/itc) and patient-level (pN0/pN1/pN2) labels
- Center-disjoint splits: 5 centers × 100 patients; hold out 1–2 centers for test
- Binary label normalization: negative=0, any metastasis=1 (consistent with TCGA)
- Patient-level split verification (no patient across splits)

## Installation
```bash
pip install camelyon17-utils
```

## Quick start
```python
from camelyon17_utils import StagesParser, CenterSplitter

parser = StagesParser("data/camelyon17/stages.csv")
df = parser.load()

splitter = CenterSplitter(test_centers=[4, 5], val_centers=[3])
splits = splitter.split(df)
print(splits.keys())  # train, val, test
```

## License
MIT
