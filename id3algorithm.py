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
        return result[0:len(result)-1]


class Node(Tree):
    """
    Nodes in Tree, inheritance of class Tree

    :param self.splitattr: one-dimensional list containing the attribute taken for the split and
        the value of the attribute all the instances in this node have e.g.: ["Weather", "cold"]
        self.splitattributes: one.dimensional list containg each attribute already used
    """
    def __init__(self):
        Tree.__init__(self)
        self.splitattr = []
        self.splitattributes = []


def entropy(classes, instances):
    """
    function to calculate the entropy of the given instances

    :param classes: is a one-dimensional list containing the class names
    :param instances: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    :return: entropy of our instances
    """
    # extract last column containg the classes
    instances = [row[-1] for row in instances]
    num_instances = len(instances)
    result = 0.0
    for dclass in classes:
        pfraction = sum(inst[0] == dclass[0] for inst in instances)/num_instances
        if pfraction != 0:
            result -= pfraction * math.log(pfraction, len(classes))
    return result

def infogain():
    #TODO
    return 0


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



