import pandas as pd
import modules.queries as queries # SPARQL queries 
import rdflib


def history(kg: rdflib.Graph,
            proposition_number: int = 0,
            base_sparql_queries: list = [
                [queries.direct_definitions(), queries.direct_postulates(), queries.direct_common_notions()],
                [queries.hierarchical_definitions(), queries.hierarchical_postulates(), queries.hierarchical_common_notions()],
                [queries.mereological_definitions(), queries.mereological_postulates(), queries.mereological_common_notions()] ],
            weights: list = [6/9, 1/9, 2/9]):
    query_lists = base_sparql_queries.copy()
    if proposition_number >= 2:
        # Generate the iris strings
        iris = create_iris_for_values(proposition_number)

        # Append the new queries to the existing lists
        query_lists[0].append(queries.direct_template_propositions_proofs(iris))
        query_lists[1].append(queries.hierarchical_template_propositions_proofs(iris))
        query_lists[2].append(queries.mereological_template_propositions_proofs(iris))

    # Generate the histories
    histories = [sparql_to_concat_df(kg, query_list) for query_list in query_lists]

    activation_dfs = []
    # calculation of activation potentials
    for history_df, weight in zip(histories, weights):
        total_use = history_df["links"].sum()
        actions_df = history_df.assign(
            activation_potential = (history_df["links"] * weight) / total_use
        )[["o", "activation_potential"]]
        activation_dfs.append(actions_df)

    # combine dataframes
    combined_df = pd.concat(activation_dfs, ignore_index=True)
    return combined_df.groupby("o")["activation_potential"].sum().reset_index()

def calculate_activation_potential(kg: rdflib.Graph,
                                   proposition_number: int = 0):
    # history potential
    calculated_history_potential_df = history(kg, proposition_number)
    # hebb potential
    hebb_potential = hebb(kg, proposition_number)
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
