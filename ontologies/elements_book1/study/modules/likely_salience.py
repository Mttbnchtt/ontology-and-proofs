"""Salient-set construction for likely activation potential."""

from __future__ import annotations

from collections.abc import Iterable

from . import queries
from .exclusion_filters import filter_excluded_rows
from .query_runner import QueryRunner
from .typical_helpers import iri_for_proposition

S_VARIANTS = {"statement_only", "statement_plus_related_chunks"}


def _values_clause(values: Iterable[str]) -> str | None:
    tokens: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text:
            continue
        if text.startswith("<") and text.endswith(">"):
            tokens.append(text)
        else:
            tokens.append(f"<{text}>")
    if not tokens:
        return None
    return " ".join(sorted(set(tokens)))


def _extract_o_values(df) -> set[str]:
    if df.empty or "o" not in df.columns:
        return set()
    return {str(value) for value in df["o"].dropna().astype(str)}


def _run_o_query(
    runner: QueryRunner,
    query: str,
    *,
    excluded_iris: set[str] | None,
    excluded_substrings: list[str] | None,
) -> set[str]:
    df = runner.fetch(query)
    df = filter_excluded_rows(
        df,
        excluded_iris,
        columns=("o",),
        excluded_substrings=excluded_substrings,
    )
    return _extract_o_values(df)


def _statement_resources(
    last_proposition_iri: str,
    *,
    runner: QueryRunner,
    type_selection: bool,
    excluded_iris: set[str] | None,
    excluded_substrings: list[str] | None,
) -> set[str]:
    direct_query = (
        queries.direct_template_last_item_types(last_proposition_iri)
        if type_selection
        else queries.direct_template_propositions_proofs(last_proposition_iri)
    )
    query_list = [
        direct_query,
        queries.hierarchical_template_propositions_proofs(last_proposition_iri),
        queries.mereological_template_propositions_proofs(last_proposition_iri),
    ]

    resources: set[str] = set()
    for query in query_list:
        resources.update(
            _run_o_query(
                runner,
                query,
                excluded_iris=excluded_iris,
                excluded_substrings=excluded_substrings,
            )
        )
    return resources


def build_salient_set_for_proof(
    proof_n: int,
    *,
    runner: QueryRunner,
    type_selection: bool,
    s_variant: str,
    excluded_iris: set[str] | None = None,
    excluded_substrings: list[str] | None = None,
) -> set[str]:
    """Return the salient set S for proof N under the selected variant."""
    if s_variant not in S_VARIANTS:
        raise ValueError(f"Unknown S variant: {s_variant}. Expected one of {sorted(S_VARIANTS)}")

    last_proposition_iri = iri_for_proposition(proof_n)
    s0 = _statement_resources(
        last_proposition_iri,
        runner=runner,
        type_selection=type_selection,
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )

    if s_variant == "statement_only":
        return s0

    if not s0:
        # Spec: if salient extraction is empty, skip salient-dependent queries.
        return set()

    resource_iris_values = _values_clause(s0)
    if not resource_iris_values:
        return set()

    d_values = _run_o_query(
        runner,
        queries.find_salient_definitions_postulates_common_notions(resource_iris_values),
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )
    e_values = _run_o_query(
        runner,
        queries.find_salient_propositions_proofs(
            resource_iris_values,
            proposition=last_proposition_iri,
        ),
        excluded_iris=excluded_iris,
        excluded_substrings=excluded_substrings,
    )

    related_resources: set[str] = set()

    d_values_clause = _values_clause(d_values)
    if d_values_clause:
        d_queries = [
            queries.direct_definitions_selected_values(d_values_clause),
            queries.direct_postulates_selected_values(d_values_clause),
            queries.direct_common_notions_selected_values(d_values_clause),
            queries.hierarchical_definitions_selected_values(d_values_clause),
            queries.hierarchical_postulates_selected_values(d_values_clause),
            queries.hierarchical_common_notions_selected_values(d_values_clause),
            queries.mereological_definitions_selected_values(d_values_clause),
            queries.mereological_postulates_selected_values(d_values_clause),
            queries.mereological_common_notions_selected_values(d_values_clause),
        ]
        for query in d_queries:
            related_resources.update(
                _run_o_query(
                    runner,
                    query,
                    excluded_iris=excluded_iris,
                    excluded_substrings=excluded_substrings,
                )
            )

    e_values_clause = _values_clause(e_values)
    if e_values_clause:
        e_query = (
            queries.direct_template_last_item_types(e_values_clause)
            if type_selection
            else queries.direct_template_propositions_proofs_selected_values(e_values_clause)
        )
        related_resources.update(
            _run_o_query(
                runner,
                e_query,
                excluded_iris=excluded_iris,
                excluded_substrings=excluded_substrings,
            )
        )

    return s0 | related_resources
