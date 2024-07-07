#########
## UTILS
#########

def update_conceptual_space(conceptual_space: dict,
                            new_data: dict) -> dict:
    for key in conceptual_space:
        conceptual_space[key].extend(new_data[key])
    return conceptual_space
