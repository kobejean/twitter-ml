#!/usr/bin/env python3
"""
               - Character Recurrent Neural Net Player -

PROGRAMMED BY: Jean Flaherty
DATE: 07/15/2017
DESCRIPTION:
    Prints text that the character recurrent nueral net generates.
"""

import os
import tensorflow as tf
from context import tml
from tml.learning.character_prediction.preprocessing import ALPHASIZE
import tml.learning.character_prediction.rnn_play as play

this_path = os.path.abspath(os.path.dirname(__file__))
checkpoints_path = os.path.join(this_path, "checkpoints")
latest_checkpoint_path = tf.train.latest_checkpoint(checkpoints_path)
meta_graph_path = latest_checkpoint_path + ".meta"
author = latest_checkpoint_path

print("PLAYING WILL START ...")
play.play(meta_graph_path, author, count=1000000000, topn=ALPHASIZE)
