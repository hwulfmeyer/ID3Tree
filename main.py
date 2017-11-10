"""
This file is for executing everything together
"""
import filehandling as fiha
import id3algorithm as id3


filepathnames = "datasets/cardaten/carnames.txt"
filepathdata = "datasets/cardaten/car.data"


classes, attributes, attribute_values = fiha.read_data_names(filepathnames)

print(classes)
print(attributes)
print(attribute_values)
