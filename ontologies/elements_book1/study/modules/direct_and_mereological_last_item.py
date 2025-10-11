"""Lookup helpers for the last proposition/proof references using direct and mereological templates.
"""

import modules.queries as queries # SPARQL queries 
import rdflib

def direct_last_item(kg: rdflib.Graph,
                     last_proposition_iri: rdflib.URIRef):
    results = kg.query(queries.direct_template_propositions_proofs(last_proposition_iri))
    return {str(row.o) for row in results}

def mereological_last_item(kg: rdflib.Graph,
                           last_proposition_iri: rdflib.URIRef):
    # results = kg.query(queries.direct_template_last_item(last_proposition_iri))
    results = kg.query(queries.mereological_template_last_item(last_proposition_iri))
    return {str(row.o) for row in results}

def main(kg: rdflib.Graph,
         last_proposition_iri: rdflib.URIRef,
         direct_and_mereological: bool = True):
    if direct_and_mereological:
        return direct_last_item(kg, last_proposition_iri), mereological_last_item(kg, last_proposition_iri)
    else:
        return direct_last_item(kg, last_proposition_iri)

