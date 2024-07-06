import re
import sparql_classes
import sparql_queries

##########################
## FIND RELATED CONCEPTS
##########################

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
    

#########
## UTILS
#########

def update_conceptual_space(conceptual_space: dict,
                            new_data: dict) -> dict:
    for key in conceptual_space:
        conceptual_space[key].extend(new_data[key])
    return conceptual_space


####################################################
## FIND CONCEPTUAL SPACE OF ANTENCEDENT PROOF STEPS
####################################################

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
    return sparql_results[0] if sparql_results else None

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
    return antencedent_proof_steps
    
def find_values_of_reified_triple(iri: str,
                                  selected_datastore: str) -> str:
    sparql_query = sparql_queries.query_find_values_of_reified_triple(iri)
    reified_values = {
            row.reified_value_iri
            for row in sparql_classes.SparqlQueryResults(
                sparql_query,
                datastore=selected_datastore
            )
        }
    return reified_values

def find_conceptual_space_of_concept(concept_iri: str,
                                     selected_datastore: str,
                                     top_property: str) -> str :
    sparql_query = sparql_queries.query_find_related_concepts(
        concept_iri, 
        top_property
    )
    related_concepts: dict = {
        "concept_iris": [],
        "concept_labels": []
    }
    for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore):
        related_concepts["concept_iris"].append(row.related_concept_iri)
        related_concepts["concept_labels"].append(row.related_concept_label)
    return related_concepts

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
        conceptual_space = update_conceptual_space_with_concepts_related_to_proof_step(
            proof_step_iri,
            selected_datastore,
            top_property,
            conceptual_space
        )
    return conceptual_space

def update_conceptual_space_with_concepts_related_to_proof_step(proof_step_iri: str, 
                                                                selected_datastore: str,
                                                                top_property: str,
                                                                conceptual_space: dict) -> dict:
    # find values of reified statement
    reified_values = find_values_of_reified_triple(proof_step_iri, selected_datastore)
    # loop through the values to find the conceptual space of that concept
    for value_iri in reified_values:
        conceptual_space_of_value = find_conceptual_space_of_concept(value_iri, selected_datastore, top_property)
        conceptual_space = update_conceptual_space(conceptual_space, conceptual_space_of_value)
    return conceptual_space

###################################
## FIND CONCEPTUAL SPACE OF PROOFS
###################################

def find_related_proofs(proof_iri: str,
                        selected_datastore: str) -> set:
    sparql_query = sparql_queries.query_find_related_proofs(proof_iri)
    related_proofs = {
        row.related_proof_iri
        for row in sparql_classes.SparqlQueryResults(
            sparql_query, 
            datastore=selected_datastore
        )
    }
    return related_proofs

def find_conceptual_space_of_related_proofs(related_proofs: set,
                                            top_property: str,
                                            selected_datastore: str) -> dict:
    conceptual_space = {
        "concept_iris": [],
        "concept_labels": []
    }
    for related_proof_iri in related_proofs:
        proof_steps = find_proof_steps(related_proof_iri, selected_datastore)
        for proof_step_iri in proof_steps:
            conceptual_space = update_conceptual_space_with_concepts_related_to_proof_step(
                proof_step_iri[1],
                selected_datastore,
                top_property,
                conceptual_space
            )
    return conceptual_space


#####################################
## FIND CONCEPTUAL BEFORE PROOF STEP
#####################################

def find_conceptual_space_before_proof_step(proof_step: str,
                                            selected_datastore: str,
                                            top_property: str = "<http://www.foom.com/mathematical_concepts#00000000000000000000>") -> dict:
    # find proof of proof step
    proof_iri = find_proof_of_proof_step(proof_step, selected_datastore)
    # find previous proof steps in proof
    if not proof_iri:
        raise ValueError("Proof iri not found.")
    antencedent_proof_steps = find_previous_proof_steps(
        proof_step,
        proof_iri,
        selected_datastore)
    
    # find conceptual space of previous steps in proof
    conceptual_space = find_conceptual_space_of_antecedent_proof_steps(
        antencedent_proof_steps,
        selected_datastore,
        top_property
    )

    # find related proofs
    related_proofs = find_related_proofs(proof_iri, selected_datastore)

    # find conceptual space of related proofs
    conceptual_space.update(
        find_conceptual_space_of_related_proofs(
            related_proofs,
            top_property,
            selected_datastore
        )
    )

    return conceptual_space

#################################
## FIND CONCEPTUAL OF PROOF STEP
#################################

def find_conceptual_space_of_proof_step(proof_step: str,
                                        selected_datastore: str,
                                        top_property: str = "<http://www.foom.com/mathematical_concepts#00000000000000000000>") -> dict:
    # initialize dictionary of related concepts
    conceptual_space = {
        "concept_iris": [],
        "concept_labels": []
    }
    # find reified values of the proof step
    reified_values = find_values_of_reified_triple(proof_step, selected_datastore)
    # find conceptual space of each reified value
    for value in reified_values:
        conceptual_space.update(
            find_conceptual_space_of_concept(
                value, 
                selected_datastore,
                top_property
            )
        )
    return conceptual_space
    
#############################################
## FIND DIFFERENCE BETWEEN CONCEPTUAL SPACES
#############################################

def diff_conceptual_spaces(conceptual_space_1: dict,
                           conceptual_space_2: dict) -> dict:
    diff_conceptual_space = {
        "concept_iris": [iri for iri in conceptual_space_2["concept_iris"] if not iri in conceptual_space_1["concept_iris"]],
        "concept_labels": [[label for label in conceptual_space_2["concept_labels"] if not label in conceptual_space_1["concept_labels"]]]
    }
    return diff_conceptual_space


#############################################
## HEURISTIC SEARCHES
#############################################



#########################################
## CONCEPTUAL SPACES OF PROOF TO ANALYZE
#########################################

