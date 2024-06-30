# %%time

def query_find_paths(start_iri: str) -> str:
    sparql_query: str = f"""
            SELECT DISTINCT 
                ?mid ?mid_label 
                ?p ?p_label 
                ?end ?end_label
            WHERE {{
                {{
                    SELECT DISTINCT
                        ?mid ?mid_label 
                        ?end ?end_label
                    WHERE {{

                        {start_iri}
                            (
                                <http://www.foom.com/mathematical_concepts#00000000000000000222> | <http://www.foom.com/mathematical_concepts#00000000000000000198> | <http://www.foom.com/mathematical_concepts#00000000000000000125> | <http://www.foom.com/mathematical_concepts#00000000000000000157> | <http://www.foom.com/mathematical_concepts#00000000000000000063> | <http://www.foom.com/mathematical_concepts#00000000000000000117> | <http://www.foom.com/mathematical_concepts#00000000000000000221> | <http://www.foom.com/mathematical_concepts#00000000000000000210> | <http://www.foom.com/mathematical_concepts#00000000000000000249> | <http://www.foom.com/mathematical_concepts#00000000000000000223> | <http://www.foom.com/mathematical_concepts#00000000000000000111> | <http://www.foom.com/mathematical_concepts#00000000000000000113> | <http://www.foom.com/core/inProof> | <http://www.foom.com/mathematical_concepts#00000000000000000148> | <http://www.foom.com/mathematical_concepts#00000000000000000077> | <http://www.foom.com/mathematical_concepts#00000000000000000064> | <http://www.foom.com/mathematical_concepts#00000000000000000185> | <http://www.foom.com/mathematical_concepts#00000000000000000184> | <http://www.foom.com/mathematical_concepts#00000000000000000110> | <http://www.foom.com/mathematical_concepts#00000000000000000163> | <http://www.foom.com/mathematical_concepts#00000000000000000109> | <http://www.foom.com/mathematical_concepts#00000000000000000147> | <http://www.foom.com/mathematical_concepts#00000000000000000214> | <http://www.foom.com/mathematical_concepts#00000000000000000107> | <http://www.foom.com/core#00000000000000000035> | <http://www.foom.com/mathematical_concepts#00000000000000000211> | <http://www.foom.com/mathematical_concepts#00000000000000000220> | <http://www.foom.com/mathematical_concepts#00000000000000000155> | <http://www.foom.com/mathematical_concepts#00000000000000000080> | <http://www.foom.com/mathematical_concepts#00000000000000000146> | <http://www.foom.com/mathematical_concepts#00000000000000000154> | <http://www.foom.com/mathematical_concepts#00000000000000000239> | <http://www.foom.com/mathematical_concepts#00000000000000000209> | <http://www.foom.com/mathematical_concepts#00000000000000000108> | <http://www.foom.com/mathematical_concepts#00000000000000000114> | <http://www.foom.com/mathematical_concepts#00000000000000000112> | <http://www.foom.com/core#00000000000000000013> | <http://www.foom.com/mathematical_concepts#00000000000000000199> | <http://www.foom.com/mathematical_concepts#00000000000000000078> | <http://www.foom.com/mathematical_concepts#00000000000000000172> | <http://www.foom.com/core#00000000000000000000> | <http://www.foom.com/mathematical_concepts#00000000000000000124> | <http://www.foom.com/mathematical_concepts#00000000000000000149> | <http://www.foom.com/mathematical_concepts#00000000000000000123> | <http://www.foom.com/mathematical_concepts#00000000000000000116> | <http://www.foom.com/mathematical_concepts#00000000000000000250> | <http://www.foom.com/mathematical_concepts#00000000000000000167>
                            )+
                                ?mid .
                        ?mid
                            (
                                <http://www.foom.com/mathematical_concepts#00000000000000000222> | <http://www.foom.com/mathematical_concepts#00000000000000000198> | <http://www.foom.com/mathematical_concepts#00000000000000000125> | <http://www.foom.com/mathematical_concepts#00000000000000000157> | <http://www.foom.com/mathematical_concepts#00000000000000000063> | <http://www.foom.com/mathematical_concepts#00000000000000000117> | <http://www.foom.com/mathematical_concepts#00000000000000000221> | <http://www.foom.com/mathematical_concepts#00000000000000000210> | <http://www.foom.com/mathematical_concepts#00000000000000000249> | <http://www.foom.com/mathematical_concepts#00000000000000000223> | <http://www.foom.com/mathematical_concepts#00000000000000000111> | <http://www.foom.com/mathematical_concepts#00000000000000000113> | <http://www.foom.com/core/inProof> | <http://www.foom.com/mathematical_concepts#00000000000000000148> | <http://www.foom.com/mathematical_concepts#00000000000000000077> | <http://www.foom.com/mathematical_concepts#00000000000000000064> | <http://www.foom.com/mathematical_concepts#00000000000000000185> | <http://www.foom.com/mathematical_concepts#00000000000000000184> | <http://www.foom.com/mathematical_concepts#00000000000000000110> | <http://www.foom.com/mathematical_concepts#00000000000000000163> | <http://www.foom.com/mathematical_concepts#00000000000000000109> | <http://www.foom.com/mathematical_concepts#00000000000000000147> | <http://www.foom.com/mathematical_concepts#00000000000000000214> | <http://www.foom.com/mathematical_concepts#00000000000000000107> | <http://www.foom.com/core#00000000000000000035> | <http://www.foom.com/mathematical_concepts#00000000000000000211> | <http://www.foom.com/mathematical_concepts#00000000000000000220> | <http://www.foom.com/mathematical_concepts#00000000000000000155> | <http://www.foom.com/mathematical_concepts#00000000000000000080> | <http://www.foom.com/mathematical_concepts#00000000000000000146> | <http://www.foom.com/mathematical_concepts#00000000000000000154> | <http://www.foom.com/mathematical_concepts#00000000000000000239> | <http://www.foom.com/mathematical_concepts#00000000000000000209> | <http://www.foom.com/mathematical_concepts#00000000000000000108> | <http://www.foom.com/mathematical_concepts#00000000000000000114> | <http://www.foom.com/mathematical_concepts#00000000000000000112> | <http://www.foom.com/core#00000000000000000013> | <http://www.foom.com/mathematical_concepts#00000000000000000199> | <http://www.foom.com/mathematical_concepts#00000000000000000078> | <http://www.foom.com/mathematical_concepts#00000000000000000172> | <http://www.foom.com/core#00000000000000000000> | <http://www.foom.com/mathematical_concepts#00000000000000000124> | <http://www.foom.com/mathematical_concepts#00000000000000000149> | <http://www.foom.com/mathematical_concepts#00000000000000000123> | <http://www.foom.com/mathematical_concepts#00000000000000000116> | <http://www.foom.com/mathematical_concepts#00000000000000000250> | <http://www.foom.com/mathematical_concepts#00000000000000000167>
                            )*
                                ?end ;
                            rdfs:label ?mid_label .
                        ?end
                            rdfs:label ?end_label .
                        }}
                    GROUP BY 
                        ?mid ?mid_label 
                        ?end ?end_label 
                }}
                {{
                    SELECT DISTINCT
                        ?mid ?p ?p_label
                    WHERE {{
                        ?mid 
                            ?p ?end .
                        ?p rdfs:label ?p_label .
                        }}
                }}
            }}
            GROUP BY 
                ?mid ?mid_label 
                ?p ?p_label 
                ?end ?end_label
    """

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


def query_find_proof_steps(proof_iri: str):
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
