"""
This file is for the methods concerning everything the id3 algorithm
"""
import math


class Tree(object):
    """
    class to create a tree object

    :param self.classes: two-dimensional list where each row is a class with the number of instances
        e.g. [["class1", 123], ["class2", 234], ["class3", 345]]
    :param self.entropy: float value of the entropy in this node
    :param self.childs: one-dimensional list containing the references to the child nodes
    """
    def __init__(self):
        self.classes = []
        self.entropy = None
        self.childs = []

    def classes_to_string(self):
        result = ""
        for classes in self.classes:
            result += str(classes[0]) + ":" + str(classes[1]) + ","
        if len(result) > 0:
            result = result[0:len(result) - 1]
        return result


class Node(Tree):
    """
    Nodes in Tree, inheritance of class Tree

    :param self.splitattr: one-dimensional list containing the attribute taken for the split and
        the value of the attribute all the instances in this node have e.g.: ["Weather", "cold"]
    :param self.splitattributes: one.dimensional list containg each attribute left to use
    :param self.data: contains current data(instances) in this node
    """
    def __init__(self):
        Tree.__init__(self)
        self.splitattr = []
        self.splitattributes = []
        self.data = []


def entropy(classes: list, instances: list):
    """
    function to calculate the entropy of the given instances

    :param classes: is a one-dimensional list containing the class names
    :param instances: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    :return: entropy of our instances
    """
    # extract last column containing the classes
    instances = [row[-1] for row in instances]
    num_instances = len(instances)
    result = 0.0
    for dclass in classes:
        pfraction = sum(inst[0] == dclass[0] for inst in instances)/num_instances
        if pfraction != 0:
            result -= pfraction * math.log(pfraction, len(classes))
    return result


def infogain(classes: list, instances: list, attributes: list, attr: str):
    """
    function to calculate the informationgain of the given attribute and instances
    TODO: Again, I really hope, that it will work on practise succeffully,
    however with first root(and attr bying) it works and show infogain 0.048

    :param classes: is a one-dimensional list containing the class names
    :param instances: is a two-dimensional list where each row respresents
          one attribute(in the order of 'attributes') and the possible values
    :param attributes: is one dimensional list that contains the names of attributes
    :param attr: atrribute for which it's calculating the infogain
    :return InformationGain on this node
    """
    sub_entropy = 0
    num_inctances = len(instances)
    index_of_attr = attributes.index(attr)
    val_freq = {}

    # this loop creates a dict where counting the frequency of attribute_value: {vhigh :20, high :10} and etc
    for i in instances:
        if i[index_of_attr] in val_freq:
            val_freq[i[index_of_attr]] += 1
        else:
            val_freq[i[index_of_attr]] = 1
    """
    this loop is creating car probability_attr(where its division of number instances of certian value and number of instances)
    further it creates the reduced_data, where only instances with certain value of attr(for example Bying = "vhigh"
    and finding entropy of this class
    """
    for attrib in val_freq.keys():
        probability_attr = val_freq[attrib] / num_inctances
        reduced_data = [i for i in instances if i[index_of_attr] == attrib]
        sub_entropy += probability_attr * entropy(classes, reduced_data)

    gain = entropy(classes, instances) - sub_entropy
    return gain


def builddtree(classes: list, instances: list, attributes: list):
    root = Tree()
    root.entropy = 0.123
    root.classes = [["class1", 123], ["class2", 234], ["class3", 345]]
    node_11 = Node()
    node_12 = Node()
    root.childs = [node_11, node_12]
    return root


def test_node_class():
    """
    this function just tests the node class and doesnt do anything else,
    I took the data from the example in the assignment
    """
    root = Tree()
    root.entropy = 0.123
    root.classes = [["class1", 123], ["class2", 234], ["class3", 345]]
    node_11 = Node()
    node_12 = Node()
    root.childs = [node_11, node_12]

    # child of root node
    node_11.entropy = 0.234
    node_11.classes = [["class1", 23], ["class2", 123]]
    node_11.splitattr = ["attr1", "value1"]
    node_111 = Node()
    node_112 = Node()
    node_11.childs = [node_111, node_112]

    # continue with childs of the node 'node_11'
    node_111.entropy = 0.0
    node_111.classes = [["class1", 23]]
    node_111.splitattr = ["attr2", "value1"]

    node_112.entropy = 0.0
    node_112.classes = [["class2", 123]]
    node_112.splitattr = ["attr2", "value2"]

    # child of root node
    node_12.entropy = 0.345
    node_12.classes = [["class1", 34], ["class2", 45], ["class3", 56]]
    node_12.splitattr = ["attr1", "value2"]

    return root



