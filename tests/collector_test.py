############################################################################################
# PROGRAMMED BY: Jean Flaherty                                                             #
# DATE: 4-07-2017                                                                          #
# DESCRIPTION: This script tests the data collection tools defined in the ttrends package  #
#                                                                                          #
############################################################################################

from ttrends.collection.data_handler import DataHandler
from ttrends.collection.data_collector import DataCollector
from ttrends.collection.stream_transformer import *
from ttrends.collection.auth_info import * # where api access information is stored

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

# filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
filter = "TRUMP" # very fast stream
# filter = "PYTHON"

abspath = os.path.abspath(os.path.dirname(__file__))
datapath = os.path.join(abspath, "data")

# quick tests for all stream transformers with very low settings
stream_transformer1 = StreamTransformer(tags=["text"])
filename1 =  filter.upper() + " 1ST STREAM.csv"
stream_transformer1.filepath = os.path.join(datapath, filename1)
stream_transformer1.sample_size = 100 # number of entries to collect before stopping stream
stream_transformer1.trim_size = 50 # the threshold of data size where the data is trimmed
stream_transformer1.period = 10 # number of entries between cleaning/writing files
stream_transformer1.read_data() # continue from existing data
print("FILTER: " + filter.upper())
collector.stream([filter], stream_transformer1)

stream_transformer2 = FHCTStreamTransformer()
filename2 =  filter.upper() + " 2ND STREAM.csv"
stream_transformer2.filepath = os.path.join(datapath, filename2)
stream_transformer2.sample_size = 100 # number of entries to collect before stopping stream
stream_transformer2.trim_size = 50 # the threshold of data size where the data is trimmed
stream_transformer2.period = 10 # number of entries between cleaning/writing files
stream_transformer2.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], stream_transformer2)

stream_transformer3 = FUCTStreamTransformer()
filename3 =  filter.upper() + " 3RD STREAM.csv"
stream_transformer3.filepath = os.path.join(datapath, filename3)
stream_transformer3.sample_size = 100 # number of entries to collect before stopping stream
stream_transformer3.trim_size = 50 # the threshold of data size where the data is trimmed
stream_transformer3.period = 10 # number of entries between cleaning/writing files
stream_transformer3.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], stream_transformer3)

stream_transformer1.dat_hand.display()
stream_transformer2.dat_hand.display()
stream_transformer3.dat_hand.display()
