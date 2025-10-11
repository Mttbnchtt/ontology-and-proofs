"""Lightweight in-memory wrapper around cached SPARQL execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

import pandas as pd
import rdflib

from modules import rdf_utils as base_rdf_utils


@dataclass
class QueryRunner:
    """Execute SPARQL queries once per graph and keep the materialised dataframe in memory."""

    graph: rdflib.Graph
    _local_cache: Dict[str, pd.DataFrame] = field(default_factory=dict)

    def fetch(self, query: str, *, refresh: bool = False) -> pd.DataFrame:
        """Return the dataframe for ``query``; reuse cached results when available."""

        if refresh or query not in self._local_cache:
            self._local_cache[query] = base_rdf_utils.sparql_to_df(self.graph, query)
        return self._local_cache[query]

    def fetch_many(self, queries: Iterable[str], *, refresh: bool = False) -> List[pd.DataFrame]:
        """Materialise several queries, preserving order."""

        return [self.fetch(query, refresh=refresh) for query in queries]
