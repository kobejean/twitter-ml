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
    tags = []
    entry_count = 10000
    period = 50
    data_transform = lambda d: {t:d[t] if t in d else None for t in self.tags} # default data transform

    #create tag, magnitude pairs directly here
    def on_data(self, data):
        data = json.loads(data)
        entry = data_transform(data)
        self.dat_hand.add(entry)

        print("on_data:"+str(len(self.dat_hand.data)))

        if len(self.dat_hand.data) % self.period == 0 :
            date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.dat_hand.write("stream_data_"+date_string+".txt", self.tags)

        # if we collected enough data entries
        if len(self.dat_hand.data) >= self.entry_count:
            date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.dat_hand.write("stream_data_"+date_string+".txt", self.tags)
            print("stream stop")
            return False # stops stream

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
    def stream(self, filters, tags, data_transform=None, entry_count=10):
        apiListener = _ApiListener()
        apiListener.tags = tags
        apiListener.entry_count = entry_count
        if data_transform:
            apiListener.data_transform = data_transform
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

    tags = ["hashtags","created_at","text"]

    # takes data from stream and returns a data entry dictionary
    def data_transform(data):
        entry = {}
        # get hashtags
        entry["hashtags"] = []
        if "entities" in data:
            if "hashtags" in data["entities"]:
                for hashtag in data["entities"]["hashtags"]:
                    entry["hashtags"].append(hashtag["text"])
        # get other values
        entry["created_at"] = data["created_at"] if "created_at" in data else None
        entry["text"] = data["text"] if "text" in data else None
        return entry

##    print("FILTER:trump")
##    collector.stream('trump', tags, data_transform, 1000)
    print("FILTER:python")
    collector.stream('python', tags, data_transform, 500)
