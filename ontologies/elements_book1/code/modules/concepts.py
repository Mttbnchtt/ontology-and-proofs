import os
import rdflib
import re

import modules.utils as utils
# import modules.tbox as tbox

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
    kg.add((concept_iri, rdfs_label, rdflib.Literal(f"{prefix_label}: {capitalize_first_letter(concept)}")))
    kg.add((concept_iri, skos_prefLabel, rdflib.Literal(capitalize_first_letter(concept))))
    kg.add((concept_iri, rdf_type, class_iri))
    return kg

def add_definition_concepts(kg: rdflib.Graph,
                            concepts: dict) -> rdflib.Graph:
    for concept, concept_data in concepts.items():
        concept_iri = create_iri(concept)
        kg = add_triples(kg, concept, concept_iri, concept_class, "Concept")
        kg.add((concept_iri, is_defined_in, create_iri("Elements Book 1")))
        kg.add((create_iri("Elements Book 1"), contains_definition_of, concept_iri))
        for subconcept in concept_data["subconcepts"]:
            subconcept_label = subconcept.replace("~", "").replace(",", "").strip()
            subconcept_iri = create_iri(subconcept_label)
            kg = add_triples(kg, subconcept_label, subconcept_iri, concept_class, "Concept")
            kg.add((create_iri(subconcept_label), definition_refers_to, create_iri(concept)))
    return kg

def main_add_definition_concepts(file_path: str,
                                 kg: rdflib.Graph) -> rdflib.Graph:
    lines = utils.read_text_file(file_path)
    concepts = extract_definition_concepts(lines)
    # kg = add_tbox(kg, ontology_items, triples)
    kg = add_definition_concepts(kg, concepts)
    return kg