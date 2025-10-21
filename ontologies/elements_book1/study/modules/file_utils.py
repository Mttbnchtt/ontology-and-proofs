"""Utilities for persisting study analyses to timestamped CSV files."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import datetime
import pandas as pd


def ensure_subdir(subdir: str | Path = "output") -> Path:
    """Return a subdirectory within the folder, creating it if necessary."""
    base_dir = Path(__file__).resolve().parent.parent
    target_dir = base_dir / Path(subdir)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def lates_file(
    folder: str | Path = "ontologies",
    filename_fragment: str = "ontology_",
) -> Optional[Path]:
    """Return the most recent file within the study folder, if any."""
    base_dir = Path(__file__).resolve().parent.parent
    target_dir = base_dir / Path(folder)
    if not target_dir.exists():
        raise FileNotFoundError("No file found in the study ontologies folder.")

    latest_path: Optional[Path] = None
    latest_timestamp: Optional[datetime.datetime] = None
    pattern = f"{filename_fragment}*"
    for candidate in target_dir.glob(pattern):
        if not candidate.is_file():
            continue
        stem = candidate.stem
        if not stem.startswith(filename_fragment):
            continue
        timestamp = stem[len(filename_fragment) :]
        try:
            candidate_ts = datetime.datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        except ValueError:
            continue
        if latest_timestamp is None or candidate_ts > latest_timestamp:
            latest_timestamp = candidate_ts
            latest_path = candidate
    if latest_path is None:
        raise FileNotFoundError("No file found in the study ontologies folder.")
    return latest_path


def write_csv(
    iris_df: pd.DataFrame,
    *,
    filename: str = "concepts.csv",
    output_dir: str | Path = "ontologies",
) -> Path:
    """Persist an iris DataFrame to CSV within the study folder."""
    target_dir = ensure_subdir(output_dir)
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
