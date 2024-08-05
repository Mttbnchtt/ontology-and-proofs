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

def finc_concepts_related_to_goal_of_proof(values: set,
                                   selected_datastore: str) -> set:



# 2. On the basis of the concepts directly related to the goal of the proof
# structure the conceptual space before the given proof step.
# Use the following categories: concepts, examples, results, thoughts
# E.g., given the concept of angle, use the conceptual space 
# before the given proof step to create a conceptual file 
# for that concept (logical items, illustrative items, heuristic principles)


# 3. Create a conceptual file for the reificiation values 
# of the antencedent proof steps and of the concepts directly related 
# to these proof steps.


# 4. Apply heuristic techniques to suggest using new concepts
# and formulate new steps

