"""
Module: concepts.py
Author: Matteo Bianchetti
Date: [Insert Date]
Description:
    This module defines functions to extract concepts and their definitions from a text file,
    and to add these concepts as RDF triples into a knowledge graph using the rdflib library.

Dependencies:
    - os
    - rdflib
    - re
    - modules.utils

Functions:
    - extract_definition_concepts: Parses lines of text to extract concepts, their definitions, and subconcepts.
    - add_triples: Adds triples related to a concept into a knowledge graph.
    - add_definition_concepts: Adds multiple concepts and their relationships to a knowledge graph.
    - add_definition: Adds definition-specific triples into a knowledge graph.
    - main_add_definition_concepts: Main function to process a file and update a knowledge graph.

Usage:
    This module is intended for processing ontological data and building RDF-based knowledge graphs.

License:
    MIT

Author:
    Matteo Bianchetti
"""

import os
import rdflib
import re

import modules.utils as utils

# common IRIs
rdf_type = rdflib.RDF.type
rdfs_label = rdflib.RDFS.label
skos_prefLabel = rdflib.SKOS.prefLabel
skos_altLabel = rdflib.SKOS.altLabel
owl_class = rdflib.OWL.Class
owl_individual = rdflib.OWL.NamedIndividual
owl_object_property = rdflib.OWL.ObjectProperty
owl_data_property = rdflib.OWL.DatatypeProperty
owl_annotation_property = rdflib.OWL.AnnotationProperty

concept_class = utils.create_iri("Concept", namespace="https://www.foom.com/core")
definition_refers_to = utils.create_iri("definition refers to", namespace="https://www.foom.com/core")
is_used_in_definition_of = utils.create_iri("is used in definition of", namespace="https://www.foom.com/core")
is_defined_in = utils.create_iri("is defined in", namespace="https://www.foom.com/core")
contains_definition_of = utils.create_iri("contains_definition_of", namespace="https://www.foom.com/core")
is_in = utils.create_iri("is in", namespace="https://www.foom.com/core")
has_definition = utils.create_iri("has definition", namespace="https://www.foom.com/core")
defines = utils.create_iri("defines", namespace="https://www.foom.com/core")


def extract_definition_concepts(lines: list) -> dict:
    """
    Extracts concepts, their definitions, and subconcepts from a list of lines.

    Args:
        lines (list): A list of strings where each string represents a line of text.

    Returns:
        dict: A dictionary where each key is a concept, and the value is a dictionary
              containing its definition and a list of subconcepts.
    """
    concepts = {line.split()[0]: {
            "definition": "",
            "subconcepts": []
        } for line in lines
    }
    for line in lines:
        items = line.split()
        concepts[items[0]]["definition"] = items[-1].replace("(", "").replace(")", "").replace("d", "").strip()
        concepts[items[0]]["subconcepts"] = [item.replace("[", "").replace("]", "").strip() for item in items[1:-1]]

    return concepts


def add_triples(kg: rdflib.Graph,
                concept: str,
                concept_iri: rdflib.URIRef,
                class_iri: rdflib.URIRef,
                prefix_label: str):
    """
    Adds RDF triples for a concept into a knowledge graph.

    Args:
        kg (rdflib.Graph): The knowledge graph to which triples are added.
        concept (str): The name of the concept.
        concept_iri (rdflib.URIRef): The IRI of the concept.
        class_iri (rdflib.URIRef): The IRI of the class the concept belongs to.
        prefix_label (str): A prefix to use for the concept label.

    Returns:
        rdflib.Graph: The updated knowledge graph with the new triples added.
    """
    kg.add((concept_iri, rdf_type, owl_individual))
    kg.add((concept_iri, rdfs_label, rdflib.Literal(f"{prefix_label}: {utils.capitalize_first_letter(concept)}")))
    kg.add((concept_iri, skos_prefLabel, rdflib.Literal(utils.capitalize_first_letter(concept))))
    kg.add((concept_iri, rdf_type, class_iri))
    return kg


def add_definition_concepts(kg: rdflib.Graph,
                            concepts: dict) -> rdflib.Graph:
    """
    Adds concepts and their relationships (definitions and subconcepts) to a knowledge graph.

    Args:
        kg (rdflib.Graph): The knowledge graph to which triples are added.
        concepts (dict): A dictionary of concepts with their definitions and subconcepts.

    Returns:
        rdflib.Graph: The updated knowledge graph with the new triples added.
    """
    for concept, concept_data in concepts.items():
        concept_iri = utils.create_iri(concept, namespace="https://www.foom.com/euclid")
        kg = add_triples(kg, concept, concept_iri, concept_class, "Concept")
        kg.add((concept_iri, is_defined_in, utils.create_iri("Elements Book 1", namespace="https://www.foom.com/euclid")))
        kg.add((utils.create_iri("Elements Book 1", namespace="https://www.foom.com/euclid"), contains_definition_of, concept_iri))
        for subconcept in concept_data["subconcepts"]:
            subconcept_label = subconcept.replace("~", "").replace(",", "").strip()
            subconcept_iri = utils.create_iri(subconcept_label, namespace="https://www.foom.com/euclid")
            kg = add_triples(kg, subconcept_label, subconcept_iri, concept_class, "Concept")
            kg.add((utils.create_iri(subconcept_label, namespace="https://www.foom.com/euclid"), is_used_in_definition_of, utils.create_iri(concept, namespace="https://www.foom.com/euclid")))
            kg.add((utils.create_iri(concept, namespace="https://www.foom.com/euclid"), is_used_in_definition_of, utils.create_iri(subconcept_label, namespace="https://www.foom.com/euclid")))
        definition_label = f"Definition: {concept_data['definition']}"
        definition_iri = utils.create_iri(definition_label, namespace="https://www.foom.com/euclid")
        kg = add_definition(kg, definition_label, definition_iri)
        kg.add((concept_iri, has_definition, definition_iri))
        kg.add((definition_iri, defines, concept_iri))
    return kg


def add_definition(kg: rdflib.Graph,
                   definition_label: str,
                   definition_iri: rdflib.URIRef) -> rdflib.Graph:
    """
    Adds a definition as RDF triples into a knowledge graph.

    Args:
        kg (rdflib.Graph): The knowledge graph to which triples are added.
        definition_label (str): The label of the definition.
        definition_iri (rdflib.URIRef): The IRI of the definition.

    Returns:
        rdflib.Graph: The updated knowledge graph with the definition triples added.
    """
    kg.add((definition_iri, rdf_type, owl_individual))
    kg.add((definition_iri, rdfs_label, rdflib.Literal(definition_label)))
    kg.add((definition_iri, rdf_type, utils.create_iri("Definition", namespace="https://www.foom.com/core")))
    kg.add((definition_iri, is_in, utils.create_iri("Elements Book 1", namespace="https://www.foom.com/euclid")))
    kg.add((definition_iri, skos_prefLabel, rdflib.Literal(definition_label)))

    return kg


def main_add_definition_concepts(file_path: str,
                                 kg: rdflib.Graph) -> rdflib.Graph:
    """
    Main function to process a file and add extracted concepts and their relationships
    to a knowledge graph.

    Args:
        file_path (str): The path to the file containing concept definitions.
        kg (rdflib.Graph): The knowledge graph to which triples are added.

    Returns:
        rdflib.Graph: The updated knowledge graph with the new triples added.
    """
    lines = utils.read_text_file(file_path)
    concepts = extract_definition_concepts(lines)
    kg = add_definition_concepts(kg, concepts)
    return kg