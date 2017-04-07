import os

from context import ttrends
from ttrends.collection.DataHandler import DataHandler

# EXAMPLE CODE
abspath = os.path.abspath(os.path.dirname(__file__))
docspath = os.path.join(abspath, "data")

# initialization
dat_hand = DataHandler()
dat_hand.csv_format = ["volume","hashtag"]
dat_hand.conversions = [int, str] # volume, hashtag

# reading data
readpath = os.path.join(docspath, "test_data.csv")
dat_hand.read(readpath)

# adding data
entry = {}
entry["hashtag"] = "フラハティ 仁"
entry["volume"] = 30
dat_hand.add(entry)

# cleaning data
priority = lambda entry: entry.get("volume",0)
trim_size = 5
dat_hand.clean(priority, trim_size)

# writing data to file in CSV format
writepath = os.path.join(docspath, "test_data_out.csv")
dat_hand.write(writepath)

# print data
dat_hand.display()
