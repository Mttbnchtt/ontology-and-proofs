import pandas as pd
import rdflib
import os


# general functions

def access_graph(file_name: str,
                 folder_name: str = "input") -> rdflib.Graph:
    """Accesses the RDF graph from the specified file.

    Args:
        file_name: The name of the file containing the RDF graph (e.g., "ontology_output.ttl").

    Returns:
        An rdflib.Graph object representing the RDF graph.
    """
    input_file = os.path.join(folder_name, file_name)
    print(input_file)
    return rdflib.Graph().parse(input_file)


def run_sparql_query(knowledge_graph: rdflib.Graph,
                     sparql_query_name: str,
                     folder_name: str = os.path.join("input", "sparql_queries")
                     ) -> rdflib.query.Result:
    """Runs a SPARQL query on the provided knowledge graph.

    Args:
        knowledge_graph: The rdflib.Graph object representing the knowledge graph.
        sparql_query_name: The name of the SPARQL query file (e.g., "query_6.sparql").
        folder_name: The folder containing the SPARQL query file. Defaults to "input/sparql_queries".

    Returns:
        The result of the SPARQL query as an rdflib.query.Result object.
    """
    # create path to sparql query
    query_path = os.path.join(folder_name, sparql_query_name)
    print(query_path)

    # access the sparql query and run it on the knowledge graph
    with open(query_path, "r") as query_file:
        sparql_query = query_file.read()
    return knowledge_graph.query(sparql_query)


def get_table_with_links(knowledge_graph: rdflib.Graph,
                         sparql_queries: set = direct_history_preface
                         ) -> pd.DataFrame:
    """Retrieves a table of textual units, conceptual items, and their usage numbers.

    Executes a set of SPARQL queries on the knowledge graph to extract links between
    textual units and conceptual items, along with their usage numbers.

    Args:
        knowledge_graph: The rdflib.Graph object representing the knowledge graph.
        sparql_queries: A list of SPARQL query names to execute. Defaults to sparql_queries_withouth_hierarchical_imports.

    Returns:
        A pandas DataFrame with columns "textual_unit", "conceptual_item", and "use_number".
    """
    # Initialize an empty list to store results
    all_results = []

    # Run SPARQL queries and append results to the list
    for sparql_query in sparql_queries:
        sparql_results = run_sparql_query(knowledge_graph, sparql_query)
        for result in sparql_results:
            all_results.append([
                getattr(result.s, "toPython", lambda: result.s)(),  # Use getattr with default lambda
                getattr(result.o, "toPython", lambda: result.o)(),  # Use getattr with default lambda
                int(result.links)
            ])

    # Return the pandas DataFrame from the list of results
    results = pd.DataFrame(all_results,
                           columns=["textual_unit", "conceptual_item", "use_number"])
    
    # Order results 
    results = results.sort_values(by=['textual_unit', 'use_number'], ascending=[True, False])

    return results