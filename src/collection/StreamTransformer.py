from src.collection.DataHandler import DataHandler

import datetime
import json
import os.path

from tweepy.streaming import StreamListener

################################################################################
#                           - StreamTransformer -                              #
#                                                                              #
#   Description: This class is a general class used to define how to operate   #
#                data taken from the Twitter Stream API. The DataHandler class #
#                is implemented here for data formating                        #
#                                                                              #
#   Methods:                                                                   #
#       -on_data(self, data):                                                  #
#       -entry(self, data):                                                    #
#       -clean(self)                                                           #
#       -write(self)                                                           #
################################################################################

class StreamTransformer(StreamListener):
    dat_hand = DataHandler()
    entry_count = 0   # for keeping track of the number of entries added

    def __init__(self, keys=[], collect_count=20, threshold_size=15, period=5,\
                 trim_size=10, priority = lambda entry: 0,
                 filename = "STREAM"):
        self.keys = keys
        self.collect_count = collect_count # number of entries to collect before stopping stream
        self.threshold_size = threshold_size # the threshold of data size where the data is trimmed
        self.period = period # number of entries between cleaning/writing files
        self.trim_size = trim_size
        self.priority = priority
        self.filename = filename

    def on_data(self, data):
        data = json.loads(data) # convert to dictionary
        # print("data: "+str(data))

        # add entry
        self.dat_hand.add(self.entry(data))
        self.entry_count += 1
        print("ADDED: ENTRY #" + str(self.entry_count))

        # clean & write if we've collected enough data entries
        if self.entry_count >= self.collect_count:
            self.clean()
            self.write()
            print("STREAM STOPPED")
            return False # stops stream

        # periodic clean and write
        if self.entry_count % self.period == 0 :
            self.clean()
            self.write()

    def entry(self, data):
        return { key : data.get(key,None) for key in self.keys }

    def clean(self):
        print("CLEANING DATA...")
        self.dat_hand.clean(self.priority, self.threshold_size, self.trim_size)

    def write(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        abspath = os.path.abspath(os.path.dirname(__file__))
        docspath = os.path.join(abspath, "../docs/")
        filepath = docspath + self.filename + " " + date +".txt"
        print("WRITING TO: "+ filepath)
        self.dat_hand.write(filepath, self.keys)

################################################################################
#                           - FHCTStreamTransformer -                          #
#                                                                              #
#   Description: This class is a more specific version of StreamTransformer    #
#                that uses the followers_count, hashtags, created_at, and text #
#                keys for the data collection. It also prioritizes entries     #
#                with higher followers_count values.                           #
#                                                                              #
################################################################################

class FHCTStreamTransformer(StreamTransformer):
    def __init__(self):
        self.keys = ["followers_count","hashtags","created_at","text"]
        self.collect_count = 20
        self.threshold_size = 15
        self.period = 5
        self.trim_size = self.threshold_size - self.period
        self.priority = lambda entry: entry.get("followers_count",0)
        self.filename = "FHCTStream"

    def entry(self, data):
        entry = {}
        entry["followers_count"] = data["user"]["followers_count"]
        hashtags = data["entities"]["hashtags"]
        entry["hashtags"] = [hashtag["text"] for hashtag in hashtags]
        entry["created_at"] = data["created_at"]
        entry["text"] = data["text"]
        return entry