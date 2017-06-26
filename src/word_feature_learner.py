import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector

import os, random, time, math
from itertools import islice
from context import tml
from tml.utils.ansi import ANSI
from tml.utils.text_preprocessing import *

TEST_MODE = True


BATCH_SIZE = 100
WORD_SIZE = 10000
SEQ_SIZE = 11
H1_SIZE = 200
H2_SIZE = 100#200 * SEQ_SIZE
LR = 0.003 # learning rate
VAL_PERIOD = 50
CHECKPOINT_PERIOD = 100

# paths
file_name = "THE STREAM"                #if not TEST_MODE else "TEST THE STREAM"
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "THE STREAM.csv")
sequence_path = os.path.join(data_path, file_name + " SEQUENCE.csv")
vocab_path = os.path.join(data_path, file_name + " VOCAB.csv")
vocab_tsv_path = os.path.join(data_path, file_name + " VOCAB.tsv ")
probs_path = os.path.join(data_path, file_name + " PROBS.csv")
log_path = os.path.join(abs_path, "log/4/")

timestamp = str(math.trunc(time.time()))
PREFIX = "bs_{}-lr_{}-ws_{}-h1_{}-h2_{}-seq_{}-{}"\
    .format(BATCH_SIZE,LR,WORD_SIZE,H1_SIZE,H2_SIZE,SEQ_SIZE, timestamp)

# generates the batch given the sequence reader
def batch_generator(seqs_reader, probs, n):
    i = iter(seqs_reader)
    while True:
        indices = np.array(list(islice(i, n)))
        size = indices.shape[0]
        Y_ = [[1,0]] * size # all default true
        for j in range(size):
            if bool(random.getrandbits(1)):
                Y_[j] = [0,1] # set y to false
                # replace middle index with random index
                rand_i = random_word_index(probs, indices[j][SEQ_SIZE//2])
                indices[j][SEQ_SIZE//2] = rand_i
        Y_ = np.array(Y_)

        if indices.size > 0:
            yield {"indices":indices, "Y_":Y_, "n":size}
        else: break


# read sequence and print text
with open(sequence_path, "r") as file:
    seqs_reader = sequences_reader_from_file_reader(file)
    vocab = read_vocab(vocab_path)
    probs = read_probs(probs_path)
    texts_reader = sequences_to_texts(seqs_reader, vocab)
    batch_gen = batch_generator(seqs_reader, probs, BATCH_SIZE)


    with tf.name_scope('Input_Layer') as scope:
        n = tf.placeholder(tf.int32) # current batch size
        indices = tf.placeholder(tf.int32, shape=[None, SEQ_SIZE],
            name="Indices")                        # [n, SEQ_SIZE]
        Xo = tf.one_hot(indices, WORD_SIZE, dtype=tf.float32,
            name="Inputs")                         # [n, SEQ_SIZE, WORD_SIZE]

        # correct answers will go here
        Y_ = tf.placeholder(tf.float32, [None, 2]) # [n, 2] 2 classifications T/F

        XX = tf.reshape(Xo, shape=[n * SEQ_SIZE, WORD_SIZE], name="Reshaped_Input") # [n * SEQ_SIZE, WORD_SIZE]

    with tf.name_scope('H1_Layer') as scope:
        # [WORD_SIZE, H1_SIZE]
        W1 = tf.Variable(tf.truncated_normal([WORD_SIZE, H1_SIZE], stddev=0.1), name="H1_Weights")
        # [H1_SIZE]
        B1 = tf.Variable(tf.zeros([H1_SIZE]), name="H1_Bias")
        # [n * SEQ_SIZE, H1_SIZE]
        YY1 = tf.nn.relu(tf.matmul(XX, W1) + B1, name="H1_Activations")
        # [n, SEQ_SIZE * H1_SIZE]
        Y1 = tf.reshape(YY1, shape=[n, SEQ_SIZE * H1_SIZE], name="Reshaped_H1_Activations")

    with tf.name_scope('H2_Layer') as scope:
        # [SEQ_SIZE * H1_SIZE, H2_SIZE]
        W2 = tf.Variable(tf.truncated_normal([SEQ_SIZE * H1_SIZE, H2_SIZE], stddev=0.1), name="H2_Weights")
        # [H2_SIZE]
        B2 = tf.Variable(tf.zeros([H2_SIZE]), name="H2_Bias")
        # [n, H2_SIZE]
        Y2 = tf.nn.relu(tf.matmul(Y1, W2) + B2, name="H2_Activations")

    with tf.name_scope('Output_Layer') as scope:
        # [H2_SIZE, 2]
        W3 = tf.Variable(tf.truncated_normal([H2_SIZE, 2], stddev=0.1), name="Output_Weights")
        # [2]
        B3 = tf.Variable(tf.zeros([2]), name="Output_Bias")
        # [n,2]
        Ylogits = tf.matmul(Y2, W3) + B3
        # [n,2]
        Y = tf.nn.softmax(Ylogits, name="Output")

    # cross entropy (scalar)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
    cross_entropy = tf.reduce_mean(cross_entropy)

    # training step
    train_step = tf.train.AdamOptimizer(LR).minimize(cross_entropy)

    # accuracy of the trained model, between 0 (worst) and 1 (best)
    correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


    with tf.Session() as sess:
        # tensorboard stuff
        summary_writer = tf.summary.FileWriter(log_path + "{}-training".format(PREFIX))
        validation_writer = tf.summary.FileWriter(log_path + "{}-validation".format(PREFIX), sess.graph)

        W1_summary = tf.summary.histogram("W1", W1)
        B1_summary = tf.summary.histogram("B1", B1)
        W2_summary = tf.summary.histogram("W2", W2)
        B2_summary = tf.summary.histogram("B2", B2)
        W3_summary = tf.summary.histogram("W3", W3)
        B3_summary = tf.summary.histogram("B3", B3)
        XX_summary = tf.summary.histogram("XX", XX)
        YY1_summary = tf.summary.histogram("YY1", YY1)

        loss_summary = tf.summary.scalar("batch_loss", cross_entropy)
        acc_summary = tf.summary.scalar("batch_accuracy", accuracy)
        summaries = tf.summary.merge([loss_summary, acc_summary])
        val_summaries = tf.summary.merge([
            loss_summary, acc_summary, W1_summary, B1_summary, W2_summary, B2_summary,
            W3_summary, B3_summary, XX_summary, YY1_summary])

        # create test and validation sets
        test_set = [next(batch_gen) for i in range(100)]
        test_set = {"indices": np.vstack([b["indices"] for b in test_set]),
                    "Y_": np.vstack([b["Y_"] for b in test_set]),
                    "n": sum([b["n"] for b in test_set])}
        validation_set = [next(batch_gen) for i in range(50)]
        validation_set = {  "indices": np.vstack([b["indices"] for b in validation_set]),
                            "Y_": np.vstack([b["Y_"] for b in validation_set]),
                            "n": sum([b["n"] for b in validation_set])}

        init = tf.global_variables_initializer()

        config = projector.ProjectorConfig()

        # You can add multiple embeddings. Here we add only one.
        embedding = config.embeddings.add()
        embedding.tensor_name = W1.name
        # Link this tensor to its metadata file (e.g. labels).
        embedding.metadata_path = vocab_tsv_path

        # The next line writes a projector_config.pbtxt in the LOG_DIR. TensorBoard will
        # read this file during startup.
        projector.visualize_embeddings(validation_writer, config)

        saver = tf.train.Saver()

        sess.run(init)


        for i, batch in enumerate(batch_gen):
            if i % VAL_PERIOD == 0:
                feed_dict = {
                    indices: validation_set["indices"],
                    Y_: validation_set["Y_"],
                    n: validation_set["n"]}

                a, c, smm, y = sess.run([accuracy, cross_entropy, val_summaries, Y], feed_dict=feed_dict)
                validation_writer.add_summary(smm, i * BATCH_SIZE)
                print("VALIDATION #" + str(i//VAL_PERIOD) + ": accuracy:" + str(a) + " loss: " + str(c))
                print("OUTPUT:" + str(y))

            feed_dict = {
                indices: batch["indices"],
                Y_: batch["Y_"],
                n: batch["n"]}

            a, c, smm = sess.run([accuracy, cross_entropy, summaries], feed_dict=feed_dict)
            summary_writer.add_summary(smm, i * BATCH_SIZE + batch["n"])
            print("BATCH #" + str(i) + ": accuracy:" + str(a) + " loss: " + str(c))

            sess.run(train_step, feed_dict=feed_dict)

            if i % CHECKPOINT_PERIOD == 0:
                save_path = saver.save(sess, log_path + "{}.ckpt".format(PREFIX))
