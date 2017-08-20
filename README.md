# twitter-ml

master: [![Build Status](https://travis-ci.org/kobejean/twitter-ml.svg?branch=master)](https://travis-ci.org/kobejean/twitter-ml)

develop: [![Build Status](https://travis-ci.org/kobejean/twitter-ml.svg?branch=develop)](https://travis-ci.org/kobejean/twitter-ml)

#### Dependencies

- tensorflow (1.2.0)
- tweepy (3.5.0)
- keras (2.0.5)

#### Credit

Character Prediction Adapted from: [tensorflow-rnn-shakespeare](https://github.com/martin-gorner/tensorflow-rnn-shakespeare)

## Table of Contents

- [Data Collection](#data-collection)
- [Data Preprocessing](#data-preprocessing)
- [Machine Learning](#machine-learning)
    - [Character Prediction](#character-prediction)
    - [Word Embeddings](#word-embeddings)

## Data Collection
First of all if you want to get started with the machine learning part you can
skip data collection by downloading twitter text data
[here](https://drive.google.com/open?id=0By-CMfnYF6bZWjY1VjNLazAtb2c).
Drop that file into `src/shared_data`, [preprocess](#data-preprocessing) the data,
and start messing with [machine learning](#machine-learning).

To start collecting twitter text, run [collection_program.py](src/data_collection/collection_program.py) :
``` bash
$ python3 src/data_collection/collection_program.py
```
For twitter text collection pick the `EngTextStreamTransformer` by typing in `2`.
For the filter, using `the` will give you a steady stream of tweets.
The sample size is the number of tweets to collect, `50000000` would be roughly
5GB of data and will take a long time to collect, but you can stop the program at any time.

Here are all the options that I use for running collection on a small server:
``` bash
$ python3 src/data_collection/collection_program.py
PICK STREAM TRANSFORMER TYPE:
     0 FUCTStreamTransformer
     1 FHCTStreamTransformer
     2 EngTextStreamTransformer
ENTER CORRESPONDING NUMBER: 2
ENTER FILTER: the
ENTER SAMPLE SIZE: 50000000
ENTER DURATION IN HOURS: 720
ENTER BUFFER SIZE: 25000
SHOULD PRINT ENTRY (0 or 1): 0
```

## Data Preprocessing
For using these examples replace `../shared_data/THE\ STREAM.csv` with the path
to your text file.

Preprocessing for character prediction:
``` bash
$ cd src/character_prediction # needs to run in the character_prediction directory
$ ./create_text.sh ../shared_data/THE\ STREAM.csv
```

Preprocessing for word embeddings:
``` bash
$ cd src/word_embeddings # needs to run in the word_embeddings directory
$ ./create_data_package.sh ../shared_data/THE\ STREAM.csv
```

A convenient script for preprocessing for both cases:
``` bash
$ cd src # neeeds to run in the src directory
$ ./preprocessing.sh shared_data/THE\ STREAM.csv
```
## Machine Learning

#### Character Prediction
After [collecting](#data-collection) and [preprocessing](#data-preprocessing)
twitter text data, run the character prediction training program with:
``` bash
$ cd src/character_prediction # needs to run in the character_prediction directory
$ ./run_rnn_train.sh data/THE\ STREAM/\*.txt
```
Replace `data/THE\ STREAM/\*.txt` with the paths to the all the text batch files.

After a bit of training you can watch the model generate text by running:
``` bash
$ cd src/character_prediction # needs to run in the character_prediction directory
$ python3 char_rnn_play.py
```

To launch tensorboard run the command:
``` bash
$ cd src/character_prediction # needs to run in the word_embeddings directory
$ tensorboard --logdir=log
```


#### Word Embeddings
After [collecting](#data-collection) and [preprocessing](#data-preprocessing)
twitter text data, run the random or not word embeddings neural net training program with:
``` bash
$ cd src/word_embeddings # needs to run in the word_embeddings directory
$ ./run_random_or_not_nn.sh data/THE\ STREAM # relative path to the data package
```
Replace `data/THE\ STREAM` with the relative path to your data package directory

To see the word embeddings in tensorboard run the command:
``` bash
$ cd src/word_embeddings # needs to run in the word_embeddings directory
$ tensorboard --logdir=log
```
