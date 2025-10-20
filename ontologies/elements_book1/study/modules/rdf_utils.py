"""Utilities to work with RDF graphs and cached SPARQL queries."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence
import pandas as pd
import rdflib

from .query_cache import cached_dataframe_query, build_query_cache_key


def save_graph_with_timestamp(graph):
    """Serialize graph to a timestamped Turtle file in the study output folder."""
    output_dir = Path("/Users/matteobianchetti/Documents/Chen.Chen.1/Filosofia/Logica/Mathematics/Math_subjects/Computer_science/Git_repositories/GitHub/ontology-and-proofs/ontologies/elements_book1/study/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"ontology_{timestamp}.ttl"
    graph.serialize(destination=output_path, format="turtle")
    return output_path


def read_graph(
    file_path: str,
    format: str = "turtle",
    *,
    cache_token: Optional[str] = None,
) -> rdflib.Graph:
    """Read an RDF graph and attach a cache token derived from the source file."""
    graph_path = Path(file_path)
    g = rdflib.Graph()
    g.parse(file_path, format=format)
    print(f"Graph has {len(g)} statements.")
    token = cache_token
    if token is None:
        try:
            stat = graph_path.stat()
            token = f"{graph_path.resolve()}::{stat.st_mtime_ns}::{stat.st_size}"
        except FileNotFoundError:
            token = None
    if token is not None:
        setattr(g, "_cache_token", token)
    return g

def sparql_to_df(kg: rdflib.Graph,
                 sparql_query: str,
                 *,
                 cache: bool = True,
                 cache_token: Optional[str] = None,
                 refresh: bool = False) -> pd.DataFrame:
    """Return query results as a DataFrame, optionally caching them on disk."""

    def materialise_query() -> pd.DataFrame:
        raw = kg.query(sparql_query)
        # Materialise each result row into a dict, converting RDF terms to native Python values when possible.
        records = [
            {
                str(variable): (
                    value.toPython() if value is not None and hasattr(value, "toPython") else value
                )
                for variable, value in zip(raw.vars, row)
            }
            for row in raw
        ]
        records_df = pd.DataFrame(records)
        if "links" in records_df.columns:
            records_df["links"] = records_df["links"].astype(int)
        return records_df

    if not cache:
        return materialise_query()

    token = cache_token or getattr(kg, "_cache_token", None)
    if token is None:
        return materialise_query()

    cache_key = build_query_cache_key(sparql_query, token)
    return cached_dataframe_query(cache_key, materialise_query, refresh=refresh)

def sparql_to_concat_df(kg: rdflib.Graph,
                        sparql_queries: Sequence[str],
                        hebb: bool = False,
                        *,
                        cache: bool = True,
                        cache_token: Optional[str] = None,
                        refresh: bool = False) -> pd.DataFrame:
    """Concatenate query results and aggregate link counts by node or node pairs."""
    if hebb:
        df = pd.concat(
            [
                sparql_to_df(
                    kg,
                    sparql_query,
                    cache=cache,
                    cache_token=cache_token,
                    refresh=refresh,
                )
                for sparql_query in sparql_queries
            ],
            ignore_index = True).groupby(by=["o1", "o2"])["links"].sum().reset_index()
    else:
        df = pd.concat(
            [
                sparql_to_df(
                    kg,
                    sparql_query,
                    cache=cache,
                    cache_token=cache_token,
                    refresh=refresh,
                )
                for sparql_query in sparql_queries
            ],
            ignore_index = True).groupby(by=["o"])["links"].sum().reset_index()
    return df

def create_iris_for_values(proposition_number: int) -> str:
    iris_strings = [f"<https://www.foom.com/core#proof_{i}> <https://www.foom.com/core#proposition_{i}>" for i in range(1, proposition_number)]
    return " ".join(iris_strings)
