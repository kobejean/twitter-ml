#!/usr/bin/env python3
"""
               - Random or Not Word Embeddings Neural Net -

PROGRAMMED BY: Jean Flaherty
DATE: 07/15/2017
DESCRIPTION:
    Runs a neural net that learns word embeddings by trying to guess whether
    or not the word in the middle is random or not.

    The path to the data package can be passed as an argumant in
    command line like this:

        $ python3 random_or_not_word_embedding_nn.py path/to/data_package_dir/
"""

import os, sys
from context import tml
from tml.learning.word_embeddings.random_or_not_nn import *

TEST_MODE = False
# paths
package_name = "THE STREAM"                if not TEST_MODE else "TEST THE STREAM"
this_path = os.path.abspath(os.path.dirname(__file__))
# parent_path = os.path.abspath(os.path.join(this_path, os.pardir))
data_path = os.path.join(this_path, "data")

data_package_path = os.path.join(data_path, package_name) # default

# get path from command line arguments if passed
if len(sys.argv) == 2:
    data_package_path = os.path.abspath(sys.argv[1])

log_path = os.path.join(this_path, "log/1/")
# meta_graph_path = os.path.join(log_path, "b_100-l_0.003-w_10000-h1_200-h2_100-s_5-1498537758.ckpt")
# meta_graph_path = tf.train.latest_checkpoint(log_path)
meta_graph_path = None

print("TRAINGING WILL START...")
run_random_or_not_nn(data_package_path, log_path, meta_graph_path)
