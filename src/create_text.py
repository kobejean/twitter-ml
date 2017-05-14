from datetime import datetime, timedelta
import random
import os

from context import tml
from tml.collection.data_handler import DataHandler


# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "SPACEX STREAM.csv")

# initialization
dat_hand = DataHandler(file_path=read_path)
# randomize order of entries
random.shuffle(dat_hand.data)
# print data
dat_hand.display()

batches = []
batch_size = 2000
for i, entry in enumerate(dat_hand.data):
    batch_num = i // batch_size
    if i % batch_size == 0:
        batches.append([])
    batches[batch_num].append(entry)

for i, batch in enumerate(batches):
    write_path = os.path.join(data_path, "SPACEX TEXT " + str(i+1) + ".txt")
    write_file = open(write_path, 'w')
    for entry in batch:
        write_file.write(entry.get("text","")) # python will convert \n to os.linesep

    write_file.close()
