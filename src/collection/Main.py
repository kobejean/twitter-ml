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

streamTransformer = FHCTStreamTransformer()
# streamTransformer = StreamTransformer(keys=["text"])

filter = "MACHINE LEARNING"
# filter = "HELLO WORLD"
# filter = "TRUMP"
# filter = "PYTHON"

print("FILTER: " + filter.upper())
collector.stream(filter, streamTransformer)
