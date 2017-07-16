"""
                              - DataCollector -

PROGRAMMED BY: Jake Jongewaard
DATE: 03/18/2017
DESCRIPTION: Handles collecting data from the Twitter Stream API and
             passing it to the DataHandler class

CLASSES:
    DataCollector: collects useful formated data from various Twitter APIs
"""

import datetime
import json
import os

from tweepy import Stream, OAuthHandler, API

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
                buffer[buffPos] = {tag : all_trends[tag]}

    def stream(self, filters, streamListener):
        """
                                  - Stream Method -

        DESCRIPTION: Gets recent tweets from the Twitter Stream API

        PARAMETERS:
            filters - the types of tweet subjects the user would like the get
            streamListener - The delegate for StreamListener
        """
        stream = Stream(auth=self.api.auth, listener=streamListener)
        stream.filter(track=filters)
