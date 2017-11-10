"""
This file is for the methods concerning everything the id3 algorithm
"""


class Tree(object):
    def __init__(self):
        self.classes = []
        self.entropy = None
        self.childs = []

    def print(self):
        print(self.classes)
        for node in self.childs:
            node.print(1)


class Node(object):
    def __init__(self):
        self.classes = []
        self.entropy = None
        self.childs = []
        self.splitattr = []

    def print(self, depth):
        print(depth, end='')
        print(self.classes)
        for node in self.childs:
            node.print(depth+1)


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



