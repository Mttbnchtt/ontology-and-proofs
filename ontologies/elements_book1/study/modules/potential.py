"""Experimental pipeline orchestrating activation and surprise computations."""

from __future__ import annotations

from typing import Set, Tuple

import rdflib

from .calculate_activation_potential import history as history_potential, hebb as hebb_potential
from .query_runner import QueryRunner
from .direct_and_mereological_last_item import (
    direct_last_item,
    main as last_item_main,
)
from .surprise_score import SelectionCriteria, main as surprise_main


def _proposition_iri(proposition_number: int) -> str:
    return f"<https://www.foom.com/core#proposition_{proposition_number}>"


def _proof_iri(proposition_number: int) -> str:
    return f"<https://www.foom.com/core#proof_{proposition_number}>"


def main(
    kg: rdflib.Graph,
    proposition_number: int,
    *,
    history_weights: Tuple[float, float, float],
    history_selection: SelectionCriteria,
    cooccurrence_selection: SelectionCriteria,
    runner: QueryRunner | None = None,
) -> Tuple[Set[str], Set[str]]:
    """Return background and surprising concepts for the requested proposition."""

    runner = runner or QueryRunner(kg)
    history_df = history_potential(
        kg,
        proposition_number,
        weights=history_weights,
        runner=runner,
    )
    cooccurrence_df = hebb_potential(kg, proposition_number, runner=runner)

    last_proposition_iri = _proposition_iri(proposition_number)
    direct_last_proposition, mereological_last_proposition = last_item_main(
        kg,
        last_proposition_iri,
        runner=runner,
    )

    last_proof_iri = _proof_iri(proposition_number)
    direct_last_proof = direct_last_item(kg, last_proof_iri, runner=runner)

    materials = {
        "direct_last_proposition": direct_last_proposition,
        "mereological_last_proposition": mereological_last_proposition,
        "direct_last_proof": direct_last_proof,
        "history": history_df,
        "cooccurrence": cooccurrence_df,
    }

    background_concepts, diff = surprise_main(
        materials,
        history_selection=history_selection,
        cooccurrence_selection=cooccurrence_selection,
    )
    return background_concepts, diff
