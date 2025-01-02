import pandas as pd
import rdflib

import modules.utils as utils
import modules.operations_relations_module as operations_relations_module

RDF_TYPE = rdflib.RDF.type
RDFS_LABEL = rdflib.RDFS.label
SKOS_PREFLABEL = rdflib.SKOS.prefLabel
OWL_INDIVIDUAL = rdflib.OWL.NamedIndividual

STATEMENT_CLASS = rdflib.URIRef("https://www.foom.com/core#statement")

def add_statement(kg: rdflib.Graph, 
                  statement: str) -> rdflib.Graph:
    # clean statement
    statement = statement.strip()
    # create statement IRI
    statement_iri = utils.create_iri(statement)
    # add statement to KG
    kg.add((statement_iri, RDF_TYPE, STATEMENT_CLASS))
    kg.add((statement_iri, RDF_TYPE, OWL_INDIVIDUAL))
    kg.add((statement_iri, RDFS_LABEL, rdflib.Literal(statement)))
    kg.add((statement_iri, SKOS_PREFLABEL, rdflib.Literal(statement)))
    # connect concepts to statement
    kg = operations_relations_module.add_concepts(kg, statement_iri, statement)

    return kg, statement_iri