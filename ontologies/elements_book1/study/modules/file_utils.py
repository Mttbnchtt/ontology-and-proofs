"""Utilities for persisting study analyses to timestamped CSV files."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import datetime
import pandas as pd


def ensure_study_subdir(subdir: str | Path = "output") -> Path:
    """Return a subdirectory within the study folder, creating it if necessary."""
    base_dir = Path(__file__).resolve().parent.parent
    target_dir = base_dir / Path(subdir)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def output_df(analyses: Sequence[Sequence[str]], filename: str = "output/analyses") -> pd.DataFrame:
    analyses_df = pd.DataFrame(analyses, columns=["proof_number", "background_concepts", "diff"])
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{t}.csv"
    analyses_df.to_csv(filename, index=False)
    print(f"Output: {filename}")
    return analyses_df
