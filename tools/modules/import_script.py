__title__ = "Formal ontology of math"
__author__ = "Matteo Bianchetti"
__date__ = "2021-11"
__version__ = "0.1"

import argparse
import datetime
import os
import sys

def read_write(input:str="",
    output:str="",
    verbose:bool=False,
    message=""):
    """Read input file;
       prepare ttl triples;
       append triple to output file.

    Args:
        input (str, optional): the input file. Defaults to "".
        output (str, optional): the output file. Defaults to "".
        verbose (bool, optional): print verbose information. Defaults to False.
        message (str, optional): the template to generate the triples. Defaults to "".
    """
    input = os.path.join("input", input)
    output = os.path.join("output", output)
    if verbose:
        print(message)
    with open(input) as ingestion:
        rows:list = ingestion.readlines()
        if len(rows) == 0:
            print("Empty ingestion file.")
            sys.exit()
        triples:list = []
        for row in rows:
            lst:list = [i.strip().replace(" ", "") for i in row.split()]
            if len(lst) > 0:
                s:str = eval("f"+repr(message))
                if verbose:
                    print(s)
                triples.append(s)
    with open(output, "a") as ontology:
        ontology.writelines(triples)

def dependency(input:str="",
    output:str="",
    verbose:bool=False):
    message:str = """
# added UTC date and time {datetime.datetime.utcnow()}
# input: dependency {row.strip()}
{lst[0]} core:hasAntecedent {lst[1]} .
        """
    read_write(input=input, 
        output=output, 
        message=message,
        verbose=verbose)

def different(input:str="",
    output:str="",
    verbose:bool=False):
    input = os.path.join("input", input)
    output = os.path.join("output", output)
    with open(input) as ingestion:
        rows:list = ingestion.readlines()
        for row in rows:
            s:str = " ".join(rows)
    message:str = f""" 
# added UTC date and time {datetime.datetime.utcnow()}
# input: list all different individuals {row.strip()}
[ a owl:AllDifferent ;
  owl:distinctMembers ( {s} )
 ] .
        """
    if verbose:
        print(message)
    with open(output, "a") as ontology:
        ontology.write(message)

def individual(input:str="",
    output:str="",
    verbose:bool=False):
    message:str = """ 
# added UTC date and time {datetime.datetime.utcnow()}
# input: link step to proof {row.strip()}
{lst[0]} rdf:type owl:NamedIndividual, {lst[1]} .
            """
    read_write(input=input, 
        output=output, 
        message=message, 
        verbose=verbose)


def for_proof(input:str="",
    output:str="",
    verbose:bool=False):
    message:str = """ 
# added UTC date and time {datetime.datetime.utcnow()}
# input: link step to proof {row.strip()}
{lst[0]} core:inProof {lst[1]} .
            """
    read_write(input=input, 
        output=output, 
        message=message, 
        verbose=verbose)
            
def step(input:str="",
    output:str="",
    verbose:bool=False):
    message = """ 
# added UTC date and time {datetime.datetime.utcnow()}
# input: {row.strip()}
{lst[0]} a owl:NamedIndividual , 
         core:Proof_step ;
         a rdf:Statement ;
        rdf:subject {lst[1]} ;
        rdf:predicate {lst[2]} ;
        rdf:object {lst[3]}  .
        """
    read_write(input=input, 
        output=output, 
        message=message, 
        verbose=verbose)

"""" MAIN """
def main(args:argparse.Namespace, 
    verbose:bool=False):
    verbose = True if args.verbose in {True, ""} else False
    if args.type == "allDifferent":
        different(input=args.input, output=args.output, verbose=verbose)
    if args.type == "individual":
        individual(input=args.input, output=args.output, verbose=verbose)
    elif args.type == "step":
        step(input=args.input, output=args.output, verbose=verbose)
    elif args.type == "dependencies":
        dependency(input=args.input, output=args.output, verbose=verbose)
    elif args.type == "forProof":
        for_proof(input=args.input, output=args.output, verbose=verbose)


#  core:proofStepStates [ a rdf:Statement ;
#                         rdf:subject {lst[1]} ;
#                         rdf:predicate {lst[2]} ;
#                         rdf:object {lst[3]} ] .