import pandas as pd
import rdflib

import modules.utils as utils
import modules.concepts_module as concepts_module

ONTOLOGY_NAMESPACE = "https://www.foom.com/core"

def add_datatype_properties(kg: rdflib.Graph,
                            input_file_path: str) -> rdflib.Graph:
    """
    Add datatype properties defined in a CSV file to the given knowledge graph (KG).

    Each row in the CSV should have at least two columns:
    - "datatype_property": The preferred label of the datatype property.
    - "hierarchy" (optional): The preferred label of a higher-level datatype property
      to establish a subPropertyOf relationship.

    Args:
        kg (rdflib.Graph): The knowledge graph to be updated.
        input_file_path (str): Path to the CSV file containing datatype properties.

    Returns:
        rdflib.Graph: The updated knowledge graph with datatype properties added.
    """
    datatype_properties = pd.read_csv(input_file_path).fillna("")

    for _, row in datatype_properties.iterrows():
        # create preflabels and iris
        datatype_property_pref_label = row["datatype_property"].strip()
        datatype_property_iri = utils.create_iri(datatype_property_pref_label, namespace=ONTOLOGY_NAMESPACE)

        # add datatype properties to the kg
        kg = concepts_module.add_datatype_property(kg, datatype_property_pref_label, datatype_property_iri)

        # add hierachical relations
        higher_datatype_property_pref_label = row.get("hierarchy", "").strip()
        if higher_datatype_property_pref_label:
            higher_datatype_property_iri = utils.create_iri(higher_datatype_property_pref_label, namespace=ONTOLOGY_NAMESPACE)
            kg = concepts_module.add_datatype_property(kg, higher_datatype_property_pref_label, higher_datatype_property_iri)
            kg.add((datatype_property_iri, rdflib.RDFS.subPropertyOf, higher_datatype_property_iri))

    return kg