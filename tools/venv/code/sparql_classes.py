import json
import urllib.parse
import requests
import typing # to add advanced type hinting
import urllib

class Row:
    """ Represents a single row of SPARQL query results. """
    def __init__(self, data):
        self.__dict__.update(data)
    """
    self.__dict__.update(data): 
    This line uses the update method 
    on the __dict__ attribute of the 
    object (self). The __dict__ attribute 
    is a special dictionary that stores 
    all the attributes (key-value pairs) 
    associated with the object. 
    By calling update on it with the 
    data dictionary, the __init__ method 
    effectively assigns all the key-value 
    pairs from the data dictionary 
    as attributes of the newly 
    created object.
    """

class SparqlQueryResults():
    """ Represents the results of a SPARQL query. """

    # initialize objects
    def __init__(self,
                sparql_query,
                rdfox_server:str = "http://localhost:12110",
                datastore:str = "/datastores/foom_pappus/sparql",
                format_response:str = "application/sparql-results+json"):
        self.sparql_query = sparql_query
        self.rdfox_server = rdfox_server
        self.datastore = datastore
        self.format_response = format_response
        self.response_text = self.query_ontology()
        self.response_dictionary = self.response_to_dictionary()
        self.rows = self.create_rows()
        self.index = 0  # For the iterator in the __next__ method
        # self.debug_query()
    
    def query_ontology(self) -> str:
        """ Submit SPARQL query and retrieve results. """
        # define the headers of the request
        headers = {
            "Accept": self.format_response
        }

        # query the datastore at the rdfox server
        response = requests.get(f"{self.rdfox_server}{self.datastore}",
                                params={"query": self.sparql_query},
                                headers=headers)
        
        # check if the REST endpoint returns an unexpected status code
        response.raise_for_status()
        
        # if the REST endpoint returns an expected response, return the text of the response
        return response.text

    # transform the text response to the ontology query
    # into a python dictionary and
    # extract the relevant information about
    # headers and values
    def response_to_dictionary(self) -> dict:
        """ Transform the SPARQL query response into a dictionary. """
        
        # transform the text response to the ontology query
        # into a json object
        response_data = json.loads(self.response_text)

        # select the headers for the new dictionary of data
        headers:list = response_data["head"]["vars"]

        # transform the json response into a dictionary
        # with headers and values
        response_dictionary:dict = {header: [] for header in headers}
        for binding in response_data["results"]["bindings"]:
            for header in headers:
                response_dictionary[header].append(binding[header]["value"])
                
        return response_dictionary

    # create rows of results
    def create_rows(self) -> list:
        """ Create Row objects for each result. """

        # list to append rows
        rows:list = []

        # find header names and number of rows to add to the list of rows
        headers:list = list(self.response_dictionary.keys())
        number_of_rows= len(self.response_dictionary[headers[0]])

        # add rows to the list of rows
        for index in range(number_of_rows):
            row_data = {header:self.response_dictionary[header][index]
                       for header in headers}
            rows.append(Row(row_data))

        return rows

    # make the object iterable using
    # the __iter__ functions and
    # the __next_ function
    def __iter__(self):
        return self

    def __next__(self):
        """ Iterate through the rows of the results. """
        if self.index < len(self.rows):
            result = self.rows[self.index]
            self.index += 1
            return result
        else:
            self.index = 0  # Reset for future iteration
            raise StopIteration