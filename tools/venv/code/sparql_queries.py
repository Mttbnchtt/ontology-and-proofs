# %%time
################################
## FIND INFORMATION CONCERCING 
## THE CONCEPTUAL SPACE OF 
## A GIVEN PROOF STEP
################################

## select a proof step
# proof_step_iri:str = "<https://www.foom.com/pappus_proofAristotle#00000000000000000014>"
proof_step_analysis:dict = {"proof_step_iri": "<https://www.foom.com/pappus_proofAristotle#00000000000000000014>" }

# find label of proof step
def query_find_proof_step_label(proof_step_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT 
            ?proof_step_label
        WHERE {{
            {proof_step_iri} 
                rdfs:label ?proof_step_label .
        }}
    """
    return sparql_query

# find reification values of proof step
def query_find_reification_values(statement_iri:str):
    sparql_query:str = f"""
        SELECT DISTINCT
        ?subject_iri 
        ?subject_label
        ?predicate_iri
        ?predicate_label
        ?object_iri
        ?object_label 
    WHERE {{
        {statement_iri}
            <http://www.foom.com/core#00000000000000000087> ?subject_iri ;
            <http://www.foom.com/core#00000000000000000089> ?predicate_iri ;
            <http://www.foom.com/core#00000000000000000088> ?object_iri .
        ?subject_iri rdfs:label ?subject_label .
        ?predicate_iri rdfs:label ?predicate_label .
        ?object_iri rdfs:label ?object_label .
    }}
    """
    return sparql_query

# find the proof to which the given proof step belongs
def query_find_proof(proof_step_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT 
            ?proof_iri
            ?proof_label
        WHERE {{
            {proof_step_iri} 
                <http://www.foom.com/core/inProof> ?proof_iri .
            ?proof_iri 
                rdfs:label ?proof_label .
        }}
    """
    return sparql_query

## find information concerning the proof:
# 1. goal
# 2. conceptual items connected to the goal
# 3. statement to prove
# 4. conceptual items connected to the statement to prove
# 5. source that contains the proof
# 6. author of the proof
# 7. remaining conceptual space of the proof

# goal
def query_find_goals_of_proof(proof_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT 
            ?goal_iri
            ?goal_label
        WHERE {{
            ?goal_iri
                <http://www.foom.com/core#00000000000000000013> {proof_iri} ; # is goal of proof_iri 
                rdfs:label ?goal_label .
        }}
    """
    return sparql_query
    
## find preceding proofs steps
def query_find_antecedent_proof_steps(proof_step_iri:str,
                                      proof_iri:str) -> str:
    sparql_query:str = f"""
        SELECT 
            ?antecedent_iri
        WHERE {{
            {proof_step_iri}
                <http://www.foom.com/core#00000000000000000186> ?antecedent_iri .
            ?antecedent_iri <http://www.foom.com/core/inProof> {proof_iri} .
        }}
    """
    return sparql_query

## find the conceptual space of given statement
def query_find_mathematically_directly_related_items(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?directly_related_iri
            ?directly_related_label
        WHERE {{
            {statement_iri}
                <http://www.foom.com/mathematical_concepts#00000000000000000251>+ ?directly_related_iri . # has mathematical relation
            ?directly_related_iri
                rdfs:label ?directly_related_label .
        }}
    """
    return sparql_query

def query_find_mathematically_directly_related_items_reverse(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?directly_related_iri
            ?directly_related_label
        WHERE {{
            ?directly_related_iri 
                <http://www.foom.com/mathematical_concepts#00000000000000000251>+ {statement_iri} . # has mathematical relation
            ?directly_related_iri
                rdfs:label ?directly_related_label .
        }}
    """
    return sparql_query

def query_find_mathematically_indirectly_related_items(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?indirectly_related_iri
            ?indirectly_related_label
        WHERE {{
            {statement_iri}
                ?p ?o .
            ?o
                <http://www.foom.com/mathematical_concepts#00000000000000000251>+ ?indirectly_related_iri . # has mathematical relation
            ?indirectly_related_iri
                rdfs:label ?indirectly_related_label .
        }}
    """
    return sparql_query

def query_find_mathematically_indirectly_related_items_reverse(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?indirectly_related_iri
            ?indirectly_related_label
        WHERE {{
            ?s ?p {statement_iri} .
            ?s
                <http://www.foom.com/mathematical_concepts#00000000000000000251>+ ?indirectly_related_iri . # has mathematical relation
            ?indirectly_related_iri
                rdfs:label ?indirectly_related_label .
        }}
    """
    return sparql_query

def query_find_conceptually_directly_related_items(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?directly_related_iri
            ?directly_related_label
        WHERE {{
            {statement_iri}
                <http://www.foom.com/mathematical_concepts#00000000000000000153>+ ?directly_related_iri . # has conceptual relation
            ?directly_related_iri
                rdfs:label ?directly_related_label .
        }}
    """
    return sparql_query

def query_find_conceptually_directly_related_items_reverse(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?directly_related_iri
            ?directly_related_label
        WHERE {{
            ?directly_related_iri 
                <http://www.foom.com/mathematical_concepts#00000000000000000153>+ {statement_iri} . # has conceptual relation
            ?directly_related_iri
                rdfs:label ?directly_related_label .
        }}
    """
    return sparql_query

def query_find_conceptually_indirectly_related_items(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?indirectly_related_iri
            ?indirectly_related_label
        WHERE {{
            {statement_iri}
                ?p ?o .
            ?o
                <http://www.foom.com/mathematical_concepts#00000000000000000153>+ ?indirectly_related_iri . # has conceptual relation
            ?indirectly_related_iri
                rdfs:label ?indirectly_related_label .
        }}
    """
    return sparql_query

def query_find_conceptually_indirectly_related_items_reverse(statement_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT
            ?indirectly_related_iri
            ?indirectly_related_label
        WHERE {{
            ?s ?p {statement_iri} .
            ?s
                <http://www.foom.com/mathematical_concepts#00000000000000000153>+ ?indirectly_related_iri . # has conceptual relation
            ?indirectly_related_iri
                rdfs:label ?indirectly_related_label .
        }}
    """
    return sparql_query

def find_related_objects(proof_step_iri:str) -> str:
    sparql_query:str = f"""
        SELECT DISTINCT 
        ?object_iri
        ?object_label
        WHERE {{
            ?object_iri 
                a/rdfs:subClassOf+ <http://www.foom.com/core/Object> ;
                <http://www.foom.com/core#00000000000000000035> {proof_step_iri} ;
                rdfs:label ?object_label .
        }}
    """
    return sparql_query

## find analogous proofs 

## find analogous proof parts

## find other proofs or proof parts connected to the given proof step or proof

