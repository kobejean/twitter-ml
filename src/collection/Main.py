from src.collection.DataHandler import DataHandler
from src.collection.DataCollector import DataCollector
from src.collection.StreamTransformer import *

# store api access information
access_token = "3911012232-MNWJkB5E5EnN8pNrqPu8TjOIJrXHs5TmsSVI6dW"
access_token_secret = "jjOsGntWGcxQdPZg3ZVamCdhmYjzNDOPZxMBa1zyn1Cic"
consumer_key = "ToqLVlPLUsqrvHokKIitbi5ps"
consumer_secret = "OSLHJZBOsu1nrCk476BAIDXiVCHEl7IbAwK8ZxjwMJWjOL4q3w"

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

streamListener = FHCTStreamTransformer()
# streamListener = StreamTransformer(keys=["text"])

filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
# filter = "TRUMP"
# filter = "PYTHON"

print("FILTER: " + filter.upper())
collector.stream(filter, streamListener)