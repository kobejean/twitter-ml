import sys
import os
# lets us import from src/collection and main directory
scriptpath = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                os.path.expanduser(__file__))))
collectionpath = os.path.join(scriptpath, "../src/collection")
mainpath = os.path.join(scriptpath, "../")
sys.path.append(os.path.normpath(collectionpath))
sys.path.append(os.path.normpath(mainpath))

from DataHandler import DataHandler
from DataCollector import DataCollector
from StreamTransformer import *
from twitter_auth import * # where api access information is stored

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

# filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
filter = "TRUMP" # very fast stream
# filter = "PYTHON"

# quick tests for all stream transformers with very low settings
streamTransformer1 = StreamTransformer(keys=["text"])
streamTransformer1.filename = filter.upper() + " 1ST STREAM.csv"
streamTransformer1.collect_count = 100 # number of entries to collect before stopping stream
streamTransformer1.trim_size = 50 # the threshold of data size where the data is trimmed
streamTransformer1.period = 10 # number of entries between cleaning/writing files
streamTransformer1.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer1)

streamTransformer2 = FHCTStreamTransformer()
streamTransformer2.filename = filter.upper() + " 2ND STREAM.csv"
streamTransformer2.collect_count = 100 # number of entries to collect before stopping stream
streamTransformer2.trim_size = 5 # the threshold of data size where the data is trimmed
streamTransformer2.period = 10 # number of entries between cleaning/writing files
streamTransformer2.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer2)

streamTransformer3 = FUCTStreamTransformer()
streamTransformer3.filename = filter.upper() + " 3RD STREAM.csv"
streamTransformer3.collect_count = 100 # number of entries to collect before stopping stream
streamTransformer3.trim_size = 50 # the threshold of data size where the data is trimmed
streamTransformer3.period = 10 # number of entries between cleaning/writing files
streamTransformer3.read_data()
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer3)
