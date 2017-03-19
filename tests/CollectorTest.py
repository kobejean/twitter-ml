import sys
import os
# let's us import from src/collection
scriptpath = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                os.path.expanduser(__file__))))
collectionpath = os.path.join(scriptpath, "../src/collection")
sys.path.append(os.path.normpath(collectionpath))

from DataHandler import DataHandler
from DataCollector import DataCollector
from StreamTransformer import *

# store api access information
access_token = "3911012232-MNWJkB5E5EnN8pNrqPu8TjOIJrXHs5TmsSVI6dW"
access_token_secret = "jjOsGntWGcxQdPZg3ZVamCdhmYjzNDOPZxMBa1zyn1Cic"
consumer_key = "ToqLVlPLUsqrvHokKIitbi5ps"
consumer_secret = "OSLHJZBOsu1nrCk476BAIDXiVCHEl7IbAwK8ZxjwMJWjOL4q3w"

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

# filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
filter = "TRUMP" # very fast stream
# filter = "PYTHON"

# quick tests for both stream transformers with very low settings
streamTransformer1 = FHCTStreamTransformer()
streamTransformer1.collect_count = 4 # number of entries to collect before stopping stream
streamTransformer1.threshold_size = 2 # the threshold of data size where the data is trimmed
streamTransformer1.period = 2 # number of entries between cleaning/writing files
streamTransformer1.trim_size = 2
print("FILTER: " + filter.upper())
collector.stream(filter, streamTransformer1)

streamTransformer2 = StreamTransformer(keys=["text"])
streamTransformer2.collect_count = 4 # number of entries to collect before stopping stream
streamTransformer2.threshold_size = 2 # the threshold of data size where the data is trimmed
streamTransformer2.period = 2 # number of entries between cleaning/writing files
streamTransformer2.trim_size = 2
print("FILTER: " + filter.upper())
collector.stream(filter, streamTransformer2)
