import copy
import re
import sparql_classes
import sparql_queries
import sys

##########################
## FIND RELATED CONCEPTS
##########################

def find_sub_properties(sparq_query_text: str, selected_datastore: str) -> set:
    """
    Finds sub-properties of a given SPARQL query.

    Args:
        sparq_query_text (str): The SPARQL query text used to find sub-properties.
        selected_datastore (str): The datastore where the query is executed.

    Returns:
        set: A set of sub-property IRIs.
    """
    sub_properties: set = set(
        f"<{row.property_iri}>"
        for row in sparql_classes.SparqlQueryResults(sparq_query_text, datastore=selected_datastore)
    )
    return sub_properties


def create_property_path_for_nodes_finding(sub_properties: set) -> str:
    """
    Creates a property path string for node finding.

    Args:
        sub_properties (set): A set of sub-property IRIs.

    Returns:
        str: A property path string constructed by joining sub-properties with '|'.
    """
    property_path: str = " | ".join(sub_properties)
    return property_path


def find_related_concepts(start_iri: str, property_path: str, selected_datastore: str) -> dict:
    """
    Finds related concepts based on a starting IRI and property path.

    Args:
        start_iri (str): The starting IRI from which to find related concepts.
        property_path (str): The property path used in the SPARQL query.
        selected_datastore (str): The datastore where the query is executed.

    Returns:
        dict: A dictionary containing lists of IRIs and their corresponding concept labels.
    """
    sparql_query = sparql_queries.query_find_nodes_path(start_iri, property_path)
    related_concepts: dict = {
        "concept_iris": [],
        "concept_labels": []
    }
    for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore):
        related_concepts["concept_iris"].extend([iri.strip() for iri in row.path_iri.split("->")])
        related_concepts["concept_labels"].extend([label.strip() for label in row.path.split("->")])
    return related_concepts


def organize_property_path_creation(top_properties: set, selected_datastore: str) -> set:
    """
    Organizes the creation of a property path by finding all sub-properties for the top properties.

    Args:
        top_properties (set): A set of top property IRIs.
        selected_datastore (str): The datastore where queries are executed.

    Returns:
        set: A set of all sub-property IRIs.
    """
    sub_properties: set = set()
    for top_property in top_properties:
        sub_properties = sub_properties.union(
            find_sub_properties(
                sparql_queries.query_find_sub_properties(top_property),
                selected_datastore
            )
        )
    return sub_properties


def organize_nodes_paths(start_iri: str, top_properties: set, selected_datastore: str) -> dict:
    """
    Organizes the process of finding related concepts by creating property paths.

    Args:
        start_iri (str): The starting IRI for finding related concepts.
        top_properties (set): A set of top property IRIs.
        selected_datastore (str): The datastore where queries are executed.

    Returns:
        dict: A dictionary containing related concept IRIs and their labels.
    """
    sub_properties: set = organize_property_path_creation(top_properties, selected_datastore)
    property_path: str = create_property_path_for_nodes_finding(sub_properties)
    related_concepts = find_related_concepts(start_iri, property_path, selected_datastore)
    return related_concepts


##########################
## FIND PROOF STEPS
##########################

def find_proof_steps(proof_iri: str, 
                     selected_datastore: str) -> list:
    """
    Finds and sorts proof steps for a given proof IRI.

    Args:
        proof_iri (str): The IRI of the proof to find steps for.
        selected_datastore (str): The datastore where the query is executed.

    Returns:
        list: A sorted list of tuples containing the ordinal number, step IRI, and step label.
    """
    sparql_query = sparql_queries.query_find_proof_steps(proof_iri)
    proof_steps: list = sorted(
        [
            tuple(
                (
                    extract_ordinal_number_of_proof_step(row.step_label),
                    row.step_iri,
                    row.step_label
                )
            )
            for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore)
        ]
    )
    return proof_steps


def extract_ordinal_number_of_proof_step(proof_step_label: str) -> int:
    """
    Extracts the ordinal number from a proof step label.

    Args:
        proof_step_label (str): The label of the proof step.

    Returns:
        int: The extracted ordinal number from the proof step label.
    """
    matches: list = re.findall(".+([0-9]).+", proof_step_label)
    if matches:
        ordinal_number: int = int(matches[0])
        return ordinal_number
    

###################################
## FIND CONCEPTUAL SPACE OF PROOFS
###################################

def find_conceptual_space_of_proof(proof_iri: str,
                                   top_properties: set, 
                                   selected_datastore: str) -> dict:
    # find proof steps in given proof
    proof_steps: list = find_proof_steps(proof_iri, 
                                         selected_datastore)
    # loop through proof steps to find related concepts
    conceptual_space: dict = {
        proof_step[1]: organize_nodes_paths(f"<{proof_step[1]}>",
                                         top_properties,
                                         selected_datastore)
        for proof_step in proof_steps
    }
    # conceptual_space_copy = copy.deepcopy(conceptual_space)
    # conceptual_space["general"] = sum_conceptual_space(conceptual_space_copy)
    return conceptual_space

def sum_conceptual_space(conceptual_space: dict) -> dict:
    sum_concepts:dict = {
        "concept_iris": set(),
        "concept_labels": set()
    }
    for proof_step, values in conceptual_space.items():
        sum_concepts["concept_iris"].update(values["concept_iris"])
        sum_concepts["concept_labels"].update(values["concept_labels"])
    return sum_concepts

def find_conceptual_space_of_proofs(proof_iri: str,
                                    top_properties: set,
                                    selected_datastore: str) -> dict:
    # find proofs of the same proposition
    sparql_query = sparql_queries.query_find_related_proofs(proof_iri)
    related_proofs: set = {
        str(row.related_proof_iri)
        for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore)
    }
    # retrieve conceptual space of each proof
    conceptual_space: dict = {}
    for related_proof_iri in related_proofs:
        conceptual_space = conceptual_space | find_conceptual_space_of_proof(
            related_proof_iri, 
            top_properties, 
            selected_datastore
            )
    conceptual_space_copy = copy.deepcopy(conceptual_space)
    conceptual_space["general"] = sum_conceptual_space(conceptual_space_copy)
    return conceptual_space


#######################################
## FIND CONCEPTUAL SPACE OF PROOF STEP
#######################################

def find_proof_of_proof_step(proof_step: str,
                             selected_datastore: str):
    sparql_query = sparql_queries.query_find_proof_of_proof_step(proof_step)
    sparql_results = [
            row.proof_iri 
            for row in sparql_classes.SparqlQueryResults(
                sparql_query, 
                datastore=selected_datastore
            )
        ]
    if sparql_results:
        return sparql_results[0]
    else:
        return False

def find_previous_proof_steps(proof_step: str,
                              proof_iri: str,
                              selected_datastore: str) -> set:
    sparql_query = sparql_queries.query_find_antencedent_proof_steps(proof_step)
    antencedent_proof_steps = {
        row.antencedent_proof_step_iri
        for row in sparql_classes.SparqlQueryResults(
            sparql_query,
            datastore=selected_datastore
        )
    }
    if antencedent_proof_steps:
        return antencedent_proof_steps
    else:
        return False
    
def find_values_of_reified_triple(iri: str,
                                  selected_datastore: str) -> str:
    sparql_query = sparql_queries.query_find_values_of_reified_triple(iri)
    reified_valies = {
            row.reified_value_iri
            for row in sparql_classes.SparqlQueryResults(
                sparql_query,
                datastore=selected_datastore
            )
        }
    return reified_valies

def find_conceptual_space_of_concept(concept_iri: str,
                                     selected_datastore: str,
                                     top_property: str) -> str :
    sparql_query = sparql_classes.query_find_related_concepts(
        concept_iri, 
        top_property
    )
    related_concepts: dict = {
        "concept_iris": [],
        "concept_labels": []
    }
    for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore):
        related_concepts["concepts_iris"].append(row.related_concept_iri)
        related_concepts["concept_labels"].append(row.related_concept_label)
    return related_concepts

    
def update_conceptual_space(conceptual_space: dict,
                            new_data: dict) -> dict:
    for key in conceptual_space:
        conceptual_space[key].extend(new_data[key])
    return conceptual_space

def find_conceptual_space_of_antecedent_proof_steps(proof_steps: set,
                                                    selected_datastore: str,
                                                    top_property: str) -> dict:
    # initialize conceptual space
    conceptual_space = {
        "concept_iris": [],
        "concept_labels": []
    }
    # loop through proof steps
    for proof_step_iri in proof_steps:
        # find values of reified statement
        reified_values = find_values_of_reified_triple(iri, selected_datastore)
        # loop through the values to find the conceptual space of that concept
        for value_iri in reified_values:
            conceptual_space_of_value = find_conceptual_space_of_concept(value_iri, selected_datastore, top_property)
            conceptual_space = update_conceptual_space(conceptual_space, conceptual_space_of_value)
    return conceptual_space

def find_conceptual_space_before_proof_step(proof_step: str,
                                            selected_datastore: str,
                                            top_property: str = "<http://www.foom.com/mathematical_concepts#00000000000000000000>") -> dict:
    # find proof of proof step
    proof_iri = find_proof_of_proof_step(proof_step, selected_datastore)
    # find previous proof steps in proof
    if proof_iri:
        antencedent_proof_steps = find_previous_proof_steps(
            proof_step,
            proof_iri,
            selected_datastore)
    else:
        print("Proof iri not found.")
        sys.exit()

    # find conceptual space of previous steps in proof
    conceptual_space = find_conceptual_space_of_antecedent_proof_steps(
        antencedent_proof_steps,
        selected_datastore,
        top_property
    )

    # find related proofs

    # find conceptual space of related proofs
    # (remove sum of conceptual space and re-add it later)

    # sum of conceptual space

    return conceptual_space
    