import pandas as pd
import rdflib

import modules.utils as utils
import modules.concepts as concepts

# common IRIs
rdf_type = rdflib.RDF.type
rdfs_label = rdflib.RDFS.label
rdfs_subclassof = rdflib.RDFS.subClassOf
skos_prefLabel = rdflib.SKOS.prefLabel
skos_altLabel = rdflib.SKOS.altLabel
owl_class = rdflib.OWL.Class
owl_individual = rdflib.OWL.NamedIndividual
owl_object_property = rdflib.OWL.ObjectProperty
owl_data_property = rdflib.OWL.DatatypeProperty
owl_annotation_property = rdflib.OWL.AnnotationProperty

# classes IRIs
common_notion_class = utils.create_iri("Common notion", namespace="https://www.foom.com/core")
concept_class = utils.create_iri("Concept", namespace="https://www.foom.com/core")
enumeration_class = utils.create_iri("Enumeration", namespace="https://www.foom.com/core")
magnitude_class = utils.create_iri("Magnitude", namespace="https://www.foom.com/core")
operation_type_class = utils.create_iri("Operation type", namespace="https://www.foom.com/core")
operation_instance_class = utils.create_iri("Operation instance", namespace="https://www.foom.com/core")
proposition_type_class = utils.create_iri("Proposition type", namespace="https://www.foom.com/core")
relation_type_class = utils.create_iri("Relation type", namespace="https://www.foom.com/core")
relation_instance_class = utils.create_iri("Relation instance", namespace="https://www.foom.com/core")
set_class = utils.create_iri("Set", namespace="https://www.foom.com/core")
statement_class = utils.create_iri("Statement", namespace="https://www.foom.com/core")

# individual IRIs
elements_book_1 = rdflib.URIRef("https://www.foom.com/core#document__elements_book_1")

# object properties IRIs
elements_book_1 = utils.create_iri("Document: Elements Book 1", namespace="https://www.foom.com/core")
proposition_type_construction = utils.create_iri("Proposition type: Construction", namespace="https://www.foom.com/core")
proposition_type_theorem = utils.create_iri("Proposition type: Theorem", namespace="https://www.foom.com/core")

refers_to = utils.create_iri("refers to", namespace="https://www.foom.com/core")
definition_refers_to = utils.create_iri("definition refers to", namespace="https://www.foom.com/core")

has_conceptual_component = utils.create_iri("has conceptual component", namespace="https://www.foom.com/core")
is_conceptual_component_of = utils.create_iri("is conceptual component of", namespace="https://www.foom.com/core")

is_sub_concept_of = utils.create_iri("is sub-concept of", namespace="https://www.foom.com/core")
is_super_concept_of = utils.create_iri("is super-concept of", namespace="https://www.foom.com/core")

is_used_in_definition_of = utils.create_iri("is used in definition of", namespace="https://www.foom.com/core")
is_defined_in = utils.create_iri("is defined in", namespace="https://www.foom.com/core")

contains_definition_of = utils.create_iri("contains_definition_of", namespace="https://www.foom.com/core")
is_used_in = utils.create_iri("is used in", namespace="https://www.foom.com/core")

has_definition = utils.create_iri("has definition", namespace="https://www.foom.com/core")
defines = utils.create_iri("defines", namespace="https://www.foom.com/core")

has_subject = utils.create_iri("has subject", namespace="https://www.foom.com/core")
has_predicate = utils.create_iri("has predicate", namespace="https://www.foom.com/core")
has_object = utils.create_iri("has object", namespace="https://www.foom.com/core")

has_domain = utils.create_iri("has domain", namespace="https://www.foom.com/core")
is_domain_of = utils.create_iri("is domain of", namespace="https://www.foom.com/core")
has_range = utils.create_iri("has_range", namespace="https://www.foom.com/core")
is_range_of = utils.create_iri("is range of", namespace="https://www.foom.com/core")

has_statement = utils.create_iri("has statement", namespace="https://www.foom.com/core")
is_statement_of = utils.create_iri("is statement of", namespace="https://www.foom.com/core")

is_in = utils.create_iri("is in", namespace="https://www.foom.com/core")
contains = utils.create_iri("contains", namespace="https://www.foom.com/core")

def add_common_notions(kg: rdflib.Graph, 
                       input_file_path: str) -> rdflib.Graph:
    # read common notions data
    common_notions = pd.read_csv(input_file_path).fillna("")
    # add common notions elements and related data
    for i in common_notions.index:
        common_notion_preflabel = common_notions.at[i, "common_notion"].strip()
        common_notion_iri = utils.create_iri(common_notion_preflabel, namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, common_notion_preflabel, common_notion_iri, common_notion_class, "Common notion")
        # common notion is in Elements book 1
        kg.add((common_notion_iri, is_in, elements_book_1))
        kg.add((elements_book_1, contains, common_notion_iri))
        # add statement
        kg, statement_iri = add_statement(kg, common_notion_iri, common_notions.at[i, "statement"])
        # add relation instance
        if relation_instance := common_notions.at[i, "relation_instance"]:
            relation_instance_iri = utils.create_iri(f"Relation instance: {relation_instance}", namespace="https://www.foom.com/core")
            kg = add_relation_operation(kg, 
                                        statement_iri, 
                                        relation_instance, 
                                        relation_instance_iri,
                                        relation_instance_class, 
                                        "Relation instance", 
                                        common_notions.at[i, "relation_instance_concepts"].split(","),)
            # add relation type
            relation_type_preflabel = common_notions.at[i, "relation_type"]
            relation_type_iri = utils.create_iri(f"Relation type: {relation_type_preflabel}", namespace="https://www.foom.com/core")
            kg = concepts.add_triples(kg, relation_type_preflabel, relation_type_iri, relation_type_class, "Relation type")
            kg.add((relation_instance_iri, refers_to, relation_type_iri))
            kg.add((relation_type_iri, is_used_in, relation_instance_iri))
            kg = add_concepts(kg, common_notions.at[i, "relation_type_concepts"].split(","), relation_type_iri)
        # add operation instance
        if operation_instance := common_notions.at[i, "operation_instance"]:
            operation_instance_iri = utils.create_iri(f"Operation instance: {operation_instance}", namespace="https://www.foom.com/core")
            kg = add_relation_operation(kg, 
                                        statement_iri, 
                                        operation_instance, 
                                        operation_instance_iri,
                                        operation_instance_class, 
                                        "Operation instance", 
                                        common_notions.at[i, "operation_instance_concepts"].split(","), 
                                        common_notions.at[i, "operation_instance_start"], 
                                        common_notions.at[i, "operation_instance_end"])
            # add operation type
            operation_type_preflabel = common_notions.at[i, "operation_type"]
            operation_type_iri = utils.create_iri(f"Operation type: {operation_type_preflabel}", namespace="https://www.foom.com/core")
            kg = concepts.add_triples(kg, operation_type_preflabel, operation_type_iri, operation_type_class, "Operation type")
            kg.add((operation_instance_iri, refers_to, operation_type_iri))
            kg.add((operation_type_iri, is_used_in, operation_instance_iri))
            if domain := common_notions.at[i, "operation_type_start"]:
                kg = add_domain_range(kg, operation_type_iri, domain, common_notions.at[i, "operation_type_end"])
    return kg

def add_relation_operation(kg: rdflib.Graph,
                           common_notion_iri: rdflib.URIRef,
                           item_preflabel: str,
                           item_iri: rdflib.URIRef,
                           class_iri: rdflib.URIRef,
                           prefix: str,
                           list_of_concepts: list,
                        #    item_type: str,
                        #    list_of_concepts_type: list,
                        #    prefix_type: str,
                           domain: str="",
                           range: str="",
                        #    add_type: bool=True
                           ) -> rdflib.Graph:
    # item_iri = utils.create_iri(f"{prefix}: {item_preflabel}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, item_preflabel, item_iri, class_iri, prefix)
    kg.add((common_notion_iri, refers_to, item_iri))
    kg.add((item_iri, is_used_in, common_notion_iri))
    # add concepts
    kg = add_concepts(kg, list_of_concepts, item_iri)
    # add domain and range
    if domain:
        kg = add_domain_range(kg, item_iri, domain, range)
    return kg

def add_concepts(kg: rdflib.Graph,
                 list_concepts: list,
                 item_iri: rdflib.URIRef) -> rdflib.Graph:
    for concept in list_concepts:
        concept_iri = utils.create_iri(f"Concept: {concept}", namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, concept, concept_iri, concept_class, "Concept")
        kg.add((item_iri, refers_to, concept_iri))
        kg.add((concept_iri, is_used_in, item_iri))
    return kg

def add_domain_range(kg: rdflib.Graph,
                     item_iri: rdflib.URIRef,
                     domain: str,
                     range: str) -> rdflib.Graph:
    # add domain
    domain_item_iri = utils.create_iri(f"Set: {domain}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, domain, domain_item_iri, set_class, "Set")
    kg.add((item_iri, has_domain, domain_item_iri))
    kg.add((domain_item_iri, is_domain_of, item_iri))
    # add range
    range_item_iri = utils.create_iri(f"Set: {range}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, range, range_item_iri, set_class, "Set")
    kg.add((item_iri, has_range, range_item_iri))
    kg.add((range_item_iri, is_range_of, item_iri))    
    return kg

def add_item_concepts(kg: rdflib.Graph,
                      item_iri: rdflib.URIRef,
                      list_of_concepts: list) -> rdflib.Graph:
    for concept in list_of_concepts:
        concept_preflabel = concept.strip().capitalize()
        concept_iri = utils.create_iri(f"Concept: {concept_preflabel}", namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, concept_preflabel, concept_iri, concept_class, "Concept")
        kg.add((item_iri, refers_to, concept_iri))
        kg.add((concept_iri, is_used_in, item_iri))
    return kg

def add_statement(kg: rdflib.Graph,
                  common_notion_iri: rdflib.URIRef,
                  statement_preflabel: str) -> rdflib.Graph:
    statement_iri = utils.create_iri(f"Statement: {statement_preflabel}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, statement_preflabel, statement_iri, statement_class, "Statement")
    kg.add((common_notion_iri, has_statement, statement_iri))
    kg.add((statement_iri, is_statement_of, common_notion_iri))
    return kg, statement_iri