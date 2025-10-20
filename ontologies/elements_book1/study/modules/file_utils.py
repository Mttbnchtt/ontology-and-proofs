"""Utilities for persisting study analyses to timestamped CSV files."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import datetime
import pandas as pd


def ensure_subdir(subdir: str | Path = "output") -> Path:
    """Return a subdirectory within the folder, creating it if necessary."""
    base_dir = Path(__file__).resolve().parent.parent
    target_dir = base_dir / Path(subdir)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def _resolve_output_dir(path_like: str | Path) -> Path:
    """Return an absolute directory, creating it if necessary."""
    candidate = Path(path_like)
    if candidate.is_absolute():
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate
    return ensure_subdir(candidate)


def write_csv(
    iris_df: pd.DataFrame,
    *,
    filename: str = "concepts.csv",
    output_dir: str | Path = "ontologies",
) -> Path:
    """Persist an iris DataFrame to CSV within the study folder."""
    target_dir = _resolve_output_dir(output_dir)
    output_path = target_dir / filename
    iris_df.to_csv(output_path, index=False)
    print(f"Saved iris to {output_path}")
    return output_path


def output_df(analyses: Sequence[Sequence[str]], filename: str = "output/analyses") -> pd.DataFrame:
    analyses_df = pd.DataFrame(analyses, columns=["proof_number", "background_concepts", "diff"])
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{t}.csv"
    analyses_df.to_csv(filename, index=False)
    print(f"Output: {filename}")
    return analyses_df
