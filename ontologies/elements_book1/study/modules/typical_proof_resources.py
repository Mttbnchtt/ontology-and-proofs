"""Proof resource extraction for typical activation potential."""

from __future__ import annotations

from . import queries
from .query_runner import QueryRunner
from .exclusion_filters import filter_excluded_rows
from .typical_helpers import iri_for_proof


def resources_in_proof(
    proof_n: int,
    *,
    runner: QueryRunner,
    type_selection: bool,
    excluded_iris: set[str] | None = None,
    excluded_substrings: list[str] | None = None,
) -> set[str]:
    """Return direct-usage resources in proof N; type_selection toggles proof queries.

    excluded_iris may contain raw IRIs with or without angle brackets; values are normalized internally.
    excluded_substrings removes IRIs containing any listed substring.
    Filtering is skipped if expected columns are missing from query results.
    """
    proof_iri = iri_for_proof(proof_n)
    if type_selection:
        query = queries.direct_template_last_item_types(proof_iri)
    else:
        query = queries.direct_template_propositions_proofs(proof_iri)
    df = runner.fetch(query)
    df = filter_excluded_rows(
        df,
        excluded_iris,
        columns=("o",),
        excluded_substrings=excluded_substrings,
    )
    if "o" not in df.columns:
        return set()
    return {str(value) for value in df["o"].dropna().astype(str)}
