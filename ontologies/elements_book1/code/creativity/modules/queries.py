def direct_definitions():
    return """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s  a <https://www.foom.com/core#definition> ; 
                <https://www.foom.com/core#defines> ?o .
        }
        group by ?o
        order by desc(?links) 
        """

def direct_postulates()
    return """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#postulate> .
            { ?s <https://www.foom.com/core#refers_to> ?o . } # refers to
            union
            { ?s <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#contains_concept> ?o . } # refers to / contains concept
            ######################
            union
            { ?s <https://www.foom.com/core#refers_to> ?o . } # refers to / range
            ######################
            union
            { ?s <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_range> ?o . } # refers to / range
            union
            { ?s <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / range / contains concept
            #####################
            union
            { ?s <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_domain> ?o . } # refers to / domain
            union
            { ?s <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / domain / contains concept
        }
        group by ?o
        order by desc(?links) 
        """