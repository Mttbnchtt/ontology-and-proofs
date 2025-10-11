"""Experimental helpers for retrieving last proposition/proof neighbourhoods without duplicate queries."""

from __future__ import annotations

from typing import Iterable, Optional, Set, Tuple, Union

import rdflib

from . import queries as base_queries

from .query_runner import QueryRunner


def _as_values_token(iri: Union[str, rdflib.term.Identifier]) -> str:
    if isinstance(iri, rdflib.term.Identifier):
        return f"<{iri}>"
    return str(iri)


def direct_last_item(
    kg: rdflib.Graph,
    last_proposition_iri: Union[str, rdflib.term.Identifier],
    *,
    runner: Optional[QueryRunner] = None,
) -> Set[str]:
    runner = runner or QueryRunner(kg)
    query = base_queries.direct_template_propositions_proofs(_as_values_token(last_proposition_iri))
    df = runner.fetch(query)
    if "o" not in df.columns:
        return set()
    return {str(value) for value in df["o"].dropna().astype(str)}


def mereological_last_item(
    kg: rdflib.Graph,
    last_proposition_iri: Union[str, rdflib.term.Identifier],
    *,
    runner: Optional[QueryRunner] = None,
) -> Set[str]:
    runner = runner or QueryRunner(kg)
    query = base_queries.mereological_template_last_item(_as_values_token(last_proposition_iri))
    df = runner.fetch(query)
    if "o" not in df.columns:
        return set()
    return {str(value) for value in df["o"].dropna().astype(str)}


def main(
    kg: rdflib.Graph,
    last_proposition_iri: Union[str, rdflib.term.Identifier],
    *,
    direct_and_mereological: bool = True,
    runner: Optional[QueryRunner] = None,
) -> Union[Tuple[Set[str], Set[str]], Set[str]]:
    runner = runner or QueryRunner(kg)
    if direct_and_mereological:
        return (
            direct_last_item(kg, last_proposition_iri, runner=runner),
            mereological_last_item(kg, last_proposition_iri, runner=runner),
        )
    return direct_last_item(kg, last_proposition_iri, runner=runner)
