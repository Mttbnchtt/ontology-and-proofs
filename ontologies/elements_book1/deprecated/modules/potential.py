"""End-to-end pipeline that scores activation potentials and evaluates conceptual surprise.

Limitations:
- Retrieves mereological proof concepts but the downstream surprise score only inspects direct proof concepts.
- Relies on upstream query helpers returning non-empty data; missing data can propagate NaNs or raise errors.
"""

from typing import Set, Tuple

import modules.calculate_activation_potential as calculate_activation_potential # calculate activation potential
import modules.direct_and_mereological_last_item as direct_and_mereological_last_item # direct and mereological last item
import modules.surprise_score as surprise_score # surprise score
from modules.surprise_score import MaterialsPayload
import rdflib

GIVEN_UPPER_PART: float = 1 / 4

def main(kg: rdflib.Graph,
         proposition_number: int = 1,
         given_upper_part: float = GIVEN_UPPER_PART) -> Tuple[Set[str], Set[str]]:
    #  calculate activation potential
    history_df, cooccurrence_df = calculate_activation_potential.main(kg, proposition_number)
    # find direct and mereological concepts of last proposition
    last_proposition_iri = f"<https://www.foom.com/core#proposition_{proposition_number}>"
    direct_last_proposition, mereological_last_proposition = direct_and_mereological_last_item.main(kg, last_proposition_iri)
    # find direct concepts of last proof
    last_proof_iri = f"<https://www.foom.com/core#proof_{proposition_number}>"
    direct_last_proof = direct_and_mereological_last_item.main(kg, last_proof_iri, direct_and_mereological=False)
    # check surprise score
    materials: MaterialsPayload = {
        "direct_last_proposition": direct_last_proposition,
        "mereological_last_proposition": mereological_last_proposition,
        "direct_last_proof": direct_last_proof,
        "history": history_df,
        "cooccurrence": cooccurrence_df
    }
    background_concepts, diff = surprise_score.main(materials, given_upper_part)
    return background_concepts, diff
