################################################################################
#                            - Data Handler Class -                            #
#                                                                              #
#   PROGRAMMED BY: Jean Flaherty                                               #
#   DATE: 03-17-2017                                                           #
#   DESCRIPTION: Handles reading/cleaning/writing our data.                    #
#                                                                              #
#   INSTANCE VARIABLES:                                                        #
#       data      - Our data in dictionary form.                               #
#                                                                              #
#   METHODS:                                                                   #
#       read      - Reads data in a specified file.                            #
#       clean     - Trims data keeping key/value pairs with higher priority.   #
#       write     - Writes data to a specified filepath as a CVS file.         #
#       add       - Adds a data entry (dictionary) to the data.                #
################################################################################
import sys
import os
# lets us import from utils
scriptpath = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                os.path.expanduser(__file__))))
utilspath = os.path.join(scriptpath, "../../utils/")
sys.path.append(os.path.normpath(utilspath))

import csv

from ANSI import ANSI

class DataHandler(object):

    def __init__(self, data = [], csv_format = None, conversions = None):
        self.data = data
        self.csv_format = csv_format
        self.conversions = conversions

    ############################################################################
    #                             - Read Method -                              #
    #                                                                          #
    #   DESCRIPTION: Reads data in a specified file.                           #
    #                                                                          #
    #   PARAPERTERS:                                                           #
    #       filepath    - The path of the file to read                         #
    #       conversions - A list of functions that takes a string and returns  #
    #                     a value. This is for converting each string value to #
    #                     the correct type. For example if our CSV format is:  #
    #                         volume, hashtag                                  #
    #                     then our conversions should be:                      #
    #                         [int, str]                                       #
    ############################################################################
    def read(self, filepath):
        """Reads data in a specified file."""
        file = open(filepath, newline="")
        reader = csv.reader(file)
        keys = list(next(reader)) # first line has keys/format
        if keys != self.csv_format:
            print("csv_format does not match this file")
            return
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

    ############################################################################
    #                             - Clean Method -                             #
    #                                                                          #
    #   DESCRIPTION: Trims data keeping key/value pairs with higher priority.  #
    #                                                                          #
    #   PARAMERTERS:                                                           #
    #       priority  - A function that takes an entry and returns a priority  #
    #                   value. Higher values means that the entry has a higher #
    #                   priority and will less likely be deleted.              #
    #       trim_size - The size of that the data should be trimmed down to.   #
    ############################################################################
    def clean(self, priority, trim_size):
        """Trims data keeping key/value pairs with higher priority."""
        self.data = sorted(self.data, key=priority, reverse=True)[0:trim_size]


    ############################################################################
    #                             - Write Method -                             #
    #                                                                          #
    #   DESCRIPTION: Writes data to a specified filepath as a CVS file.        #
    #                                                                          #
    #   PARAPERTERS:                                                           #
    #       filepath   - The path to write the file.                           #
    #       csv_format - The cvs format as a list of keys. For example if each #
    #                    entry looks something like:                           #
    #                        {"hashtag":"some value", "volume":20}             #
    #                    and we want the CVS format to look something like:    #
    #                        hashtag, volume                                   #
    #                    our csv_format parameter should look like:            #
    #                        [hashtag,volume]                                  #
    ############################################################################
    def write(self, filepath):
        """Writes data to a specified filepath as a CVS file. """

        # save previous write by renaming file with prefix TMP_
        path, filename = os.path.split(filepath)
        tmppath = os.path.join(path, "TMP_" + filename)
        if os.path.isfile(filepath):
            os.rename(filepath, tmppath)

        file = open(filepath, "w")
        writer = csv.writer(file)
        keys = self.csv_format if self.csv_format else list(self.data.keys())

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
                    value = str(value)[2:-1] # b"\x00" remove b" and " w/ [2:-1]
                    print(value)
                values.append(value)
            writer.writerow(values)

        # remove temporary file
        if os.path.isfile(tmppath):
            os.remove(tmppath)

    ############################################################################
    #                             - Add Method -                               #
    #                                                                          #
    #   DESCRIPTION: Adds a data entry (dictionary) to the data.               #
    #                                                                          #
    #   PARAPERTERS:                                                           #
    #       entry - a dictionary of key/values                                 #
    ############################################################################
    """Adds a data entry (dictionary) to the data. """
    def add(self, entry):
        self.data.append(entry)


    def display(self):
        print(ANSI.RED + "DATA:" + ANSI.ENDC)
        for i, entry in enumerate(self.data):
            print(ANSI.GREEN + "ENTRY #"+ str(i+1) + ANSI.ENDC)
            for key in self.csv_format:
                key_text = ANSI.CYAN + str(key).upper() + ": " + ANSI.ENDC
                text = key_text + str(entry.get(key, None))
                print(text)

            # keys not included in csv_format
            neglected_keys = entry.keys() - set(self.csv_format)
            for key in neglected_keys:
                key_text = ANSI.LIGHT_GREY + str(key).upper() + ": " + ANSI.ENDC
                text = key_text + str(entry.get(key, None))
                print(text)

    def display_entry(self, entry):
        for key in self.csv_format:
            key_text = ANSI.PURPLE + str(key).upper() + ": " + ANSI.ENDC
            text = key_text + str(entry.get(key, None))
            print(text)

        # keys not included in csv_format
        neglected_keys = entry.keys() - set(self.csv_format)
        for key in neglected_keys:
            key_text = ANSI.PURPLE + str(key).upper() + ": " + ANSI.ENDC
            text = key_text + str(entry.get(key, None))
            print(text)
