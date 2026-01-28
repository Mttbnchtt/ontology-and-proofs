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


def normalize_excluded_substrings(excluded: Iterable[object] | None) -> tuple[str, ...]:
    if not excluded:
        return tuple()
    normalized = tuple(_normalize_iri(value) for value in excluded)
    return tuple(value for value in normalized if value)


def _looks_like_iri(value: str) -> bool:
    return value.startswith(("http://", "https://", "urn:"))


def filter_excluded_rows(
    df: pd.DataFrame,
    excluded: set[str] | None,
    *,
    columns: Sequence[str],
    excluded_substrings: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Drop rows where any specified column matches an excluded IRI.

    Assumes SPARQL bindings for the specified columns are IRIs; literals are stringified
    and only excluded if they exactly match an excluded IRI. Filtering is skipped when
    required columns are missing. Substring filtering drops rows whose IRIs contain any
    excluded substring.
    """
    if df.empty or (not excluded and not excluded_substrings):
        return df
    excluded_normalized = normalize_excluded_iris(excluded)
    excluded_substrings_normalized = normalize_excluded_substrings(excluded_substrings)
    if not excluded_normalized and not excluded_substrings_normalized:
        return df
    if any(column not in df.columns for column in columns):
        return df
    mask = pd.Series(True, index=df.index)
    for column in columns:
        normalized = df[column].map(_normalize_iri)
        if excluded_normalized:
            mask &= ~normalized.isin(excluded_normalized)
        if excluded_substrings_normalized:
            mask &= ~normalized.apply(
                lambda value: any(
                    substring in value for substring in excluded_substrings_normalized
                )
                if _looks_like_iri(value)
                else False
            )
    return df.loc[mask].copy()
