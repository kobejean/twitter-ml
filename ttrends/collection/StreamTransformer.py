"""
################################################################################
#                            - Stream Transformer -                            #
#                                                                              #
#   PROGRAMMED BY: Jean Flaherty                                               #
#   DATE: 04-07-2017                                                           #
#   DESCRIPTION: Handles collecting data from the Twitter Stream API and       #
#                passing it to the DataHandler class                           #
#                                                                              #
#   Classes:                                                                   #
#       StreamTransformer: A general class that defines how to operate tweepy  #
#           stream                                                             #
#       FHCTStreamTransformer: A subclass of StreamTransformer that reads      #
#           followers_count, hashtags, created_at, and text tags.              #
#       FUCTStreamTransformer: Defines how to operate tweepy stream data taken #
################################################################################
"""
from datetime import datetime, timedelta
import json
import os
from tweepy.streaming import StreamListener

from .DataHandler import DataHandler
from ..utils.ANSI import ANSI

################################################################################
#                           - StreamTransformer -                              #
#                                                                              #
#   Description: This class is a general class used to define how to operate   #
#                data taken from the Twitter Stream API. The DataHandler class #
#                is implemented here for data formating                        #
#                                                                              #
#   StreamListener Methods:                                                    #
#       - on_connect(self):                                                    #
#       - on_disconnect(self):                                                 #
#       - on_error(self, status_code):                                         #
#       - on_data(self, data):                                                 #
#       - keep_alive(self):                                                    #
#       - on_limit(self, track):                                               #
#       - on_timeout(self):                                                    #
#       - on_warning(self, notice):                                            #
#                                                                              #
#   Methods:                                                                   #
#       - entry(self, data):                                                   #
#       - clean_data(self)                                                     #
#       - read_data(self)                                                      #
#       - write_data(self)                                                     #
################################################################################

class StreamTransformer(StreamListener):
    entry_count = None
    start_time = None

    def __init__(self, tags, filepath = "STREAM.csv", sample_size = 20,
                 duration = None, trim_size = 10, period = 5,
                 priority = lambda entry: 0):
        self.dat_hand = DataHandler()
        self.dat_hand.csv_format = tags
        self.dat_hand.conversions = len(tags) * [str]

        self.sample_size = sample_size
        self.duration = duration
        self.trim_size = trim_size
        self.period = period
        self.priority = priority
        self.filepath = filepath

    def entry(self, data):
        """
        A method that takes a dictionary of data and returns a dictionary
        with the keys we are interested in.
        """
        return { key : data.get(key, None) for key in self.dat_hand.csv_format }

    def clean_data(self):
        print("CLEANING DATA...")
        self.dat_hand.clean(self.priority, self.trim_size)

    def read_data(self):
        filepath = self.filepath
        if os.path.isfile(self.filepath):
            print("CONTINUE FROM: " + self.filepath)
            self.dat_hand.read(self.filepath)
        else:
            print("NO FILE AT: " + self.filepath)

    def write_data(self):
        print("WRITING TO: "+ self.filepath)
        self.dat_hand.write(self.filepath)

    def on_data(self, data):
        data = json.loads(data) # convert to dictionary

        # add entry
        entry = self.entry(data)
        self.dat_hand.add(entry)
        self.entry_count += 1

        # print entry
        print(ANSI.BLUE + "ADDED: ENTRY #" + str(self.entry_count) + ANSI.ENDC)
        self.dat_hand.display_entry(entry)
        # print(data)

        # check if time is up
        now = datetime.now()
        end_time = datetime.max if self.duration == None else self.start_time + self.duration
        time_is_up = now > end_time

        # check if collected all
        last_entry = float('inf') if self.sample_size == None else self.sample_size
        collected_all = self.entry_count >= last_entry

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
    def __init__(self, filename = "FHCTStream", sample_size = 10,
                 duration = None, trim_size = 5, period = 5):
        self.dat_hand = DataHandler()
        self.dat_hand.csv_format = ["followers_count","hashtags","created_at","text"]
        self.dat_hand.conversions = [int,eval,str,str]

        self.filename = filename
        self.sample_size = sample_size
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
    def __init__(self, filename = "FUCTStream", sample_size = 10,
                 duration = None, trim_size = 5, period = 5):
        self.dat_hand = DataHandler()
        self.dat_hand.csv_format = ["followers_count","urls","created_at","text"]
        self.dat_hand.conversions = [int,eval,str,str]

        self.filename = filename
        self.sample_size = sample_size
        self.duration = duration
        self.trim_size = trim_size
        self.period = period

        # priorizes entries with higher follower count and at least one url
        def priority(entry):
            urls = entry.get("urls",[])
            at_least_1_url = len(urls) > 0
            followers_count = entry.get("followers_count",0)
            return (at_least_1_url, followers_count)

        self.priority = priority
        # self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, data):
        entry = {}
        entry["followers_count"] = data.get("user",{}).get("followers_count",0)

        # urls
        tmp_urls = data.get("entities", {}).get("urls", [])
        urls = []
        for url in tmp_urls:
            expanded_url = url.get("expanded_url", None)
            if expanded_url:
                urls.append(expanded_url)

        entry["urls"] = urls

        entry["created_at"] = data.get("created_at", None)
        entry["text"] = data.get("text", None)
        return entry
