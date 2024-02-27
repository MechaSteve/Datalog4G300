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

import csv
from datetime import date
from collections.abc import Iterable
from os.path import isfile
from os import listdir


def get_input_units(raw_data : str) -> list[str]:
    # read line with column units and convert to G3X format
    units = []
    for name in [field.strip() for field in raw_data.split(',')] :
        if name == 'enum' or name == '+/-1.0' or name == 'ident':
            units.append('')
        elif name == 'deg true':
            units.append('deg')
        elif name == 'kts':
            units.append('kt')
        elif name == 'fpm':
            units.append('ft/min')
        else:
            units.append(name)
    return units

def get_input_lables(raw_data: str) -> list[str]:
    # read in the data column labels from the input file and replace some to match the G3X formatting.
    converted_labels = []
    for label in [label.strip() for label in raw_data.split(',')]:
        if label.startswith('Local'):
            converted_labels.append(label.split(' ')[1])
        elif label.startswith('Ground'):
            converted_labels.append(f"GPS {label}")
        elif label.startswith('Active Waypoint'):
            converted_labels.append(f"Nav {label.split(' ')[-1]}")
        elif label.endswith('Alt'):
            converted_labels.append(f"{label}itude")
        elif label == 'Cross Track Error':
            converted_labels.append(f"Nav Cross Track Distance")
        elif label == 'IAS':
            converted_labels.append(f"Indicated Airspeed")
        elif label == 'TAS':
            converted_labels.append(f"True Airspeed")
        elif label == 'Heading':
            converted_labels.append(f"Magnetic Heading")
        elif label == 'HSI Source':
            converted_labels.append(f"Active Nav Source")
        elif label == 'Course':
            converted_labels.append(f"Nav Course")
        elif label == 'GPS Fix':
            converted_labels.append(f"GPS Fix Status")
        else:
            converted_labels.append(label)
    return converted_labels

def get_full_labels(input_labels : list[str], input_units : list[str]):
    # create full labels
    full_labels = []
    for (label, unit) in zip(input_labels, input_units):
        if unit == '':
            full_labels.append(label)
        else:
            full_labels.append(f"{label} ({unit})")
    return full_labels

def read_in_file(f : Iterable[str], labels : list[str], date_offset : int ) -> list[dict]:
    file_data = csv.DictReader(f, labels)
    clean_data = []
    line = 'START'
    last_date = 1
    while line != 'EOF':
        if line != 'START':
            new_date = date.fromisoformat(line['Date (yyyy-mm-dd)']).toordinal()
            line['Date (yyyy-mm-dd)'] = date.fromordinal(new_date + date_offset).isoformat()
            if new_date - last_date > 2:
                clean_data = [line]
            else:
                clean_data.append(line)
            last_date = new_date
        line = next(file_data, 'EOF')
    return clean_data

def get_example_header() -> dict[str, str]:
    # Read in the header of the example template
    f = open('example/log_G3X.csv')
    example_header = {'file_info': f.readline().strip()}
    example_header['labels'] = f.readline().strip()
    example_header['names'] = f.readline().strip()
    return example_header

def write_data_log(data: list[dict]):
    csv.register_dialect('garmin_datalog',
                        lineterminator='\n',
                        delimiter=",",
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL
                        )
    
    example = get_example_header()
    labels = example['labels'].split(',')
    filename = 'log_'
    filename += ''.join(data[0]['Date (yyyy-mm-dd)'].split('-'))
    filename += '_'
    filename += ''.join(data[0]['Time (hh:mm:ss)'].split(':'))

    duplicate_counter = 0
    file_path = f'output/{filename}.csv'
    while isfile(file_path):
        duplicate_counter += 1
        file_path = f'output/{filename}_{duplicate_counter}.csv'

    with open(file_path, mode='x') as output:
        output.write(example['file_info'] + '\n')
        output.write(example['labels'] + '\n')
        output.write(example['names'] + '\n')
        output_writer = csv.DictWriter(output, labels, extrasaction='ignore', dialect='garmin_datalog')
        output_writer.writerows(data)

    print(f'Wrote file to output : {file_path}')



path = 'input/'
print(listdir(path))
for input_file in listdir(path):
    if input_file.endswith('.csv'):
        with open(f'{path}{input_file}', 'r') as f:
            input_file_info = f.readline()
            input_units = get_input_units(f.readline())
            input_labels = get_input_lables(f.readline())
            full_labels = get_full_labels(input_labels, input_units)
            clean_data = read_in_file(f, full_labels, 7168)

            write_data_log(clean_data)

