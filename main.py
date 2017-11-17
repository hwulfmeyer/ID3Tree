"""
This file is for executing everything together
"""
import filehandling as fiha
import id3algorithm as id3


filepathnames = "datasets/cardaten/carnames.txt"
filepathdata = "datasets/cardaten/car.data"


classes, attributes, attribute_values = fiha.read_data_names(filepath=filepathnames)
instances = fiha.read_data(filepath=filepathdata)

print("Number of Classes: " + str(len(classes)))
print("Number of Attributes: " + str(len(attributes)))
print("Number of Instances: " + str(len(instances)))

# at this point call the id3 algorithm and build tree
# dtree = id3.test_node_class()
dtree = id3.builddtree(classes=classes, instances=instances, attributes=attributes,
                       attributesvalues=attribute_values, attributesleft=attributes.copy())

# at this point call the xml writer
fiha.write_xml(dtree=dtree)
# attributes: buying, maint, doors, persons, lug_boot, safety
instance = ["high", "med", "5more", "more", "med", "high", "unacc"]

print(id3.getclass(dtree, instance, attributes))
#check accuracy of our tree?

