from src.collection.DataHandler import DataHandler
import os

# # EXAMPLE CODE
abspath = os.path.abspath(os.path.dirname(__file__))
docspath = os.path.join(abspath, "../docs/")
dat_hand = DataHandler()

# # reading data
conversions = [int, str] # volume, hashtag
dat_hand.read(docspath+"test_data.txt", conversions)

# # adding data
entry = {}
entry["hashtag"] = "フラハティ 仁"
entry["volume"] = 30
dat_hand.add(entry)

# # cleaning data
priority = lambda entry: entry.get("volume",0)
threshold_size = 10
trim_size = threshold_size - 5
dat_hand.clean(priority, threshold_size, trim_size)

# # writing data to file in CSV format
cvs_format = ["volume", "hashtag"]
dat_hand.write(docspath+"test_data_out.txt", cvs_format)

print(dat_hand.data)