"""Utilities for caching SPARQL query results on disk."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

try:
    import diskcache
except ImportError:  # pragma: no cover - handled gracefully at runtime.
    diskcache = None

# Cache configuration -------------------------------------------------------

_CACHE_NAME = "sparql"
_CACHE_VERSION = "1"
_DEFAULT_CACHE_DIR = Path(
    os.environ.get("FOOM_QUERY_CACHE_DIR", Path.home() / ".foom_query_cache")
)
_CACHE_SIZE_LIMIT = int(os.environ.get("FOOM_QUERY_CACHE_SIZE", 2_000_000_000))  # ~2GB default


def _ensure_cache_dir(directory: Path) -> Path:
    directory = directory.expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


if diskcache is not None:
    _CACHE_DIR = _ensure_cache_dir(_DEFAULT_CACHE_DIR)
    _CACHE = diskcache.Cache(_CACHE_DIR, size_limit=_CACHE_SIZE_LIMIT)
else:  # pragma: no cover - we defer to runtime for optional dependency.
    _CACHE_DIR = None
    _CACHE = None


# Key helpers ---------------------------------------------------------------

def build_query_cache_key(
    sparql_query: str,
    graph_token: Optional[str],
    *,
    extra: Iterable[str] = (),
) -> str:
    """Return a stable cache key for a SPARQL query and graph signature."""

    components = [
        _CACHE_NAME,
        _CACHE_VERSION,
        graph_token or "no-graph-token",
        sparql_query,
        *extra,
    ]
    joined = "\u241f".join(components)  # use delimiter unlikely to appear naturally
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


# Cache API -----------------------------------------------------------------

def cached_dataframe_query(
    key: str,
    loader: Callable[[], Any],
    *,
    refresh: bool = False,
) -> Any:
    """Run ``loader`` and persist its return value unless already cached."""

    if _CACHE is None:
        return loader()

    if not refresh:
        cached = _CACHE.get(key)
        if cached is not None:
            return cached

    result = loader()
    _CACHE.set(key, result)
    return result


def clear_cache() -> None:
    """Clear the SPARQL cache when the backend is available."""

    if _CACHE is not None:
        _CACHE.clear()


def cache_directory() -> Optional[Path]:
    """Expose the active cache directory for diagnostics."""

    return _CACHE_DIR
