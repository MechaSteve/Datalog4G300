# Use file open to open the example G3X file  and read in the example 
# From this file create a dictionary from the first line as the file header
# Create a rowHeaders dictionary from the next two lines of format { "var name": "Value Label", ...
# when varName is ommited create a dummy name "unused1", "unused2", ...
# Open the G300 file and create the same dictionaries. use "noName1", "noName2", ... (don't match to the dummy names used in the example)
# read in the data rows from the G300 file using the dicitonary reader with row_headers.keys.tolist() to a datalog object

# iterate through datalog and create datalog_clean
# cache last lcl_date, and if it changes by more than 2 days, reset, and discard any rows previous
# add an offset to the lcl_date
# GPS time of week is calculatable as seconds since midnight sunday morning plus 18

# Name the new datalog based on the Aircraft N number and the local datetime stamp
# Write a new file header based on the example file
# write the two row header lines from the example to the new file
# use the dictionary writer to write out the datalog object

import shlex, csv
from datetime import date


# parse fields in input file to create datalog object: a list of dictionaries
f = open('input/log_G300MFD.csv', 'r')
input_file_info = {key:value for (key, value) in [(field.split('=')[0], shlex.split(field.split('=')[1])[0]) for field in f.readline().split(',')[1:]]}


# read line with column units and convert to G3X format
input_units = []
for name in [unit.strip() for unit in f.readline().split(',')] :
    if name == 'enum' or name == '+/-1.0' or name == 'ident':
        input_units.append('')
    elif name == 'deg true':
        input_units.append('deg')
    elif name == 'kts':
        input_units.append('kt')
    elif name == 'fpm':
        input_units.append('ft/min')
    else:
        input_units.append(name)

# read in the data column labels from the input file and replace some to match the G3X formatting.
input_row_labels = []
for label in [label.strip() for label in f.readline().split(',')]:
    if label.startswith('Local'):
        input_row_labels.append(label.split(' ')[1])
    elif label.startswith('Ground'):
        input_row_labels.append(f"GPS {label}")
    elif label.startswith('Active Waypoint'):
        input_row_labels.append(f"Nav {label.split(' ')[-1]}")
    elif label.endswith('Alt'):
        input_row_labels.append(f"{label}itude")
    elif label == 'Cross Track Error':
        input_row_labels.append(f"Nav Cross Track Distance")
    elif label == 'IAS':
        input_row_labels.append(f"Indicated Airspeed")
    elif label == 'TAS':
        input_row_labels.append(f"True Airspeed")
    elif label == 'Heading':
        input_row_labels.append(f"Magnetic Heading")
    elif label == 'HSI Source':
        input_row_labels.append(f"Active Nav Source")
    elif label == 'Course':
        input_row_labels.append(f"Nav Course")
    elif label == 'GPS Fix':
        input_row_labels.append(f"GPS Fix Status")
    else:
        input_row_labels.append(label)

# create full labels
input_labels_full = []
for (label, unit) in zip(input_row_labels, input_units):
    if unit == '':
        input_labels_full.append(label)
    else:
        input_labels_full.append(f"{label} ({unit})")

# TODO : clean up jumps in date and time (combine with reading in data rows)
# If the date jumps by more than 1 day or the time jumps by more than one hour, throw out all of the previous rows
        
# TODO offset the date field based on the file name
# use datetime.fromordinal(date.toordinal() + date_offset)
# 
        
# TODO create input label for GPS time of week and calculate for each row of data log
# date.isoweekday() % 7 will yield 0 for sunday and 6 for Saturday

# Read in the header of the example template
f = open('example/log_G3X.csv')
example_file_info = {key:value for (key, value) in [(field.split('=')[0], shlex.split(field.split('=')[1])[0]) for field in f.readline().split(',')[1:]]}
example_file_labels = [label.strip() for label in f.readline().split(',')]
example_file_name = f.readline().strip()


print(input_file_info)
print(input_row_labels)
print(input_units)
print(input_labels_full)



print('example file\n=================\n')
print(example_file_info)

input_matching = {}
for label in example_file_labels:
    input_matching[label] = label in input_labels_full

print(input_matching)


print('\ninput file matching\n=================\n')
input_matching = {}
for label in input_labels_full:
    input_matching[label] = label in example_file_labels

for label in input_labels_full:
    print(f"{label} : {input_matching[label]}")





