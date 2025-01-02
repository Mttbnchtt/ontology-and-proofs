import pandas as pd
import rdflib

import modules.utils as utils
import modules.statements_module as statements_module

rdf_type = rdflib.RDF.type
rdfs_label = rdflib.RDFS.label
skos_prefLabel = rdflib.SKOS.prefLabel

ELEMENTS_BOOK_1 = utils.create_iri("Document: Elements Book 1", namespace="https://www.foom.com/core")

IS_IN = utils.create_iri("is in", namespace="https://www.foom.com/core")
CONTAINS = utils.create_iri("contains", namespace="https://www.foom.com/core")

ONTOLOGY_NAMESPACE = "https://www.foom.com/core"
PROOF_CLASS = utils.create_iri("Proof", namespace=ONTOLOGY_NAMESPACE)
CONTAINS_CONCEPT = utils.create_iri("contains concept", namespace="https://www.foom.com/core")
IS_CONCEPT_IN = utils.create_iri("is concept in", namespace="https://www.foom.com/core")
REFERS_TO = utils.create_iri("refers to", namespace="https://www.foom.com/core")
IS_USED_IN = utils.create_iri("is used in", namespace="https://www.foom.com/core")
USES_REDUCTION = utils.create_iri("uses_reductio", namespace=ONTOLOGY_NAMESPACE)

def add_proofs(kg: rdflib.Graph,
               input_file_path: str,
               add_book_1: bool = True,
               add_statements: bool = False) -> rdflib.Graph:

    # read database of proofs
    proofs_df = pd.read_csv(input_file_path).fillna("")
    for _, row in proofs_df.iterrows():
        # add proof
        kg, proof_iri = add_proof(kg, row["proof"])

        # proof is in Elements book 1
        if add_book_1:
            kg.add((proof_iri, IS_IN, ELEMENTS_BOOK_1))
            kg.add((ELEMENTS_BOOK_1, CONTAINS, proof_iri))

        # add concepts
        if concepts := row["additional_proof_concepts"]:
            kg = add_concepts(kg, proof_iri, concepts)

        # add relation instance
        if relation_instance := row["relation_instance"]:
            kg = add_relation_instance(kg, relation_instance.strip(), proof_iri)

        # add operation instance
        if operation_instance := row["operation_instance"]:
            kg = add_operation_instance(kg, operation_instance.strip(), proof_iri)

        # add implicit operation instance
        if implicit_operation_instance := row["implicit_operation_instance"]:
            kg = add_operation_instance(kg, implicit_operation_instance.strip(), proof_iri)

        # add uses_reductio
        if uses_reductio := row["reductio"]:
            kg.add((proof_iri, USES_REDUCTION, rdflib.Literal("true", datatype=rdflib.XSD.boolean)))

        # add statements
        if add_statements:
            statement = row["statement"].strip()
            if statement.replace(" ", ""):
                kg, statement_iri = statements_module.add_statement(kg, statement)
                kg.add((proof_iri, REFERS_TO, statement_iri))
                kg.add((statement_iri, IS_USED_IN, proof_iri))

    return kg

def add_statements_to_proof(kg: rdflib.Graph,
                            proof_iri: rdflib.URIRef,
                            statements: str) -> rdflib.Graph:
    
    
    return kg

def add_proof(kg: rdflib.Graph,
              proof_number: str) -> rdflib.Graph:
    proof_label = f"Proof {proof_number}"
    proof_iri = utils.create_iri(proof_label, namespace=ONTOLOGY_NAMESPACE)
    kg.add((proof_iri, rdf_type, PROOF_CLASS))
    kg.add((proof_iri, rdfs_label, rdflib.Literal(proof_label)))
    kg.add((proof_iri, skos_prefLabel, rdflib.Literal(proof_number)))

    return kg, proof_iri

def add_concepts(kg: rdflib.Graph,
                 proof_iri: rdflib.URIRef,
                 concepts: str) -> rdflib.Graph:
    concepts_list = [concept.strip() for concept in concepts.split(",")]
    for concept in concepts_list:
        concept_iri = utils.create_iri(f"Concept: {concept}", namespace=ONTOLOGY_NAMESPACE)
        kg.add((proof_iri, CONTAINS_CONCEPT, concept_iri))
        kg.add((concept_iri, IS_CONCEPT_IN, proof_iri))

    return kg

def add_relation_instance(kg: rdflib.Graph,
                          relation_instance: str,
                          proof_iri: rdflib.URIRef) -> rdflib.Graph:
    relation_instance_iri = utils.create_iri(f"Relation instance: {relation_instance}", namespace=ONTOLOGY_NAMESPACE)
    kg.add((proof_iri, REFERS_TO, relation_instance_iri))
    kg.add((relation_instance_iri, IS_USED_IN, proof_iri))
            
    return kg

            
def add_operation_instance(kg: rdflib.Graph,
                           operation_instance: str,
                           proof_iri: rdflib.URIRef) -> rdflib.Graph:
    operation_instance_instance_iri = utils.create_iri(f"Operation instance: {operation_instance}", namespace=ONTOLOGY_NAMESPACE)
    kg.add((proof_iri, REFERS_TO, operation_instance_instance_iri))
    kg.add((operation_instance_instance_iri, IS_USED_IN, proof_iri))
            
    return kg