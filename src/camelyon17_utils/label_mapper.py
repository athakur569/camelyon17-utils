"""Label normalization utilities for CAMELYON17."""

from __future__ import annotations

import pandas as pd

_BINARY_MAP = {
    "negative": 0,
    "itc": 1,
    "micro": 1,
    "macro": 1,
    "pN0": 0,
    "pN1mi": 1,
    "pN1": 1,
    "pN2": 1,
    0: 0, 1: 1,
}


def binarize_labels(
    df: pd.DataFrame,
    label_col: str = "stage_label",
    out_col: str = "binary_label",
) -> pd.DataFrame:
    """Map CAMELYON17 stage labels to binary (0=negative, 1=any metastasis).

    Handles both slide-level (negative/itc/micro/macro) and
    patient-level (pN0/pN1mi/pN1/pN2) labels.
    """
    df = df.copy()
    df[out_col] = df[label_col].str.strip().str.lower().map(
        {k.lower() if isinstance(k, str) else k: v for k, v in _BINARY_MAP.items()}
    )
    n_unmapped = df[out_col].isna().sum()
    if n_unmapped > 0:
        unique_unmapped = df.loc[df[out_col].isna(), label_col].unique()
        raise ValueError(
            f"{n_unmapped} labels could not be mapped: {unique_unmapped}. "
            "Add them to _BINARY_MAP."
        )
    return df
