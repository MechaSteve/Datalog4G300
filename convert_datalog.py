import csv
from datetime import date

# Use file open to open the example G3X file  and read in the example 
# From this file create a dictionary from the first line as the file header
# Create a rowHeaders dictionary from the next two lines of format { "var name": "Value Label", ...
# when varName is ommited create a dummy name "unused1", "unused2", ...
# Open the G300 file and create the same dictionaries. use "noName1", "noName2", ... (don't match to the dummy names used in the example)
# read in the data rows from the G300 file using the dicitonary reader with row_headers.keys.tolist() to a datalog object

# iterate through datalog and create datalog_clean
# cache last lcl_date, and if it changes by more than 2 days, reset, and discard any rows previous
# add an offset to the lcl_date

# Name the new datalog based on the Aircraft N number and the local datetime stamp
# Write a new file header based on the example file
# write the two row header lines from the example to the new file
# use the dictionary writer to write out the datalog object

