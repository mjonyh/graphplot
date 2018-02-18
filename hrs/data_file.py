import numpy.ma as MA

class DataFile:
    """
    This class is written to fetch the experimental data obtained at the
    Nonlinear Optics Research Laboratory, Department of Physics, SUST,
    Sylhet-3114.

    The data file obtained in Tabular form with the header comments and column
    for the data.
    """
def readHeader(fname):
    # Open the file and read the relevant lines
    f = open(fname)
    head = f.readlines()[:1]
    f.close()

    # Get important stuff
    author, experiment, components, date = head[0].split()
    #units = units.replace("(", "").replace(")", "")

    # Put others lines in comments
    #comments = head[1:6]
    return (author, experiment, components, date)

def checkValue(value):
    # Check if value should be a float
    # or flagged as missing
    if value == "---":
        value = MA.masked
    else:
        value = float(value)

    return value


def readData(fname):
    # Open file and read column names and data block
    f = open(fname)

    # Ignore header
    for i in range(2):
        f.readline()

    col_names = f.readline().split()
    data_block = f.readlines()
    f.close()
    # Create a data dictionary, containing
    # a list of values for each variable
    data = {}

    # Add an entry to the dictionary for each column
    for col_name in col_names:
        data[col_name] = MA.zeros(len(data_block), 'f',
                        fill_value = -999.999)

    # Loop through each value: append to each column
    for (line_count, line) in enumerate(data_block):
        items = line.split()
        for (col_count, col_name) in enumerate(col_names):
            value = items[col_count]
            data[col_name][line_count] = checkValue(value)

    return data

comments = readHeader("exp_data.hrs")

print(comments)

data = readData("exp_data.hrs")

print(data)

