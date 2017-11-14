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

# at this point call the id3 algorithm and build tree
dtree = id3.test_node_class()


# at this point call the xml writer
fiha.write_xml(dtree)
