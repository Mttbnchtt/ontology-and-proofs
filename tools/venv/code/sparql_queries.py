# %%time

def query_find_sub_properties(property: str) -> str:
    sparql_query: str = f"""
        SELECT DISTINCT
            ?property_iri
        WHERE {{
            ?property_iri
                rdfs:subPropertyOf+ {property} .
        }}
    """
    return sparql_query

def query_find_nodes_path(start_iri: str,
                          property_path: str) -> str:
    start_iri = iri_enclosing(start_iri)
    sparql_query:str = f"""
        SELECT 
            (GROUP_CONCAT(?step_iri; SEPARATOR=" -> ") AS ?path_iri)
            (GROUP_CONCAT(?step; SEPARATOR=" -> ") AS ?path)
        WHERE {{
        {{
            SELECT 
                ?step_iri
                ?step
            WHERE {{
                {start_iri}
                    (
                        {property_path}
                    )+
                        ?next .
                        ?next rdfs:label ?label .
                
                BIND(CONCAT(" ", STR(?next)) AS ?step_iri)
                BIND(CONCAT(" ", STR(?label)) AS ?step)
                }}
            }}
        }}
    """
    return sparql_query


def query_find_proof_steps(proof_iri: str) -> str:
    proof_iri = iri_enclosing(proof_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?step_iri
            ?step_label 
        WHERE {{
            ?step_iri
                rdfs:label ?step_label ;
                <http://www.foom.com/core/inProof> {proof_iri} .
        }}
    """
    return sparql_query


def query_find_proof_of_proof_step(proof_step_iri: str) -> str:
    proof_step_iri = iri_enclosing(proof_step_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?proof_iri
        WHERE {{
            {proof_step_iri}
                <http://www.foom.com/core/inProof> ?proof_iri .
        }}
    """
    return sparql_query

def query_find_antencedent_proof_steps(proof_step_iri: str) -> str:
    proof_step_iri = iri_enclosing(proof_step_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?antencedent_proof_step_iri
        WHERE {{
            {proof_step_iri}
                <http://www.foom.com/core#00000000000000000186> ?antencedent_proof_step_iri .
        }}
    """
    return sparql_query


def iri_enclosing(iri: str) -> str:
    if not (iri.startswith("<") and iri.endswith(">")):
        iri = f"<{iri}>"
    return iri

def query_find_related_concepts(concept_iri: str,
                                top_property_iri: str) -> str:
    concept_iri = iri_enclosing(concept_iri)
    top_property_iri = iri_enclosing(top_property_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?related_concept_iri
            ?related_concept_label
        WHERE {{
            {concept_iri}
                {top_property_iri}+ ?related_concept_iri .
        ?related_concept_iri
            rdfs:label ?related_concept_label .
        }}
    """
    return sparql_query

def query_find_values_of_reified_triple(iri: str) -> str :
    iri = iri_enclosing(iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?reified_value_iri
        WHERE {{
            {iri}
                <http://www.foom.com/core#00000000000000000086> ?reified_value_iri .
        }}
    """
    return sparql_query

def query_find_related_proofs(proof_iri: str) -> str:
    proof_iri = iri_enclosing(proof_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?related_proof_iri
        WHERE {{
            {proof_iri}
                <http://www.foom.com/mathematical_concepts#00000000000000000250> ?related_proof_iri .
        }}
    """
    return sparql_query

def query_find_goal_of_proof(proof_iri: str) -> str:
    proof_iri = iri_enclosing(proof_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?goal_iri
        WHERE {{
            {proof_iri}
                <http://www.foom.com/mathematical_concepts#00000000000000000249> ?goal_iri .
        }}
    """
    return sparql_query

def query_find_last_proof_step_of_proof(proof_iri: str) -> str:
    proof_iri = iri_enclosing(proof_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?last_proof_step
        WHERE {{
            ?last_proof_step
                <http://www.foom.com/core/inProof> {proof_iri} ;
                <http://www.foom.com/core#00000000000000000044> true .
        }}
    """
    return sparql_query