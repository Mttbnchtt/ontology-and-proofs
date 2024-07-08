###########################
## UPDATE CONCEPTUAL SPACE
###########################

def update_conceptual_space(conceptual_space: dict,
                            new_data: dict) -> dict:
    for key in conceptual_space:
        conceptual_space[key].extend(new_data[key])
    return conceptual_space


#############################################
## FIND DIFFERENCE BETWEEN CONCEPTUAL SPACES
#############################################

def diff_conceptual_spaces(conceptual_space_1: dict,
                           conceptual_space_2: dict) -> dict:
    """
    Finds the difference between two conceptual spaces.

    Args:
        conceptual_space_1 (dict): The first conceptual space.
        conceptual_space_2 (dict): The second conceptual space.

    Returns:
        dict: A dictionary containing IRIs and labels of concepts present in the second conceptual space but not in the first.
    """
    diff_conceptual_space = {
        "concept_iris": [iri for iri in conceptual_space_2["concept_iris"] if not iri in conceptual_space_1["concept_iris"]],
        "concept_labels": [label for label in conceptual_space_2["concept_labels"] if not label in conceptual_space_1["concept_labels"]]
    }
    return diff_conceptual_space