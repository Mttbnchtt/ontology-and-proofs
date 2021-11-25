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
    input = os.path.join("input", input)
    output = os.path.join("output", output)
    if verbose:
        print(message)
    with open(input) as ingestion:
        rows:list = ingestion.readlines()
        add:list = []
        for row in rows:
            lst:list = row.split()
            if len(lst) > 0:
                s:str = eval("f"+repr(message))
                if verbose:
                    print(s)
                add.append(s)
    with open(output, "a") as ontology:
        ontology.writelines(add)

def dependency(input:str="",
    output:str="",
    verbose:bool=False):
    message:str = """ 
# added UTC date and time {datetime.datetime.utcnow()}
# input: {row.strip()}
{lst[0]} a owl:NamedIndividual , 
         core:Proof_step ;
         core:proofStepStates [ a rdf:Statement ;
                                rdf:subject {lst[1]} ;
                                rdf:predicate {lst[2]} ;
                                rdf:object {lst[3]} ] .
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
         core:proofStepStates [ a rdf:Statement ;
                                rdf:subject {lst[1]} ;
                                rdf:predicate {lst[2]} ;
                                rdf:object {lst[3]} ] .
        """
    read_write(input=input, 
        output=output, 
        message=message, 
        verbose=verbose)


def main(args:argparse.Namespace, 
    verbose:bool=False):
    if args.type == "step":
        verbose = True if args.verbose in {True, ""} else False
        step(input=args.input, output=args.output)
    