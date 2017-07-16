# TwitterML

master: [![Build Status](https://travis-ci.org/kobejean/TwitterML.svg?branch=master)](https://travis-ci.org/kobejean/TwitterML)

develop: [![Build Status](https://travis-ci.org/kobejean/TwitterML.svg?branch=develop)](https://travis-ci.org/kobejean/TwitterML)

#### Dependencies

- tensorflow (1.1.0)
- tweepy (3.5.0)
- keras (2.0.5)

#### Credit

Character Prediction Adapted from: [tensorflow-rnn-shakespeare](https://github.com/martin-gorner/tensorflow-rnn-shakespeare)

## Table of Contents

- [Data Collection](#data-collection)
- [Data Preprocessing](#data-processing)
- [Machine Learning](#machine-learning)
    - [Character Prediction](#character-prediction)
    - [Word Embeddings](#word-embeddings)

## Data Collection
First of all if you want to get started with the machine learning part you can
skip data collection by downloading twitter text data
[here](https://drive.google.com/open?id=0By-CMfnYF6bZWjY1VjNLazAtb2c).
Drop that file into `src/shared_data`, [preprocess](#data-processing) the data,
and start messing with [machine learning](#machine-learning).

To start collecting twitter text, run [collection_program.py](src/data_collection/collection_program.py) :
``` bash
$ python3 src/data_collection/collection_program.py
```
For twitter text collection pick the `EngTextStreamTransformer` by typing in `2`.
For the filter, using `the` will give you a steady stream of tweets.
The sample size is the number of tweets to collect, `500000000` would be roughly
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
ENTER SAMPLE SIZE: 500000000
ENTER DURATION IN HOURS: 720
ENTER BUFFER SIZE: 25000
SHOULD PRINT ENTRY (0 or 1): 0
```

## Data Preprocessing
For using these examples replace `src/shared_data/THE\ STREAM.csv` with the path
to your text file.

Preprocessing for character prediction:
``` bash
$ python3 src/character_prediction/create_text.py src/shared_data/THE\ STREAM.csv
```

Preprocessing for word embeddings:
``` bash
$ python3 src/word_embeddings/create_data_package.py src/shared_data/THE\ STREAM.csv
```

A convenient script for preprocessing for both cases:
``` bash
$ cd src # neeeds to run in the src directory
$ ./preprocessing.sh shared_data/THE\ STREAM.csv
$ cd ../ # back to project root directory
```
## Machine Learning

#### Character Prediction
After [collecting](#data-collection) and [preprocessing](#data-processing)
twitter text data, run the character prediction training program with:
``` bash
$ python3 src/character_prediction/char_rnn_train.py src/character_prediction/data/THE\ STREAM
```
Replace `src/character_prediction/data/THE\ STREAM` with the path to the
directory of all the text batch files.

After a bit of training you can watch the model generate text by running:
``` bash
$ python3 src/character_prediction/char_rnn_play.py
```


#### Word Embeddings
After [collecting](#data-collection) and [preprocessing](#data-processing)
twitter text data, run the random or not word embeddings neural net training program with:
``` bash
$ python3 src/word_embeddings/random_or_not_word_embedding_nn.py
```

To see the word embeddings in tensorboard run the command:
``` bash
$ tensorboard --logdir=src/word_embeddings/log/1/
```
