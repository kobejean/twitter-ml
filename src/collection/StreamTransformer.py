from DataHandler import DataHandler

from datetime import datetime, timedelta
import json
# import os.path
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

    def __init__(self, filename = "STREAM", keys = [], collect_count = 20,
                 duration = None, trim_size = 10, period = 5,
                 priority = lambda entry: 0):
        self.keys = keys
        self.collect_count = collect_count
        self.start_time = datetime.now()
        self.duration = duration
        self.trim_size = trim_size
        self.period = period # number of entries between cleaning/writing files
        self.priority = priority
        self.filename = filename

    def on_status(self, status):
        print("STATUS: " + str(status.text))

    def on_error(self, status_code):
        print("ERROR: " + str(status_code))
        return False

    def on_data(self, data):
        data = json.loads(data) # convert to dictionary

        # add entry
        entry = self.entry(data)
        self.dat_hand.add(entry)
        self.entry_count += 1
        print("ADDED: ENTRY #" + str(self.entry_count))
        # print entry
        for key in self.keys:
            text = "    " + str(key).upper() + ": " + str(entry.get(key,None))
            print(text)
        # print(data)

        # check if time is up
        now = datetime.now()
        time_is_up = self.duration and now >= self.start_time + self.duration

        # clean & write if we've collected enough data entries
        if self.entry_count >= self.collect_count or time_is_up:
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

    def read(self, conversions = None):
        abspath = os.path.abspath(os.path.dirname(__file__))
        docspath = os.path.join(abspath, "../../docs/")
        filepath = docspath + self.filename

        if os.path.isfile(filepath):
            print("READING FROM: " + filepath)
            self.dat_hand.read(filepath, conversions)
        else:
            print("NO FILE AT: " + filepath)

    def write(self):
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
    def __init__(self, filename = "FHCTStream", collect_count = 10,
                 duration = None, trim_size = 5, period = 5):
        self.filename = filename
        self.keys = ["followers_count","hashtags","created_at","text"]
        self.collect_count = collect_count
        self.start_time = datetime.now()
        self.duration = duration
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

    def read(self):
        super(FHCTStreamTransformer, self).read([int,str,str,str])


################################################################################
#                           - FHCTStreamTransformer -                          #
#                                                                              #
#   Description: This class is a more specific version of StreamTransformer    #
#                that uses the followers_count, hashtags, created_at, and text #
#                keys for the data collection. It also prioritizes entries     #
#                with higher followers_count values.                           #
#                                                                              #
################################################################################

class FUCTStreamTransformer(StreamTransformer):
    def __init__(self, filename = "FHCTStream", collect_count = 10,
                 duration = None, trim_size = 5, period = 5):
        self.filename = filename
        self.keys = ["followers_count","urls","created_at","text"]
        self.collect_count = collect_count
        self.start_time = datetime.now()
        self.duration = duration
        self.trim_size = trim_size
        self.period = period
        self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, data):
        entry = {}
        entry["followers_count"] = data.get("user",{}).get("followers_count",0)
        urls = data.get("entities",{}).get("urls",[])
        entry["urls"] = [url.get("expanded_url", None) for url in urls]
        entry["created_at"] = data.get("created_at", None)
        entry["text"] = data.get("text", None)
        return entry

    def read(self):
        super(FUCTStreamTransformer, self).read([int,str,str,str])
