"""Context construction for typical activation potential."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

from . import queries
from .query_runner import QueryRunner
from .exclusion_filters import filter_excluded_rows
from .typical_helpers import iri_for_proof, iri_for_proposition

def _iris_for_context(proof_n: int) -> list[str]:
    propositions = [iri_for_proposition(i) for i in range(1, proof_n + 1)]
    proofs = [iri_for_proof(i) for i in range(1, proof_n)]
    return propositions + proofs


def _values_clause(values: Iterable[str]) -> str | None:
    tokens = [value for value in values if value]
    if not tokens:
        return None
    return " ".join(tokens)


def _fetch_sum_links(
    runner: QueryRunner,
    queries_to_run: Iterable[str],
    *,
    excluded_iris: set[str] | None,
    excluded_substrings: list[str] | None,
) -> pd.DataFrame:
    frames = []
    for query in queries_to_run:
        df = runner.fetch(query)
        df = filter_excluded_rows(
            df,
            excluded_iris,
            columns=("o",),
            excluded_substrings=excluded_substrings,
        )
        if df.empty or "o" not in df.columns:
            continue
        if "links" in df.columns:
            frame = df[["o", "links"]].copy()
        else:
            frame = df[["o"]].copy()
            frame["links"] = 1
        frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["o", "links"])
    return (
        pd.concat(frames, ignore_index=True)
        .groupby("o", as_index=False)["links"]
        .sum()
    )


def _fetch_hebb_links(
    runner: QueryRunner,
    queries_to_run: Iterable[str],
    *,
    excluded_iris: set[str] | None,
    excluded_substrings: list[str] | None,
) -> pd.DataFrame:
    frames = []
    for query in queries_to_run:
        df = runner.fetch(query)
        df = filter_excluded_rows(
            df,
            excluded_iris,
            columns=("o1", "o2"),
            excluded_substrings=excluded_substrings,
        )
        if df.empty or "o1" not in df.columns or "o2" not in df.columns:
            continue
        if "links" in df.columns:
            frame = df[["o1", "o2", "links"]].copy()
        else:
            frame = df[["o1", "o2"]].copy()
            frame["links"] = 1
        frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["o1", "o2", "links"])
    return (
        pd.concat(frames, ignore_index=True)
        .groupby(["o1", "o2"], as_index=False)["links"]
        .sum()
    )


def build_context_for_proof(
    proof_n: int,
    *,
    runner: QueryRunner,
    type_selection: bool,
    excluded_iris: set[str] | None = None,
    excluded_substrings: list[str] | None = None,
) -> tuple[set[str], dict[str, pd.DataFrame], pd.DataFrame]:
    """Return (context_resources, family_dfs, hebb_df).

    excluded_iris may contain raw IRIs with or without angle brackets; values are normalized internally.
    excluded_substrings removes IRIs containing any listed substring.
    Filtering is skipped if expected columns are missing from query results.
    """
    values = _values_clause(_iris_for_context(proof_n))

    direct_queries = [
        queries.direct_definitions(),
        queries.direct_postulates(),
        queries.direct_common_notions(),
    ]
    if values:
        direct_queries.append(queries.direct_template_propositions_proofs(values))
    direct_df = _fetch_sum_links(
        runner,
        direct_queries,
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )

    hierarchical_queries = [
        queries.hierarchical_definitions(),
        queries.hierarchical_postulates(),
        queries.hierarchical_common_notions(),
    ]
    if values:
        hierarchical_queries.append(queries.hierarchical_template_propositions_proofs(values))
    hierarchical_df = _fetch_sum_links(
        runner,
        hierarchical_queries,
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )

    mereological_queries = [
        queries.mereological_definitions(),
        queries.mereological_postulates(),
        queries.mereological_common_notions(),
    ]
    if values:
        mereological_queries.append(queries.mereological_template_propositions_proofs(values))
    mereological_df = _fetch_sum_links(
        runner,
        mereological_queries,
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )

    hebb_queries = [
        queries.hebb_definitions(),
        queries.hebb_postulates(),
        queries.hebb_common_notions(),
    ]
    if values:
        if type_selection:
            hebb_queries.append(queries.hebb_template_propositions_proofs_types(values))
        else:
            hebb_queries.append(queries.hebb_template_propositions_proofs(values))
    hebb_df = _fetch_hebb_links(
        runner,
        hebb_queries,
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )

    context_resources: set[str] = set()
    for df in (direct_df, hierarchical_df, mereological_df):
        if not df.empty and "o" in df.columns:
            context_resources.update(df["o"].dropna().astype(str))

    family_dfs = {
        "direct": direct_df,
        "hierarchical": hierarchical_df,
        "mereological": mereological_df,
    }
    return context_resources, family_dfs, hebb_df
