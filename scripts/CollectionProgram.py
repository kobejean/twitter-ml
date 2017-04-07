from datetime import datetime, timedelta
import sys
import os

from context import ttrends
from ttrends.collection.DataHandler import DataHandler
from ttrends.collection.DataCollector import DataCollector
from ttrends.collection.StreamTransformer import *
from ttrends.collection.AuthInfo import * # where api access information is stored

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

filters = input("ENTER FILTER: ")
collect_count = int(input("ENTER COLLECT COUNT: "))
hours = float(input("ENTER DURATION IN HOURS: "))

# calculate duration
d = int(hours / 24)
h = int(hours % 24)
m = int(hours % 1 * 60)
s = int(hours * 60 % 1 * 60)
print("DURATION: d", d, "h", h, "m", m, "s", s)
duration = timedelta(days=d, hours=h, minutes=m, seconds=s)

trim_size = int(input("ENTER TRIM SIZE: "))
period = int(input("ENTER PERIOD: "))

abspath = os.path.abspath(os.path.dirname(__file__))
datapath = os.path.join(abspath, "data")
filename = filters.upper() + " STREAM.csv"
filepath = os.path.join(datapath, filename)
print("FILE PATH: " + filepath)

stream_transformer = FUCTStreamTransformer()
stream_transformer.filepath = filepath
stream_transformer.collect_count = collect_count
stream_transformer.duration = duration
stream_transformer.trim_size = trim_size
stream_transformer.period = period
stream_transformer.read_data()

# convert comma separated filters into list
filters = filters.split(",")
print("FILTERS: " + str(filters))
collector.stream(filters, stream_transformer)

stream_transformer.dat_hand.display()
