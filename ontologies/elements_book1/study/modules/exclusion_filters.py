"""Helpers for filtering SPARQL results by excluded IRIs."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import pandas as pd


def _normalize_iri(value: object) -> str:
    text = str(value).strip()
    if text.startswith("<") and text.endswith(">"):
        text = text[1:-1].strip()
    return text


def normalize_excluded_iris(excluded: Iterable[object] | None) -> set[str]:
    if not excluded:
        return set()
    normalized = {_normalize_iri(value) for value in excluded}
    return {value for value in normalized if value}


def filter_excluded_rows(
    df: pd.DataFrame,
    excluded: set[str] | None,
    *,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Drop rows where any specified column matches an excluded IRI."""
    if df.empty or not excluded:
        return df
    excluded_normalized = normalize_excluded_iris(excluded)
    if not excluded_normalized:
        return df
    if any(column not in df.columns for column in columns):
        return df
    mask = pd.Series(True, index=df.index)
    for column in columns:
        normalized = df[column].map(_normalize_iri)
        mask &= ~normalized.isin(excluded_normalized)
    return df.loc[mask].copy()
