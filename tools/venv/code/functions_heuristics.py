import functions_find_conceptual_space
import functions_utils
import sparql_classes
import sparql_queries

#############################################
## HEURISTIC SEARCHES
#############################################
## find the conceptual space of the goal of the proof
# find statement that the proof proves
# def find_goal_of_proof(proof_iri: str,
#                        selected_datastore: str):
#     sparql_query = sparql_queries.query_find_goal_of_proof(proof_iri)
#     sparql_results = [
#         row.goal_iri
#         for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore)
#     ]
#     if sparql_results:
#         return sparql_results[0]
#     else:
#         raise ValueError("Goal of proof not found.")

# # find statement that ends the proof
# def find_last_step_of_proof(proof_iri: str,
#                             selected_datastore: str):
#     sparql_query = sparql_queries.query_find_last_proof_step_of_proof(proof_iri)
#     sparql_results = [
#         row.last_proof_step
#         for row in sparql_classes.SparqlQueryResults(sparql_query, datastore=selected_datastore)
#     ]
#     if sparql_results:
#         return sparql_results[0]
#     else:
#         raise ValueError("Goal of proof not found.")
    

# ## extract concepts from the goal of the proof and
# # find the conceptual space of the goal of the proof and of its last step
# def find_conceptual_space_of_goal_of_proof(proof_iri: str,
#                                            selected_datastore: str) -> dict:
#     goal_iri = find_goal_of_proof(proof_iri, selected_datastore)
#     conceptual_space = functions_find_conceptual_space.find_conceptual_space_of_claim(
#         goal_iri, 
#         selected_datastore
#         )
#     last_step_iri = find_last_step_of_proof(proof_iri, selected_datastore)
#     conceptual_space = functions_utils.update_conceptual_space(
#         conceptual_space,
#         functions_find_conceptual_space.find_conceptual_space_of_proof_step(
#             last_step_iri,
#             selected_datastore
#         )
#     )
#     return conceptual_space


# ## extract encyclopedic knowledge (= conceptual space) before the proof step
# def find_conceptual_space_before_proof_step(proof_step_iri: str,
#                                             selected_datastore: str,
#                                             top_property: str = "<http://www.foom.com/mathematical_concepts#00000000000000000000>") -> dict:
#     # find proof to which the proof step belongs
#     proof_iri = functions_find_conceptual_space.find_proof_of_proof_step(
#             proof_step_iri, 
#             selected_datastore
#         )
#     # find conceptual space of goal of proof
#     conceptual_space = find_conceptual_space_of_goal_of_proof(
#             proof_iri,
#             selected_datastore
#         )
#     # find conceptual space of antecedent steps
#     # and related proofs
#     conceptual_space = functions_utils.update_conceptual_space(
#             conceptual_space,
#             functions_find_conceptual_space.find_conceptual_space_before_proof_step(
#                 proof_step_iri,
#                 selected_datastore,
#                 top_property
#             )
#         )
#     return conceptual_space


## organize conceptual space along heuristic dimensions (concepts, results, examples)


## apply strategic knowledge
# 1. select concepts for working memory
# 2. select heuristic techniques
# 3. apply means-ends analysis: asses difference between the current problem state and the possible future problem state after the heuristic enrichment and evaluate the difference with respect to the goal


## MAIN
def main(proof_step_iri: str,
         selected_datastore: str,
         top_property: str = "<http://www.foom.com/mathematical_concepts#00000000000000000000>"):
    ## find conceptual space before proof step
    conceptual_space_before_proof_step = functions_find_conceptual_space.find_conceptual_space_before_proof_step(
            proof_step_iri,
            selected_datastore,
            top_property
        )

    # find conceptual space of proof step
    conceptual_space_of_proof_step = functions_find_conceptual_space.find_conceptual_space_of_proof_step(
                proof_step_iri,
                selected_datastore,
                top_property
        )

    # apply heuristics on conceptual space before proof step

