"""
This file is for the methods concerning everything from file reading to file writing
"""
import re
import xml.etree.cElementTree as ET


def read_data_names(filepath):
    """
    function to read class names & attributes

    :param filepath: the relative path to the file containing the specifications of the data
    :return: a tuple of lists
        classes: is a one-dimensional list containing the class names
        attributes: is a one-dimensional list containing the attribute names
        attributes_values: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    """

    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    classes = re.sub(r'^' + re.escape("class values: "), '', lines.pop(0))
    classes = classes.split(", ")
    attributes = re.sub(r'^' + re.escape("attributes: "), '', lines.pop(0))
    attributes = attributes.split(", ")

    attributes_values = []
    for i in range(0, len(attributes)):
        values = re.sub(r'^' + re.escape(attributes[i] + ": "), '', lines.pop(0))
        attributes_values.append(values.split(", "))

    return classes, attributes, attributes_values


def read_data(filepath):
    """
    function to read the actual data

    :param filepath: the relative path to the file containing the specifications of the data
    :return: the data in filepath as a two-dimensional list where each row represents one instance and
        its values
    """

    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    data = []
    for line in lines:
        data.append(line.split(","))
    return data


# recursion funtction to output the leaves and nodes, but not the root
def xmlcreator(dtree, root):  
        for childs1 in dtree.childs:
            if len(childs1.classes) > 1:
                root1 = ET.SubElement(root, "node", classes=childs1.classes,
                                      entropy=str(childs1.entropy), attr=childs1.splitattr[1])
                xmlcreator(childs1, root1)
            else:
                    ET.SubElement(root, "node", classes=childs1.classes,
                                  entropy=str(dtree.entropy), attr=dtree.splitattr[1]).text = str(childs1.classes[0][0])


# function, that creates a root of ElementTree and prtinting final XML
def write_xml(dtree):
    root = ET.Element("tree", classes=dtree.classes, entropy=str(dtree.entropy))
    xmlcreator(dtree, root)
    tree = ET.ElementTree(root)
    tree.write("test1.xml")
    return 0
