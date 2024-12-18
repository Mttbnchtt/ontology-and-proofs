import os
import pandas as pd
import rdflib
import re

def edit_string(input_string: str) -> str:
    # import re
    """Cleans up an input string for use in an IRI.

    Replaces whitespace, multiple consecutive underscores, and non-alphanumeric
    characters with single underscores. Also removes leading/trailing whitespace.

    Args:
        input_string: The string to be cleaned.

    Returns:
        The cleaned string.
    """
    input_string = input_string.replace(" -> ", "->")
    # Use a regular expression to replace all unwanted characters
    string = re.sub(r'\s|_{2,}|[^\w\s]', '_', input_string)
    # \s matches withespace characters (spaces, tabs, newlines, etc.)
    # | acts as an OR operator: it will match if the pattern on either side of the | is found
    # _{2,} matches an underscore character that appears two or more times consecutively
    # {2,} is a quantifier specifying '2 or more' occurrences of the preceding element
    # [^\w\s] matches any character that is not a word character or a whitespace character
    # ^ inside the square brackets acts as a negation
    # \w matches any word character (alphanumeric characters and underscores)
    return string.lower().strip()

def capitalize_first_letter(text):
    if len(text) == 0:
        return text  # Return empty string if input is empty
    return text[0].upper() + text[1:]

def read_text_file(file_path: str) -> list:
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def create_iri(input_string: str,
               namespace:str = "https://www.foom.com/core") -> rdflib.URIRef:
    """Creates an IRI (Internationalized Resource Identifier).

    Combines a namespace with a cleaned version of the input string to form
    a unique IRI using the rdflib library.

    Args:
        input_string: The base string for the IRI.
        namespace: The namespace for the IRI (defaults to "https://www.foom.com/euclid").

    Returns:
        An rdflib.URIRef object representing the IRI.
    """

    iri = rdflib.URIRef(f"{namespace}#{edit_string(input_string)}")
    return iri

def output_ontology(kg: rdflib.Graph,
                    folder_path: str,
                    file_name: str,
                    selected_format: str) -> None:
    output_file_path = os.path.join(folder_path, file_name)
    with open(output_file_path, "w") as f:
        f.write(kg.serialize(format=selected_format))


def diff_concepts_propositions_and_concepts_list(propositions_input_file_path: str,
                                                 concepts_analysis_input_file_path: str) -> None:
    propositions_df = pd.read_csv(propositions_input_file_path).fillna("")
    concepts_df = pd.read_csv(concepts_analysis_input_file_path).fillna("")

    concepts_propositions_set = set()
    concepts_set = {row["concepts"] for _, row in concepts_df.iterrows()}

    for _, row in propositions_df.iterrows():
        concepts = [concept.strip() for concept in row["proposition_concepts"].split(",")]
        for concept in concepts:
            concepts_propositions_set.add(concept)
    
    concepts_not_in_propositions_set = sorted(list(concepts_set - concepts_propositions_set))
    concepts_not_in_concepts_set = sorted(list(concepts_propositions_set - concepts_set))

    print("Concepts not in propositions:")
    print(concepts_not_in_propositions_set)

    print("Concepts not in set of concepts:")
    print(concepts_not_in_concepts_set)