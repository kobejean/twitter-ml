import sys
import os
# lets us import from utils
scriptpath = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                os.path.expanduser(__file__))))
utilspath = os.path.join(scriptpath, "../../utils/")
sys.path.append(os.path.normpath(utilspath))

from DataHandler import DataHandler

from datetime import datetime, timedelta
import json
import os
# import ast

from ANSI import ANSI

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

    def __init__(self, filename = "STREAM", keys = [], collect_count = 20,
                 duration = None, trim_size = 10, period = 5,
                 priority = lambda entry: 0):
        self.dat_hand = DataHandler()
        self.dat_hand.csv_format = keys
        self.dat_hand.conversions = [str for _ in range(len(keys))]

        self.entry_count = None
        self.start_time = None

        # self.keys = keys
        # self.conversions = [str for _ in range(len(keys))]
        self.collect_count = collect_count
        self.duration = duration
        self.trim_size = trim_size
        self.period = period # number of entries between cleaning/writing files
        self.priority = priority
        self.filename = filename

    def on_connect(self):
        print("CONNECTED...")
        if not self.entry_count and not self.start_time:
            self.entry_count = 0   # for keeping track of the number of entries added
            self.start_time = datetime.now()

    def on_disconnect(self, notice):
        print("DISCONNECTED:", notice)

    def on_error(self, status_code):
        print("ERROR: ", status_code)
        return False

    def on_data(self, data):
        data = json.loads(data) # convert to dictionary

        # add entry
        entry = self.entry(data)
        self.dat_hand.add(entry)
        self.entry_count += 1

        print(ANSI.BLUE + "ADDED: ENTRY #" + str(self.entry_count) + ANSI.ENDC)
        # print entry
        self.dat_hand.display_entry(entry)
        # print(data)

        # check if time is up
        now = datetime.now()
        end_time = datetime.max if self.duration == None else self.start_time + self.duration
        time_is_up = now > end_time
        collected_all = self.entry_count >= self.collect_count

        # clean & write when we are done
        if collected_all or time_is_up:
            self.clean_data()
            self.write_data()
            print("STREAM STOPPED")
            return False # stops stream

        # periodic clean and write
        if self.entry_count % self.period == 0 :
            self.clean_data()
            self.write_data()

    def keep_alive(self):
        """Called when a keep-alive arrived"""
        print("KEEP ALIVE...")
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        print(ANSI.WARNING + "LIMIT:", track, ANSI.ENDC)
        return

    def on_timeout(self):
        """Called when stream connection times out"""
        print(ANSI.WARNING + "TIMED OUT" + ANSI.ENDC)
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        print(ANSI.WARNING + "WARNING:", notice, ANSI.ENDC)
        return

    def entry(self, data):
        return { key : data.get(key,None) for key in self.dat_hand.csv_format }


    def filepath(self):
        abspath = os.path.abspath(os.path.dirname(__file__))
        docspath = os.path.join(abspath, "../../docs/")
        return docspath + self.filename

    def read_data(self, filepath = None):
        if not filepath:
            filepath = self.filepath()

        if os.path.isfile(filepath):
            print("CONTINUE FROM: " + filepath)
            self.dat_hand.read(filepath)
        else:
            print("NO FILE AT: " + filepath)

    def clean_data(self):
        print("CLEANING DATA...")
        self.dat_hand.clean(self.priority, self.trim_size)

    def write_data(self):
        print("WRITING TO: "+ self.filepath())
        self.dat_hand.write(self.filepath())

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
        super(FHCTStreamTransformer, self).__init__()
        self.dat_hand.csv_format = ["followers_count","hashtags","created_at","text"]
        self.dat_hand.conversions = [int,eval,str,str]


        self.filename = filename
        self.collect_count = collect_count
        self.duration = duration
        self.trim_size = trim_size
        self.period = period
        self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, data):
        entry = {}
        entry["followers_count"] = data.get("user",{}).get("followers_count",0)
        hashtags = data.get("entities",{}).get("hashtags",[])
        if len(hashtags) > 0:
            entry["hashtags"] = [hashtag.get("text", "") for hashtag in hashtags]
        entry["created_at"] = data.get("created_at", None)
        entry["text"] = data.get("text", None)
        return entry


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
    def __init__(self, filename = "FUCTStream", collect_count = 10,
                 duration = None, trim_size = 5, period = 5):
        super(FUCTStreamTransformer, self).__init__()
        self.dat_hand.csv_format = ["followers_count","urls","created_at","text"]
        self.dat_hand.conversions = [int,eval,str,str]

        self.filename = filename
        self.collect_count = collect_count
        self.duration = duration
        self.trim_size = trim_size
        self.period = period
        self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, data):
        entry = {}
        entry["followers_count"] = data.get("user",{}).get("followers_count",0)
        urls = data.get("entities", {}).get("urls", [])
        if len(urls) > 0:
            entry["urls"] = [url.get("expanded_url", None) for url in urls]
        entry["created_at"] = data.get("created_at", None)
        entry["text"] = data.get("text", None)
        return entry
