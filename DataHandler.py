################################################################################
#                            - Data Handler Class -                            #
#                                                                              #
#   PROGRAMMED BY: Jean Flaherty                                               #
#   DATE: 03-04-2017                                                           #
#   DESCRIPTION: Handles reading/cleaning/writing our data.                    #
#                                                                              #
#   INSTANCE VARIABLES:                                                        #
#       data      - Our data in dictionary form.                               #
#                                                                              #
#   METHODS:                                                                   #
#       read      - Reads data in a specified file.                            #
#       clean     - Trims data by keeping key/value pairs with higher value.   #
#       write     - Writes data sorted by value to a specified filepath.       #
################################################################################
import csv
from urllib.parse import unquote, quote

class DataHandler(object):
    data = []

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
    def read(self, filepath, conversions = None):
        """Reads data in a specified file."""
        file = open(filepath, newline="")
        reader = csv.reader(file)
        keys = next(reader) # first line has keys

        if not conversions:
            # let them all be strings if not specified
            conversions = [str for _ in range(len(keys))]

        self.data = []
        for values in reader:
            decode = lambda val, conv: conv(unquote(val)) if val else None
            entry = {}
            for key, val, conv in zip(keys, values, conversions):
                entry[key] = decode(val, conv)
            self.data.append(entry)

    ############################################################################
    #                             - Clean Method -                             #
    #                                                                          #
    #   DESCRIPTION: Trims data by keeping key/value pairs with higher value.  #
    #                                                                          #
    #   PARAMERTERS:                                                           #
    #       priority  - A function that takes an entry and returns a priority  #
    #                   value. Higher values means that the entry has a higher #
    #                   priority and will less likely be deleted.              #
    #       trim_size - The size of that the data should be trimmed down to.   #
    ############################################################################
    def clean(self, priority, trim_size):
        self.data = sorted(self.data, key=priority, reverse=True)[0:trim_size]

    ############################################################################
    #                             - Write Method -                             #
    #                                                                          #
    #   DESCRIPTION: Writes data to a specified filepath.                      #
    #                                                                          #
    #   PARAPERTERS:                                                           #
    #       filepath   - The path to write the file.                           #
    #       csv_format - The format as a string of keys separated by commas.   #
    #                   for example if each entry looks something like:        #
    #                       {"hashtag":"some value", "volume":20}              #
    #                   and we want the CVS format to look something like:     #
    #                       hashtag, volume                                    #
    #                   our csv_order parameter should look like:              #
    #                       "hashtag,volume"                                   #
    ############################################################################
    def write(self, filepath, csv_format = None):
        """Writes data to a specified filepath. """
        file = open(filepath, "w")
        writer = csv.writer(file)
        keys = csv_format if csv_format else list(self.data.keys())

        # write header
        writer.writerow(keys)

        # write data
        for entry in self.data:
            convert = lambda e,k: quote(str(e[k])) if k in e else None
            values = [convert(entry, key) for key in keys]
            writer.writerow(values)

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


# # EXAMPLE CODE
# dat_hand = DataHandler()
#
# # reading data
# conversions = [int, str] # volume, hashtag
# dat_hand.read("data.txt", conversions)
#
#
# # adding data
# entry = {}
# entry["hashtag"] = "piday"
# entry["volume"] = 3
# dat_hand.add(entry)
#
# # cleaning data
# priority = lambda entry: entry["volume"]
# max_size = 10000
# trim_size = max_size - 1000
# if len(dat_hand.data) >= max_size:
#    dat_hand.clean(priority, trim_size)
#
# # sort
# dat_hand.data = sorted(dat_hand.data, key=priority, reverse=True)
#
# # writing data to file in CSV format
# cvs_format = ["volume", "hashtag"]
# dat_hand.write("data_out.txt", cvs_format)
