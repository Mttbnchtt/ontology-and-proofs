"""Shared helpers for typical proof analysis."""

from __future__ import annotations


def iri_for_proof(proof_n: int) -> str:
    return f"<https://www.foom.com/core#proof_{proof_n}>"


def iri_for_proposition(proof_n: int) -> str:
    return f"<https://www.foom.com/core#proposition_{proof_n}>"
