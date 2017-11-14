"""
This file is for the methods concerning everything from file reading to file writing
"""
import re
import xml.etree.ElementTree as XElementTree


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


def buildxmltree(cur_node, xml_parent):
    """
    recursion funtction to output the leaves and nodes, but not the roo

    :param cur_node:
    :param xml_parent:
    :return:
    """
    if len(cur_node.childs) > 1:
        for node_child in cur_node.childs:
                xml_child = XElementTree.SubElement(xml_parent, "node", classes=node_child.classes_to_string(),
                                                    entropy=str(node_child.entropy), attr=node_child.splitattr[1])
                buildxmltree(node_child, xml_child)

    else:
        xml_parent.text = str(cur_node.classes[0][0])


def write_xml(dtree):
    """
    function, that creates a root of ElementTree and writing final XML

    :param dtree:
    :return:
    """
    root = XElementTree.Element("tree", classes=dtree.classes_to_string(), entropy=str(dtree.entropy))
    buildxmltree(dtree, root)
    tree = XElementTree.ElementTree(root)
    tree.write("test1.xml")
    return 0
