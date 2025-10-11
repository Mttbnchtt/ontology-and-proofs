import pandas as pd
import modules.queries as queries # SPARQL queries 
import modules.rdf_utils as rdf_utils # RDF utilities
import rdflib

def history(kg: rdflib.Graph,
            proposition_number: int = 0,
            base_sparql_queries: list = [
                [queries.direct_definitions(), queries.direct_postulates(), queries.direct_common_notions()],
                [queries.hierarchical_definitions(), queries.hierarchical_postulates(), queries.hierarchical_common_notions()],
                [queries.mereological_definitions(), queries.mereological_postulates(), queries.mereological_common_notions()] ],
            weights: list = [6/9, 1/9, 2/9]):
    """Compute activation potentials by weighting concept frequencies from multiple SPARQL histories.

    Each query family (direct, hierarchical, mereological) contributes a dataframe of link counts.
    The counts are normalised within their family, scaled by ``weights``, and combined so the
    returned dataframe lists each concept with its aggregated activation potential.
    """
    query_lists = base_sparql_queries.copy()
    if proposition_number >= 2:
        # Generate the iris strings
        iris = rdf_utils.create_iris_for_values(proposition_number)

        # Append the new queries to the existing lists
        query_lists[0].append(queries.direct_template_propositions_proofs(iris))
        query_lists[1].append(queries.hierarchical_template_propositions_proofs(iris))
        query_lists[2].append(queries.mereological_template_propositions_proofs(iris))

    # Generate the histories
    histories = [rdf_utils.sparql_to_concat_df(kg, query_list) for query_list in query_lists]

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


def hebb(kg: rdflib.Graph,
         proposition_number: int = 0,
         sparql_queries: list = [queries.hebb_definitions(), queries.hebb_postulates(), queries.hebb_common_notions()]):
    if proposition_number >= 2:
        # Generate the iris strings
        iris = rdf_utils.create_iris_for_values(proposition_number)
        # Append the new queries to the existing lists
        sparql_queries.append(queries.hebb_template_propositions_proofs(iris))
    df = rdf_utils.sparql_to_concat_df(kg, sparql_queries, hebb=True)
    total_use = df["links"].sum()
    df["activation_potential"] = df["links"] / total_use
    df = df.drop(columns=["links"])
    df = df.sort_values(by="activation_potential", ascending=False)
    df = df.reset_index(drop=True)
    return df


def main(kg: rdflib.Graph,
         proposition_number: int = 0):
    # history potential
    calculated_history_potential_df = history(kg, proposition_number)
    # hebb potential
    hebb_potential = hebb(kg, proposition_number)
    return calculated_history_potential_df, hebb_potential
