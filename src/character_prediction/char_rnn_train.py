#!/usr/bin/env python3
"""
               - Character Recurrent Neural Net Training -

PROGRAMMED BY: Jean Flaherty
DATE: 07/15/2017
DESCRIPTION:
    Trains a model to predict the next character given a sequence of chars.

    The path to the text file batch directory can be passed as an argumant in
    command line like this:

        $ python3 char_rnn_train.py path/to/text_batches/
"""

import os, sys
from context import tml
import tml.learning.character_prediction.rnn_train as train

this_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(this_path, "data")
checkpoints_path = os.path.join(this_path, "checkpoints")
log_path = os.path.join(this_path, "log/1")

text_path = os.path.join(data_path, "THE TEXT") # default

# get path from command line arguments if passed
if len(sys.argv) == 2:
    text_path = os.path.abspath(sys.argv[1])

text_files = os.path.join(text_path, "*.txt") # default src/character_prediction/data/THE TEXT/*.txt

# create directories if they do not exist
if not os.path.exists(checkpoints_path):
    os.mkdir(checkpoints_path)

print("TRAINING WILL START ...")
train.train(text_files, checkpoints_path, log_path)
