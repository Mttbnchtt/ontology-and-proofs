"""Utilities for running surprise analyses and persisting results."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
import rdflib

from . import potential, queries
from .file_utils import output_df
from .query_runner import QueryRunner

try:
    from modules.surprise_score import SelectionCriteria, SelectionMode  # type: ignore
except ImportError:  # pragma: no cover
    # Fallback for module-relative imports when used outside the package root
    from ..surprise_score import SelectionCriteria, SelectionMode  # type: ignore

CORE_PREFIX = "https://www.foom.com/core#"


def print_results_stats(results_df: pd.DataFrame) -> None:
    """Print how many rows have empty surprising concept sets."""

    def _is_empty(value):
        if isinstance(value, (list, tuple, set)):
            return len(value) == 0
        if isinstance(value, str):
            return value.strip() == ""
        if value is None:
            return True
        return bool(pd.isna(value))

    empty_surprising = results_df["surprising_concepts"].apply(_is_empty).sum()
    print(f"Empty surprising_concepts rows: {empty_surprising} out of {len(results_df)}")


def _strip_prefix(items: Iterable[str]) -> list[str]:
    """Return sorted concept identifiers without the core namespace prefix."""
    return [concept.replace(CORE_PREFIX, "") for concept in sorted(items)]


def _extract_proposition_number(label: str) -> int | None:
    """Extract the first integer found in a proposition label, if any."""
    if not isinstance(label, str):
        return None
    match = re.search(r"\d+", label)
    if match is None:
        return None
    try:
        return int(match.group(0))
    except ValueError:
        return None


def _is_numeric_label(label: str) -> bool:
    """Return True when the label is purely numeric or matches a small number word."""
    if not isinstance(label, str):
        return False
    stripped = label.strip().lower()
    if stripped.isdigit():
        return True
    number_words = {
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
    }
    return stripped in number_words


def _filter_numeric_concepts(concepts: Sequence[str], *, exclude_numeric: bool) -> list[str]:
    """Optionally remove concept labels that look like simple numbers."""
    if not exclude_numeric:
        return list(concepts)
    return [concept for concept in concepts if not _is_numeric_label(concept)]


def _ensure_runner(graph: rdflib.Graph | None, runner: QueryRunner | None) -> QueryRunner:
    """Return a QueryRunner, creating one from the supplied graph when missing."""
    if graph is None:
        raise ValueError("A graph instance is required to run analyse().")
    return runner or QueryRunner(graph)


def _fetch_proposition_types(runner: QueryRunner) -> dict[int, str]:
    """Build a map from proposition numbers to their type labels via SPARQL."""
    proposition_types_df = runner.fetch(queries.find_proposition_types())
    proposition_types_map: dict[int, str] = {}
    if proposition_types_df.empty:
        return proposition_types_map
    for _, row in proposition_types_df.iterrows():
        label = row.get("proposition_pref_label")
        type_label = row.get("proposition_type_pref_label")
        number = _extract_proposition_number(label)
        if number is not None and isinstance(type_label, str):
            proposition_types_map[number] = type_label
    return proposition_types_map


def _compute_proposition_row(
    graph: rdflib.Graph,
    proposition: int,
    *,
    history_weights: tuple[float, float, float, float],
    history_selection: SelectionCriteria,
    cooccurrence_selection: SelectionCriteria,
    runner: QueryRunner,
    type_selection: bool,
    proposition_type: str,
    exclude_numeric_concepts: bool,
    verbose: bool = False,
) -> tuple[dict[str, object], tuple[object, ...]]:
    """Compute analysis artefacts for one proposition and return row data plus CSV payload."""
    if verbose:
        print(f"Analysing proposition {proposition}")

    background_concepts, surprising = potential.main(
        graph,
        proposition,
        history_weights=history_weights,
        history_selection=history_selection,
        cooccurrence_selection=cooccurrence_selection,
        runner=runner,
        type_selection=type_selection,
    )

    background_list = _filter_numeric_concepts(
        _strip_prefix(concept for concept in background_concepts if concept),
        exclude_numeric=exclude_numeric_concepts,
    )
    surprising_list = _filter_numeric_concepts(
        _strip_prefix(concept for concept in surprising if concept),
        exclude_numeric=exclude_numeric_concepts,
    )
    ratio_surprising = (
        len(surprising_list) / len(background_list) if len(background_list) > 0 else 0.0
    )

    row_dict: dict[str, object] = {
        "proposition": proposition,
        "background_concepts": background_list,
        "surprising_concepts": surprising_list,
        "proposition_type": proposition_type,
        "number_of_background_concepts": len(background_list),
        "number_of_surprising_concepts": len(surprising_list),
        "ratio_surprising_over_background": ratio_surprising,
    }

    output_row = (
        str(proposition),
        background_list,
        surprising_list,
        proposition_type,
        len(background_list),
        len(surprising_list),
        ratio_surprising,
    )
    return row_dict, output_row


def _format_value(value: float) -> str:
    """Format numeric values for filenames, trimming redundant zeroes."""
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def _build_run_description(
    history_selection: SelectionCriteria,
    cooccurrence_selection: SelectionCriteria,
    history_weights: tuple[float, float, float, float],
    type_selection: bool,
    exclude_numeric_concepts: bool,
) -> str:
    """Compose the descriptor token that names analysis outputs."""
    parts = [
        f"history-{history_selection.mode.value}-{_format_value(history_selection.value)}",
        f"coocc-{cooccurrence_selection.mode.value}-{_format_value(cooccurrence_selection.value)}",
        "weights-" + "-".join(_format_value(weight) for weight in history_weights),
        "type" if type_selection else "no-type",
        "no-numeric" if exclude_numeric_concepts else "with-numeric",
    ]
    return "__".join(parts)


def _write_outputs(output_rows: Sequence[tuple[object, ...]], description: str, base_dir: Path) -> None:
    """Persist the collected rows to a timestamped CSV under the output directory."""
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"analyses_{description}"
    output_df(
        output_rows,
        filename=str(output_path),
        columns=[
            "proposition",
            "background_concepts",
            "surprising_concepts",
            "proposition_type",
            "number_of_background_concepts",
            "number_of_surprising_concepts",
            "ratio_surprising_over_background",
        ],
    )


def analyse(
    upper_proposition_number: int,
    history_weights: tuple[float, float, float, float],
    history_selection: SelectionCriteria,
    cooccurrence_selection: SelectionCriteria,
    *,
    graph: rdflib.Graph | None = None,
    runner: QueryRunner | None = None,
    type_selection: bool = False,
    exclude_numeric_concepts: bool = False,
    verbose: bool = False,
    output_base_dir: Path | None = None,
) -> pd.DataFrame:
    """Run the surprise analysis up to the requested proposition and return a dataframe."""

    runner = _ensure_runner(graph, runner)
    proposition_types = _fetch_proposition_types(runner)

    analyses: list[dict[str, object]] = []
    output_rows: list[tuple[object, ...]] = []
    for proposition in range(1, upper_proposition_number + 1):
        row_dict, output_row = _compute_proposition_row(
            graph,  # type: ignore[arg-type]
            proposition,
            history_weights=history_weights,
            history_selection=history_selection,
            cooccurrence_selection=cooccurrence_selection,
            runner=runner,
            type_selection=type_selection,
            proposition_type=proposition_types.get(proposition, ""),
            exclude_numeric_concepts=exclude_numeric_concepts,
            verbose=verbose,
        )
        analyses.append(row_dict)
        output_rows.append(output_row)

    description = _build_run_description(
        history_selection,
        cooccurrence_selection,
        history_weights,
        type_selection,
        exclude_numeric_concepts,
    )

    base_dir = output_base_dir if output_base_dir is not None else Path.cwd()
    _write_outputs(output_rows, description, base_dir)

    results_df = pd.DataFrame(analyses)
    print_results_stats(results_df)
    return results_df


__all__ = [
    "analyse",
    "print_results_stats",
    "SelectionCriteria",
    "SelectionMode",
]
