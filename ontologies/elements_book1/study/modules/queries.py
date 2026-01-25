"""SPARQL query helpers grouped by conceptual family."""

from __future__ import annotations

import textwrap


def _wrap(query: str) -> str:
    """Dedent and strip a SPARQL query so the string literals stay tidy."""
    return textwrap.dedent(query).strip()


# ---------------------------------------------------------------------------
# Direct queries
# ---------------------------------------------------------------------------

def direct_definitions() -> str:
    """Return a query that counts concepts explicitly linked from definitions via `core#defines`."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s  a <https://www.foom.com/core#definition> .
            { ?s    <https://www.foom.com/core#defines> ?o . }
            UNION
            { ?s  <https://www.foom.com/core#contains_concept> ?o . }
        }
        group by ?o
        order by desc(?links)
        """
    )


def direct_postulates() -> str:
    """Return a query counting how often postulates reach a concept through `refers_to` paths, including domain, range, and contained concepts."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#postulate> .
            { ?s <https://www.foom.com/core#refers_to> ?o . } # refers to
            UNION
            { ?s <https://www.foom.com/core#contains_concept> ?o . } # contains concept
            union
            { ?s <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to / contains concept
            ######################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range> ?o . } # refers to / range
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / range / contains concept
                union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                     / <https://www.foom.com/core#refers_to> ?o . } # refers to / range / refers to
            #####################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain> ?o . } # refers to / domain
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / domain / contains concept
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#refers_to>  ?o . } # refers to / domain / refers to
        }
        group by ?o
        order by desc(?links)
        """
    )


def direct_common_notions() -> str:
    """Return a query counting concepts referenced by common notions through `has_statement` and expanded `refers_to` links."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#common_notion> .
            { ?s <https://www.foom.com/core#has_statement> ?o .}
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to> ?o . } # refers to
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to / contains concept
            ######################
            union
            { ?s <https://www.foom.com/core#has_statement>+
                    / <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#has_range>+ ?o . } # refers to / range
            union
            { ?s <https://www.foom.com/core#has_statement>+
                    / <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#has_range>+
                    / <https://www.foom.com/core#contains_concept>+  ?o . } # refers to / range / contains concept
            union
            { ?s <https://www.foom.com/core#has_statement>+
                    / <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#has_range>+
                    / <https://www.foom.com/core#refers_to>+  ?o . } # refers to / range / refers to
            #####################
            union
            { ?s <https://www.foom.com/core#has_statement>+
                    / <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#has_domain>+ ?o . } # refers to / domain
            union
            { ?s <https://www.foom.com/core#has_statement>+
                    / <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#has_domain>+
                    / <https://www.foom.com/core#contains_concept>+  ?o . } # refers to / domain / contains concept
            union
            { ?s <https://www.foom.com/core#has_statement>+
                    / <https://www.foom.com/core#refers_to>+
                    / <https://www.foom.com/core#has_domain>+
                    / <https://www.foom.com/core#refers_to>+  ?o . } # refers to / domain / refers to
        }
        group by ?o
        order by desc(?links)
        """
    )


def direct_template_propositions_proofs(iris: str) -> str:
    """Return a query counting concepts referenced by the supplied proposition/proof IRIs via direct `refers_to` property paths."""
    return _wrap(
        f"""
        SELECT 
                ?o 
                (count (*) as ?links) 
        WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#has_given_concept> ?o . }} # has given concept
                union
                {{ ?s <https://www.foom.com/core#contains_concept> ?o . }} # contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to> ?o . }} # refers to
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept> ?o . }} # refers to / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range> ?o . }} # refers to / range
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / range / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#refers_to>  ?o . }} # refers to / range / refers to
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain> ?o . }} # refers to / domain
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / domain / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#refers_to>  ?o . }} # refers to / domain / refers to
        }} 
        group by ?o 
        order by desc(?links)
        """
    )


def direct_template_last_item_types(iris: str) -> str:
    """Return a query listing distinct concepts that the given proposition/proof IRIs touch through direct `refers_to` paths."""
    return _wrap(
        f"""
        SELECT DISTINCT 
                ?o 
                (COUNT(?o) as ?links) 
        WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#refers_to> 
                        / <https://www.foom.com/core#has_relation_type>  ?o . }}  # refers to / has relation type 
                union
                {{ ?s <https://www.foom.com/core#refers_to> 
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#contains_concept>  ?o . }}  # refers to / has relation type / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to> 
                        / <https://www.foom.com/core#has_operation_type>  ?o . }}  # refers to / has operation type 
                union
                {{ ?s <https://www.foom.com/core#refers_to> 
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#contains_concept>  ?o . }}  # refers to / has operation type / contains concept
        }}  
        group by ?o 
        order by desc(?links)
        """
    )


# ---------------------------------------------------------------------------
# Hierarchical queries
# ---------------------------------------------------------------------------

def hierarchical_definitions() -> str:
    """Return a query counting super-concepts that definitions reach by following `defines` then `is_sub_concept_of`."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#definition> .
            ?s <https://www.foom.com/core#defines>
                    / <https://www.foom.com/core#is_sub_concept_of> ?o .  # sub concept of
        }
        group by ?o
        order by desc(?links)
        """
    )


def hierarchical_postulates() -> str:
    """Return a query counting higher-level concepts that postulates reach through `refers_to` plus hierarchical `contains_concept/is_sub_concept_of` paths."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#postulate> .
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#is_sub_concept_of> ?o . } # refers to / contains concept / super-concept
            ######################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#is_sub_concept_of>  ?o . } # refers to / range / contains concept / super-concept
            #####################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#is_sub_concept_of>  ?o . } # refers to / domain / contains concept / super-concept
            #########################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to> ?o . } # refers to [2]
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to [2] / contains concept
            ####################################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range> ?o . } # refers to [2] / range
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to [2] / range / contains concept
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#refers_to>  ?o . } # refers to [2] / range / refers to
            #####################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain> ?o . } # refers to [2] / domain
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to [2] / domain / contains concept
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#refers_to>  ?o . } # refers to [2] / domain / refers to
            #####################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_relation_type> ?o . } # refers to / has relation type
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_relation_type>
                    / <https://www.foom.com/core#contains_concept>  ?o . }  # refers to / has relation type / contains concept
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_operation_type> ?o . } # refers to / has operation type
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_operation_type>
                    / <https://www.foom.com/core#contains_concept>  ?o . }  # refers to / has operation type / contains concept
        }
        group by ?o
        order by desc(?links)
        """
    )


def hierarchical_common_notions() -> str:
    """Return a query counting super-concepts that common notions reach through `has_statement` and hierarchical property chains."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#common_notion> .
            { ?s <https://www.foom.com/core#has_statement> ?o .}
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#is_sub_concept_of> ?o . } # refers to / contains concept / super-concept
            ######################
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#is_sub_concept_of>  ?o . } # refers to / range / contains concept / super-concept
            #####################
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#is_sub_concept_of>  ?o . } # refers to / domain / contains concept / super-concept
            #########################
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to> ?o . } # refers to [2]
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to [2] / contains concept
            ####################################
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range> ?o . } # refers to [2] / range
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to [2] / range / contains concept
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#refers_to>  ?o . } # refers to [2] / range / refers to
            #####################
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain> ?o . } # refers to [2] / domain
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to [2] / domain / contains concept
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#refers_to>  ?o . } # refers to [2] / domain / refers to
        }
        group by ?o
        order by desc(?links)
        """
    )


def hierarchical_template_propositions_proofs(iris: str) -> str:
    """Return a query counting hierarchical concept references for the supplied proposition/proof IRIs using `refers_to` and `is_sub_concept_of` chains."""
    return _wrap(
        f"""
        SELECT ?o (count (*) as ?links) WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#has_given_concept>
                        / <https://www.foom.com/core#is_sub_concept_of> ?o . }} # has given concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#is_sub_concept_of> ?o . }} # contains concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#is_sub_concept_of> ?o . }} # refers to / contains concept / super-concept
                        
                        #####################
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#is_sub_concept_of>  ?o . }} # refers to / range / contains concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#is_sub_concept_of>  ?o . }} # refers to / domain / contains concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#refers_to> ?o . }} # refers to [2]
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept> ?o . }} # refers to [2] / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range> ?o . }} # refers to [2] / range
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to [2] / range / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain> ?o . }} # refers to [2] / domain
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to [2] / domain / contains concept
                        
                        #####################
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type> ?o . }} # refers to / has relation type
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#contains_concept> ?o . }} # refers to / has relation type / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#has_range> ?o . }} # refers to / has relation type / range
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / has relation type / range / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#has_domain> ?o . }} # refers to / has relation type / domain
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / has relation type / domain / contains concept 
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type> ?o . }} # refers to / has operation type
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#contains_concept> ?o . }} # refers to / has operation type / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#has_range> ?o . }} # refers to / has operation type / range
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / has operation type / range / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#has_domain> ?o . }} # refers to / has operation type / domain
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / has operation type / domain / contains concept

        }} 
        group by ?o order by desc(?links)
        """
    )


# ---------------------------------------------------------------------------
# Mereological queries
# ---------------------------------------------------------------------------

def mereological_definitions() -> str:
    """Return a query counting concept parts that definitions reference through `contains_concept` or `definition_refers_to`."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#definition> .
            { ?s <https://www.foom.com/core#defines>
                    / <https://www.foom.com/core#contains_concept> ?o . }
            UNION
            { ?s <https://www.foom.com/core#defines>
                    / <https://www.foom.com/core#definition_refers_to> ?o . }
        }
        group by ?o
        order by desc(?links)
        """
    )


def mereological_postulates() -> str:
    """Return a query counting nested concept parts that postulates reach through `refers_to` with repeated `contains_concept` or `definition_refers_to`."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#postulate> .
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to / contains concept / contains concept
            UNION
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to> ?o . } # refers to / contains concept / contains concept
            ######################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / range / contains concept / super-concept
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to>  ?o . } # refers to / range / contains concept / super-concept
            #####################
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / domain / contains concept / super-concept
            union
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to>  ?o . } # refers to / range / contains concept / super-concept
        }
        group by ?o
        order by desc(?links)
        """
    )


def mereological_common_notions() -> str:
    """Return a query counting concept parts that common notions reach via `has_statement` followed by mereological expansions."""
    return _wrap(
        """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#common_notion> .
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to / contains concept / contains_concept
            UNION
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to> ?o . } # refers to / contains concept / definition_refers_to
            ######################
            UNION
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / range / contains concept / contains_concept
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to>  ?o . } # refers to / range / contains concept / contains_concept
            #####################
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / domain / contains concept / contains_concept
            union
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to>  ?o . } # refers to / domain / contains concept / contains_concept
        }
        group by ?o
        order by desc(?links)
        """
    )


def mereological_template_propositions_proofs(iris: str) -> str:
    """Return a query counting part-level concepts connected to the given proposition/proof IRIs through repeated mereological property paths."""
    return _wrap(
        f"""
        SELECT ?o (count (*) as ?links) WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#contains_concept> ?o . }} # refers to / contains concept / contains concept
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#definition_refers_to> ?o . }} # refers to / contains concept / contains concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / range / contains concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#definition_refers_to>  ?o . }} # refers to / range / contains concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / domain / contains concept / super-concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#definition_refers_to>  ?o . }} # refers to / range / contains concept / super-concept
        }} group by ?o order by desc(?links)
        """
    )


def mereological_template_last_item(iris: str) -> str:
    """Return a query listing distinct concept parts connected to the supplied proposition/proof IRIs via mereological paths."""
    return _wrap(
        f"""
        SELECT DISTINCT ?o WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#contains_concept> ?o . }} # refers to / contains concept / contains concept
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#definition_refers_to> ?o . }} # refers to / contains concept / definition_refers_to
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / range / contains concept / contains_concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_range>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#definition_refers_to>  ?o . }} # refers to / range / contains concept / contains_concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#contains_concept>  ?o . }} # refers to / domain / contains concept / contains_concept
                union
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_domain>
                        / <https://www.foom.com/core#contains_concept>
                        / <https://www.foom.com/core#definition_refers_to>  ?o . }} # refers to / domain / contains concept / contains_concept
        }}
        """
    )


def mereological_is_concept_in(iris: str) -> str:
    return _wrap(
        f"""
        PREFIX core: <https://www.foom.com/core#>

        SELECT
        ?o
        (COUNT(*) AS ?links)
        WHERE {{
        VALUES ?s {{ {iris} }}
        ?s
                core:is_concept_in ?o .
        }}
        GROUP BY ?o
        ORDER BY DESC(?links)
        """
    ) 



# ---------------------------------------------------------------------------
# Hebbian-style queries
# ---------------------------------------------------------------------------

def hebb_definitions() -> str:
    """Return a query counting how often pairs of concepts are defined together by the same definition individual."""
    return _wrap(
        """
        SELECT
            ?o1
            ?o2
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#definition> .
            ?s <https://www.foom.com/core#defines> ?o1 .
            ?s <https://www.foom.com/core#defines> ?o2 .
            FILTER(?o1 != ?o2)
        }
        group by ?o1 ?o2
        order by desc(?links)
        """
    )


def hebb_postulates() -> str:
    """Return a query counting concept pairs co-occurring within a postulate's `refers_to` links and contained concepts."""
    return _wrap(
        """
        SELECT
            ?o1
            ?o2
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#postulate> .
            { ?s <https://www.foom.com/core#refers_to> ?o1 . }
            UNION
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o1 . }
            { ?s <https://www.foom.com/core#refers_to> ?o2 . }
            UNION
            { ?s <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o2 . }
            FILTER(?o1 != ?o2)
        }
        group by ?o1 ?o2
        order by desc(?links)
        """
    )


def hebb_common_notions() -> str:
    """Return a query counting concept pairs co-occurring in common notions via `has_statement` and derived `refers_to` edges."""
    return _wrap(
        """
        SELECT
            ?o1
            ?o2
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#common_notion> .
            { ?s <https://www.foom.com/core#has_statement> ?o1 . }
            UNION
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to> ?o1 . }
            UNION
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o1 . }
            { ?s <https://www.foom.com/core#has_statement> ?o2 . }
            UNION
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to> ?o2 . }
            UNION
            { ?s <https://www.foom.com/core#has_statement>
                    / <https://www.foom.com/core#refers_to>
                    / <https://www.foom.com/core#contains_concept> ?o2 . }
            FILTER(?o1 != ?o2)
        }
        group by ?o1 ?o2
        order by desc(?links)
        """
    )


def hebb_template_propositions_proofs(iris: str) -> str:
    """Return a query counting concept pairs referenced together by the supplied proposition/proof IRIs through direct `refers_to` paths."""
    return _wrap(
        f"""
        SELECT ?o1 ?o2 (count (*) as ?links) WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#refers_to> ?o1 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept> ?o1 . }}
                {{ ?s <https://www.foom.com/core#refers_to> ?o2 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#contains_concept> ?o2 . }}
                FILTER(?o1 != ?o2)
        }} group by ?o1 ?o2 order by desc(?links)
        """
    )


def hebb_template_propositions_proofs_types(iris: str) -> str:
    """Return a query counting type-based concept pairs for the supplied proposition/proof IRIs."""
    return _wrap(
        f"""
        SELECT ?o1 ?o2 (count (*) as ?links) WHERE {{
            values ?s {{ {iris} }}
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type> ?o1 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#contains_concept> ?o1 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type> ?o1 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#contains_concept> ?o1 . }}
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type> ?o2 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_relation_type>
                        / <https://www.foom.com/core#contains_concept> ?o2 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type> ?o2 . }}
                UNION
                {{ ?s <https://www.foom.com/core#refers_to>
                        / <https://www.foom.com/core#has_operation_type>
                        / <https://www.foom.com/core#contains_concept> ?o2 . }}
                FILTER(?o1 != ?o2)
        }} group by ?o1 ?o2 order by desc(?links)
        """
    )


##########
def find_proposition_types() -> str:
    return _wrap(
        """
        SELECT ?proposition_pref_label ?proposition_type_pref_label
        WHERE {
                ?proposition
                        a <https://www.foom.com/core#proposition> ;
                        <http://www.w3.org/2004/02/skos/core#prefLabel> ?proposition_pref_label ;
                        <https://www.foom.com/core#has_proposition_type> ?proposition_type .
                ?proposition_type
                        <http://www.w3.org/2004/02/skos/core#prefLabel> ?proposition_type_pref_label .
        }
        """
    )
