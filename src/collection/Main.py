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

filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
# filter = "TRUMP"
# filter = "PYTHON"

streamTransformer = FHCTStreamTransformer()
streamTransformer.filename = filter.upper() + " STREAM.csv"
streamTransformer.collect_count = 4 # number of entries to collect before stopping stream
streamTransformer.trim_size = 2 # the threshold of data size where the data is trimmed
streamTransformer.period = 2 # number of entries between cleaning/writing files

# streamTransformer = StreamTransformer(keys=["text"])

print("FILTER: " + filter.upper())
collector.stream([filter], streamTransformer)
