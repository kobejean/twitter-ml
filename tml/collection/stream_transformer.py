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
import csv
from tweepy.streaming import StreamListener
from threading import Thread

from ..utils.ansi import ANSI

"""
#   - StreamTransformer -
#
#   Description: This class is a general class used to define how to operate
#                data taken from the Twitter Stream API. The DataHandler class
#                is implemented here for data formating
#
#   StreamListener Methods:
#       - on_data(self, data):
#       - on_connect(self):
#       x on_disconnect(self):
#       x on_error(self, status_code):
#       x keep_alive(self):
#       x on_limit(self, track):
#       x on_timeout(self):
#       x on_warning(self, notice):
#
#   Methods:
#       - entry(self, data):
#       - clean_data(self)
#       - read_data(self)
#       - write_data(self)
"""

class StreamTransformer(StreamListener):
    start_time = None
    data = []
    collect_buffer = []

    def __init__(self, tags, file_path = "STREAM.csv", sample_size = 20,
                 duration = None, # trim_size = 10,
                 buffer_size = 5, priority = lambda entry: 0):
        self.csv_format = tags
        self.conversions = len(tags) * [str]

        self.sample_size = sample_size
        self.duration = duration
        # self.trim_size = trim_size
        self.buffer_size = buffer_size
        self.priority = priority
        self.file_path = file_path

        if self.file_path:
            self.read_data()

    """
    #   - Read Method -
    #
    #   DESCRIPTION: Reads data in a specified file.
    #
    #   PARAMETERS:
    #       file_path    - The path of the file to read
    #       conversions - A list of functions that takes a string and returns
    #                     a value. This is for converting each string value to
    #                     the correct type. For example if our CSV format is:
    #                         volume, hashtag
    #                     then our conversions should be:
    #                         [int, str]
    """
    def read_data(self):
        """Reads data in file at file_path."""
        if os.path.isfile(self.file_path):
            print("CONTINUE FROM: " + self.file_path)
            with open(self.file_path, newline="") as file:
                reader = csv.reader(file)
                keys = list(next(reader)) # first line has keys/format

                if self.csv_format == None:
                    self.csv_format = keys
                else:
                    # include keys not includes in csv_format
                    keys = self.csv_format + list(set(keys) - set(self.csv_format))

                conversions = self.conversions if self.conversions else [str] * len(keys)

                self.data = [] # reset data
                for values in reader:
                    entry = {}
                    for key, value, conversion in zip(keys, values, conversions):
                        if value != "":
                            # unescape value
                            value = value.encode('utf-8')\
                                    .decode("unicode_escape")\
                                    .encode('latin1')\
                                    .decode('utf-8')
                            entry[key] = conversion(value)
                    self.data.append(entry)
        else:
            print("NO FILE AT: " + self.file_path)


    """
    #   - Clean Method -
    #
    #   DESCRIPTION: Trims data keeping key/value pairs with higher priority.
    #
    #   PARAMERTERS:
    #       priority  - A function that takes an entry and returns a priority
    #                   value. Higher values means that the entry has a higher
    #                   priority and will less likely be deleted.
    #       trim_size - The size of that the data should be trimmed down to.
    """
    def clean_data(self):
        """Trims data keeping key/value pairs with higher priority."""
        print("CLEANING DATA...")
        self.data = sorted(self.data, key=self.priority, reverse=True)#[0:self.trim_size]


    """"
    #   - Write Method -
    #
    #   DESCRIPTION: Writes data to a specified file path as a CVS file.
    #
    #   PARAPERTERS:
    #       file_path   - The path to write the file.
    #       csv_format - The cvs format as a list of keys. For example if each
    #                    entry looks something like:
    #                        {"hashtag":"some value", "volume":20}
    #                    and we want the CVS format to look something like:
    #                        hashtag, volume
    #                    our csv_format parameter should look like:
    #                        [hashtag,volume]
    """
    def write_data(self):
        """Writes data to file_path as a CVS file. """
        print("WRITING TO: "+ self.file_path)
        # save previous write by renaming file with prefix TMP_
        path, file_name = os.path.split(self.file_path)
        tmppath = os.path.join(path, "TMP_" + file_name)
        if os.path.isfile(self.file_path):
            os.rename(self.file_path, tmppath)

        with open(self.file_path, "w") as file:
            writer = csv.writer(file)
            keys = self.csv_format if self.csv_format else list(self.data[0].keys())

            # write header
            writer.writerow(keys)

            # write data
            for entry in self.data:
                values = []
                for key in keys:
                    value = entry.get(key, None)
                    if value != None:
                        # escape value
                        value = str(value).encode("utf-8")
                        # value looks like b"\x00" so remove the b" and " w/ [2:-1]
                        value = str(value)[2:-1]
                    values.append(value)
                writer.writerow(values)

        # remove temporary file
        if os.path.isfile(tmppath):
            os.remove(tmppath)

    """
    #                          - Display Method -
    #
    #   DESCRIPTION: Prints the data out with colors.
    """
    def display_data(self):
        """Prints the data out with colors. """
        print(ANSI.RED + "DATA:" + ANSI.ENDC)
        for i, entry in enumerate(self.data):
            print(ANSI.GREEN + "ENTRY #"+ str(i+1) + ANSI.ENDC)
            # print in the order of csv_format
            for key in self.csv_format:
                key_text = ANSI.CYAN + str(key).upper() + ": " + ANSI.ENDC
                text = key_text + str(entry.get(key, None))
                print(text)

            # print key/value pairs not included in csv_format
            neglected_keys = entry.keys() - set(self.csv_format)
            for key in neglected_keys:
                key_text = ANSI.LIGHT_GREY + str(key).upper() + ": " + ANSI.ENDC
                text = key_text + str(entry.get(key, None))
                print(text)

    """
    #                        - Display Entry Method -
    #
    #   DESCRIPTION: Prints an entry out with colors.
    #
    #   PARAPERTERS:
    #       entry - a dictionary of key/values
    """
    def display_entry(self, entry, show_extras=True):
        """Prints an entry out with colors. """
        # print in the order of csv_format
        for key in self.csv_format:
            key_text = ANSI.PURPLE + str(key).upper() + ": " + ANSI.ENDC
            text = key_text + str(entry.get(key, None))
            print(text)

        if show_extras:
            # print key/value pairs not included in csv_format
            neglected_keys = entry.keys() - set(self.csv_format)
            for key in neglected_keys:
                key_text = ANSI.LIGHT_GREY + str(key).upper() + ": " + ANSI.ENDC
                text = key_text + str(entry.get(key, None))
                print(text)

    def entry_count(self):
        return len(self.data) + len(self.collect_buffer)

    def entry(self, feed_data_dict):
        """
        A method that takes a dictionary of data and returns a dictionary
        with the keys we are interested in.
        """
        return { key : feed_data_dict.get(key, None) for key in self.csv_format }


    def on_data(self, feed_data):
        feed_data_dict = json.loads(feed_data) # convert to dictionary

        # add entry
        entry = self.entry(feed_data_dict)
        if entry:
            self.collect_buffer.append(entry)

            # print entry
            print(ANSI.CURSOR_UP+ANSI.CLEAR_LINE+ANSI.BLUE + "ADDED: ENTRY #" + str(self.entry_count()) + ANSI.ENDC)

            # self.display_entry(entry, show_extras=True)
            # print(feed_data_dict)

            # check if time is up
            now = datetime.now()
            end_time = datetime.max if self.duration == None else self.start_time + self.duration
            time_is_up = now > end_time

            # check if collected all
            last_entry = float('inf') if self.sample_size == None else self.sample_size
            collected_all = self.entry_count() >= last_entry

            def clean_write():
                self.clean_data()
                self.write_data()

            # clean & write when we are done
            if collected_all or time_is_up:
                self.data += self.collect_buffer
                self.collect_buffer = []
                self.clean_data()
                self.data = self.data[:last_entry]
                self.write_data()
                print("STREAM STOPPED")
                return False # stops stream

            # periodic clean and write
            if len(self.collect_buffer) >= self.buffer_size:
                self.data += self.collect_buffer
                self.collect_buffer = []
                thread = Thread(target=clean_write)
                thread.setDaemon(True)
                thread.start()

    def on_connect(self):
        print("CONNECTED...")
        if not self.start_time:
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

"""
#                           - FHCTStreamTransformer -
#
#   Description: This class is a more specific version of StreamTransformer
#                that uses the followers_count, hashtags, created_at, and text
#                keys for the data collection. It also prioritizes entries
#                with higher followers_count values.
#
"""
class FHCTStreamTransformer(StreamTransformer):
    def __init__(self, file_path = "FHCTStream.csv", sample_size = 10,
                 duration = None, # trim_size = 5,
                 buffer_size = 5):

        self.csv_format = ["followers_count","hashtags","created_at","text"]
        self.conversions = [int,eval,str,str]

        self.file_path = file_path
        self.sample_size = sample_size
        self.duration = duration
        # self.trim_size = trim_size
        self.buffer_size = buffer_size
        self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, feed_data_dict):
        entry = {}
        entry["followers_count"] = feed_data_dict.get("user",{}).get("followers_count",0)
        hashtags = feed_data_dict.get("entities",{}).get("hashtags",[])
        if len(hashtags) > 0:
            entry["hashtags"] = [hashtag.get("text", "") for hashtag in hashtags]
        entry["created_at"] = feed_data_dict.get("created_at", None)
        entry["text"] = feed_data_dict.get("text", None)
        return entry


"""
#   - FHCTStreamTransformer -
#
#   Description: This class is a more specific version of StreamTransformer
#                that uses the followers_count, hashtags, created_at, and text
#                keys for the data collection. It also prioritizes entries
#                with higher followers_count values.
#
"""
class FUCTStreamTransformer(StreamTransformer):
    def __init__(self, file_path = "FUCTStream.csv", sample_size = 10,
                 duration = None, # trim_size = 5,
                 buffer_size = 5):

        self.csv_format = ["followers_count","urls","created_at","text"]
        self.conversions = [int,eval,str,str]

        self.file_path = file_path
        self.sample_size = sample_size
        self.duration = duration
        # self.trim_size = trim_size
        self.buffer_size = buffer_size

        # priorizes entries with higher follower count and at least one url
        def priority(entry):
            urls = entry.get("urls",[])
            at_least_1_url = len(urls) > 0
            followers_count = entry.get("followers_count",0)
            return (at_least_1_url, followers_count)

        self.priority = priority
        # self.priority = lambda entry: entry.get("followers_count",0)

    def entry(self, feed_dict):
        entry = {}
        entry["followers_count"] = feed_dict.get("user",{}).get("followers_count",0)

        # urls
        tmp_urls = feed_dict.get("entities", {}).get("urls", [])
        urls = []
        for url in tmp_urls:
            expanded_url = url.get("expanded_url", None)
            if expanded_url:
                urls.append(expanded_url)

        entry["urls"] = urls

        entry["created_at"] = feed_dict.get("created_at", None)
        entry["text"] = feed_dict.get("text", None)
        return entry

"""
#                           - FHCTStreamTransformer -
#
#   Description: This class is a more specific version of StreamTransformer
#                that uses the followers_count, hashtags, created_at, and text
#                keys for the data collection. It also prioritizes entries
#                with higher followers_count values.
#
"""
class EngTextStreamTransformer(StreamTransformer):
    _entry_count = 0
    write_buffer = []

    def __init__(self, file_path = "EngTextStream.csv", sample_size = 10,
                 duration = None, # trim_size = 5,
                 buffer_size = 5):

        self.csv_format = ["text"]
        self.conversions = [str]

        self.file_path = file_path
        self.sample_size = sample_size
        self.duration = duration
        # self.trim_size = trim_size
        self.buffer_size = buffer_size
        self.priority = lambda entry: 0#len(entry.get("text",0))


    def entry_count(self):
        return self._entry_count + len(self.collect_buffer)

    def entry(self, feed_dict):

        lang = feed_dict.get("lang", None)
        text = feed_dict.get("text", "")
        tr = feed_dict.get("display_text_range", [0,len(text)])

        entities = feed_dict.get("entities", {})
        hashtags = entities.get("hashtags", [])
        urls = entities.get("urls", [])
        user_mentions = entities.get("user_mentions", [])
        symbols = entities.get("symbols", [])
        media = entities.get("media", [])
        # print(entities)

        replace_ranges = []

        # for hashtag in hashtags:
        #     hi = hashtag.get("indices", None)
        #     if hi and hi[0] >= tr[0] and hi[1] <= tr[1]:
        #         replace_ranges.append((hi[0],hi[1],"¤"))

        for url in urls:
            ui = url.get("indices", None)
            if ui and ui[0] >= tr[0] and ui[1] <= tr[1]:
                replace_ranges.append((ui[0],ui[1],"¥"))

        for user_mention in user_mentions:
            umi = user_mention.get("indices", None)
            if umi and umi[0] >= tr[0] and umi[1] <= tr[1]:
                replace_ranges.append((umi[0],umi[1],"¦"))

        for symbol in symbols:
            si = symbol.get("indices", None)
            if si and si[0] >= tr[0] and si[1] <= tr[1]:
                replace_ranges.append((si[0],si[1],"§"))

        for medii in media:
            mi = medii.get("indices", None)
            if mi and mi[0] >= tr[0] and mi[1] <= tr[1]:
                replace_ranges.append((mi[0],mi[1],"¨"))

        # replace_ranges.sort()

        entry = None
        if lang == "en" and text:
            entry = {
                "text" : text,
                "replace_ranges" : replace_ranges,
                "display_text_range" : tr
            }

        return entry

    def clean_data(self):
        """Trims data keeping key/value pairs with higher priority."""
        # print("CLEANING DATA...")

        def check_char(c):
            a = ord(c)
            if 32 <= a <= 126:
                return True
            else:
                return False


        new_text = set([])
        for entry in self.data:
            orig_text = entry.get("text", None)
            replace_ranges = entry.get("replace_ranges", [])
            replace_ranges.sort()
            tr = entry.get("display_text_range", [0, len(orig_text)])
            should_add = True
            text = ""

            if replace_ranges:
                r = 0
                text = ""
                for i in range(tr[0], tr[1]):

                    if not r in range(len(replace_ranges)):
                        for c in orig_text[i:tr[1]]:
                            if check_char(c):
                                text += c
                            else:
                                should_add = False
                        break

                    start, end, replacement = replace_ranges[r]
                    assert start <= end

                    if i < start:
                        if check_char(orig_text[i]):
                            text += orig_text[i]
                        else:
                            should_add = False

                    if i == end-1:
                        r += 1
                        text += replacement

                if text[:6].upper() == "RT ¦: ":
                    text = text[6:]
                # entry["text"] = text
                # entry["replace_ranges"] = None
                # entry["display_text_range"] = None

                if text and should_add:
                    new_text.add(text)
            else:
                orig_text = orig_text[tr[0]:tr[1]]
                for c in orig_text:
                    if not check_char(c):
                        should_add = False
                if orig_text and should_add:
                    new_text.add(orig_text)

        new_data = [{"text" : text} for text in new_text]
        # self.write_buffer = new_data
        self.write_buffer = sorted(new_data, key=self.priority, reverse=True)#[0:self.trim_size]

    def read_data(self):
        """Reads data in file at file_path."""
        if os.path.isfile(self.file_path):
            print("CONTINUE FROM: " + self.file_path)
            with open(self.file_path, "r") as file:
                # lines = file.readlines()
                self._entry_count = 0
                # self.write_buffer = []
                for _ in file:
                    self._entry_count += 1
                # self.write_buffer = [{"text" : line.rstrip('\n')} for line in lines]
        else:
            print("NO FILE AT: " + self.file_path)


    def write_data(self):
        """Writes data to file_path as a CVS file. """
        print("WRITING TO: " + self.file_path)
        print()
        # save previous write by renaming file with prefix TMP_
        # path, file_name = os.path.split(self.file_path)
        # tmppath = os.path.join(path, "TMP_" + file_name)
        # if os.path.isfile(self.file_path):
        #     os.rename(self.file_path, tmppath)

        with open(self.file_path, "a") as file:
            # write data
            while self.write_buffer:
                entry = self.write_buffer.pop()
                text = entry.get("text", None)
                if text:
                    self._entry_count += 1
                    file.write(text + "\n")
            # self.write_buffer = []
        # remove temporary file
        # if os.path.isfile(tmppath):
        #     os.remove(tmppath)

    def on_connect(self):
        print("CONNECTED...")
        print()
        if not self.start_time:
            self.start_time = datetime.now()
