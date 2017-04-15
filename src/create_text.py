from datetime import datetime, timedelta
import os

from context import ttrends
from ttrends.collection.data_handler import DataHandler
from ttrends.collection.data_collector import DataCollector
from ttrends.collection.stream_transformer import *
from ttrends.collection.auth_info import * # where api access information is stored

import random
import os

# EXAMPLE CODE
abspath = os.path.abspath(os.path.dirname(__file__))
docspath = os.path.join(abspath, "data")

# initialization
dat_hand = DataHandler()
dat_hand.csv_format = ["followers_count","urls","created_at","text"]

# reading data
readpath = os.path.join(docspath, "SPACEX STREAM.csv")
dat_hand.read(readpath)

random.shuffle(dat_hand.data)
dat_hand.display()

batches = []
batch_size = 2000
for i, entry in enumerate(dat_hand.data):
    batch_num = i // batch_size
    if i % batch_size == 0:
        batches.append([])
    batches[batch_num].append(entry)

for i, batch in enumerate(batches):
    # dat_hand.data = batch
    writepath = os.path.join(docspath, "SPACEX TEXT " + str(i) + ".txt")
    # dat_hand.write(writepath)

    f = open(writepath, 'w')
    for entry in batch:
        f.write(entry["text"])  # python will convert \n to os.linesep

    f.close()  # you can omit in most cases as the destructor will call it
