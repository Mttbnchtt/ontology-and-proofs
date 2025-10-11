"""Tools for deriving background concepts and surprise sets from activation data.

Limitations:
- Assumes incoming dataframes are pre-sorted by relevance; `highest_potential` simply slices the top rows.
- Emits diagnostic `print` statements rather than using a logger or returning metadata.
"""

import math
from typing import Set, Tuple, TypedDict

import pandas as pd
import modules.queries as queries # SPARQL queries 
import modules.rdf_utils as rdf_utils # RDF utilities
import rdflib

ConceptId = str


class MaterialsPayload(TypedDict):
    history: pd.DataFrame
    cooccurrence: pd.DataFrame
    direct_last_proposition: Set[ConceptId]
    mereological_last_proposition: Set[ConceptId]
    direct_last_proof: Set[ConceptId]


UPPER_PART_HISTORY: float = 1 / 10
UPPER_PART_COOCCURRENCE: float = 1 / 20
SELECTION_TYPES = ("top_fraction", "top_n", "threshold")


def highest_potential(df: pd.DataFrame,
                      upper_part: float,
                      selection_type: str = "top_fraction") -> pd.DataFrame:
    """Return the highest potential concepts from a dataframe, based on a selection strategy."""
    if df.empty:
        return df.copy()

    if selection_type not in SELECTION_TYPES:
        raise ValueError(f"Unsupported selection type: {selection_type}")

    if selection_type == "threshold":
        return df[df["activation_potential"] >= upper_part].copy()

    if selection_type == "top_n":
        top_n = max(0, int(upper_part))
        if top_n <= 0:
            return df.iloc[0:0].copy()
        return df.nlargest(top_n, "activation_potential").copy()

    if selection_type == "top_fraction":
        keep_count = max(1, math.ceil(len(df) * upper_part))
        print("keep ", keep_count)
        return df.iloc[:keep_count].copy()

    return df.iloc[0:0].copy()

def get_background_concepts(materials: MaterialsPayload,
                            upper_part_history: float,
                            upper_part_cooccurrence: float) -> Set[ConceptId]:
    history_highest_concepts = set(highest_potential(materials["history"], upper_part_history)["o"])
    cooccurrence_df = highest_potential(materials["cooccurrence"], upper_part_cooccurrence)
    cooccurrence_concepts = set(cooccurrence_df["o1"]) | set(cooccurrence_df["o2"])
    proposition_concepts = materials["direct_last_proposition"] | materials["mereological_last_proposition"]
    return history_highest_concepts | cooccurrence_concepts | proposition_concepts

def main(
        materials: MaterialsPayload, 
        upper_part_history: float = UPPER_PART_HISTORY, 
        upper_part_cooccurrence: float = UPPER_PART_COOCCURRENCE
) -> Tuple[Set[ConceptId], Set[ConceptId]]:
    background_concepts = get_background_concepts(
        materials,
        upper_part_history,
        upper_part_cooccurrence,
    )
    proof_concepts = materials["direct_last_proof"]
    # print("background", len(background_concepts), background_concepts)
    diff = proof_concepts - background_concepts
    # print("diff ", len(diff), diff)
    return background_concepts, diff
