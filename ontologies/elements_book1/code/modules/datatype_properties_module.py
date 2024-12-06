import pandas as pd
import rdflib

import modules.utils as utils
import modules.concepts_module as concepts_module


ONTOLOGY_NAMESPACE = "https://www.foom.com/core"

def add_datatype_properties(kg: rdflib.Graph,
                            input_file_path: str) -> rdflib.Graph:
    datatype_properties = pd.read_csv(input_file_path).fillna("")
    for i in datatype_properties.index:
        # create preflabels and iris
        datatype_property_pref_label = datatype_properties.at[i, "datatype_property"]
        datatype_property_iri = utils.create_iri(datatype_property_pref_label, namespace=ONTOLOGY_NAMESPACE)

        # add datatype properties to the kg
        kg = concepts_module.add_datatype_property(kg, datatype_property_pref_label, datatype_property_iri)

        # add hierachical relations
        if higher_datatype_property_pref_label := datatype_properties.at[i, "hierarchy"]:
            higher_datatype_property_iri = utils.create_iri(higher_datatype_property_pref_label, namespace=ONTOLOGY_NAMESPACE)
            kg = concepts_module.add_datatype_property(kg, higher_datatype_property_pref_label, higher_datatype_property_iri)
            kg.add((datatype_property_iri, rdflib.RDFS.subPropertyOf, higher_datatype_property_iri))

    return kg