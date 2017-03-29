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

# quick tests for both stream transformers with very low settings
streamTransformer1 = FHCTStreamTransformer()
streamTransformer1.filename = filter.upper() + " STREAM 1.csv"
streamTransformer1.collect_count = 10 # number of entries to collect before stopping stream
streamTransformer1.trim_size = 5 # the threshold of data size where the data is trimmed
streamTransformer1.period = 5 # number of entries between cleaning/writing files
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer1)

streamTransformer2 = StreamTransformer(keys=["text"])
streamTransformer2.filename = filter.upper() + " STREAM 2.csv"
streamTransformer2.collect_count = 10 # number of entries to collect before stopping stream
streamTransformer2.trim_size = 5 # the threshold of data size where the data is trimmed
streamTransformer2.period = 5 # number of entries between cleaning/writing files
print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer2)
