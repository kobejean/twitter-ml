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
import csv
import os.path

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
    #       threshold_size - The threshold at which point the data is trimmed. #
    #       trim_size - The size of that the data should be trimmed down to.   #
    ############################################################################
    def clean(self, priority, threshold_size, trim_size):
        """Trims data keeping key/value pairs with higher priority."""
        k = len(self.data)
        if k >= threshold_size:
            k = trim_size
        self.data = sorted(self.data, key=priority, reverse=True)[0:k]

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
    def write(self, filepath, csv_format = None):
        """Writes data to a specified filepath as a CVS file. """
        file = open(filepath, "w")
        writer = csv.writer(file)
        keys = csv_format if csv_format else list(self.data.keys())
        # write header
        writer.writerow(keys)

        # write data
        for entry in self.data:
            values = []
            for key in keys:
                value = entry.get(key,None)
                if value != None:
                    # escape value
                    value = str(value).encode("utf-8")
                    value = str(value)[2:-1]
                values.append(value)
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

# # DATA HANDLER EXAMPLE CODE
# abspath = os.path.abspath(os.path.dirname(__file__))
# docspath = os.path.join(abspath, "../../docs/")
# dat_hand = DataHandler()
#
# # reading data
# conversions = [int, str] # volume, hashtag
# dat_hand.read(docspath+"test_data.txt", conversions)
#
# # adding data
# entry = {}
# entry["hashtag"] = "フラハティ 仁"
# entry["volume"] = 30
# dat_hand.add(entry)
#
# # cleaning data
# priority = lambda entry: entry.get("volume",0)
# threshold_size = 10
# trim_size = threshold_size - 5
# dat_hand.clean(priority, threshold_size, trim_size)
#
# # writing data to file in CSV format
# cvs_format = ["volume", "hashtag"]
# dat_hand.write(docspath+"test_data_out.txt", cvs_format)

# print(dat_hand.data)
