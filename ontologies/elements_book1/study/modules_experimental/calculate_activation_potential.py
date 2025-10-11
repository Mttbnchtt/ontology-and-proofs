"""Experimental activation potential calculations with deduplicated SPARQL execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional, Tuple

import pandas as pd
import rdflib

from modules import queries as base_queries
from modules import rdf_utils as base_rdf_utils

from .query_runner import QueryRunner


@dataclass(frozen=True)
class HistoryFamily:
    weight: float
    base_queries: Tuple[str, ...]
    template_factory: Optional[Callable[[str], str]] = None

WEIGHT_DIRECT = 6 / 9
WEIGHT_HIERARCHICAL = 1 / 9
WEIGHT_MEREOLOGICAL = 2 / 9

HISTORY_FAMILIES: Tuple[HistoryFamily, ...] = (
    HistoryFamily(
        weight=WEIGHT_DIRECT,
        base_queries=(
            base_queries.direct_definitions(),
            base_queries.direct_postulates(),
            base_queries.direct_common_notions(),
        ),
        template_factory=base_queries.direct_template_propositions_proofs,
    ),
    HistoryFamily(
        weight=WEIGHT_HIERARCHICAL,
        base_queries=(
            base_queries.hierarchical_definitions(),
            base_queries.hierarchical_postulates(),
            base_queries.hierarchical_common_notions(),
        ),
        template_factory=base_queries.hierarchical_template_propositions_proofs,
    ),
    HistoryFamily(
        weight=WEIGHT_MEREOLOGICAL,
        base_queries=(
            base_queries.mereological_definitions(),
            base_queries.mereological_postulates(),
            base_queries.mereological_common_notions(),
        ),
        template_factory=base_queries.mereological_template_propositions_proofs,
    ),
)


HEBB_QUERIES: Tuple[str, ...] = (
    base_queries.hebb_definitions(),
    base_queries.hebb_postulates(),
    base_queries.hebb_common_notions(),
)


def _history_query_plan(proposition_number: int) -> Iterable[Tuple[float, Tuple[str, ...]]]:
    iris: Optional[str] = None
    if proposition_number >= 2:
        iris = base_rdf_utils.create_iris_for_values(proposition_number)

    for family in HISTORY_FAMILIES:
        queries = list(family.base_queries)
        if iris and family.template_factory is not None:
            queries.append(family.template_factory(iris))
        yield family.weight, tuple(queries)


def history(
    kg: rdflib.Graph,
    proposition_number: int = 0,
    *,
    runner: Optional[QueryRunner] = None,
) -> pd.DataFrame:
    """Return weighted activation potentials, avoiding repeated SPARQL query execution."""

    runner = runner or QueryRunner(kg)
    family_frames: list[pd.DataFrame] = []

    for weight, queries in _history_query_plan(proposition_number):
        query_frames = []
        for query in queries:
            df = runner.fetch(query)
            if df.empty:
                continue
            query_frames.append(df[["o", "links"]].copy())

        if not query_frames:
            continue

        family_df = (
            pd.concat(query_frames, ignore_index=True)
            .groupby("o", as_index=False)["links"]
            .sum()
        )
        total_links = family_df["links"].sum()
        if total_links == 0:
            continue
        family_df["activation_potential"] = (family_df["links"] * weight) / total_links
        family_frames.append(family_df[["o", "activation_potential"]])

    if not family_frames:
        return pd.DataFrame(columns=["o", "activation_potential"])

    combined_history_df = pd.concat(family_frames, ignore_index=True)
    combined_history_df = (
        combined_history_df
        .groupby("o", as_index=False)["activation_potential"]
        .sum()
        .sort_values(by="activation_potential", ascending=False)
        .reset_index(drop=True)
    )
    return combined_history_df


def hebb(
    kg: rdflib.Graph,
    proposition_number: int = 0,
    *,
    runner: Optional[QueryRunner] = None,
) -> pd.DataFrame:
    """Return Hebbian activation potentials with per-query caching."""

    runner = runner or QueryRunner(kg)
    queries = list(HEBB_QUERIES)
    if proposition_number >= 2:
        iris = base_rdf_utils.create_iris_for_values(proposition_number)
        queries.append(base_queries.hebb_template_propositions_proofs(iris))

    frames = []
    for query in queries:
        df = runner.fetch(query)
        if df.empty:
            continue
        frames.append(df[["o1", "o2", "links"]].copy())

    if not frames:
        return pd.DataFrame(columns=["o1", "o2", "activation_potential"])

    combined_hebb_df = (
        pd.concat(frames, ignore_index=True)
        .groupby(["o1", "o2"], as_index=False)["links"]
        .sum()
    )
    total_links = combined_hebb_df["links"].sum()
    if total_links == 0:
        combined_hebb_df["activation_potential"] = 0.0
    else:
        combined_hebb_df["activation_potential"] = combined_hebb_df["links"] / total_links
    combined_hebb_df = combined_hebb_df.drop(columns=["links"])
    combined_hebb_df = combined_hebb_df.sort_values(by="activation_potential", ascending=False).reset_index(drop=True)
    return combined_hebb_df


def main(
    kg: rdflib.Graph,
    proposition_number: int = 0,
    *,
    runner: Optional[QueryRunner] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return history and Hebbian activation potentials using shared query results."""

    runner = runner or QueryRunner(kg)
    history_df = history(kg, proposition_number, runner=runner)
    hebb_df = hebb(kg, proposition_number, runner=runner)
    return history_df, hebb_df
