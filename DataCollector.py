################################################################################
#                          - Data Collector Class -                            #
#                                                                              #
#   PROGRAMMED BY: Jake Jongewaard                                             #
#   DATE: 03-06-2017                                                           #
#   DESCRIPTION: Handles collecting data from the Twitter Stream API and       #
#                passing it to the DataHandler class                           #
#                                                                              #
#   METHODS:                                                                   #
#       authenticate    - Use api access credentials to authenticate user      #
#       trends  - Get the current top 50 twitter trends                        #
#       stream  - Get live data from Stream API                                #
################################################################################
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler, API
from DataHandler import DataHandler
import json
import datetime


#This is a basic listener that just prints received tweets to stdout.
class _ApiListener(StreamListener):
    dat_hand = DataHandler()
    keys = ["followers_count","hashtags","created_at","text"]
    collect_count = 20  # number of entries to collect before stopping stream
    threshold_size = 15 # the threshold of data size where the data is trimmed
    period = 5          # number of entries between cleaning/writing files
    trim_size = threshold_size - period
    entry_count = 0     # keeping track of the muber of entries added

    # create tag, magnitude pairs directly here
    def on_data(self, data):
        data = json.loads(data) # convert to dictionary
        # print("data: "+str(data))

        # get entry
        entry = {}
        entry["followers_count"] = data["user"]["followers_count"]
        hashtags = data["entities"]["hashtags"]
        entry["hashtags"] = [hashtag["text"] for hashtag in hashtags]
        entry["created_at"] = data["created_at"]
        entry["text"] = data["text"]

        self.dat_hand.add(entry)

        self.entry_count += 1
        print("ADDED: ENTRY #" + str(self.entry_count))

        # if we collected enough data entries
        if self.entry_count >= self.collect_count:
            self.clean()
            self.write()
            print("STREAM STOPPED")
            return False # stops stream

        # periodic clean and write
        if self.entry_count % self.period == 0 :
            self.clean()
            self.write()

    def clean(self):
        # prioritize entries with more hash tags
        # priority = lambda entry: len(entry.get("hashtags",[]))
        # prioritize entries with more followers
        priority = lambda entry: entry.get("followers_count",0)
        self.dat_hand.clean(priority, self.threshold_size, self.trim_size)

    def write(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        filepath = "STREAM DATA "+ date +".txt"
        print("WRITING TO: "+ filepath)
        self.dat_hand.write(filepath, self.keys)

class DataCollector(object):

    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.api = None #lazy initialization?

    ############################################################################
    #                       - Authenticate Method -                            #
    #                                                                          #
    #   DESCRIPTION: Authenticates user with the Twitter Stream API.           #
    #                                                                          #
    #   PARAMETERS:                                                            #
    #       none                                                               #
    ############################################################################
    def authenticate(self):
        # authenticate and connect to stream api
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = API(auth)

    ############################################################################
    #                               - Trends Method -                          #
    #                                                                          #
    #   DESCRIPTION: Gets current top 50 trending twitter subjects             #
    #                                                                          #
    #   PARAMETERS:                                                            #
    #       tags - The parts of the JSON encoded tweets that the user would    #
    #              like to include in the data                                 #
    ############################################################################
    def trends(self, tags):
        all_trends = self.api.trends_place(1)[0]['trends']
        buffer = []
        buffPos = 0

        # iterate through each trend and fill the cooresponding position in the
        # buffer with the specified tags from that trend
        for trend in all_trends:
            for tag in tags:
                buffer[buffPos] = {tag : all_trends[tag]}

    ############################################################################
    #                               - Stream Method -                          #
    #                                                                          #
    #   DESCRIPTION: Gets recent tweets from the Twitter Stream API            #
    #                                                                          #
    #   PARAMETERS:                                                            #
    #       filters - the types of tweet subjects the user would like the get  #
    #       streamListener - The delegate for StreamListener                   #
    ############################################################################
    def stream(self, filters, streamListener):
        stream = Stream(auth=self.api.auth, listener=streamListener)
        stream.filter(track=[filters])


if __name__ == '__main__':
    # store api access information
    access_token = "3911012232-MNWJkB5E5EnN8pNrqPu8TjOIJrXHs5TmsSVI6dW"
    access_token_secret = "jjOsGntWGcxQdPZg3ZVamCdhmYjzNDOPZxMBa1zyn1Cic"
    consumer_key = "ToqLVlPLUsqrvHokKIitbi5ps"
    consumer_secret = "OSLHJZBOsu1nrCk476BAIDXiVCHEl7IbAwK8ZxjwMJWjOL4q3w"

    collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
    collector.authenticate()

    streamListener = _ApiListener()

    filter = "MACHINE LEARNING"
    # filter = "HELLO WORLD"
    # filter = "TRUMP"
    # filter = "PYTHON"

    print("FILTER: " + filter.upper())
    collector.stream(filter, streamListener)
