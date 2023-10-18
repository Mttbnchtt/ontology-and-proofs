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
    

# Euclid's heuristic techniques
# 1. Draw a diagram
# 1.1 Add auxiliary lines
# 1.1.1 Divide a figure into simpler figures
# 2. Work backwards
# 3. Apply previous theorems
# 3.2 Apply results concerning parallel lines
# 3.3 Apply results concerning perpendicular lines
# 3.4 Apply results concerning angles
# 3.1 Apply results on congruence of triangles
# 4. Reason by cases
# 5. Apply translation
# 5.1 Make figures overlap
# 5.2 Juxapose figures

# Pappus' heuristic techniques
# 1. Analysis (in the sense of Pappus)

# Heuristic techniques
# 1. Drawing a Diagram: Creating a clear, accurately scaled diagram to help visualize the problem.
# 2. Adding Auxiliary Lines: Adding extra lines such as medians or altitudes to simplify the problem.
# 3. Finding Symmetry: Identifying lines of symmetry or rotational symmetry in figures.
# 4. Applying Transformations: Using transformations like translation, rotation, or reflection.
# 5. Working Backwards: Starting from the goal and working backwards to what is given.
# 6. Considering Special Cases: Simplifying the problem by considering a specific or special case.
# 7. Using Coordinates: Assigning coordinates to points and using algebraic methods.
# 8. Applying Similar Triangles: Using properties of similar triangles to solve problems.
# 9. Checking for Parallel and Perpendicular Lines: Identifying parallel and perpendicular relationships.
# 10. Using Angle and Segment Relationships: Applying theorems related to angles and segments.
# 11. Applying Circle Theorems: Using theorems related to circles, such as arc length or sector area.
# 12. Dividing into Simpler Figures: Breaking a complex figure into simpler shapes.
