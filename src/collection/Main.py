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

from datetime import datetime, timedelta

collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()

filters = input("ENTER FILTER: ")
collect_count = int(input("ENTER COLLECT COUNT: "))
hours = float(input("ENTER DURATION IN HOURS: "))
trim_size = int(input("ENTER TRIM SIZE: "))
period = int(input("ENTER PERIOD: "))

d = int(hours/24)
h = int(hours % 24)
m = int(hours * 60)
s = int(hours * 60 * 60)
duration = timedelta(days=d, hours=h, minutes=m, seconds=s)

# filter = "MACHINE LEARNING"
# filter = "DEEP LEARNING"
# filter = "HELLO WORLD"
# filter = "TRUMP"
# filter = "PYTHON"

streamTransformer = FUCTStreamTransformer()
streamTransformer.filename = filters.upper() + " STREAM.csv"
streamTransformer.collect_count = collect_count
streamTransformer.duration = duration
streamTransformer.trim_size = trim_size
streamTransformer.period = period
streamTransformer.read()

# streamTransformer = StreamTransformer(keys=["text"])

filters = [filter.strip().upper() for filter in filters.split(",")]
print("FILTERS: " + str(filters))
collector.stream(filters, streamTransformer)
