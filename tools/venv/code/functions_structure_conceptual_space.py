import copy
import sparql_classes
import sparql_queries

#########################################
## CONCEPTUAL SPACES OF PROOF TO ANALYZE
#########################################

# structure
# memory: working and paper
# production
# selection of production
# representation: concepts, results, and problem
# knowledge: domain (organized in concepts, results [theorems, conjectures, techniques, gists], examples), strategic (), control of development
# item evocation, connectedness, polyvalence

## The structure of the conceptual space before a given proof step depends on the goal of the proof.

# 1. (Understand the claim: part 1) Find goal of proof

def find_concepts_of_goal_of_proof(proof_iri: str,
                                   selected_datastore: str) -> set:
    
    """
    Identify and retrieve the concepts related to the goal and last step of a proof.

    This function finds the goal of a proof and its last step, then retrieves the reified values and directly related concepts
    associated with these elements. The identified concepts form a conceptual space pertinent to the proof's goal.

    Parameters:
    proof_iri (str): The IRI of the proof whose goal and last step are to be analyzed.
    selected_datastore (str): The datastore where the SPARQL queries will be executed.

    Returns:
    set: A set of IRIs representing the concepts related to the goal and last step of the proof.
    """
    # find goal of proof
    sparql_query_goal = sparql_queries.query_find_goal_of_proof(proof_iri)
    goal_iri = {
            row.goal_iri 
            for row in sparql_classes.SparqlQueryResults(
                    sparql_query_goal,
                    datastore=selected_datastore
                )
    }
    # find last step of proof
    sparql_query_last_step = sparql_queries.query_find_last_proof_step_of_proof(proof_iri)
    last_step_iri = {
            row.last_proof_step 
            for row in sparql_classes.SparqlQueryResults(
                    sparql_query_last_step,
                    datastore=selected_datastore
                )
    }
    # find reified values of goal of proof and last step of proof
    iris = {iri for iri in goal_iri.union(last_step_iri)}
    values = set()
    for iri in iris:
        sparq_query_reified_values = sparql_queries.query_find_values_of_reified_triple(iri)
        values.update(
                {
                    row.reified_value_iri
                    for row in sparql_classes.SparqlQueryResults(
                        sparq_query_reified_values,
                        datastore=selected_datastore)
                }
            )
        sparq_query_directly_related_concepts = sparql_queries.query_find_directly_related_concepts(iri)
        values.update(
                {
                    row.related_concept_iri
                    for row in sparql_classes.SparqlQueryResults(
                        sparq_query_directly_related_concepts,
                        datastore=selected_datastore)
                }
            )
    return values

# 2. (Understand the claim: part 2) find ontological items 
# related to the values of the claim to prove

def find_concepts_related_to_goal_of_proof(values: set,
                                           selected_datastore: str) -> set:
    """
    Identify and categorize concepts related to the goal of a proof based on logical and heuristic connections.

    This function enhances the input set of values by identifying logically and heuristically connected and remotely connected 
    concepts. It categorizes these connections into four groups for each value: logically connected items, logically remotely 
    connected items, heuristically connected items, and heuristically remotely connected items.

    Parameters:
    values (set): A set of IRIs representing initial concepts related to the goal of a proof.
    selected_datastore (str): The datastore where the SPARQL queries will be executed.

    Returns:
    dict: A dictionary where each key is an IRI from the input set, and the value is another dictionary with the following keys:
          - "logically_connected_items": Set of IRIs logically connected to the key IRI.
          - "logically_remotely_connected_items": Set of IRIs logically remotely connected to the key IRI.
          - "heuristically_connected_items": Set of IRIs heuristically connected to the key IRI.
          - "heuristically_remotely_connected_items": Set of IRIs heuristically remotely connected to the key IRI.
    """
    values_enhanced = {value: {
                "logically_connected_items": set(),
                "logically_remotely_connected_items": set(),
                "heuristically_connected_items": set(),
                "heuristically_remotely_connected_items": set()
                
            }
            for value in values
        }
    # iterate through value iris to select connected and remotely connected items
    for value in values:
        # select logically connected items
        sparql_connected_items = sparql_queries.query_find_concepts_connected_to_goal(value)
        connected_items = {
            row.connected_item_iri
            for row in sparql_classes.SparqlQueryResults(sparql_connected_items,
                                                         datastore=selected_datastore)
        }
        values_enhanced[value]["logically_connected_items"] = connected_items
        # select logically remotely connected items
        sparql_remotely_connected_items = sparql_queries.query_find_concepts_remotely_connected_to_goal(value)
        remotely_connected_items = {
            row.connected_item_iri
            for row in sparql_classes.SparqlQueryResults(sparql_remotely_connected_items,
                                                         datastore=selected_datastore)
            if not row.connected_item_iri in connected_items
        }
        values_enhanced[value]["logically_remotely_connected_items"] = remotely_connected_items
        # select heuristically connected items
        sparql_connected_items = sparql_queries.query_find_concepts_heuristically_connected_to_goal(value)
        connected_items = {
            row.connected_item_iri
            for row in sparql_classes.SparqlQueryResults(sparql_connected_items,
                                                         datastore=selected_datastore)
        }
        values_enhanced[value]["heuristically_connected_items"] = connected_items
        # select heuristically remotely connected items
        sparql_remotely_connected_items = sparql_queries.query_find_concepts_heuristically_remotely_connected_to_goal(value)
        remotely_connected_items = {
            row.connected_item_iri
            for row in sparql_classes.SparqlQueryResults(sparql_remotely_connected_items,
                                                         datastore=selected_datastore)
            if not row.connected_item_iri in connected_items
        }
        values_enhanced[value]["heuristically_remotely_connected_items"] = remotely_connected_items
        
    return values_enhanced

# 3. find triples connecting related concepts


# 3. find enciclopedic material: previous proofs, analogous proofs, relevant facts



# 4. given a proof step, repeat previous steps for antencedent proof steps



# 2. On the basis of the concepts directly related to the goal of the proof
# structure the conceptual space before the given proof step.
# Use the following categories: concepts, examples, results, thoughts
# E.g., given the concept of angle, use the conceptual space 
# before the given proof step to create a conceptual file 
# for that concept (logical items, illustrative items, heuristic principles)


# 3. Create a conceptual file for the reification values 
# of the antencedent proof steps and of the concepts directly related 
# to these proof steps.


# 4. Apply heuristic techniques to suggest using new concepts
# and formulate new steps

