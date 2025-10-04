import rdflib
import pandas as pd

def read_graph(file_path: str, format: str = "turtle") -> rdflib.Graph:
    """
    Reads an RDF graph from a file.
    """
    g = rdflib.Graph()
    g.parse(file_path, format=format)
    print(f"Graph has {len(g)} statements.")
    return g

def sparql_to_df(kg: rdflib.Graph,
                 sparql_query: str):
    """Return query results as a DataFrame, normalising the optional `links` column."""
    raw = kg.query(sparql_query)
    # Materialise each result row into a dict, converting RDF terms to native Python values when possible.
    records = [
        {
            str(variable): (value.toPython() if value is not None and hasattr(value, "toPython") else value)
            for variable, value in zip(raw.vars, row)
        }
        for row in raw
    ]
    records_df = pd.DataFrame(records)
    if "links" in records_df.columns:
        records_df["links"] = records_df["links"].astype(int)
    return records_df

def sparql_to_concat_df(kg: rdflib.Graph,
                        sparql_queries: list,
                        hebb: bool = False):
    """Concatenate query results and aggregate link counts by node or node pairs."""
    if hebb:
        df = pd.concat(
            [sparql_to_df(kg, sparql_query) for sparql_query in sparql_queries],
            ignore_index = True).groupby(by=["o1", "o2"])["links"].sum().reset_index()
    else:
        df = pd.concat(
            [sparql_to_df(kg, sparql_query) for sparql_query in sparql_queries],
            ignore_index = True).groupby(by=["o"])["links"].sum().reset_index()
    return df
