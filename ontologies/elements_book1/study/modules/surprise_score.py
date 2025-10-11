import math
import pandas as pd
import modules.queries as queries # SPARQL queries 
import modules.rdf_utils as rdf_utils # RDF utilities
import rdflib

def highest_potential(df: pd.DataFrame,
                      upper_part: float = 1/4):
    keep_count = math.ceil(len(df) * upper_part)
    print("keep ", keep_count)
    return df.iloc[:keep_count].copy()

def get_background_concepts(materials: dict, upper_part: float=1/4):
    history_highest_concepts = set(highest_potential(materials["history"], upper_part)["o"])
    cooccurrence_df = highest_potential(materials["cooccurrence"], upper_part)
    cooccurrence_concepts = set(cooccurrence_df["o1"]) | set(cooccurrence_df["o2"])
    proposition_concepts = materials["direct_last_proposition"] | materials["mereological_last_proposition"]
    return history_highest_concepts | cooccurrence_concepts | proposition_concepts

def main(materials: dict, upper_part: float=1/4):
    cooccurrence_df = highest_potential(materials["cooccurrence"], upper_part)
    background_concepts = get_background_concepts(materials, upper_part)
    proof_concepts = materials["direct_last_proof"]
    print("background", len(background_concepts), background_concepts)
    diff = proof_concepts - background_concepts
    print("diff ", len(diff), diff)
    return background_concepts, diff

