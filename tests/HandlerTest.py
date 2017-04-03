import sys
import os
# let's us import from src/collection
scriptpath = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                os.path.expanduser(__file__))))
collectionpath = os.path.join(scriptpath, "../src/collection")
sys.path.append(os.path.normpath(collectionpath))

from DataHandler import DataHandler

# EXAMPLE CODE
abspath = os.path.abspath(os.path.dirname(__file__))
docspath = os.path.join(abspath, "../docs/")

# initialization
dat_hand = DataHandler()
dat_hand.csv_format = ["volume","hashtag"]
dat_hand.conversions = [int, str] # volume, hashtag

# reading data
dat_hand.read(docspath + "test_data.csv")

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
dat_hand.write(docspath + "test_data_out.csv")

dat_hand.display()
