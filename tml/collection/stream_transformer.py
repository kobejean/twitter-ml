"""
                         - Stream Transformer -

PROGRAMMED BY: Jean Flaherty
DATE: 07/15/2017
DESCRIPTION: Handles collecting data from the Twitter Stream API and
             writing it to a file.

CLASSES:
    StreamTransformer: A general class that defines how to operate tweepy
        stream
    FHCTStreamTransformer: A subclass of StreamTransformer that reads
        followers_count, hashtags, created_at, and text tags.
    FUCTStreamTransformer: A subclass of StreamTransformer that reads
        followers_count, urls, created_at, and text tags.
    EngTextStreamTransformer: A subclass of StreamTransformer that reads
        takes only english text. It will also replace entities with special
        characters to make the text machine learning friendly.
"""
import json, os, csv
from datetime import datetime, timedelta
from tweepy.streaming import StreamListener
from threading import Thread
# within module
from ..utils.ansi import ANSI


class StreamTransformer(StreamListener):
    """
    This class is a general class used to define how to transform
    data taken from the Twitter Stream API.
    """
    collect_buffer = []
    write_buffer = []
    _entry_count = 0

    def __init__(self, tags, file_path = "STREAM.csv", sample_size = 20,
                 buffer_size = 5, should_print_entry = True):
        """
        Initializer

        ARGUMENTS:
        tags                - Key names for values to retrieve from the stream.
        file_path           - The file path to write to.
        sample_size         - The number of entries to collect.
        buffer_size         - The max number of entries for the buffer.
        should_print_entry  - Boolean value that determins whether or not the
                              entries should be printed as they are collected.
        """
        self.csv_format = tags
        self.conversions = len(tags) * [str]

        self.sample_size = sample_size
        self.buffer_size = buffer_size
        self.file_path = file_path
        self.should_print_entry = should_print_entry

        if self.file_path:
            self.scan_file()


    def scan_file(self):
        """ Scans file to count the number of entries. """
        if os.path.isfile(self.file_path):
            print("CONTINUE FROM: " + self.file_path)
            with open(self.file_path, "r") as file:
                self._entry_count = 0
                for _ in file:
                    if self._entry_count % 10000 == 0: # printing every single one slows it down
                        print(ANSI.CLEAR_LINE + "SCANNING ENTRY NUMBER: {}".format(self._entry_count), end='\r')
                    self._entry_count += 1
                print(ANSI.CLEAR_LINE + "SCANNED {} ENTRIES".format(self._entry_count))
        else:
            print("NO FILE AT: " + self.file_path)


    def write_data(self, async=False):
        """" Writes buffer to a specified file path as a CVS file. """
        self.write_buffer += self.collect_buffer
        self.collect_buffer = []

        print("WRITING TO: " + self.file_path)
        if async:
            thread = Thread(target=self._write_process)
            thread.setDaemon(True)
            thread.start()
        else:
            self._write_process()


    def _write_process(self):
        """" The writing process that could be called on a different thread. """
        should_write_header = not os.path.exists(self.file_path)
        with open(self.file_path, "a") as file:
            writer = csv.writer(file)
            keys = self.csv_format if self.csv_format else list(self.write_buffer[0].keys())

            # write header
            if should_write_header:
                writer.writerow(keys)

            # write data
            while self.write_buffer:
                entry = self.write_buffer.pop()
                values = []
                for key in keys:
                    value = entry.get(key, None)
                    if value != None:
                        # escape value
                        value = str(value).encode("utf-8")
                        # value looks like b"\x00" so remove the b" and " w/ [2:-1]
                        value = str(value)[2:-1]
                    values.append(value)
                    del value
                writer.writerow(values)
                del entry, values
                self._entry_count += 1
            # del self.write_buffer[:] # don't need reference after write


    def display_data(self):
        """ Prints the data out with colors. """
        print(ANSI.RED + "DATA:" + ANSI.ENDC)
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                reader = csv.reader(file)
                keys = list(next(reader)) # first line has keys/format

                if self.csv_format == None:
                    self.csv_format = keys
                else:
                    # include keys not includes in csv_format
                    keys = self.csv_format + list(set(keys) - set(self.csv_format))

                conversions = self.conversions if self.conversions else [str] * len(keys)

                for i, values in enumerate(reader):
                    entry = {}
                    for key, value, conversion in zip(keys, values, conversions):
                        if value != "":
                            # unescape value
                            value = value.encode('utf-8')\
                                    .decode("unicode_escape")\
                                    .encode('latin1')\
                                    .decode('utf-8')
                            entry[key] = conversion(value)

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
        else:
            print("NO FILE AT PATH", self.file_path)

    def display_entry(self, entry, show_extras=True):
        """
        Prints an entry out with colors.

        ARGUMENTS:
        entry       - A dictionary of key/values
        show_extras - (optional) A boolean value that determines whether or not
                      to print values that are not specified in the csv format
        """
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
        """ Returns the number of entries that were collected """
        return self._entry_count + len(self.collect_buffer)

    def entry(self, feed_dict):
        """
        Takes a dictionary of data and returns a dictionary with the keys
        we are interested in.

        ARGUMENTS:
        feed_dict - The data feed dictionary from the stream
        """
        return { key : feed_dict.get(key, None) for key in self.csv_format }


    def on_data(self, feed_data):
        feed_dict = json.loads(feed_data) # convert to dictionary

        # add entry
        entry = self.entry(feed_dict)
        if entry:
            self.collect_buffer.append(entry)

            # print entry
            if self.should_print_entry:
                print(ANSI.BLUE + "ADDED: ENTRY #" + str(self.entry_count()) + ANSI.ENDC)
                self.display_entry(entry, show_extras=True)
            else:
                print(ANSI.CLEAR_LINE+ANSI.BLUE + "ADDED: ENTRY #" + str(self.entry_count()) + ANSI.ENDC, end='\r')
            # print(feed_dict)

            # check if collected all
            last_entry = float('inf') if self.sample_size == None else self.sample_size
            collected_all = self.entry_count() >= last_entry

            # clean & write when we are done
            if collected_all:
                self.write_data(async=False)
                print("STREAM STOPPED")
                return False # stops stream

            # periodic clean and write
            if len(self.collect_buffer) >= self.buffer_size:
                self.write_data(async=True)

    def on_connect(self):
        print("CONNECTED...")
        self.write_buffer = []
        self.collect_buffer = []


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


class FHCTStreamTransformer(StreamTransformer):
    """
    This class is a more specific version of StreamTransformer
    that uses the followers_count, hashtags, created_at, and text
    keys for the data collection. It also prioritizes entries
    with higher followers_count values.
    """
    def __init__(self, file_path = "FHCTStream.csv", sample_size = 10,
                 buffer_size = 5, should_print_entry = True):

        self.csv_format = ["followers_count","hashtags","created_at","text"]
        self.conversions = [int,eval,str,str]
        self.file_path = file_path
        self.sample_size = sample_size
        self.buffer_size = buffer_size
        self.should_print_entry = should_print_entry

    def entry(self, feed_dict):
        """
        Takes a dictionary of data and returns a dictionary with the keys
        we are interested in.

        ARGUMENTS:
        feed_dict - The data feed dictionary from the stream
        """
        entry = {}
        entry["followers_count"] = feed_dict.get("user",{}).get("followers_count",0)
        hashtags = feed_dict.get("entities",{}).get("hashtags",[])
        if len(hashtags) > 0:
            entry["hashtags"] = [hashtag.get("text", "") for hashtag in hashtags]
        entry["created_at"] = feed_dict.get("created_at", None)
        entry["text"] = feed_dict.get("text", None)
        return entry


class FUCTStreamTransformer(StreamTransformer):
    """
    This class is a more specific version of StreamTransformer
    that uses the followers_count, hashtags, created_at, and text
    keys for the data collection. It also prioritizes entries
    with higher followers_count values.
    """
    def __init__(self, file_path = "FUCTStream.csv", sample_size = 10,
                 buffer_size = 5, should_print_entry = True):

        self.csv_format = ["followers_count","urls","created_at","text"]
        self.conversions = [int,eval,str,str]
        self.file_path = file_path
        self.sample_size = sample_size
        self.buffer_size = buffer_size
        self.should_print_entry = should_print_entry

    def entry(self, feed_dict):
        """
        Takes a dictionary of data and returns a dictionary with the keys
        we are interested in.

        ARGUMENTS:
        feed_dict - The data feed dictionary from the stream
        """
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


class EngTextStreamTransformer(StreamTransformer):
    """
    This class is a more specific version of StreamTransformer
    that uses the followers_count, hashtags, created_at, and text
    keys for the data collection. It also prioritizes entries
    with higher followers_count values.
    """

    def __init__(self, file_path = "EngTextStream.csv", sample_size = 1000,
                 buffer_size = 100, should_print_entry = False):

        self.csv_format = ["text"]
        self.conversions = [str]
        self.file_path = file_path
        self.sample_size = sample_size
        self.buffer_size = buffer_size
        self.should_print_entry = should_print_entry

    def entry(self, feed_dict):
        """
        Takes a dictionary of data and returns a dictionary with the keys
        we are interested in.

        ARGUMENTS:
        feed_dict - The data feed dictionary from the stream
        """

        lang = feed_dict.get("lang", None)
        text = feed_dict.get("text", "")
        tr = feed_dict.get("display_text_range", [0,len(text)]) # text ranges

        entities = feed_dict.get("entities", {})
        hashtags = entities.get("hashtags", [])
        urls = entities.get("urls", [])
        user_mentions = entities.get("user_mentions", [])
        symbols = entities.get("symbols", [])
        media = entities.get("media", [])

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

        entry = None
        if lang == "en" and text:
            entry = {
                "text" : text,
                "replace_ranges" : replace_ranges,
                "display_text_range" : tr
            }

        return entry


    def clean_write_buffer(self):
        """
        Cleans the write buffer, preventing duplicates and replacing
        entities with characters.
        """
        print("CLEANING BUFFER...")

        def check_char(c):
            a = ord(c)
            if 32 <= a <= 126:
                return True
            else:
                return False


        new_text = set([])
        while self.write_buffer:
            entry = self.write_buffer.pop()
            orig_text = entry.get("text", None)
            replace_ranges = entry.get("replace_ranges", [])
            replace_ranges.sort()
            tr = entry.get("display_text_range", [0, len(orig_text)])
            should_add = True
            text = ""

            # replace ranges
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

        self.write_buffer = [{"text" : text} for text in new_text]


    def _write_process(self):
        """" The writing process that could be called on a different thread. """
        self.clean_write_buffer()

        with open(self.file_path, "a") as file:
            # write data
            while self.write_buffer:
                entry = self.write_buffer.pop()
                text = entry.get("text", None)
                if text:
                    self._entry_count += 1
                    file.write(text + "\n")
