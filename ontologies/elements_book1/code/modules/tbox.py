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


def add_tbox_triples(kg: rdflib.Graph,
                     label: str,
                     graph_type: rdflib.URIRef,
                     selected_namespace: str="https://www.foom.com/core") -> rdflib.Graph:
    iri = utils.create_iri(label, selected_namespace)
    kg.add((iri, rdf_type, graph_type))
    kg.add((iri, rdfs_label, rdflib.Literal(label)))
    kg.add((iri, skos_prefLabel, rdflib.Literal(label)))
    return kg

def add_tbox(kg: rdflib.Graph,
             ontology_items: set,
             triples: set) -> rdflib.Graph:
    for label, ontology_type in ontology_items:
        kg = add_tbox_triples(kg, label, ontology_type)
    for s, p, o in triples:
        kg.add((s, p, o))
    return kg