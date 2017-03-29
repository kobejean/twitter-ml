from DataHandler import DataHandler

import datetime
import json
import os.path
import os

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

    def __init__(self, filename = "STREAM", keys=[], collect_count=20,
                 trim_size=10, period=5, priority = lambda entry: 0):
        self.keys = keys
        self.collect_count = collect_count # number of entries to collect before stopping stream
        self.trim_size = trim_size
        self.period = period # number of entries between cleaning/writing files
        self.priority = priority
        self.filename = filename

    def on_data(self, data):
        data = json.loads(data) # convert to dictionary
        # print("data: "+str(data))

        # add entry
        self.dat_hand.add(self.entry(data))
        self.entry_count += 1
        print("ADDED: ENTRY #" + str(self.entry_count))

        # sort & write if we've collected enough data entries
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
        self.dat_hand.clean(self.priority, self.trim_size)

    def write(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        abspath = os.path.abspath(os.path.dirname(__file__))
        docspath = os.path.join(abspath, "../../docs/")
        filepath = docspath + self.filename

        # save previous write by renaming file with prefix TMP_
        tmppath = docspath + "TMP_" + self.filename
        if os.path.isfile(filepath):
            os.rename(filepath, tmppath)

        print("WRITING TO: "+ filepath)
        self.dat_hand.write(filepath, self.keys)

        # remove temporary file
        if os.path.isfile(tmppath):
            os.remove(tmppath)

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
    def __init__(self, filename = "FHCTStream", collect_count=10, trim_size=5, period=5):
        self.filename = filename
        self.keys = ["followers_count","hashtags","created_at","text"]
        self.collect_count = collect_count
        self.trim_size = trim_size
        self.period = period
        self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, data):
        entry = {}
        entry["followers_count"] = data.get("user",{}).get("followers_count",0)
        hashtags = data.get("entities",{}).get("hashtags",[])
        entry["hashtags"] = [hashtag.get("text", None) for hashtag in hashtags]
        entry["created_at"] = data.get("created_at", None)
        entry["text"] = data.get("text", None)
        return entry
