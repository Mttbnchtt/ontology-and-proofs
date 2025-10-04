import pandas as pd
import rdflib



def calculate_activation_potential(kg: rdflib.Graph,
                                   proposition_number: int = 0):
    # history potential
    calculated_history_potential_df = history(kg, proposition_number)
    # print(len(calculated_history_potential_df))
    # print(calculated_history_potential_df["activation_potential"].sum())
    # hebb potential
    hebb_potential = hebb(kg, proposition_number)
    # print(len(hebb_potential))
    # print(hebb_potential["activation_potential"].sum())
    return calculated_history_potential_df, hebb_potential

def main(kg: rdflib.Graph,
         proposition_number: int = 1,
         given_upper_part: float = 1/4):
    #  calculate activation potential
    history_df, cooccurrence_df = calculate_activation_potential(kg, proposition_number)
    # find direct and mereological concepts of last proposition
    last_proposition_iri = f"<https://www.foom.com/core#proposition_{proposition_number}>"
    direct_last_proposition, mereological_last_proposition = direct_and_mereological_last_item(kg, last_proposition_iri)
    # find direct concepts of last proof
    last_proof_iri = f"<https://www.foom.com/core#proof_{proposition_number}>"
    direct_last_proof, mereological_last_proof = direct_and_mereological_last_item(kg, last_proof_iri)
    # check surprise score
    materials = {
        "direct_last_proposition": direct_last_proposition,
        "mereological_last_proposition": mereological_last_proposition,
        "direct_last_proof": direct_last_proof,
        "history": history_df,
        "cooccurrence": cooccurrence_df
    }
    # check surprisingness
    background_concepts, diff = check_surprise_score(materials, given_upper_part)
    return background_concepts, diff
