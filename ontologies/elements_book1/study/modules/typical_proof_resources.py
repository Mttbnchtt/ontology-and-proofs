"""Proof resource extraction for typical activation potential."""

from __future__ import annotations

from . import queries
from .query_runner import QueryRunner
from .typical_helpers import iri_for_proof


def resources_in_proof(
    proof_n: int,
    *,
    runner: QueryRunner,
    type_selection: bool,
) -> set[str]:
    """Return direct-usage resources in proof N; type_selection toggles proof queries."""
    proof_iri = iri_for_proof(proof_n)
    if type_selection:
        query = queries.direct_template_last_item_types(proof_iri)
    else:
        query = queries.direct_template_propositions_proofs(proof_iri)
    df = runner.fetch(query)
    if "o" not in df.columns:
        return set()
    return {str(value) for value in df["o"].dropna().astype(str)}
