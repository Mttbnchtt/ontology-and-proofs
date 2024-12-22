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


#################################################################################
# github issue 128
# Diff of concepts considering the analysis of proofs
CONCEPTS_INPUT_FILE_PATH = "input/Euclid.ConceptsAnalysis.Book1.csv"
PROOFS_INPUT_FILE_PATH = "input/Euclid.Proofs.Book1.csv"

def find_diff_concepts_proofs(concepts_input_file_path: str = CONCEPTS_INPUT_FILE_PATH,
                              proofs_input_file_path: str = PROOFS_INPUT_FILE_PATH,
                              verbose: bool = False):
    """
    Find concepts that are in proofs_df but not in concepts_df.

    Args:
        concepts_input_file_path (str): Path to the concepts input file. Defaults to CONCEPTS_INPUT_FILE_PATH.
        proofs_input_file_path (str): Path to the proofs input file. Defaults to PROOFS_INPUT_FILE_PATH.

    Returns:
        set: Concepts that are in proofs_df but not in concepts_df.
    """
    #  read input files
    concepts_df = pd.read_csv(concepts_input_file_path).fillna("")
    proofs_df = pd.read_csv(proofs_input_file_path).fillna("")

    # read columns from proofs_df and extract their concepts
    relation_concepts = extract_concepts(set(proofs_df["relation_instance"].values))
    operation_concepts = extract_concepts(set(proofs_df["operation_instance"].values))
    additional_proof_concepts = extract_concepts(set(proofs_df["additional_proof_concepts"].values))

    # store all the concepts from proofs_df in a unique set
    extracted_concepts_proofs = relation_concepts.union(operation_concepts).union(additional_proof_concepts)

    # store the concepts from concepts_df in a set
    extracted_concepts_concepts = set(concepts_df["concepts"].values)

    # find concepts that are in proofs_df but not in concepts_df
    diff_proofs_concepts = extracted_concepts_proofs.difference(extracted_concepts_concepts)

    if verbose:
        print("Concepts in proofs but not in list of concepts:")
        print(len(diff_proofs_concepts))
        print(*diff_proofs_concepts, sep="\n")

    return diff_proofs_concepts


def extract_concepts(items: set) -> set:
    """
    Extract concepts from a set of items.

    Args:
        items (set): Set of items to extract concepts from.

    Returns:
        set: Extracted concepts.
    """
    extracted_concepts = set()
    for item in items:
        item_edited = item.replace("(", " ").replace(")", " ").replace(",", " ").replace("->", " ")
        extracted_concepts.update({concept.strip() for concept in item_edited.split()})

    return extracted_concepts

#################################################################################
# github issue 135
# Diff of relations considering the analysis of proofs
RELATIONS_INPUT_FILE_PATH = "input/Euclid.RelationsAnalysis.Book1.csv"
OPERATIONS_INPUT_FILE_PATH = "input/Euclid.OperationsAnalysis.Book1.csv"
PROOFS_INPUT_FILE_PATH = "input/Euclid.Proofs.Book1.csv"

def find_diff_proofs(input_file_path: str = RELATIONS_INPUT_FILE_PATH, 
                     proofs_input_file_path: str = PROOFS_INPUT_FILE_PATH,
                     column_name: str = "relation_instance",
                     verbose: bool = False) -> set:
    """Finds the difference between relations in proofs and the list of relations.

    This function reads two CSV files, one containing a list of relations and the other containing relations used in proofs.
    It then compares the two lists and returns a set of relations that are in the proofs but not in the list of relations.

    Args:
        relations_input_file_path: The path to the CSV file containing the list of relations.
        proofs_input_file_path: The path to the CSV file containing the relations used in proofs.
        verbose: Whether to print information about the difference.

    Returns:
        A set of relations that are in the proofs but not in the list of relations.
    """
    #  read input files
    df = pd.read_csv(input_file_path).fillna("")
    proofs_df = pd.read_csv(proofs_input_file_path).fillna("")

    # put relation instances into sets
    items = set(item for item in df[column_name].str.strip() if item)
    proofs = set(item for item in proofs_df[column_name].str.strip() if item)

    # diff: relations in list proofs but not in list of relations
    diff_proofs = proofs.difference(items)

    # print information
    if verbose:
        print("Items in proofs but not in list of relations:")
        print(len(diff_proofs))
        print(*diff_proofs, sep="\n")

    # return the diff
    return diff_proofs