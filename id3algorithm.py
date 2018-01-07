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
            result = result[0:-1]
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
        self.classname = None


def entropy(classes: list, instances: list):
    """
    function to calculate the entropy of the given instances

    :param classes: is a one-dimensional list containing the class names
    :param instances: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    :return: entropy of our instances, classes with absolute frequency in instances
    """
    # extract last column containing the classes
    if len(instances) == 0:
        return 0, []
    instances = [row[-1] for row in instances]
    numclassinstances = []
    num_instances = len(instances)
    result = 0.0
    for dclass in classes:
        classfrequency = [dclass, sum(inst[0] == dclass[0] for inst in instances)]
        pfraction = classfrequency[-1]/num_instances
        if pfraction != 0:
            numclassinstances.append(classfrequency)
            result -= pfraction * math.log(pfraction, len(classes))
    return result, numclassinstances


def infogain(classes: list, instances: list, attributes: list, attr: str):
    """
    function to calculate the informationgain of the given attribute and instances

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
        sub_entropy += probability_attr * entropy(classes, reduced_data)[0]
    gain = entropy(classes, instances)[0] - sub_entropy
    return gain


def builddtree(classes: list, instances: list, attributes: list, attributesvalues: list, attributesleft: list):
    """
    ID3 Algorithm start for root node

    :param classes: is a one-dimensional list containing the class names
    :param instances: is a two-dimensional list where each row respresents
          one attribute(in the order of 'attributes') and the possible values
    :param attributes: is one dimensional list that contains the names of attributes
    :param attributesvalues: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    :param attributesleft: attributes left for the current node to split on
    :return: a decision tree for the data
    """
    decisiontree = Tree()
    decisiontree.entropy, decisiontree.classes = entropy(classes=classes, instances=instances)
    if decisiontree.entropy == 0.0:
        return decisiontree
    largestclass = 0
    for dclass in decisiontree.classes:
        if dclass[1] > largestclass:
            largestclass = dclass[1]
            decisiontree.classname = dclass[0]
    decisiontree.childs = builddtreechilds(classes=classes, instances=instances, attributes=attributes,
                                           attributesvalues=attributesvalues, attributesleft=attributesleft)
    return decisiontree


def builddtreechilds(classes: list, instances: list, attributes: list, attributesvalues: list, attributesleft: list):
    """
    ID3 Algorithm for child nodes

    :param classes: is a one-dimensional list containing the class names
    :param instances: is a two-dimensional list where each row respresents
          one attribute(in the order of 'attributes') and the possible values
    :param attributes: is one dimensional list that contains the names of attributes
    :param attributesvalues: is a two-dimensional list where each row respresents
            one attribute(in the order of 'attributes') and the possible values
    :param attributesleft: attributes left for the current node to split on
    :return: childs of current node with recursion on childs
    """
    if len(attributesleft) == 0 or len(instances) == 0:
        return []

    # get best attribute
    bestinfog = [None, -1]
    for attrib in attributesleft:
        curinfogain = infogain(classes=classes, instances=instances, attributes=attributes, attr=attrib)
        if curinfogain > bestinfog[1]:
            bestinfog[1] = curinfogain
            bestinfog[0] = attrib

    attributesleft.remove(bestinfog[0])
    childlist = []

    # create child nodes
    for value in attributesvalues[attributes.index(bestinfog[0])]:
        childnode = Node()
        childnode.splitattr = [bestinfog[0], value]
        childnodeinstances = []
        for instance in instances:
            if instance[attributes.index(bestinfog[0])] == value:
                childnodeinstances.append(instance)
        childnode.entropy, childnode.classes = entropy(classes=classes, instances=childnodeinstances)

        largestclass = -1
        for dclass in childnode.classes:
            if dclass[1] > largestclass:
                largestclass = dclass[1]
                childnode.classname = dclass[0]

        if childnode.entropy > 0:
            childnode.childs = builddtreechilds(classes=classes, instances=childnodeinstances, attributes=attributes,
                                                attributesvalues=attributesvalues, attributesleft=attributesleft.copy())
            for childchild in childnode.childs:
                if len(childchild.classes) == 0:
                    childchild.classname = childnode.classname

        childlist.append(childnode)

    return childlist


def get_classes(dtree: Node, attributes: list, data: list):
    """
    function to get the predicted classes of each instance in data

    :param dtree: a 2-dimensional list containg the classes, the total frequency, the number of total instances
        and the fraction of instances being that class
    :param attributes: a x-dimensional list containing the probability of each attribute value to occur under a
        specific class
    :param data: is a two-dimensional list where each row respresents
        one attribute(in the order of 'attributes') and the possible values
    :return: a 1-dimensional list containg the orignal and predicted class of each instance in data
    """
    dataclasses = []
    for d in data:
        dataclasses.append([d[-1], getclass(dtree, d, attributes)])
    return dataclasses


def getclass(dtree: Node, instance: list, attributes: list):
    iklass = ''
    while iklass == '':
        for childnode in dtree.childs:
            if instance[attributes.index(childnode.splitattr[0])] == childnode.splitattr[1]:
                dtree = childnode
        if len(dtree.childs) == 0:
            iklass = dtree.classname
    return iklass


def calculate_error(dataclasses):
    """
    calculates error
    """
    wrong = 0
    correct = 0

    for d in dataclasses:
            if d[0] == d[1]:
                correct += 1
            else:
                wrong += 1
    return wrong / (wrong+correct)


def get_confusion_matrix(classes: list, dataclasses: list):
    """
    creates a confusion matrix

    :param classes: is a one-dimensional list containing the class names
    :param dataclasses: a 1-dimensional list containg the orignal and predicted class of each instance in data
    :return: a 2-dimensional list with the first row being the actual class and every other row corresponding
        to the number of instances being predicted as class x
    """
    confmatrix = []
    for x in classes:
        line = [x]
        for y in classes:
            line.append(sum(x == inst[0] and y == inst[1] for inst in dataclasses))
        confmatrix.append(line)
    return confmatrix
