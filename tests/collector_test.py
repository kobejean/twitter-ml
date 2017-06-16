############################################################################################
# PROGRAMMED BY: Jean Flaherty                                                             #
# DATE: 4-07-2017                                                                          #
# DESCRIPTION: This script tests the data collection tools defined in the tml package      #
#                                                                                          #
############################################################################################

from context import tml
from tml.collection.data_handler import DataHandler
from tml.collection.data_collector import DataCollector
from tml.collection.stream_transformer import *
from tml.collection.auth_info import * # where api access information is stored

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

# filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
filter = "THE" # very fast stream
# filter = "PYTHON"

abspath = os.path.abspath(os.path.dirname(__file__))
datapath = os.path.join(abspath, "data")

# quick tests for all stream transformers with very low settings
st1 = StreamTransformer(tags=["text"])
filename1 =  filter.upper() + " 1ST STREAM.csv"
st1.file_path = os.path.join(datapath, filename1)
st1.sample_size = 100 # number of entries to collect before stopping stream
# st1.trim_size = 50 # the threshold of data size where the data is trimmed
st1.buffer_size = 10 # number of entries between cleaning/writing files
st1.read_data() # continue from existing data
print("FILTER: " + filter.upper())
collector.stream([filter], st1)

st2 = FHCTStreamTransformer()
filename2 =  filter.upper() + " 2ND STREAM.csv"
st2.file_path = os.path.join(datapath, filename2)
st2.sample_size = 100 # number of entries to collect before stopping stream
# st2.trim_size = 50 # the threshold of data size where the data is trimmed
st2.buffer_size = 10 # number of entries between cleaning/writing files
st2.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], st2)

st3 = FUCTStreamTransformer()
filename3 =  filter.upper() + " 3RD STREAM.csv"
st3.file_path = os.path.join(datapath, filename3)
st3.sample_size = 100 # number of entries to collect before stopping stream
# st3.trim_size = 50 # the threshold of data size where the data is trimmed
st3.buffer_size = 10 # number of entries between cleaning/writing files
st3.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], st3)

st1.display_data()
st2.display_data()
st3.display_data()
