"""
This file is for executing everything together
"""
import filehandling as fiha
import id3algorithm as id3


filepathnames = "datasets/cardaten/carnames.txt"
filepathdata = "datasets/cardaten/car.data"


classes, attributes, attribute_values = fiha.read_data_names(filepathnames)
data = fiha.read_data(filepathdata)

print("Number of Classes: " + str(len(classes)))
print("Number of Attributes: " + str(len(attributes)))
print("Number of Instances: " + str(len(data)))
print(classes)
#print(data)

# at this point call the id3 algorithm and build tree
dtree = id3.test_node_class()
print (dtree.entropy)
dtree.print()
for childs in dtree.childs:
    print(childs.entropy)

# at this point call the xml writer
fiha.write_xml(dtree)
