"""Experimental surprise scoring with flexible selection strategies."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Set, Tuple, TypedDict

import math
import pandas as pd


ConceptId = str


class MaterialsPayload(TypedDict):
    history: pd.DataFrame
    cooccurrence: pd.DataFrame
    direct_last_proposition: Set[ConceptId]
    mereological_last_proposition: Set[ConceptId]
    direct_last_proof: Set[ConceptId]


class SelectionMode(str, Enum):
    THRESHOLD = "threshold"
    TOP_N = "top_n"
    TOP_FRACTION = "top_fraction"


@dataclass(frozen=True)
class SelectionCriteria:
    mode: SelectionMode
    value: float


DEFAULT_HISTORY_SELECTION = SelectionCriteria(SelectionMode.TOP_FRACTION, 1 / 10)
DEFAULT_COOCCURRENCE_SELECTION = SelectionCriteria(SelectionMode.TOP_FRACTION, 1 / 20)


def highest_potential(df: pd.DataFrame, criteria: SelectionCriteria) -> pd.DataFrame:
    """Filter ``df`` according to the provided selection criteria."""

    if df.empty:
        return df.copy()

    if criteria.mode is SelectionMode.THRESHOLD:
        return df[df["activation_potential"] >= criteria.value].copy()

    if criteria.mode is SelectionMode.TOP_N:
        top_n = max(0, int(criteria.value))
        if top_n <= 0:
            return pd.DataFrame(columns=df.columns)
        return df.nlargest(top_n, "activation_potential").copy()

    if criteria.mode is SelectionMode.TOP_FRACTION:
        fraction = max(0.0, float(criteria.value))
        if fraction <= 0:
            return pd.DataFrame(columns=df.columns)
        keep_count = max(1, math.ceil(len(df) * fraction))
        return df.iloc[:keep_count].copy()

    raise ValueError(f"Unsupported selection mode: {criteria.mode}")


def get_background_concepts(
    materials: MaterialsPayload,
    *,
    history_selection: SelectionCriteria,
    cooccurrence_selection: SelectionCriteria,
) -> Set[ConceptId]:
    history_df = highest_potential(materials["history"], history_selection)
    history_concepts = set(history_df.get("o", pd.Series(dtype=object)).dropna())

    cooccurrence_df = highest_potential(materials["cooccurrence"], cooccurrence_selection)
    cooccurrence_concepts = set(
        cooccurrence_df.get("o1", pd.Series(dtype=object)).dropna()
    ) | set(cooccurrence_df.get("o2", pd.Series(dtype=object)).dropna())

    proposition_concepts = materials["direct_last_proposition"] | materials["mereological_last_proposition"]
    return {str(concept) for concept in history_concepts | cooccurrence_concepts | proposition_concepts}


def main(
    materials: MaterialsPayload,
    *,
    history_selection: SelectionCriteria = DEFAULT_HISTORY_SELECTION,
    cooccurrence_selection: SelectionCriteria = DEFAULT_COOCCURRENCE_SELECTION,
) -> Tuple[Set[ConceptId], Set[ConceptId]]:
    background_concepts = get_background_concepts(
        materials,
        history_selection=history_selection,
        cooccurrence_selection=cooccurrence_selection,
    )
    proof_concepts = materials["direct_last_proof"]
    surprising = {str(concept) for concept in proof_concepts if concept not in background_concepts}
    return background_concepts, surprising
