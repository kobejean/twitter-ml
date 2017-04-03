from datetime import datetime, timedelta
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

filters = input("ENTER FILTER: ")
collect_count = int(input("ENTER COLLECT COUNT: "))
hours = float(input("ENTER DURATION IN HOURS: "))
trim_size = int(input("ENTER TRIM SIZE: "))
period = int(input("ENTER PERIOD: "))

d = int(hours / 24)
h = int(hours % 24)
m = int(hours % 1 * 60)
s = int(hours * 60 % 1 * 60)
print("DURATION:")
print("d:", d, "h:", h, "m:", m, "s:", s)
duration = timedelta(days=d, hours=h, minutes=m, seconds=s)

stream_transformer = FUCTStreamTransformer()
stream_transformer.filename = filters.upper() + " STREAM.csv"
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
