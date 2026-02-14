"""Activation potential helpers for likely proof analysis."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def compute_phi_lc(
    proof_resources: Iterable[str],
    hebb_df: pd.DataFrame,
    salient_resources: Iterable[str],
    context_resources: Iterable[str],
) -> pd.DataFrame:
    """Compute likely co-occurrence potential for resources used in a proof.

    - `deg_C^S(r)` is computed from symmetrized ordered pairs:
      hebb_C(r, s) + hebb_C(s, r).
    - Denominator is over unique filtered context resources U_C.
    """
    resources = sorted(set(proof_resources))
    if not resources:
        return pd.DataFrame(columns=["resource_used_in_proof", "phi_lc"])

    salient = sorted(set(salient_resources))
    u_c = set(context_resources)
    if not salient or not u_c:
        return pd.DataFrame({
            "resource_used_in_proof": resources,
            "phi_lc": [0.0 for _ in resources],
        })

    pair_links: dict[tuple[str, str], float] = {}
    if not hebb_df.empty and {"o1", "o2", "links"}.issubset(hebb_df.columns):
        for _, row in hebb_df.iterrows():
            o1 = str(row["o1"])
            o2 = str(row["o2"])
            pair_links[(o1, o2)] = pair_links.get((o1, o2), 0.0) + float(row["links"])

    if not pair_links:
        return pd.DataFrame({
            "resource_used_in_proof": resources,
            "phi_lc": [0.0 for _ in resources],
        })

    def deg(resource: str) -> float:
        total = 0.0
        for s in salient:
            if s == resource:
                continue
            total += pair_links.get((resource, s), 0.0)
            total += pair_links.get((s, resource), 0.0)
        return total

    z = sum(deg(u) for u in u_c)
    if z == 0.0:
        phi_lc = {resource: 0.0 for resource in resources}
    else:
        phi_lc = {resource: deg(resource) / z for resource in resources}

    return pd.DataFrame({
        "resource_used_in_proof": resources,
        "phi_lc": [phi_lc[resource] for resource in resources],
    })


def compute_phi_l(
    proof_resources: Iterable[str],
    phi_h_df: pd.DataFrame,
    phi_lc_df: pd.DataFrame,
    epsilon: float,
) -> pd.DataFrame:
    resources = sorted(set(proof_resources))
    if not resources:
        return pd.DataFrame(columns=["resource_used_in_proof", "phi_l"])

    phi_h_map = {}
    if not phi_h_df.empty:
        phi_h_map = dict(zip(phi_h_df["resource_used_in_proof"], phi_h_df["phi_h"]))
    phi_lc_map = {}
    if not phi_lc_df.empty:
        phi_lc_map = dict(zip(phi_lc_df["resource_used_in_proof"], phi_lc_df["phi_lc"]))

    phi_l = {
        resource: epsilon * float(phi_h_map.get(resource, 0.0))
        + (1 - epsilon) * float(phi_lc_map.get(resource, 0.0))
        for resource in resources
    }

    return pd.DataFrame({
        "resource_used_in_proof": resources,
        "phi_l": [phi_l[resource] for resource in resources],
    })
