
"""
propositions_module.py

This module is part of a knowledge graph framework designed to represent and manage propositions
and related concepts from Book 1 of Euclid's Elements. It provides functionality to add various
components to an RDF-based knowledge graph, including propositions, implications, givens,
relations, operations, gists, and morals.

Key Features:
- **Proposition Management**: Functions to add propositions with their types (e.g., construction, theorem).
- **Implication Handling**: Methods to incorporate implications and associated concepts.
- **Given Concepts Integration**: Capabilities to add given concepts related to propositions.
- **Relation and Operation Instances**: Support for adding relation and operation instances.
- **Gist and Moral Inclusion**: Functions to include gists and morals associated with propositions.
- **CSV Input Parsing**: Reads propositions data from CSV files to populate the knowledge graph.
- **Ontology Output**: Exports the constructed ontology in Turtle format.

Classes and IRIs Utilized:
- **Common RDF Vocabularies**: RDF, RDFS, SKOS, OWL.
- **Custom Ontology Classes and Properties**: Defined within the 'https://www.foom.com/core' namespace.

License:
This code is licensed under the MIT License.

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
common_notion_class = utils.create_iri("Common notion", namespace="https://www.foom.com/core")
concept_class = utils.create_iri("Concept", namespace="https://www.foom.com/core")
enumeration_class = utils.create_iri("Enumeration", namespace="https://www.foom.com/core")
implication_class = utils.create_iri("Implication", namespace="https://www.foom.com/core")
magnitude_class = utils.create_iri("Magnitude", namespace="https://www.foom.com/core")
operation_type_class = utils.create_iri("Operation type", namespace="https://www.foom.com/core")
operation_instance_class = utils.create_iri("Operation instance", namespace="https://www.foom.com/core")
proposition_class = utils.create_iri("Proposition", namespace="https://www.foom.com/core")
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

has_implication = utils.create_iri("has implication", namespace="https://www.foom.com/core")
is_implication_of = utils.create_iri("is implication of", namespace="https://www.foom.com/core")

is_in = utils.create_iri("is in", namespace="https://www.foom.com/core")
contains = utils.create_iri("contains", namespace="https://www.foom.com/core")

has_given_concept = utils.create_iri("has given concept", namespace="https://www.foom.com/core")
is_given_concept_of = utils.create_iri("is given concept of", namespace="https://www.foom.com/core")

has_gist = utils.create_iri("has gist", namespace="https://www.foom.com/core")
is_gist_of = utils.create_iri("is gist of", namespace="https://www.foom.com/core")

has_moral = utils.create_iri("has moral", namespace="https://www.foom.com/core")
is_moral_of = utils.create_iri("is moral of", namespace="https://www.foom.com/core")



def add_propositions(kg: rdflib.Graph,
                     propositions_input_file_path: str) -> rdflib.Graph:
    """
    Populate the knowledge graph with propositions and their related components.

    This function reads propositions data from a CSV file and adds corresponding
    propositions, implications, givens, relation instances, operation instances,
    gists, and morals to the provided RDF knowledge graph.

    Parameters:
        kg (rdflib.Graph): The RDF graph to be populated.
        propositions_input_file_path (str): Path to the CSV file containing propositions data.

    Returns:
        rdflib.Graph: The updated RDF graph with added propositions and related components.
    """
    # read propositions data
    propositions = pd.read_csv(propositions_input_file_path).fillna("")
    for i in propositions.index:
        # add propositions
        proposition_preflabel = propositions.at[i, "proposition"].replace("_", " ").strip()
        proposition_iri = utils.create_iri(proposition_preflabel, namespace="https://www.foom.com/core")
        proposition_type = propositions.at[i, "proposition_type"]
        kg = add_proposition(kg, proposition_iri, proposition_preflabel, proposition_type)
        # add implications
        implication_preflabel = propositions.at[i, "implication"].strip()
        if implication_preflabel:
            implication_concepts = [concept.strip() for concept in propositions.at[i, "implication_concepts"].split(",")]
            kg = add_implications(kg, proposition_iri, implication_preflabel, implication_concepts)

        # add givens
        given_concepts = [concept.strip() for concept in propositions.at[i, "given_concepts"].split(",")]
        if given_concepts:
            kg = add_givens(kg, proposition_iri, given_concepts)

        # add relation instances
        relation_instance_preflabel = propositions.at[i, "relation_instance"].strip()
        if relation_instance_preflabel:
            kg = add_relation_operation_instance(kg, proposition_iri, relation_instance_preflabel, "Relation")

        # add operation instances
        operation_instance_preflabel = propositions.at[i, "operation_instance"].strip()
        if operation_instance_preflabel:
            kg = add_relation_operation_instance(kg, proposition_iri, operation_instance_preflabel, "Operation")

        # add gists
        gist_preflabel = propositions.at[i, "gist"].strip()
        if gist_preflabel:
            kg = add_gist_moral(kg, proposition_iri, gist_preflabel, "Gist")

        # add morals
        moral_preflabel = propositions.at[i, "moral"].strip()
        if moral_preflabel:
            kg = add_gist_moral(kg, proposition_iri, moral_preflabel, "Moral")

    return kg

def add_gist_moral(kg: rdflib.Graph,
                   proposition_iri: rdflib.URIRef,
                   item_preflabel: str,
                   item_type: str) -> rdflib.Graph:
    """
    Add a gist or moral to a proposition in the knowledge graph.

    Depending on the specified item type ('Gist' or 'Moral'), this function creates
    the corresponding concept and establishes relationships between the proposition
    and the gist or moral within the RDF graph.

    Parameters:
        kg (rdflib.Graph): The RDF graph to be updated.
        proposition_iri (rdflib.URIRef): IRI of the proposition to which the gist or moral is related.
        item_preflabel (str): Preferred label for the gist or moral.
        item_type (str): Type of the item, either 'Gist' or 'Moral'.

    Returns:
        rdflib.Graph: The updated RDF graph with the added gist or moral.
    """
    item_iri = utils.create_iri(f"{item_type}: {item_preflabel}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, item_preflabel, item_iri, concept_class, item_type)
    if item_type == "Gist":
        kg.add((proposition_iri, has_gist, item_iri))
        kg.add((item_iri, is_gist_of, proposition_iri))
    elif item_type == "Moral":
        kg.add((proposition_iri, has_moral, item_iri))
        kg.add((item_iri, is_moral_of, proposition_iri))
    return kg

def add_relation_operation_instance(kg: rdflib.Graph,
                                    proposition_iri: rdflib.URIRef,
                                    item_instance_preflabel: str,
                                    type_name: str) -> rdflib.Graph:
    """
    Add a relation or operation instance to a proposition in the knowledge graph.

    This function creates a relation or operation instance based on the provided type
    name and establishes relationships between the proposition and the instance within
    the RDF graph.

    Parameters:
        kg (rdflib.Graph): The RDF graph to be updated.
        proposition_iri (rdflib.URIRef): IRI of the proposition to which the instance is related.
        item_instance_preflabel (str): Preferred label for the relation or operation instance.
        type_name (str): Type of the instance, either 'Relation' or 'Operation'.

    Returns:
        rdflib.Graph: The updated RDF graph with the added relation or operation instance.
    """
    item_instance_iri = utils.create_iri(f"{type_name} instance: {item_instance_preflabel}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, item_instance_preflabel, item_instance_iri, relation_instance_class, "Relation instance")
    kg.add((proposition_iri, refers_to, item_instance_iri))
    kg.add((item_instance_iri, is_used_in, proposition_iri))
    return kg

def add_givens(kg: rdflib.Graph,
               proposition_iri: rdflib.URIRef,
               given_concepts: list) -> rdflib.Graph:
    """
    Add given concepts to a proposition in the knowledge graph.

    This function adds the specified given concepts to the proposition and establishes
    the appropriate relationships within the RDF graph.

    Parameters:
        kg (rdflib.Graph): The RDF graph to be updated.
        proposition_iri (rdflib.URIRef): IRI of the proposition to which the given concepts are related.
        given_concepts (list): List of given concepts to be added.

    Returns:
        rdflib.Graph: The updated RDF graph with the added given concepts.
    """
    for given_concept in given_concepts:
        given_concept_iri = utils.create_iri(f"Concept: {given_concept}", namespace="https://www.foom.com/core")
        kg.add((proposition_iri, has_given_concept, given_concept_iri))
        kg.add((given_concept_iri, is_given_concept_of, proposition_iri))
    return kg

def add_proposition(kg: rdflib.Graph,
                    proposition_iri: rdflib.URIRef,
                    proposition_preflabel: str,
                    proposition_type: str) -> rdflib.Graph:
    """
    Add a proposition to the knowledge graph.

    This function creates a proposition with the specified type (e.g., 'construction', 'theorem')
    and establishes relationships within the RDF graph.

    Parameters:
        kg (rdflib.Graph): The RDF graph to be updated.
        proposition_iri (rdflib.URIRef): IRI of the proposition to be added.
        proposition_preflabel (str): Preferred label for the proposition.
        proposition_type (str): Type of the proposition, e.g., 'construction' or 'theorem'.

    Returns:
        rdflib.Graph: The updated RDF graph with the added proposition.
    """
    kg = concepts.add_triples(kg, proposition_preflabel, proposition_iri, proposition_class, "Proposition")
    kg.add((proposition_iri, is_in, elements_book_1))
    kg.add((elements_book_1, contains, proposition_iri))
    if proposition_type == "construction":
        kg.add((proposition_iri, refers_to, proposition_type_construction))
        kg.add((proposition_type_construction, is_used_in, proposition_iri))
    elif proposition_type == "theorem": 
        kg.add((proposition_iri, refers_to, proposition_type_theorem))
        kg.add((proposition_type_theorem, is_used_in, proposition_iri))
    return kg

def add_implications(kg: rdflib.Graph,
                     proposition_iri: rdflib.URIRef,
                     implication_preflabel: str,
                     implication_concepts: list) -> rdflib.Graph:
    """
    Add implications to a proposition in the knowledge graph.

    This function creates an implication with the specified concepts and establishes
    relationships between the proposition and the implication within the RDF graph.

    Parameters:
        kg (rdflib.Graph): The RDF graph to be updated.
        proposition_iri (rdflib.URIRef): IRI of the proposition to which the implication is related.
        implication_preflabel (str): Preferred label for the implication.
        implication_concepts (list): List of concepts associated with the implication.

    Returns:
        rdflib.Graph: The updated RDF graph with the added implication.
    """
    # read propositions data
    implication_iri = utils.create_iri(f"Implication: {implication_preflabel}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, implication_preflabel, implication_iri, implication_class, "Implication")
    for concept in implication_concepts:
        concept_iri = utils.create_iri(concept, namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, concept, concept_iri, concept_class, "Concept")
        kg.add((proposition_iri, refers_to, concept_iri))
        kg.add((concept_iri, is_used_in, proposition_iri))
    kg.add((proposition_iri, has_implication, implication_iri))
    kg.add((implication_iri, is_implication_of, proposition_iri))
    return kg