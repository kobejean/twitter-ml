import os
from context import tml
import tml.learning.character_prediction.rnn_train as train

this_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(this_path, "data")
checkpoints_path = os.path.join(this_path, "checkpoints")
log_path = os.path.join(this_path, "log/1")
text_path = os.path.join(data_path, "THE TEXT")
text_files = os.path.join(text_path, "*.txt") # data/THE TEXT/*.txt

print("TRAINING WILL START ...")
train.train(text_files, checkpoints_path, log_path)
