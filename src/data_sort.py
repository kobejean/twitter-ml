import os, fileinput
import bisect# import *
import random
# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "THE STREAM.csv")

# lines = []
# with fileinput.input(files=(read_path)) as f:
#     for line in f:
#         print("Read:", line)
#         bisect.insort(lines, line)
#         # lines.insert(bisect_left())
lines = set([])
with open(read_path, mode='r') as file:
    for line in file:
        print("Read:", line)
        lines.add(line)
        # bisect.insort(lines, line)
        # lines.insert(bisect_left())

l = list(lines)
random.shuffle(l)

with open(read_path, mode='w') as file:
    for line in l:
        print("Write:", line)
        file.write(line)
