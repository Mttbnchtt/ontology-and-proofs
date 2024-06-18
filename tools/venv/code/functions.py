import re
import sparql_classes
import sparql_queries

##########################
## FIND RELATED CONCEPTS
##########################

def find_sub_properties(sparq_query_text: str,
                        selected_datastore:str):
    sub_properties: set = set(f"<{row.property_iri}>"
                              for row in sparql_classes.SparqlQueryResults(sparq_query_text,
                                                                           datastore = selected_datastore)
                             )
    return sub_properties
        
def create_property_path_for_nodes_finding(sub_properties: set) -> str:
    # initialize property-path string
    property_path: str = " | ".join(sub_properties)
    return property_path

def find_related_concepts(start_iri: str,
                          property_path: str,
                          selected_datastore: str):
    print(property_path)
    sparql_query = sparql_queries.query_find_nodes_path(
        start_iri,
        property_path)
    related_concepts: dict = {
        "iris": [],
        "concepts": []
    }
    for row in sparql_classes.SparqlQueryResults(sparql_query,
                                                 datastore = selected_datastore):
        related_concepts["iris"].extend([iri.strip() for iri in row.path_iri.split("->")])
        related_concepts["concepts"].extend([label.strip() for label in row.path.split("->")])
    # paths = set()
    # for row in sparql_classes.SparqlQueryResults(sparql_query,
    #                                              datastore = selected_datastore):
    #     iris = tuple(iri.strip() for iri in row.path_iri.split("->"))
    #     labels = tuple(label.strip() for label in row.path.split("->"))
    #     paths.add((iris, labels))
    return related_concepts
    # return paths

def organize_property_path_creation(top_properties: set,
                                    selected_datastore: str):
    sub_properties: set = set()
    for top_property in top_properties:
        sub_properties = sub_properties.union(
            find_sub_properties(
                sparql_queries.query_find_sub_properties(top_property),
                selected_datastore
            )
        )
    return sub_properties

def organize_nodes_paths(start_iri: str,
                         top_properties: set,
                         selected_datastore: str):
    sub_properties: set = organize_property_path_creation(top_properties, selected_datastore)
    property_path: str = create_property_path_for_nodes_finding(sub_properties)
    # add paths
    related_concepts = find_related_concepts(start_iri, property_path, selected_datastore)
    return related_concepts

##########################
## FIND PROOF STEPS
##########################

def find_proof_steps(proof_iri: str,
                     selected_datastore:str):
    sparql_query = sparql_queries.query_find_proof_steps(
        proof_iri)
    proof_steps:list = sorted([
        tuple(
                (
                    extract_step_ordinal_number(row.step_label), 
                    row.step_iri, 
                    row.step_label
                )
            ) 
        for row in sparql_classes.SparqlQueryResults(sparql_query)
        ])
    return proof_steps

def extract_step_ordinal_number(proof_step_label: str):
    matches: list = re.findall(".+([0-9]).+", proof_step_label)
    if matches:
        ordinal_number: int = int(matches[0])
    return ordinal_number