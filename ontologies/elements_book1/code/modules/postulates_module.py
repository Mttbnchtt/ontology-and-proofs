"""
Module: postulates_module.py
Author: [Your Name]
Date: [Insert Date]
Description:
    This module provides functions to define and manage postulates within an RDF knowledge graph.
    It includes functionality to add postulates as RDF triples and to ensure their logical consistency.

Dependencies:
    - os
    - rdflib
    - re
    - modules.utils

Functions:
    - extract_postulates: Parses lines of text to extract postulates and their logical components.
    - add_postulate_triples: Adds RDF triples related to a postulate into a knowledge graph.
    - validate_postulates: Checks the logical consistency of postulates within the knowledge graph.
    - main_add_postulates: Main function to process a file and update a knowledge graph with postulates.

Usage:
    This module is intended for processing postulates and integrating them into RDF-based knowledge graphs.

License:
    MIT

Author:
    Matteo Bianchetti
"""

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
concept_class = utils.create_iri("Concept", namespace="https://www.foom.com/core")
enumeration_class = utils.create_iri("Enumeration", namespace="https://www.foom.com/core")
magnitude_class = utils.create_iri("Magnitude", namespace="https://www.foom.com/core")
operation_type_class = utils.create_iri("Operation type", namespace="https://www.foom.com/core")
operation_instance_class = utils.create_iri("Operation instance", namespace="https://www.foom.com/core")
proposition_type_class = utils.create_iri("Proposition type", namespace="https://www.foom.com/core")
relation_type_class = utils.create_iri("Relation type", namespace="https://www.foom.com/core")
relation_instance_class = utils.create_iri("Relation instance", namespace="https://www.foom.com/core")
set_class = utils.create_iri("Set", namespace="https://www.foom.com/core")

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

is_in = utils.create_iri("is in", namespace="https://www.foom.com/core")
contains = utils.create_iri("contains", namespace="https://www.foom.com/core")


CONTAINS_CONCEPT = utils.create_iri("contains concept", namespace=ONTOLOGY_NAMESPACE)
IS_CONCEPT_IN = utils.create_iri("is concept in", namespace=ONTOLOGY_NAMESPACE)


def add_postulates(kg: rdflib.Graph,
                   input_file_path: str) -> rdflib.Graph:
    """
    Adds postulates, relations, operations, and concept hierarchies to an RDF knowledge graph.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        input_file_path (str): Path to the CSV file containing postulate data.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    postulates = pd.read_csv(input_file_path).fillna("")

    # add postulates
    kg = add_postulate_triples(kg, postulates)

    # add relations
    kg = add_relations(kg, postulates)

    # add operations
    kg = add_operations(kg, postulates)

    # add concept hierarchy
    kg = add_concept_hierarchy(kg, postulates)

    return kg

def add_concept_hierarchy(kg: rdflib.Graph,
                          postulates: pd.DataFrame) -> rdflib.Graph:
    """
    Adds a hierarchy of concepts to the RDF knowledge graph.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        postulates (pd.DataFrame): DataFrame containing hierarchy information.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph with concept hierarchy.
    """
    for i in postulates.index:
        if hierarchy_items := postulates.at[i, "hierarchy_of_concepts"]:
            hierarchy_items = [hierarchy_item.strip() for hierarchy_item in hierarchy_items.split(",")]
            for hierarchy_item in hierarchy_items:
                concepts_pair = hierarchy_item.split("->")
                subconcept = concepts_pair[0].strip()
                superconcept = concepts_pair[1].strip()
                subconcept_iri = utils.create_iri(f"Concept: {subconcept}", namespace="https://www.foom.com/core")
                superconcept_iri = utils.create_iri(f"Concept: {superconcept}", namespace="https://www.foom.com/core")
                kg.add((subconcept_iri, is_sub_concept_of, superconcept_iri))
                kg.add((superconcept_iri, is_super_concept_of, subconcept_iri))
    return kg

def add_relation_operation_triples(kg: rdflib.Graph,
                                  main_iri: rdflib.URIRef,
                                  main_preflabel: str,
                                  class_iri: rdflib.Graph,
                                  thing_that_refers: rdflib.Graph,
                                  prefix_class: str) -> rdflib.Graph:
    """
    Adds triples representing a relation or operation instance.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        main_iri (rdflib.URIRef): IRI of the main entity.
        main_preflabel (str): Preferred label of the entity.
        class_iri (rdflib.Graph): IRI of the class the entity belongs to.
        thing_that_refers (rdflib.Graph): Entity referring to the main entity.
        prefix_class (str): Prefix indicating the entity class.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    kg.add((main_iri, rdf_type, owl_individual))
    kg.add((main_iri, rdf_type, class_iri))
    kg.add((main_iri, rdfs_label, rdflib.Literal(f"{prefix_class}: {main_preflabel}")))
    kg.add((main_iri, skos_prefLabel, rdflib.Literal(main_preflabel)))
    kg.add((thing_that_refers, refers_to, main_iri))
    kg.add((main_iri, is_used_in, thing_that_refers))
    return kg

def add_relation_operation_concept_triples(kg: rdflib.Graph,
                                           list_of_concepts: list,
                                           thing_that_refers: rdflib.Graph) -> rdflib.Graph:
    """
    Adds RDF triples linking concepts to a referring entity.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        list_of_concepts (list): List of concept labels to link.
        thing_that_refers (rdflib.Graph): Entity that refers to the concepts.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    for concept in list_of_concepts:
            concept_preflabel = concept.strip()
            concept_iri = utils.create_iri(f"Concept: {concept_preflabel}", namespace="https://www.foom.com/core")
            kg = concepts.add_triples(kg, concept_preflabel, concept_iri, concept_class, "Concept")
            kg.add((thing_that_refers, CONTAINS_CONCEPT, concept_iri))
            kg.add((concept_iri, IS_CONCEPT_IN, thing_that_refers))
    return kg

def add_relations(kg: rdflib.Graph,
                  postulates: pd.DataFrame) -> rdflib.Graph:
    """
    Adds relations and their associated metadata to the RDF knowledge graph.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        postulates (pd.DataFrame): DataFrame containing postulate data and relations.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    for i in postulates.index:
        postulate = postulates.at[i, "postulate_name"].strip()
        postulate_iri = utils.create_iri(postulate, namespace="https://www.foom.com/core")
        # add relation instance
        relation_preflabel = postulates.at[i, "relations"].strip()
        if relation_preflabel:
            relation_iri = utils.create_iri(f"Relation instance: {relation_preflabel}", namespace="https://www.foom.com/core")
            kg = add_relation_operation_triples(kg, relation_iri, relation_preflabel, relation_instance_class, postulate_iri, "Relation instance")
            # add links between relation instance and concepts
            kg = add_relation_operation_concept_triples(kg, postulates.at[i, "relations_concepts"].split(","), relation_iri)
            # add relation types
            relation_type_preflabel = postulates.at[i, "relation_types"].strip()
            relation_type_iri = utils.create_iri(f"Relation type: {relation_type_preflabel}", namespace="https://www.foom.com/core")
            kg = add_relation_operation_triples(kg, relation_type_iri, relation_type_preflabel, relation_type_class, relation_iri, "Relation type")
            # add links between relation types and concepts
            kg = add_relation_operation_concept_triples(kg, postulates.at[i, "relation_type_concepts"].split(","), relation_type_iri)
    return kg

def add_operations(kg: rdflib.Graph,
                   postulates: dict) -> rdflib.Graph:
    """
    Adds operations and their associated metadata to the RDF knowledge graph.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        postulates (pd.DataFrame): DataFrame containing postulate data and operations.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    for i in postulates.index:
        postulate = postulates.at[i, "postulate_name"].strip()
        postulate_iri = utils.create_iri(postulate, namespace="https://www.foom.com/core")
        operation_prelabel = postulates.at[i, "operations"].replace(" -> ", "->").strip()
        # add operation instance
        if operation_prelabel:
            operation_iri = utils.create_iri(f"Operation: {operation_prelabel}", namespace="https://www.foom.com/core")
            kg = add_relation_operation_triples(kg, operation_iri, operation_prelabel, operation_instance_class, postulate_iri, "Operation instance")
            # add links between operation instance and concepts
            kg = add_relation_operation_concept_triples(kg, postulates.at[i, "operations_concepts"].split(","), operation_iri)
            # add domain and range to operation instance
            kg = add_domain_range(kg, postulates, "operations", operation_iri, postulates.at[i, "operations_start"].strip(), postulates.at[i, "operations_end"].strip())
            # add operation types
            operation_type_prelabel = postulates.at[i, "operations_types"].strip()
            operation_type_iri = utils.create_iri(f"Operation type: {operation_type_prelabel}", namespace="https://www.foom.com/core")
            kg = add_relation_operation_triples(kg, operation_type_iri, operation_type_prelabel, operation_type_class, operation_iri, "Operation type")
            # add links between operation types and concepts
            kg = add_relation_operation_concept_triples(kg, postulates.at[i, "operation_type_concepts"].split(","), operation_type_iri)
            # add domain and range to operation types
            kg = add_domain_range(kg, postulates, "operations_type", operation_type_iri, postulates.at[i, "operations_type_start"].strip(), postulates.at[i, "operations_type_end"].strip())
    return kg

def add_domain_range(kg: rdflib.Graph,
                     postulates: pd.DataFrame,
                     main_column: str,
                     main_operation_iri: rdflib.URIRef,
                     domain_preflabel: str,
                     range_preflabel: str) -> rdflib.Graph:
    """
    Adds domain and range information for a given operation or type.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        postulates (pd.DataFrame): DataFrame containing postulate data.
        main_column (str): Column name representing the main operation type.
        main_operation_iri (rdflib.URIRef): IRI of the main operation.
        domain_preflabel (str): Preferred label for the domain.
        range_preflabel (str): Preferred label for the range.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    if domain_preflabel:
        domain_iri = utils.create_iri(f"Set: {domain_preflabel}", namespace="https://www.foom.com/core")
        range_iri = utils.create_iri(f"Set: {range_preflabel}", namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, domain_preflabel, domain_iri, set_class, "Set")
        kg = concepts.add_triples(kg, range_preflabel, range_iri, set_class, "Set")
        kg.add((main_operation_iri, has_domain, domain_iri))
        kg.add((domain_iri, is_domain_of, main_operation_iri))
        kg.add((main_operation_iri, has_range, range_iri))
        kg.add((range_iri, is_range_of, main_operation_iri))
    return kg


def add_postulate_triples(kg: rdflib.Graph,
                          postulates: pd.DataFrame) -> rdflib.Graph:
    """
    Adds RDF triples representing postulates to the knowledge graph.

    Args:
        kg (rdflib.Graph): The RDF knowledge graph to update.
        postulates (pd.DataFrame): DataFrame containing postulate data.

    Returns:
        rdflib.Graph: Updated RDF knowledge graph.
    """
    for i in postulates.index:
        postulate = postulates.at[i, "postulate_name"].strip()
        postulate_iri = utils.create_iri(postulate, namespace="https://www.foom.com/core")
        postulate_label = rdflib.Literal(postulate.replace("_", " "))
        kg.add((postulate_iri, rdfs_label, rdflib.Literal(postulate_label)))
        kg.add((postulate_iri, rdf_type, owl_individual))
        kg.add((postulate_iri, rdf_type, utils.create_iri("Postulate", namespace="https://www.foom.com/core")))
        kg.add((postulate_iri, rdfs_label, postulate_label))
        kg.add((postulate_iri, skos_prefLabel, postulate_label))
        # postulate is in Elements book 1
        kg.add((postulate_iri, is_in, elements_book_1))
        kg.add((elements_book_1, contains, postulate_iri))
    return kg