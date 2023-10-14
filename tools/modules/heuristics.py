__title__ = "Heuristics"
__author__ = "Matteo Bianchetti"
__date__ = "2023-10"
__version__ = "0.1"

import argparse
import json


def assert_response_ok(response, message):
    """
    Helper function to raise exception if the REST endpoint returns an
    unexpected status code

    Args:
        response (_type_): _description_
        message (_type_): _description_

    Raises:
        Exception: _description_
    """    
    if not response.ok:
        raise Exception(
            f"{message}\nStatus received= {response.status_code}\n{response.text}")
    
def read_input_file(input_file:str=""):
    with open(input_file) as f_input:
        input_data = json.load(f_input)
        return input_data
        


"""" MAIN """
def main(args:argparse.Namespace):
    input_data:dict = read_input_file(input_file=args.input)
    endpoint:str = input_data["endpoint"]
    dstore:str = input_data["dstore"]
