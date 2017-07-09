import os
from context import tml
import tml.learning.character_prediction.rnn_play as play

this_path = os.path.abspath(os.path.dirname(__file__))
checkpoints_path = os.path.join(this_path, "checkpoints")
latest_checkpoint_path = tf.train.latest_checkpoint(checkpoints_path)
meta_graph_path = latest_checkpoint_path + ".meta"
author = latest_checkpoint_path

print("PLAYING WILL START ...")
play.play(meta_graph_path, author, count=1000000000, topn=ALPHASIZE)
