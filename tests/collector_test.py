############################################################################################
# PROGRAMMED BY: Jean Flaherty                                                             #
# DATE: 4-07-2017                                                                          #
# DESCRIPTION: This script tests the data collection tools defined in the tml package      #
#                                                                                          #
############################################################################################

import time
from context import tml
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

time.sleep(3)

st2 = FHCTStreamTransformer()
filename2 =  filter.upper() + " 2ND STREAM.csv"
st2.file_path = os.path.join(datapath, filename2)
st2.sample_size = 100 # number of entries to collect before stopping stream
# st2.trim_size = 50 # the threshold of data size where the data is trimmed
st2.buffer_size = 10 # number of entries between cleaning/writing files
st2.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], st2)

time.sleep(3)

st3 = FUCTStreamTransformer()
filename3 =  filter.upper() + " 3RD STREAM.csv"
st3.file_path = os.path.join(datapath, filename3)
st3.sample_size = 100 # number of entries to collect before stopping stream
# st3.trim_size = 50 # the threshold of data size where the data is trimmed
st3.buffer_size = 10 # number of entries between cleaning/writing files
st3.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], st3)

time.sleep(3)

st4 = EngTextStreamTransformer()
filename4 =  filter.upper() + " 4TH STREAM.csv"
st4.file_path = os.path.join(datapath, filename4)
st4.sample_size = 100 # number of entries to collect before stopping stream
# st4.trim_size = 50 # the threshold of data size where the data is trimmed
st4.buffer_size = 10 # number of entries between cleaning/writing files
st4.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], st4)


st1.display_data()
st2.display_data()
st3.display_data()
st4.display_data()

os.remove(st1.file_path)
os.remove(st2.file_path)
os.remove(st3.file_path)
os.remove(st4.file_path)
