################################################################################
#                            - Data Handler Class -                            #
#                                                                              #
#   PROGRAMMED BY: Jean Flaherty                                               #
#   DATE: 04-07-2017                                                           #
#   DESCRIPTION: Handles reading, cleaning, writing and adding to our data.    #
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
import os
import csv

from ..utils.ansi import ANSI

class DataHandler(object):

    def __init__(self, file_path = None, data = [], csv_format = None,
                 conversions = None):
        self.data = data
        self.csv_format = csv_format
        self.conversions = conversions
        if file_path:
            self.read(file_path)
    """
    #   - Read Method -
    #
    #   DESCRIPTION: Reads data in a specified file.
    #
    #   PARAMETERS:
    #       filepath    - The path of the file to read
    #       conversions - A list of functions that takes a string and returns
    #                     a value. This is for converting each string value to
    #                     the correct type. For example if our CSV format is:
    #                         volume, hashtag
    #                     then our conversions should be:
    #                         [int, str]
    """
    def read(self, file_path):
        """Reads data in a specified file."""
        file = open(file_path, newline="")
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
    def clean(self, priority, trim_size):
        """Trims data keeping key/value pairs with higher priority."""
        self.data = sorted(self.data, key=priority, reverse=True)[0:trim_size]


    """"
    #   - Write Method -
    #
    #   DESCRIPTION: Writes data to a specified filepath as a CVS file.
    #
    #   PARAPERTERS:
    #       filepath   - The path to write the file.
    #       csv_format - The cvs format as a list of keys. For example if each
    #                    entry looks something like:
    #                        {"hashtag":"some value", "volume":20}
    #                    and we want the CVS format to look something like:
    #                        hashtag, volume
    #                    our csv_format parameter should look like:
    #                        [hashtag,volume]
    """
    def write(self, file_path):
        """Writes data to a specified filepath as a CVS file. """

        # save previous write by renaming file with prefix TMP_
        path, file_name = os.path.split(file_path)
        tmppath = os.path.join(path, "TMP_" + file_name)
        if os.path.isfile(file_path):
            os.rename(file_path, tmppath)

        file = open(file_path, "w")
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
                    # value looks like b"\x00" so remove the b" and " w/ [2:-1]
                    value = str(value)[2:-1]
                values.append(value)
            writer.writerow(values)

        # remove temporary file
        if os.path.isfile(tmppath):
            os.remove(tmppath)

    """
    #   - Add Method -
    #
    #   DESCRIPTION: Adds a data entry (dictionary) to the data.
    #
    #   PARAPERTERS:
    #       entry - a dictionary of key/values
    """
    def add(self, entry):
        """Adds a data entry (dictionary) to the data. """
        self.data.append(entry)

    """
    #                          - Display Method -
    #
    #   DESCRIPTION: Prints the data out with colors.
    """
    def display(self):
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
