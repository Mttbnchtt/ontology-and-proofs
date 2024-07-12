import functions_find_conceptual_space
import functions_utils
import sparql_classes
import sparql_queries

#############################################
## HEURISTIC SEARCHES
#############################################

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

    return conceptual_space_of_proof_step