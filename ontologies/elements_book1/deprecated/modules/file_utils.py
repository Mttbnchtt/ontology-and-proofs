"""Utilities for persisting study analyses to timestamped CSV files.

Limitations:
- Assumes the output directory already exists and is writable; no path creation is attempted.
- Expects each analysis dict/tuple to match the hard-coded column order when building the DataFrame.
"""

from typing import Sequence

import datetime
import pandas as pd

def output_df(analyses: Sequence[Sequence[str]], filename: str = "output/analyses") -> pd.DataFrame:
    analyses_df = pd.DataFrame(analyses, columns=["proof_number", "background_concepts", "diff"])
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{t}.csv"
    analyses_df.to_csv(filename, index=False)
    print(f"Output: {filename}")
    return analyses_df
