import os
from context import tml
from tml.learning.word_embeddings.random_or_not_nn import *

TEST_MODE = False
# paths
package_name = "THE STREAM"                if not TEST_MODE else "TEST THE STREAM"
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
data_package_path = os.path.join(data_path, package_name)
# sequence_path = os.path.join(data_package_path, "SEQUENCE.tsv")
# vocab_path = os.path.join(data_package_path, "VOCAB.tsv")
# vocab_meta_path = os.path.join(data_package_path, "VOCAB META.tsv")
# probs_path = os.path.join(data_package_path, "PROBS.tsv")

log_path = os.path.join(abs_path, "log/1/")
# meta_graph_path = os.path.join(log_path, "b_100-l_0.003-w_10000-h1_200-h2_100-s_5-1498537758.ckpt")
# meta_graph_path = tf.train.latest_checkpoint(log_path)
meta_graph_path = None

run_random_or_not_nn(data_package_path, log_path, meta_graph_path)
