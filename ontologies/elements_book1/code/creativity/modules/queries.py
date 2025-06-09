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

def direct_postulates():
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

def direct_common_notions():
    return """
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
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> ?o . } # refers to 
            union
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_range> ?o . } # refers to / range
            union
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / range / contains concept
            #####################
            union
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_domain> ?o . } # refers to / domain
            union
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / domain / contains concept
        }
        group by ?o
        order by desc(?links) 
        """

def hierarchical_definitions():
    return """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#definition> .
            ?s <https://www.foom.com/core#defines> 
                    / <https://www.foom.com/core#is_sub_concept_of> ?o . # sub concept of
        }
        group by ?o
        order by desc(?links) 
        """

def hierarchical_postulates():
    return """
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
        }
        group by ?o
        order by desc(?links) 
        """

def hierarchical_common_notions():
    return """
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
        }
        group by ?o
        order by desc(?links) 
    """

def mereological_definitions():
    return """
        SELECT
            ?o
            (count (*) as ?links)
        WHERE {
            ?s a <https://www.foom.com/core#definition> .
            { ?s <https://www.foom.com/core#defines> 
                    / <https://www.foom.com/core#definition_refers_to> ?o . } 
            UNION
            { ?s <https://www.foom.com/core#defines> 
                    / <https://www.foom.com/core#contains_concept> ?o . } 
        }
        group by ?o
        order by desc(?links)
        """
def mereological_postulates():  
    return """
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

def mereological_common_notions():
    return """
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
            UNION
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_range>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to>  ?o . } # refers to / range / contains concept / definition_refers_to
            #####################
            UNION
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#contains_concept>  ?o . } # refers to / domain / contains concept / contains_concept
            UNION
            { ?s <https://www.foom.com/core#has_statement> 
                    / <https://www.foom.com/core#refers_to> 
                    / <https://www.foom.com/core#has_domain>
                    / <https://www.foom.com/core#contains_concept>
                    / <https://www.foom.com/core#definition_refers_to>  ?o . } # refers to / domain / contains concept / definition_refers_to
        }
        group by ?o
        order by desc(?links) 
    """