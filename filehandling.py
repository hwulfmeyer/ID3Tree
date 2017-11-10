"""
This file is for the methods concerning everything from file reading to file writing
"""
import re


# function to read class names & attributes
def read_data_names(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    classes = re.sub(r'^' + re.escape("class values: "), '', lines.pop(0))
    classes = classes.split(", ")
    attributes = re.sub(r'^' + re.escape("attributes: "), '', lines.pop(0))
    attributes = attributes.split(", ")
    attributes_values = []

    for i in range(0, len(attributes)):
        values = re.sub(r'^' + re.escape(attributes[i] + ": "), '', lines.pop(0)).split(", ")
        attributes_values.append(values)

    return classes, attributes, attributes_values


# function to read the actual data
def read_data(filepath):
    # open file
    file = open(filepath, "r")


