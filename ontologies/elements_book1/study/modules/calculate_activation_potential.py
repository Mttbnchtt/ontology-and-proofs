"""Experimental activation potential calculations with deduplicated SPARQL execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional, Sequence, Set, Tuple

import pandas as pd
import rdflib

from . import queries as base_queries
from . import rdf_utils as base_rdf_utils

from .query_runner import QueryRunner


WeightVector = Sequence[float]


@dataclass(frozen=True)
class HistoryFamily:
    weight: float
    base_queries: Tuple[str, ...]
    template_factory: Optional[Callable[[str], str]] = None


def _build_history_families(weights: Tuple[float, float, float]) -> Tuple[HistoryFamily, ...]:
    direct_weight, hierarchical_weight, mereological_weight = weights
    return (
        HistoryFamily(
            weight=direct_weight,
            base_queries=(
                base_queries.direct_definitions(),
                base_queries.direct_postulates(),
                base_queries.direct_common_notions(),
            ),
            template_factory=base_queries.direct_template_propositions_proofs,
        ),
        HistoryFamily(
            weight=hierarchical_weight,
            base_queries=(
                base_queries.hierarchical_definitions(),
                base_queries.hierarchical_postulates(),
                base_queries.hierarchical_common_notions(),
            ),
            template_factory=base_queries.hierarchical_template_propositions_proofs,
        ),
        HistoryFamily(
            weight=mereological_weight,
            base_queries=(
                base_queries.mereological_definitions(),
                base_queries.mereological_postulates(),
                base_queries.mereological_common_notions(),
            ),
            template_factory=base_queries.mereological_template_propositions_proofs,
        ),
    )


def _normalise_weights(weights: WeightVector) -> Tuple[float, float, float, float]:
    """Return a 4-tuple of weights, splitting the legacy mereological weight when needed."""

    raw = tuple(weights)
    if len(raw) == 4:
        return raw  # already expanded
    if len(raw) == 3:
        direct, hierarchical, mereological = raw
        # Split the historical mereological share evenly between the two mereological families.
        split = mereological / 2 if mereological else 0.0
        return direct, hierarchical, split, split
    raise ValueError(
        f"Expected 3 or 4 weights, received {len(raw)} entries: {weights!r}"
    )


def _format_value_token(value: object) -> Optional[str]:
    if isinstance(value, rdflib.term.Identifier):
        text = str(value)
    else:
        text = str(value)
    if not text:
        return None
    if text.startswith("<") and text.endswith(">"):
        return text
    return f"<{text}>"


def _concept_values_clause(concepts: Iterable[object]) -> Optional[str]:
    tokens = {
        token
        for concept in concepts
        if (token := _format_value_token(concept)) is not None
    }
    if not tokens:
        return None
    return " ".join(sorted(tokens))


HEBB_QUERIES: Tuple[str, ...] = (
    base_queries.hebb_definitions(),
    base_queries.hebb_postulates(),
    base_queries.hebb_common_notions(),
)


def _history_query_plan(
    proposition_number: int,
    families: Tuple[HistoryFamily, ...],
) -> Iterable[Tuple[float, Tuple[str, ...]]]:
    iris: Optional[str] = None
    if proposition_number >= 2:
        iris = base_rdf_utils.create_iris_for_values(proposition_number)

    for family in families:
        queries = list(family.base_queries)
        if iris and family.template_factory is not None:
            queries.append(family.template_factory(iris))
        yield family.weight, tuple(queries)


def history(
    kg: rdflib.Graph,
    proposition_number: int = 0,
    *,
    weights: WeightVector,
    runner: Optional[QueryRunner] = None,
) -> pd.DataFrame:
    """Return weighted activation potentials, avoiding repeated SPARQL query execution."""

    runner = runner or QueryRunner(kg)
    family_frames: list[pd.DataFrame] = []
    normalised = _normalise_weights(weights)
    base_weights = normalised[:3]
    concept_membership_weight = normalised[3]
    families = _build_history_families(base_weights)
    seen_concepts: Set[str] = set()

    for weight, queries in _history_query_plan(proposition_number, families):
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
        seen_concepts.update(family_df["o"].astype(str))
        family_frames.append(family_df[["o", "activation_potential"]])

    if concept_membership_weight > 0:
        values_clause = _concept_values_clause(seen_concepts)
        if values_clause:
            concept_query = base_queries.mereological_is_concept_in(values_clause)
            concept_df = runner.fetch(concept_query)
            if not concept_df.empty:
                concept_frame = (
                    concept_df[["o", "links"]]
                    .groupby("o", as_index=False)["links"]
                    .sum()
                )
                total_links = concept_frame["links"].sum()
                if total_links != 0:
                    concept_frame["activation_potential"] = (
                        concept_frame["links"] * concept_membership_weight
                    ) / total_links
                    family_frames.append(
                        concept_frame[["o", "activation_potential"]]
                    )

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
    type_selection: bool = False,
) -> pd.DataFrame:
    """Return Hebbian activation potentials with per-query caching.

    When type_selection is True, proposition/proof co-occurrence uses relation/operation types.
    """

    runner = runner or QueryRunner(kg)
    queries = list(HEBB_QUERIES)
    if proposition_number >= 2:
        iris = base_rdf_utils.create_iris_for_values(proposition_number)
        if type_selection:
            queries.append(base_queries.hebb_template_propositions_proofs_types(iris))
        else:
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
    weights: WeightVector,
    runner: Optional[QueryRunner] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return history and Hebbian activation potentials using shared query results."""

    runner = runner or QueryRunner(kg)
    history_df = history(kg, proposition_number, weights=weights, runner=runner)
    hebb_df = hebb(kg, proposition_number, runner=runner)
    return history_df, hebb_df
