# TwitterPrediction

master: [![Build Status](https://travis-ci.org/kobejean/TwitterPrediction.svg?branch=master)](https://travis-ci.org/kobejean/TwitterPrediction)

develop: [![Build Status](https://travis-ci.org/kobejean/TwitterPrediction.svg?branch=develop)](https://travis-ci.org/kobejean/TwitterPrediction)

## Usage

###### DataHandler

I will work on better documentation for `DataHandler` later.

    import os
    from ttrends.collection.data_handler import DataHandler
    from ttrends.collection.stream_transformer import StreamTransformer

    # EXAMPLE CODE
    abspath = os.path.abspath(os.path.dirname(__file__))
    docspath = os.path.join(abspath, "data")

    # initialization
    dat_hand = DataHandler()
    dat_hand.csv_format = ["volume","hashtag"]
    dat_hand.conversions = [int, str] # volume, hashtag

    # reading data
    readpath = os.path.join(docspath, "test_data.csv")
    dat_hand.read(readpath)

    # adding data
    entry = {}
    entry["hashtag"] = "フラハティ 仁"
    entry["volume"] = 30
    dat_hand.add(entry)

    # cleaning data
    priority = lambda entry: entry.get("volume",0)
    trim_size = 5
    dat_hand.clean(priority, trim_size)

    # writing data to file in CSV format
    writepath = os.path.join(docspath, "test_data_out.csv")
    dat_hand.write(writepath)

    # print data
    dat_hand.display()


###### StreamTransformer

    # initialization
    st = StreamTransformer(tags=["followers_count","text"])

The `priority` attribute can be any function that takes an entry and returns a comparable that represents the priority rank. For example it could return a number like 23 or even a tupel like (23,12). A higher value means a higher priority.

    # priority
    def priority(entry):
        return entry["followers_count"]
    st.priority = priority

You can use lambda too...

    # priority
    st.priority = lambda entry: entry["followers_count"]

The `filepath` attribute is where the stream will be written to.

    # filepath
    abspath = os.path.abspath(os.path.dirname(__file__))
    datapath = os.path.join(abspath, "data")
    st.filepath = os.path.join(datapath,"STREAM.csv")

The `sample_size` attribute is the number of entries to stream before closing the stream. This is one of the two conditions that make the stream stop.

    # sample size
    st.sample_size = 1000

The duration attribute is the amount of time to wait before closing the stream. This takes a `timedelta` object. This is the second condition that that makes the stream stop.

    # duration
    st.duration = timedelta(minutes=30)

The `trim_size` attribute is the maximum number of entries to keep in the data file.

    # trim size
    st.trim_size = 100

The `period` attribute is how often the stream transformer should clean and write the data or how many entries the stream transformer should collect before cleaning and writing the data again.

    # period
    st.period = 10

When you want to continue from an already saved file call the method `read_data()`. It will read from the file path specified with the `filepath` attribute.

    # continue from last write
    st.read_data()

To use the stream transformer, pass it into the stream method of the DataCollector

    # data collector
    collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
    collector.authenticate()
    collector.stream(["machine learning"], st)

To print the data, call the `display` method on the `dat_hand` attribute.

    # print data
    st.dat_hand.display()

###### FHCTStreamTransformer
`FHCTStreamTransformer` is a subclass of `StreamTransformer`. FHCT stands for followers_count, hashtags, creation_date, text which are the tags that this stream transformer reads from. It also has a predefined priority function that is set to prioritize high followers_count entries.

    # initialization
    st = FHCTStreamTransformer()

    # filepath
    abspath = os.path.abspath(os.path.dirname(__file__))
    datapath = os.path.join(abspath, "data")
    st.filepath = os.path.join(datapath, "FHCTSTREAM.csv")

    # sample size
    st.sample_size = 1000

    # duration
    st.duration = timedelta(minutes=30)

    # trim size
    st.trim_size = 50

    # period
    st.period = 10

    # continue from last write
    st.read_data()


    # data collector
    collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
    collector.authenticate()
    collector.stream(["machine learning"], st)


    # print data
    st.dat_hand.display()

###### FUCTStreamTransformer
`FUCTStreamTransformer` is also a subclass of `StreamTransformer`. FUCT stands for followers_count, urls, creation_date, text which are the tags that this stream transformer reads from. It also has a predefined priority function that is set to prioritize entries with at least one url and has a high followers_count.

    # initialization
    st = FUCTStreamTransformer()

    # filepath
    abspath = os.path.abspath(os.path.dirname(__file__))
    datapath = os.path.join(abspath, "data")
    st.filepath = os.path.join(datapath, "FHCTSTREAM.csv")

    # sample size
    st.sample_size = 1000

    # duration
    st.duration = timedelta(minutes=30)

    # trim size
    st.trim_size = 50

    # period
    st.period = 10

    # continue from last write
    st.read_data()


    # data collector
    collector = DataCollector(access_token, access_token_secret, consumer_key, consumer_secret)
    collector.authenticate()
    collector.stream(["machine learning"], st)


    # print data
    st.dat_hand.display()
