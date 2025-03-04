SPARQL queries

1. q1: count links between elements

"""
SELECT
    ?s ?o
    (count (*) as ?links)
WHERE {
    ?s <https://www.foom.com/core#refers_to> / <https://www.foom.com/core#contains_concept>* / <https://www.foom.com/core#is_super_concept_of>* / <https://www.foom.com/core#has_range>*  ?o .
}
group by ?s ?o
order by desc(?links)
"""