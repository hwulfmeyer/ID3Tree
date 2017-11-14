"""
This file is for the methods concerning everything from file reading to file writing
"""
import re
import xml.etree.ElementTree as XElementTree
import id3algorithm as id3


def read_data_names(filepath: str):
    """
    function to read class names & attributes

    :param filepath: the relative path to the file containing the specifications of the attribute_values
    :return: a tuple of lists
        classes: is a one-dimensional list containing the class names
        attributes: is a one-dimensional list containing the attribute names
        attribute_values: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    """
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    classes = re.sub(r'^' + re.escape("class values: "), '', lines.pop(0))
    classes = classes.split(", ")
    attributes = re.sub(r'^' + re.escape("attributes: "), '', lines.pop(0))
    attributes = attributes.split(", ")

    attribute_values = []
    for i in range(0, len(attributes)):
        values = re.sub(r'^' + re.escape(attributes[i] + ": "), '', lines.pop(0))
        attribute_values.append(values.split(", "))

    return classes, attributes, attribute_values


def read_data(filepath: str):
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


def buildxmltree(cur_node: id3.Node, xml_parent: XElementTree.Element):
    """
    recursion function to output the leaves and nodes, but not the roo

    :param cur_node: the current node handled in our dtree
    :param xml_parent: the parent of in our xml tree
    """
    if len(cur_node.childs) > 1:
        for node_child in cur_node.childs:
                xml_child = XElementTree.SubElement(xml_parent, "node", classes=node_child.classes_to_string(),
                                                    entropy=str(node_child.entropy), attr=node_child.splitattr[1])
                buildxmltree(cur_node=node_child, xml_parent=xml_child)

    else:
        # get most popular class
        largestclass = -1
        for dclass in cur_node.classes:
            if dclass[1] > largestclass:
                xml_parent.text = dclass[0]


def indent(xmlnode: XElementTree.Element, level=0):
    i = "\n" + level*"  "
    if len(xmlnode):
        if not xmlnode.text or not xmlnode.text.strip():
            xmlnode.text = i + "  "
        if not xmlnode.tail or not xmlnode.tail.strip():
            xmlnode.tail = i
        for xmlnode in xmlnode:
            indent(xmlnode, level + 1)
        if not xmlnode.tail or not xmlnode.tail.strip():
            xmlnode.tail = i
    else:
        if level and (not xmlnode.tail or not xmlnode.tail.strip()):
            xmlnode.tail = i


def write_xml(dtree: id3.Node):
    """
    function, that creates a root of ElementTree and writing final XML

    :param dtree: Decision Tree object, see id3algorithm.py class Tree
    """
    root = XElementTree.Element("tree", classes=dtree.classes_to_string(), entropy=str(dtree.entropy))
    buildxmltree(cur_node=dtree, xml_parent=root)
    indent(xmlnode=root)
    tree = XElementTree.ElementTree(root)
    tree.write("test1.xml", "UTF-8", True)



