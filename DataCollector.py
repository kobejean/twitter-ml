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
    tags = ["hashtags","created_at","text"]
    entry_count = 15 # number of entries to collect
    period = 5 # number of entries between writing files

    # create tag, magnitude pairs directly here
    def on_data(self, data):
        data = json.loads(data) # convert to dictionary

        # get entry
        entry = {}
        hashtags = data.get("entities",{}).get("hashtags",[])
        entry["hashtags"] = [hashtag["text"] for hashtag in hashtags]
        entry["created_at"] = data.get("created_at", None)
        entry["text"] = data.get("text", None)
        self.dat_hand.add(entry)

        print("ADDED: ENTRY #"+str(len(self.dat_hand.data)))

        def write():
            date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filepath = "STREAM DATA "+ date_string +".txt"
            print("WRITING TO: "+ filepath)
            self.dat_hand.write(filepath, self.tags)

        # if we collected enough data entries
        if len(self.dat_hand.data) >= self.entry_count:
            write()
            print("STREAM STOPPED")
            return False # stops stream

        # periodic write
        if len(self.dat_hand.data) % self.period == 0 :
            write()

class DataCollector(object):

    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.api = None #lazy initialization?

    ################################################################################
    #                       - Authenticate Method -                                #
    #                                                                              #
    #   DESCRIPTION: Authenticates user with the Twitter Stream API.               #
    #                                                                              #
    #   PARAMETERS:                                                                #
    #       none                                                                   #
    ################################################################################
    def authenticate(self):
        # authenticate and connect to stream api
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = API(auth)

    ################################################################################
    #                               - Trends Method -                              #
    #                                                                              #
    #   DESCRIPTION: Gets current top 50 trending twitter subjects                 #
    #                                                                              #
    #   PARAMETERS:                                                                #
    #       tags - The parts of the JSON encoded tweets that the user would like   #
    #              to include in the data                                          #
    ################################################################################
    def trends(self, tags):
        all_trends = self.api.trends_place(1)[0]['trends']
        buffer = []
        buffPos = 0

        #iterate through each trend and fill the cooresponding position in the buffer
        #with the specified tags from that trend
        for trend in all_trends:
            for tag in tags:
                buffer[buffPos] = {tag : all_trends[tag]}

    ################################################################################
    #                               - Stream Method -                              #
    #                                                                              #
    #   DESCRIPTION: Gets recent tweets from the Twitter Stream API                #
    #                                                                              #
    #   PARAMETERS:                                                                #
    #       filters - the types of tweet subjects the user would like the get      #
    #       tags - The parts of the JSON encoded tweets that the user would like   #
    #              to include in the data                                          #
    ################################################################################
    def stream(self, filters, apiListener):
        stream = Stream(auth=self.api.auth, listener=apiListener)
        stream.filter(track=[filters])


if __name__ == '__main__':
    # store api access information
    access_token = "3911012232-MNWJkB5E5EnN8pNrqPu8TjOIJrXHs5TmsSVI6dW"
    access_token_secret = "jjOsGntWGcxQdPZg3ZVamCdhmYjzNDOPZxMBa1zyn1Cic"
    consumer_key = "ToqLVlPLUsqrvHokKIitbi5ps"
    consumer_secret = "OSLHJZBOsu1nrCk476BAIDXiVCHEl7IbAwK8ZxjwMJWjOL4q3w"

    collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
    collector.authenticate()

    apiListener = _ApiListener()

    filter = "MACHINE LEARNING"
    # filter = "HELLO WORLD"
    # filter = "TRUMP"
    # filter = "PYTHON"

    print("FILTER: " + filter.upper())
    collector.stream(filter, apiListener)
