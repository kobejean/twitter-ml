import os, fileinput
import bisect# import *

# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "THE STREAM.csv")

lines = []
with fileinput.input(files=(read_path)) as f:
    for line in f:
        print("Read:", line)
        bisect.insort(lines, line)
        # lines.insert(bisect_left())

with open(read_path, mode='w') as file:
    for line in lines:
        print("Write:", line)
        file.write(line)
