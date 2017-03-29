import sys
import os
# lets us import from main directory
scriptpath = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                os.path.expanduser(__file__))))
mainpath = os.path.join(scriptpath, "../../")
sys.path.append(os.path.normpath(mainpath))

from DataHandler import DataHandler
from DataCollector import DataCollector
from StreamTransformer import *
from twitter_auth import * # where api access information is stored

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

filter = "MACHINE LEARNING"
# filter = "DEEP LEARNING"
# filter = "HELLO WORLD"
# filter = "TRUMP"
# filter = "PYTHON"

streamTransformer = FHCTStreamTransformer()
streamTransformer.filename = filter.upper() + " STREAM.csv"
streamTransformer.collect_count = 5000 # number of entries to collect before stopping stream
streamTransformer.trim_size = 500 # the threshold of data size where the data is trimmed
streamTransformer.period = 10 # number of entries between cleaning/writing files

# streamTransformer = StreamTransformer(keys=["text"])

print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer)
