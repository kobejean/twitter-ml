from datetime import datetime, timedelta
import os

from context import tml
from tml.collection.data_handler import DataHandler
from tml.collection.data_collector import DataCollector
from tml.collection.stream_transformer import *
from tml.collection.auth_info import * # where api access information is stored

TEST_MODE = True

st_types = [(0, FUCTStreamTransformer, "FUCTStreamTransformer"),
            (1, FHCTStreamTransformer, "FHCTStreamTransformer"),
            (2, EngTextStreamTransformer, "EngTextStreamTransformer")]

# inputs
print("PICK STREAM TRANSFORMER TYPE:")
for num, _, name in st_types:
    print("    ", num, name)
st_num = int(input("ENTER CORRESPONDING NUMBER: ")) if not TEST_MODE else 2
filters_str = input("ENTER FILTER: ")               if not TEST_MODE else "the"
sample_size = int(input("ENTER SAMPLE SIZE: "))     if not TEST_MODE else 500000
hours = float(input("ENTER DURATION IN HOURS: "))   if not TEST_MODE else 100
# trim_size = int(input("ENTER TRIM SIZE: "))         if not TEST_MODE else 500000
buffer_size = int(input("ENTER BUFFER SIZE: "))     if not TEST_MODE else 10000

# calculate duration
d = int(hours / 24)
h = int(hours % 24)
m = int(hours % 1 * 60)
s = int(hours * 60 % 1 * 60)
print("DURATION: ", d, "days", h, "hours", m, "minutes", s, "seconds")
duration = timedelta(days=d, hours=h, minutes=m, seconds=s)
# get chosen stream transformer class
ChosenStreamTransformer = st_types[st_num][1]
# determine file path
abspath = os.path.abspath(os.path.dirname(__file__))
datapath = os.path.join(abspath, "data")
file_name = ("" if not TEST_MODE else "TEST ") + filters_str.upper() + " STREAM.csv"
file_path = os.path.join(datapath, file_name)
print("FILE PATH: " + file_path)
# convert comma separated filters into list
filters = filters_str.split(",")
print("FILTERS: " + str(filters))

# set up stream transformer
st = ChosenStreamTransformer()
st.file_path = file_path
st.sample_size = sample_size
st.duration = duration
# st.trim_size = trim_size
st.buffer_size = buffer_size
st.read_data()

# set up collector
collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
collector.authenticate()
collector.stream(filters, st)

show_data = input("WOULD YOU LIKE TO SEE THE DATA? (Y/N): ")
if show_data.upper() == "Y":
    st.display_data()
