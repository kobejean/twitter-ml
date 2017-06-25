import tensorflow as tf
import numpy as np

import os, random, time, math
from itertools import islice
from context import tml
from tml.utils.ansi import ANSI
from tml.utils.text_preprocessing import *

TEST_MODE = True

file_name = input("FILE NAME OF TXT FILE:") if not TEST_MODE else "THE STREAM.csv"
# num_words = int(input("NUM WORDS:"))        if not TEST_MODE else 10000
# words_per_training_case = 3
BATCH_SIZE = 1000
WORD_SIZE = 10000
H1_SIZE = 1000
H2_SIZE = 1000
SEQ_SIZE = 5
# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, file_name)
sequence_path = os.path.join(data_path, "SEQUENCE " + file_name)
vocab_path = os.path.join(data_path, "VOCAB " + file_name)

timestamp = str(math.trunc(time.time()))
summary_writer = tf.summary.FileWriter("log/1/ws{}-h1{}-h2{}-seq{}-{}-training"\
    .format(WORD_SIZE,H1_SIZE,H2_SIZE,SEQ_SIZE, timestamp))
# validation_writer = tf.summary.FileWriter("log/1/" + timestamp + "-validation")

def batch_generator(seqs_reader, n):
    i = iter(seqs_reader)

    indices = np.array(list(islice(i, n)))
    size = indices.shape[0]
    Y_ = [[1,0]] * size # all default true
    for j in range(size):
        if bool(random.getrandbits(1)):
            Y_[j] = [0,1] # set y to false
            rand_i = random.randint(1, WORD_SIZE-1)
            rand_i = WORD_SIZE if rand_i == indices[j][SEQ_SIZE//2] else rand_i
            indices[j][SEQ_SIZE//2] = rand_i
    Y_ = np.array(Y_)

    while indices.size > 0:
        yield {"indices":indices, "Y_":Y_, "n":size}

        indices = np.array(list(islice(i, n)))
        size = indices.shape[0]
        Y_ = [[1,0]] * size # all default true
        for j in range(size):
            if bool(random.getrandbits(1)):
                Y_[j] = [0,1] # set y to false
                rand_i = random.randint(1, WORD_SIZE-1)
                rand_i = WORD_SIZE if rand_i == indices[j][SEQ_SIZE//2] else rand_i
                indices[j][SEQ_SIZE//2] = rand_i
        Y_ = np.array(Y_)


# read sequence and print text
with open(sequence_path, "r") as file:
    seqs_reader = sequences_reader_from_file_reader(file)
    vocab = read_vocab(vocab_path)
    texts_reader = sequences_to_texts(seqs_reader, vocab)

    indices = tf.placeholder(
        tf.int32,
        shape=[None, SEQ_SIZE],
        name="indices"
    ) # [BATCH_SIZE, SEQ_SIZE]
    Xo = tf.one_hot(
        indices,
        WORD_SIZE,
        dtype=tf.float32,
        name="inputs"
    ) # [BATCH_SIZE, SEQ_SIZE, WORD_SIZE]

    # correct answers will go here
    Y_ = tf.placeholder(tf.float32, [None, 2])

    n = tf.placeholder(tf.int32)

    W1 = tf.Variable(tf.truncated_normal([WORD_SIZE, H1_SIZE], stddev=0.1))  #
    B1 = tf.Variable(tf.zeros([H1_SIZE]))
    W2 = tf.Variable(tf.truncated_normal([SEQ_SIZE * H1_SIZE, H2_SIZE], stddev=0.1))  #
    B2 = tf.Variable(tf.zeros([H1_SIZE]))
    W3 = tf.Variable(tf.truncated_normal([H2_SIZE, 2], stddev=0.1))
    B3 = tf.Variable(tf.zeros([2]))

    XX = tf.reshape(Xo, shape=[n * SEQ_SIZE, WORD_SIZE])
    YY1 = tf.nn.relu(tf.matmul(XX, W1) + B1)
    Y1 = tf.reshape(YY1, shape=[n, SEQ_SIZE * H1_SIZE])
    Y2 = tf.nn.relu(tf.matmul(Y1, W2) + B2)

    Ylogits = tf.matmul(Y2, W3) + B3
    Y = tf.nn.softmax(Ylogits)

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_)
    cross_entropy = tf.reduce_mean(cross_entropy) * tf.to_float(n)

    # accuracy of the trained model, between 0 (worst) and 1 (best)
    correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    loss_summary = tf.summary.scalar("batch_loss", cross_entropy)
    acc_summary = tf.summary.scalar("batch_accuracy", accuracy)
    summaries = tf.summary.merge([loss_summary, acc_summary])

    # training step, learning rate = 0.003
    learning_rate = 0.003
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        for i, batch in enumerate(batch_generator(seqs_reader, BATCH_SIZE)):
            feed_dict = {
                indices: batch["indices"],
                Y_: batch["Y_"],
                n: batch["n"]}

            a, c, smm = sess.run([accuracy, cross_entropy, summaries], feed_dict=feed_dict)
            summary_writer.add_summary(smm, i * BATCH_SIZE + batch["n"])
            print("BATCH #" + str(i) + ": accuracy:" + str(a) + " loss: " + str(c))

            sess.run(train_step, feed_dict=feed_dict)
            # for i,x in enumerate(xn):
            #     print("X{}:{}".format(i,x))
            # print("X{}:{}".format(0,xn[0]))
            # print("X{}:{}".format(1,xn[1]))
            # print("X{}:{}".format(2,xn[2]))
