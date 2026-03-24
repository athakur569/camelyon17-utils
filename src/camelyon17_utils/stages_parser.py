"""Parse CAMELYON17 stages.csv into a structured DataFrame."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# stages.csv columns: patient, node0, node1, node2, node3, node4
# Each node column: negative / macro / micro / itc
# Patient-level: pN0 (no metastasis) / pN1mi / pN1 / pN2


class StagesParser:
    """Load and parse CAMELYON17 stages.csv.

    Args:
        stages_csv: Path to the official stages.csv file.
        slide_dir:  Optional path to the slide directory for path resolution.
    """

    SLIDE_LABELS = {"negative": 0, "itc": 1, "micro": 1, "macro": 1}
    PATIENT_LABELS = {"pN0": 0, "pN1mi": 1, "pN1": 1, "pN2": 1}

    def __init__(self, stages_csv: str | Path, slide_dir: str | Path | None = None) -> None:
        self.stages_csv = Path(stages_csv)
        self.slide_dir = Path(slide_dir) if slide_dir else None

    def load(self) -> pd.DataFrame:
        """Load stages.csv and return a tidy slide-level DataFrame.

        Returns:
            DataFrame with columns: patient_id, center, node_id, slide_id,
            stage_label (original), binary_label, patient_label.
        """
        raw = pd.read_csv(self.stages_csv)
        rows = []
        for _, row in raw.iterrows():
            patient_id = str(row["patient"])
            # patient_id encodes center: patient_0xx → center 1, etc.
            center = self._infer_center(patient_id)
            patient_label = str(row.get("stage", "pN0"))

            for node_idx in range(5):
                col = f"node_{node_idx}"
                if col not in row or pd.isna(row[col]):
                    continue
                stage = str(row[col]).strip().lower()
                slide_id = f"patient_{int(patient_id):03d}_node_{node_idx}"
                rows.append({
                    "patient_id": patient_id,
                    "center": center,
                    "node_id": node_idx,
                    "slide_id": slide_id,
                    "stage_label": stage,
                    "binary_label": self.SLIDE_LABELS.get(stage, 0),
                    "patient_label_raw": patient_label,
                    "patient_binary": self.PATIENT_LABELS.get(patient_label, 0),
                })
        return pd.DataFrame(rows)

    @staticmethod
    def _infer_center(patient_id: str) -> int:
        """Infer center (1–5) from patient ID (0-indexed 100-patient blocks)."""
        try:
            pid = int(patient_id)
            return (pid // 100) + 1
        except ValueError:
            return -1
