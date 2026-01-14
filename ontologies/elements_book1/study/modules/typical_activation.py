"""Activation potential helpers for typical proof analysis."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def compute_phi_h(
    proof_resources: Iterable[str],
    family_dfs: dict[str, pd.DataFrame],
    weights: tuple[float, float, float],
) -> pd.DataFrame:
    resources = sorted(set(proof_resources))
    if not resources:
        return pd.DataFrame(columns=["resource_used_in_proof", "phi_h"])

    phi_h = {resource: 0.0 for resource in resources}
    for family_name, weight in zip(
        ("direct", "hierarchical", "mereological"),
        weights,
    ):
        df = family_dfs.get(family_name, pd.DataFrame())
        if df.empty or "links" not in df.columns:
            continue
        total_links = float(df["links"].sum())
        if total_links == 0:
            continue
        link_map = {
            str(row["o"]): float(row["links"])
            for _, row in df.iterrows()
        }
        for resource in resources:
            links = link_map.get(resource, 0.0)
            if links:
                phi_h[resource] += (links * weight) / total_links

    return pd.DataFrame({
        "resource_used_in_proof": resources,
        "phi_h": [phi_h[resource] for resource in resources],
    })


def compute_phi_tc(
    proof_resources: Iterable[str],
    hebb_df: pd.DataFrame,
) -> pd.DataFrame:
    resources = sorted(set(proof_resources))
    if not resources:
        return pd.DataFrame(columns=["resource_used_in_proof", "phi_tc"])

    degrees: dict[str, float] = {}
    if not hebb_df.empty and "links" in hebb_df.columns:
        for _, row in hebb_df.iterrows():
            o1 = str(row["o1"])
            o2 = str(row["o2"])
            weight = float(row["links"])
            degrees[o1] = degrees.get(o1, 0.0) + weight
            degrees[o2] = degrees.get(o2, 0.0) + weight

    total_degree = sum(degrees.values())
    if total_degree == 0:
        phi_tc = {resource: 0.0 for resource in resources}
    else:
        phi_tc = {
            resource: degrees.get(resource, 0.0) / total_degree
            for resource in resources
        }

    return pd.DataFrame({
        "resource_used_in_proof": resources,
        "phi_tc": [phi_tc[resource] for resource in resources],
    })


def compute_phi_t(
    proof_resources: Iterable[str],
    phi_h_df: pd.DataFrame,
    phi_tc_df: pd.DataFrame,
    delta: float,
) -> pd.DataFrame:
    resources = sorted(set(proof_resources))
    if not resources:
        return pd.DataFrame(columns=["resource_used_in_proof", "phi_t"])

    phi_h_map = {}
    if not phi_h_df.empty:
        phi_h_map = dict(zip(phi_h_df["resource_used_in_proof"], phi_h_df["phi_h"]))
    phi_tc_map = {}
    if not phi_tc_df.empty:
        phi_tc_map = dict(zip(phi_tc_df["resource_used_in_proof"], phi_tc_df["phi_tc"]))

    phi_t = {
        resource: delta * float(phi_h_map.get(resource, 0.0))
        + (1 - delta) * float(phi_tc_map.get(resource, 0.0))
        for resource in resources
    }
    return pd.DataFrame({
        "resource_used_in_proof": resources,
        "phi_t": [phi_t[resource] for resource in resources],
    })


def compute_new_resources(
    proof_resources: Iterable[str],
    context_resources: Iterable[str],
) -> list[str]:
    proof_set = set(proof_resources)
    context_set = set(context_resources)
    return sorted(proof_set - context_set)
