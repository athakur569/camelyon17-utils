"""Center-disjoint train/val/test splits for CAMELYON17."""

from __future__ import annotations

import pandas as pd


class CenterSplitter:
    """Split a CAMELYON17 slide DataFrame by center assignment.

    Centers 1–5 contain 100 patients each. Assigning disjoint centers to
    each split prevents site leakage and tests cross-center generalization.

    Args:
        test_centers:  Center IDs held out for testing (e.g. [4, 5]).
        val_centers:   Center IDs used for validation (e.g. [3]).
        label_col:     Column used for positive-count verification.
    """

    def __init__(
        self,
        test_centers: list[int] | None = None,
        val_centers: list[int] | None = None,
        label_col: str = "binary_label",
    ) -> None:
        self.test_centers = test_centers or [5]
        self.val_centers = val_centers or [4]
        self.label_col = label_col

    def split(self, df: pd.DataFrame, center_col: str = "center") -> dict[str, pd.DataFrame]:
        """Return {'train': df, 'val': df, 'test': df}."""
        test_mask = df[center_col].isin(self.test_centers)
        val_mask = df[center_col].isin(self.val_centers)
        train_mask = ~(test_mask | val_mask)

        splits = {
            "train": df[train_mask].copy(),
            "val": df[val_mask].copy(),
            "test": df[test_mask].copy(),
        }

        self._verify(splits)
        return splits

    def _verify(self, splits: dict[str, pd.DataFrame]) -> None:
        for name, df in splits.items():
            n_pos = int((df[self.label_col] == 1).sum()) if self.label_col in df else 0
            n = len(df)
            if n == 0:
                raise ValueError(f"Split '{name}' is empty — check center assignments")
            if n_pos == 0:
                raise ValueError(
                    f"Split '{name}' has no positive cases — "
                    "choose different center assignments or use slide-level labels"
                )
            print(f"  {name:6s}: {n} slides, {n_pos} positives ({100*n_pos/n:.1f}%)")
