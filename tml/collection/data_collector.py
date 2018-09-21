import datetime
import json
import os
import time

from tweepy import Stream, OAuthHandler, API
from .stream_transformer import StreamTransformer
from .auth_info import *


class DataCollector(object):

    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.api = None

    def authenticate(self):
        """
                                - Authenticate Method -

        DESCRIPTION: Authenticates user with the Twitter Stream API.
        """
        # authenticate and connect to stream api
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = API(auth)

    def trends(self, tags):
        """
                                  - Trends Method -

        DESCRIPTION: Gets current top 50 trending twitter subjects

        PARAMETERS:
            tags - The parts of the JSON encoded tweets that the user would
                 like to include in the data
        """
        all_trends = self.api.trends_place(1)[0]['trends']
        buffer = []
        buffPos = 0

        # iterate through each trend and fill the cooresponding position in the
        # buffer with the specified tags from that trend
        for trend in all_trends:
            for tag in tags:
                buffer[buffPos] = {tag: all_trends[tag]}

    def stream(self, filters, stream_listener):
        """
                                  - Stream Method -

        DESCRIPTION: Gets recent tweets from the Twitter Stream API

        PARAMETERS:
            filters - the types of tweet subjects the user would like the get
            streamListener - The delegate for StreamListener
        """
        stream = Stream(auth=self.api.auth, listener=stream_listener)
        stream.filter(track=filters)


def get_live_tweets(filters, tags, output_file='STREAM.csv', sample_size=100, buffer_size=100):
    '''
    Builder method that simplifies the data gathering processes from the twitter
    stream API

    :param filters: Words that will be contained in each tweet collected
    :param tags: Tweet parameters that will be retrieved
    :param output_file: Name of the file to write tweets to
    :param sample_size: Number of tweets to collect
    :param buffer_size: Size of the tweet buffer
    :return:
    '''
    st = StreamTransformer(tags, output_file, sample_size, buffer_size)
    st.scan_file()

    try_again = True
    while try_again:
        try:
            # set up collector
            collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
            collector.authenticate()
            collector.stream(filters, st)
        except Exception as e:
            print(e)
            print("SAVING CURRENT BUFFER...")
            st.write_data()
            print("TRY AGAIN IN 1MIN...")
            time.sleep(60)
        else:
            try_again = False


# get_live_tweets('the', ['text'])
