"""
This module is part of the ontology-and-proofs project. It provides functions for managing and 
adding concepts, concept types, and hierarchies to a knowledge graph using RDF and OWL standards. 
The main goal of this module is to streamline the process of integrating conceptual data and 
associated properties into the ontology for reasoning and knowledge representation.

Key functionalities:
- Adding concept types, concepts, and their hierarchies.
- Associating datatype properties with concepts.
- Managing relationships between concepts, such as hierarchy or type relations.
"""

import pandas as pd
import rdflib

import modules.utils as utils
import modules.concepts as concepts
import modules.tbox as tbox

# common IRIs
rdf_type = rdflib.RDF.type
rdfs_label = rdflib.RDFS.label
rdfs_subclassof = rdflib.RDFS.subClassOf
rdfs_range = rdflib.RDFS.range
skos_prefLabel = rdflib.SKOS.prefLabel
skos_altLabel = rdflib.SKOS.altLabel
owl_class = rdflib.OWL.Class
owl_individual = rdflib.OWL.NamedIndividual
owl_object_property = rdflib.OWL.ObjectProperty
owl_data_property = rdflib.OWL.DatatypeProperty
owl_annotation_property = rdflib.OWL.AnnotationProperty
xsd_boolean = rdflib.XSD.boolean
xsd_true = rdflib.Literal("true", datatype=xsd_boolean)
xsd_false = rdflib.Literal("false", datatype=xsd_boolean)

# classes IRIs
ONTOLOGY_NAMESPACE = "https://www.foom.com/core"
common_notion_class = utils.create_iri("Common notion", namespace="https://www.foom.com/core")
concept_class = utils.create_iri("Concept", namespace="https://www.foom.com/core")
concept_type_class = utils.create_iri("Concept type", namespace="https://www.foom.com/core")
gist_class = utils.create_iri("Gist", namespace="https://www.foom.com/core")
enumeration_class = utils.create_iri("Enumeration", namespace="https://www.foom.com/core")
implication_class = utils.create_iri("Implication", namespace="https://www.foom.com/core")
magnitude_class = utils.create_iri("Magnitude", namespace="https://www.foom.com/core")
moral_class = utils.create_iri("Moral", namespace="https://www.foom.com/core")
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
object_individual = utils.create_iri("Concept type: Object", namespace="https://www.foom.com/core")
relation_individual = utils.create_iri("Concept type: Relation", namespace="https://www.foom.com/core")
operation_individual = utils.create_iri("Concept type: Operation", namespace="https://www.foom.com/core")

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

has_concept_type = utils.create_iri("has concept type", namespace="https://www.foom.com/core")
is_concept_type_of = utils.create_iri("is concept type of", namespace="https://www.foom.com/core")



def add_concepts(kg: rdflib.Graph,
                 concepts_analysis_input_file_path: str) -> rdflib.Graph:
    """
    Adds concepts and their associated data to a knowledge graph.

    This function processes an input CSV file containing concept information, adds the concepts
    to the knowledge graph (KG), associates datatype properties, and establishes relationships 
    such as hierarchy and concept types.

    Args:
        kg (rdflib.Graph): The knowledge graph to which concepts will be added.
        concepts_analysis_input_file_path (str): Path to the CSV file containing concepts data.

    Returns:
        rdflib.Graph: The updated knowledge graph with new concepts.
    """
    # add concept types
    kg = add_concept_types(kg, {"Object", "Operation", "Relation"})

    # add object properties for conceptual components
    kg, has_conceptual_component_iri = add_conceptual_object_property(kg, "has conceptual component")
    kg, is_conceptual_component_of_iri = add_conceptual_object_property(kg, "is conceptual component of")
    kg, is_equivalent_to_iri = add_conceptual_object_property(kg, "is equivalent to")
    kg, is_opposite_to_iri = add_conceptual_object_property(kg, "is opposite to")

    # read concepts data
    concepts_df = pd.read_csv(concepts_analysis_input_file_path).fillna("")
    for i in concepts_df.index:
        concept_preflabel = concepts_df.at[i, "concepts"].replace("_", " ").strip().capitalize()

        # add concept
        concept_iri = utils.create_iri(f"Concept: {concept_preflabel}", namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, concept_preflabel, concept_iri, concept_class, "Concept")

        # add hierarchy
        concept_hierarchy_preflabel = concepts_df.at[i, "hierarchy"].replace("_", " ").strip().capitalize()
        if concept_hierarchy_preflabel:
            kg = add_concept_hierarchy(kg, concept_iri, concept_hierarchy_preflabel)

        # add concept type
        concept_type_iri = utils.create_iri(f"Concept type: {concepts_df.at[i, 'type']}", namespace="https://www.foom.com/core")
        kg.add((concept_iri, has_concept_type, concept_type_iri))
        kg.add((concept_type_iri, is_concept_type_of, concept_iri))

        # add datatype properties
        datatype_properties = [datatype_property.strip() for datatype_property in concepts_df.at[i, "datatype_property"].split(",")]
        for datatype_property in datatype_properties:
            datatype_property_iri = utils.create_iri(datatype_property, namespace="https://www.foom.com/core")
            kg = add_datatype_property(kg, datatype_property, datatype_property_iri)
            kg.add((concept_iri, datatype_property_iri, xsd_true))

        # add conceptual components
        kg = add_conceptual_components(
                kg, 
                concept_iri, 
                concepts_df, 
                has_conceptual_component_iri, 
                is_conceptual_component_of_iri,
                i
            )

        # add equivalent concepts
        equivalent_concept = concepts_df.at[i, "equivalent_to"].replace("_", " ").strip().capitalize()
        if equivalent_concept:
            kg = add_equivalent__opposite_concepts(kg, concept_iri, equivalent_concept, is_equivalent_to_iri)

        # add opposite concepts
        opposite_concept = concepts_df.at[i, "opposite_to"].replace("_", " ").strip().capitalize()
        if opposite_concept:
            kg = add_equivalent__opposite_concepts(kg, concept_iri, opposite_concept, is_opposite_to_iri)

    return kg

def add_equivalent__opposite_concepts(kg: rdflib.Graph,
                            concept_iri: rdflib.URIRef,
                            selected_concept: str,
                            selected_object_property_iri: rdflib.URIRef) -> rdflib.Graph:
    selected_concept_iri = utils.create_iri(f"Concept: {selected_concept}", namespace=ONTOLOGY_NAMESPACE)
    kg.add((concept_iri, selected_object_property_iri, selected_concept_iri))
    kg.add((selected_concept_iri, selected_object_property_iri, concept_iri))
    return kg

def add_conceptual_components(kg: rdflib.Graph,
                              concept_iri: rdflib.URIRef,
                              concepts_df: pd.DataFrame,
                              has_conceptual_component_iri: rdflib.URIRef,
                              is_conceptual_component_of_iri: rdflib.Graph,
                              df_index: int) -> rdflib.Graph:
    # list conceptual components
    conceptual_components = [
            conceptual_component.replace("_", " ").strip().capitalize() 
            for conceptual_component in concepts_df.at[df_index, "conceptual_components"].split(",")
            if conceptual_component.replace(" ", "")
        ]
    # connect conceptual components to the main concept
    for conceptual_component in conceptual_components:
        conceptual_component_iri = utils.create_iri(f"Concept: {conceptual_component}", namespace=ONTOLOGY_NAMESPACE)
        kg.add((concept_iri, has_conceptual_component_iri, conceptual_component_iri))
        kg.add((conceptual_component_iri, is_conceptual_component_of_iri, concept_iri))
    return kg

def add_conceptual_object_property(kg: rdflib.Graph,
                                   label: str) -> rdflib.Graph:
    property_iri = utils.create_iri(label, namespace=ONTOLOGY_NAMESPACE)
    kg = tbox.add_tbox_triples(
        kg,
        label,
        owl_object_property,
        ONTOLOGY_NAMESPACE
    )
    return kg, property_iri

def add_datatype_property(kg: rdflib.Graph,
                          datatype_property_preflabel: str,
                          datatype_property_iri = rdflib.URIRef) -> rdflib.Graph:
    """
    Adds a datatype property to the knowledge graph.

    This function creates a datatype property with the provided preflabel and IRI,
    associates it with an RDF type, and sets its range as a boolean datatype.

    Args:
        kg (rdflib.Graph): The knowledge graph to which the datatype property will be added.
        datatype_property_preflabel (str): The preferred label for the datatype property.
        datatype_property_iri (rdflib.URIRef): The IRI of the datatype property.

    Returns:
        rdflib.Graph: The updated knowledge graph with the new datatype property.
    """
    kg.add((datatype_property_iri, rdf_type, owl_data_property))
    kg.add((datatype_property_iri, rdfs_label, rdflib.Literal(datatype_property_preflabel)))
    kg.add((datatype_property_iri, skos_prefLabel, rdflib.Literal(datatype_property_preflabel)))
    kg.add((datatype_property_iri, rdfs_range, xsd_boolean))
    return kg

def add_concept_types(kg: rdflib.Graph,
                      concept_types_preflabels: set) -> rdflib.Graph:
    """
    Adds concept types to the knowledge graph.

    This function iterates through a set of concept type preflabels, creates corresponding IRIs, 
    and adds them to the knowledge graph along with their associated data.

    Args:
        kg (rdflib.Graph): The knowledge graph to which concept types will be added.
        concept_types_preflabels (set): A set of preflabels for concept types.

    Returns:
        rdflib.Graph: The updated knowledge graph with new concept types.
    """
    for concept_type_preflabel in concept_types_preflabels:
        concept_type_iri = utils.create_iri(f"Concept type: {concept_type_preflabel}", namespace="https://www.foom.com/core")
        kg = concepts.add_triples(kg, concept_type_preflabel, concept_type_iri, concept_type_class, "Concept type")
    return kg

def add_concept_hierarchy(kg: rdflib.Graph,
                          concept_iri: rdflib.URIRef,
                          concept_hierarchy_preflabel: str) -> rdflib.Graph:
    """
    Adds a concept hierarchy to the knowledge graph.

    This function links a concept to a parent concept in a hierarchical structure by adding 
    sub-concept and super-concept relationships.

    Args:
        kg (rdflib.Graph): The knowledge graph to which the hierarchy will be added.
        concept_iri (rdflib.URIRef): The IRI of the concept being added to the hierarchy.
        concept_hierarchy_preflabel (str): The preferred label of the parent concept in the hierarchy.

    Returns:
        rdflib.Graph: The updated knowledge graph with the new hierarchy relationships.
    """
    concept_hierarchy_iri = utils.create_iri(f"Concept: {concept_hierarchy_preflabel}", namespace="https://www.foom.com/core")
    kg = concepts.add_triples(kg, concept_hierarchy_preflabel, concept_hierarchy_iri, concept_class, "Concept")
    kg.add((concept_iri, is_sub_concept_of, concept_hierarchy_iri))
    kg.add((concept_hierarchy_iri, is_super_concept_of, concept_iri))
    return kg