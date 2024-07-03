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

def query_find_related_proofs(proof_iri: str) -> str:
    proof_iri = iri_enclosing(proof_iri)
    sparql_query: str = f"""
        SELECT DISTINCT
            ?related_proof_iri
        WHERE {{
            {proof_iri}
                <http://www.foom.com/mathematical_concepts#00000000000000000249> ?claim_iri .
             ?related_proof_iri   
                <http://www.foom.com/mathematical_concepts#00000000000000000249> ?claim_iri .
            FILTER ( {proof_iri} != ?related_proof_iri )
        }}
    """
    return sparql_query

def iri_enclosing(iri: str) -> str:
    if not (iri.startswith("<") and iri.endswith(">")):
        iri = f"<{iri}>"
    return iri
