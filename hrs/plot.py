import numpy.ma as MA
import numpy as np
import matplotlib.pyplot as plt

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

print("Experiment conducted by: ", comments[0], " for sample: ", comments[2], ".")

print("Experiment conducted on: ", comments[3])
data = readData("exp_data.hrs")


data_marker = ['o','^','s','p','*','h','H','D','d','1','','']

ax = plt.subplot(111, projection='polar')
x_tag = 0;
num = 0
for col in data:
    if (x_tag == 0):
        x_axis = col
        data[x_axis] = data[x_axis]*2*np.pi/360.
        x_tag = 1
    else:
        ax.plot(data[x_axis], data[col], data_marker[num], label=col, color='k')
        num += 1

#plt.xlabel("Angle in Degree")
#plt.ylabel("Output power in mW")
plt.legend(loc=4)
plt.show()

