import io
import math
import os

import pandas as pd
import sympy
from sympy.parsing.sympy_parser import parse_expr
import tailer as tl

from settings import HEADERS


def calculate_hypotenuse(triangle_number):
    # A custom function for calculating the hypotenuse of the triangles can be
    # set. To get an exact value, use sympy instead of math. For example, do
    # "sympy.sqrt()" instead of "math.sqrt()".
    return math.sqrt(triangle_number + 1)


def write_triangle_data(triangle_dataframe, filename, create_new_file):
    """Save a dataframe to a csv file."""
    print("\nSaving data...")
    if create_new_file:
        print("Creating new file...")
        triangle_dataframe.to_csv(os.path.join("data", filename), index=False)
    else:
        print("Adding to file...")
        with open(os.path.join("data", filename), "a") as f:
            triangle_dataframe.to_csv(f, header=False, index=False)
    print("Done.")


def str_to_sympy(values):
    """Convert the strings in the csv file into numbers."""
    return [parse_expr(value) for value in values]


def read_last_triangle(filename):
    """Efficiently read only the last triangle's data from a csv file."""
    try:
        file = open(os.path.join("data", filename))
    except FileNotFoundError:
        return
    
    # Get the last line in the
    last_line = tl.tail(file, 1)
    file.close()
    
    try:
        triangle_dataframe = pd.read_csv(
            io.StringIO("\n".join(last_line)), names=HEADERS,
            dtype=str)
        try:
            return triangle_dataframe.apply(str_to_sympy)
        except SyntaxError:
            # There is only a header in the data file, so there is no actual
            # data.
            return
    except FileNotFoundError:
        return


def read_triangle_points(filename):
    """Get all triangle points from a csv file."""
    points = []
    
    # Read the file with the data.
    try:
        print("\nReading the data file...")
        try:
            triangle_dataframe = pd.read_csv(
                os.path.join("data", filename), index_col=HEADERS[0],
                dtype=str)
        except ValueError:
            print("\nThe index column title in the data file does not match "
                  "with the one set in the \"settings.py\" file. Make sure "
                  "the first string in the constant \"HEADERS\" matches the "
                  "index column of the data file (the leftmost column with "
                  "the triangle numbers).")
            return
        try:
            triangle_dataframe = triangle_dataframe.apply(str_to_sympy)
        except SyntaxError:
            # There is only a header in the data file, so there is no actual
            # data.
            return
    except FileNotFoundError:
        print("\nNo data file was found.")
        
        return
    
    try:
        assert len(triangle_dataframe) != 0
    except AssertionError:
        print("\nThe data file found doesn't contain anything.")
        
        return
    
    # Save each triangle's three points and number.
    for number, row in triangle_dataframe.iterrows():
        outside_left_point = [row['outside left x'],
                              row['outside left y']]
        outside_right_point = [row['outside right x'],
                               row['outside right y']]
        inside_point = [row['inside x'], row['inside y']]
        
        points.append((outside_left_point, outside_right_point, inside_point,
                       number))
    
    return points


def get_input(input_message, input_type, default=None, valid_inputs=()):
    """Get user input."""
    value = None
    while value is None:
        value = input(input_message)
        if value == "":
            if default is not None:
                print(f"Defaulted to {default}.")
                value = default
            else:
                print("There is no default value for this option.")
        else:
            try:
                value = input_type(value)
                if valid_inputs and value not in valid_inputs:
                    print("That is not a valid input.")
                    value = None
            except ValueError:
                print("That is not a valid input type.")
                value = None
    
    return value
