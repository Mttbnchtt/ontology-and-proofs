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
is_defined_in = utils.create_iri("is defined in", namespace="https://www.foom.com/core")
contains_definition_of = utils.create_iri("contains_definition_of", namespace="https://www.foom.com/core")
is_in = utils.create_iri("is in", namespace="https://www.foom.com/core")
has_definition = utils.create_iri("has definition", namespace="https://www.foom.com/core")
defines = utils.create_iri("defines", namespace="https://www.foom.com/core")
def extract_definition_concepts(lines: list) -> dict:
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
    kg.add((concept_iri, rdf_type, owl_individual))
    kg.add((concept_iri, rdfs_label, rdflib.Literal(f"{prefix_label}: {utils.capitalize_first_letter(concept)}")))
    kg.add((concept_iri, skos_prefLabel, rdflib.Literal(utils.capitalize_first_letter(concept))))
    kg.add((concept_iri, rdf_type, class_iri))
    return kg

def add_definition_concepts(kg: rdflib.Graph,
                            concepts: dict) -> rdflib.Graph:
    for concept, concept_data in concepts.items():
        concept_iri = utils.create_iri(concept)
        kg = add_triples(kg, concept, concept_iri, concept_class, "Concept")
        kg.add((concept_iri, is_defined_in, utils.create_iri("Elements Book 1")))
        kg.add((utils.create_iri("Elements Book 1"), contains_definition_of, concept_iri))
        for subconcept in concept_data["subconcepts"]:
            subconcept_label = subconcept.replace("~", "").replace(",", "").strip()
            subconcept_iri = utils.create_iri(subconcept_label)
            kg = add_triples(kg, subconcept_label, subconcept_iri, concept_class, "Concept")
            kg.add((utils.create_iri(subconcept_label), definition_refers_to, utils.create_iri(concept)))
        
    return kg

def add_definition(kg: rdflib.Graph,
                   definition: str,
                   definition_iri: rdflib.URIRef) -> rdflib.Graph:
    definiton_label = f"Definition: {definition}"
    kg.add((definition_iri, rdf_type, owl_individual))
    kg.add((definition_iri, rdfs_label, rdflib.Literal(definiton_label)))
    kg.add((definition_iri, rdf_type, utils.create_iri("Definition")))
    kg.add((definition_iri, is_in, utils.create_iri("Elements Book 1")))
    kg.add((definition_iri, skos_prefLabel, rdflib.Literal(definiton_label)))

    return kg

def main_add_definition_concepts(file_path: str,
                                 kg: rdflib.Graph) -> rdflib.Graph:
    lines = utils.read_text_file(file_path)
    concepts = extract_definition_concepts(lines)
    kg = add_definition_concepts(kg, concepts)
    return kg