import pandas as pd
import rdflib

RELATIONS_INPUT_FILE_PATH = "input/Euclid.RelationsAnalysis.Book1.csv"
OPERATIONS_INPUT_FILE_PATH = "input/Euclid.OperationsAnalysis.Book1.csv"

ONTOLOGY_NAMESPACE = "https://www.foom.com/core"
CONCEPT_CLASS = utils.create_iri("Concept", namespace=ONTOLOGY_NAMESPACE)
CONTAINS_CONCEPT = utils.create_iri("contains concept", namespace=ONTOLOGY_NAMESPACE)
IS_CONCEPT_IN = utils.create_iri("is concept in", namespace=ONTOLOGY_NAMESPACE)
OPERATION_INSTANCE_CLASS = utils.create_iri("Operation instance", namespace=ONTOLOGY_NAMESPACE)
OPERATION_TYPE_CLASS = utils.create_iri("Operation type", namespace=ONTOLOGY_NAMESPACE)
RELATION_INSTANCE_CLASS = utils.create_iri("Relation instance", namespace=ONTOLOGY_NAMESPACE)
RELATION_TYPE_CLASS = utils.create_iri("Relation type", namespace=ONTOLOGY_NAMESPACE)

def add_relations_operations(kg: rdflib.Graph,
                             input_file_path: str,
                             item_type: typing.Literal["relations", "operations"]) -> rdflib.Graph:
    items_df = pd.read_csv(input_file_path).fillna("")
    for _, row in items_df.iterrows():

        if item_type == "relations":
            instance_pref_label = row["relation_instance"].strip().capitalize()
            type_pref_label = row["relation_type"].strip().capitalize()
            kg, instance_iri, type_iri = add_relation_instance_type(kg, instance_pref_label, type_pref_label, "Relation instance", "Relation type")

            # find concepts in instance and in type and add them to the graph
            kg = add_concepts(kg, instance_iri, instance_pref_label)
            kg = add_concepts(kg, type_iri, type_pref_label)

        elif item_type == "operations":
            instance_pref_label = row["operation_instance"].strip().capitalize()
            type_pref_label = row["operation_type"].strip().capitalize()
            kg, instance_iri, type_iri = add_operation_instance_type(kg, instance_pref_label, type_pref_label, "Operation instance", "Operation type")

            # find concepts in instance and in type and add them to the graph
            kg = add_concepts(kg, instance_iri, instance_pref_label)
            kg = add_concepts(kg, type_iri, type_pref_label)

        else:
            raise ValueError(f"Invalid item type: {item_type}")

    return kg

def find_concepts(item_pref_label: str) -> set:
    item_pref_label_v1 = item_pref_label.replace("(", " ").replace(")", " ").replace(",", " ")

    return {concept.strip() for concept in item_pref_label_v1.split()}


def add_concepts(kg: rdflib.Graph,
                 item_iri: rdflib.URIRef,
                 item_pref_label: str) -> rdflib.Graph:
    concepts = find_concepts(item_pref_label)

    for concept in concepts:
        concept_iri = utils.create_iri(f"Concept: {concept}", namespace=ONTOLOGY_NAMESPACE)
        kg.add((item_iri, CONTAINS_CONCEPT, concept_iri))
        kg.add((concept_iri, IS_CONCEPT_IN, item_iri))

    return kg

def add_basic_triples(kg: rdflib.Graph,
                      pref_label: str,
                      class_iri: rdflib.URIRef,
                      prefix: str) -> rdflib.Graph:
    item_label = f"{prefix}: {pref_label}"
    item_iri = utils.create_iri(item_label, namespace=ONTOLOGY_NAMESPACE)
    kg.add((item_iri, rdf_type, class_iri))
    kg.add((item_iri, rdfs_label, rdflib.Literal(item_label)))
    kg.add((item_iri, skos_prefLabel, rdflib.Literal(pref_label)))

    return kg, item_iri

def add_relation_instance_type(kg: rdflib.Graph,
                               relation_instance_pref_label: str,
                               relation_type_pref_label: str,
                               prefix_instance: str,
                               prefix_type: str) -> rdflib.Graph:

    kg, instance_iri = add_basic_triples(kg, relation_instance_pref_label, RELATION_INSTANCE_CLASS, prefix_instance)
    kg, type_iri = add_basic_triples(kg, relation_type_pref_label, RELATION_TYPE_CLASS, prefix_type)

    kg.add((instance_iri, HAS_RELATION_TYPE, type_iri))
    kg.add((type_iri, IS_RELATION_TYPE_OF, instance_iri))

    return kg, instance_iri, type_iri

def add_operation_instance_type(kg: rdflib.Graph,
                                operation_instance_pref_label: str,
                                operation_type_pref_label: str,
                                prefix_instance: str,
                                prefix_type: str) -> rdflib.Graph:
    kg, instance_iri = add_basic_triples(kg, operation_instance_pref_label, OPERATION_INSTANCE_CLASS, prefix_instance)
    kg, type_iri = add_basic_triples(kg, operation_type_pref_label, OPERATION_TYPE_CLASS, prefix_type)

    kg.add((instance_iri, HAS_RELATION_TYPE, type_iri))
    kg.add((type_iri, IS_RELATION_TYPE_OF, instance_iri))

    return kg, instance_iri, type_iri