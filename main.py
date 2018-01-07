"""
This file is for executing everything together
"""
import filehandling as fiha
import id3algorithm as id3


filepathnames = "datasets/cardaten/carnames.data"
filepathdata = "datasets/cardaten/car.data"

# read data
classes, attributes, attribute_values = fiha.read_data_names(filepath=filepathnames)
instances = fiha.read_data(filepath=filepathdata)
print("Number of Classes: " + str(len(classes)))
print("Number of Attributes: " + str(len(attributes)))
train_data, test_data = fiha.separation(instances)
print("Number of Training Instances: " + str(len(train_data)))
print("Number of Test Instances: " + str(len(test_data)))

# at this point call the id3 algorithm and build tree
dtree = id3.builddtree(classes, train_data, attributes, attribute_values, attributes.copy())

print("ID3 algorithm finished")

# at this point call the xml writer
fiha.write_xml(dtree=dtree)
print("XML writing finished")

testdata_classes = id3.get_classes(dtree, attributes, test_data)
test_error = id3.calculate_error(testdata_classes)
print("Error rate: " + str(test_error))

confusion_matrix = id3.get_confusion_matrix(classes, testdata_classes)

print("\nConfusion Matrix:")
for x in confusion_matrix:
    print(x)

