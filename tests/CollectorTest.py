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
streamTransformer1 = FHCTStreamTransformer()
streamTransformer1.filename = filter.upper() + " STREAM 1.csv"
streamTransformer1.collect_count = 10 # number of entries to collect before stopping stream
streamTransformer1.trim_size = 5 # the threshold of data size where the data is trimmed
streamTransformer1.period = 5 # number of entries between cleaning/writing files
streamTransformer1.read()
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer1)

streamTransformer2 = FHCTStreamTransformer()
streamTransformer2.filename = filter.upper() + " STREAM 2.csv"
streamTransformer2.collect_count = 10 # number of entries to collect before stopping stream
streamTransformer2.trim_size = 5 # the threshold of data size where the data is trimmed
streamTransformer2.period = 5 # number of entries between cleaning/writing files
streamTransformer2.read()
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer2)

streamTransformer3 = StreamTransformer(keys=["text"])
streamTransformer3.filename = filter.upper() + " STREAM 3.csv"
streamTransformer3.collect_count = 10 # number of entries to collect before stopping stream
streamTransformer3.trim_size = 5 # the threshold of data size where the data is trimmed
streamTransformer3.period = 5 # number of entries between cleaning/writing files
streamTransformer3.read()
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer3)
