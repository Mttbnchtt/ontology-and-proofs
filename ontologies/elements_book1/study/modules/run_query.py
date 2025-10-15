"""Utilities for executing ad-hoc SPARQL queries against a prepared rdflib graph."""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Iterable, Mapping, MutableMapping, Optional

import pandas as pd
import rdflib

TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"

PREFIXES = """\
PREFIX core: <https://www.foom.com/core#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""


def _to_python(term: Optional[rdflib.term.Identifier]) -> Optional[object]:
    if term is None:
        return None
    return term.toPython() if hasattr(term, "toPython") else str(term)


def _normalise_bindings(bindings: Iterable[Mapping[rdflib.term.Variable, object]]) -> list[dict[str, object]]:
    normalised: list[dict[str, object]] = []
    for binding in bindings:
        row: MutableMapping[str, object] = {}
        for key, value in binding.items():
            row[str(key)] = _to_python(value)
        normalised.append(dict(row))
    return normalised


def run_query(
    graph: rdflib.Graph,
    sparql_query: str,
    *,
    prefixes: str = PREFIXES,
) -> pd.DataFrame:
    """Execute ``sparql_query`` against ``graph`` and return the materialised dataframe."""

    results = graph.query(f"{prefixes} {sparql_query}")
    bindings = getattr(results, "bindings", [])
    records = _normalise_bindings(bindings)
    df = pd.DataFrame.from_records(records)
    print(f"Query returned {len(df)} results.")
    return df


def df_to_csv(
    df: pd.DataFrame,
    directory: Path | str,
    *,
    filename_prefix: str = "query_results",
    timestamp_format: str = TIMESTAMP_FORMAT,
) -> Path:
    """Persist ``df`` as a timestamped CSV in ``directory`` and return the created path."""

    output_dir = Path(directory).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = _dt.datetime.now().strftime(timestamp_format)
    output_file = output_dir / f"{filename_prefix}_{timestamp}.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved results to {output_file}")
    return output_file


def main(
    graph: rdflib.Graph,
    sparql_query: str,
    *,
    write_to_csv: bool = False,
    output_dir: Path | str | None = None,
    prefixes: str = PREFIXES,
) -> pd.DataFrame:
    """Execute ``sparql_query`` and optionally save results to ``output_dir``."""

    df = run_query(graph, sparql_query, prefixes=prefixes)
    if write_to_csv:
        target_dir = output_dir if output_dir is not None else Path.cwd()
        df_to_csv(df, target_dir)
    return df
