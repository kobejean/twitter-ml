"""
                        - Random or Not Neural Net -

PROGRAMMED BY: Jean Flaherty
DATE: 07/20/2017
DESCRIPTION:
    Contains a function that constructs and runs a neural net that learns word
    embeddings by trying to guess whether or not the word in the middle is
    random or not.
FUNCTIONS:
    run_random_or_not_nn(data_package_path, log_path, meta_graph_path=None)
"""

import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import os, random, time, math, sys, getopt
from itertools import islice, count as itercount

from ...utils.ansi import ANSI
from .preprocessing import read_data_package, random_word_index, VOCABULARY_FILENAME

def run_random_or_not_nn(data_package_path, log_path = None, meta_graph_path = None, epochs = None, batches = None,
                         val_period = 200,  # how often to validate in batches per validation
                         cp_period = 500,   # how often to save checkpoints in batches per validation
                         # nn hyper params
                         batch_size = 100,      # number of training cases per batch
                         val_size = 50,         # validation set size in batches
                         vocab_size = 10000,    # vocabulary size
                         seq_size = 5,          # sub sequence size
                         h1_size = 200,         # 1st hidden layer size
                         h2_size = 100,         # 2nd hidden layer size
                         learning_rate = 0.003, # learning rate
                         ):
    """
    DESCRIPTION:
        Constructs and runs a neural net that learns word embeddings by trying
        to guess whether or not the word in the middle is random or not.

    ARGUMENTS:
        data_package_path   The path to the data package
        log_path            The path to the directory for logging
        meta_graph_path     (optional) If specified will restore the session
        from this file path
        epochs              (optional) The number of epochs the nn should run
        batches             (optional) The number of batches the nn should run

        val_period          (optional) How often to test validation sets in
                            batches per validation
        cp_period           (optional) How often to save checkpoints in
                            batches per checkpoint

        batch_size          (optional) The number of training cases per batch
        test_size           (optional) The test set size in batches
        val_size            (optional) The validation set size in batches
        vocab_size          (optional) The vocabulary size
        seq_size            (optional) The sub sequence size
        h1_size             (optional) The 1st hidden layer size
        h2_size             (optional) The 2nd hidden layer size
        learning_rate       (optional) The learning rate
    """
    RESTORE_SESSION = (meta_graph_path != None)

    # paths
    vocab_path = os.path.join(data_package_path, VOCABULARY_FILENAME)
    log_path = log_path if log_path else os.path.join(data_package_path, "log")
    print("LOG DIRECTORY: {}".format(log_path))

    epochscount = range(epochs) if epochs != None else itercount()

    timestamp = str(math.trunc(time.time()))
    PREFIX = "b_{}-l_{}-w_{}-h1_{}-h2_{}-s_{}-{}"\
        .format(batch_size,learning_rate,vocab_size,h1_size,h2_size,seq_size, timestamp)

################################################################################
#                                                                              #
#                         NEURAL NET CODE STARTS HERE                          #
#                                                                              #
################################################################################


    with tf.name_scope('Input_Layer') as scope:
        # current batch size
        n = tf.placeholder(tf.int32)
        # [n, seq_size]
        indices = tf.placeholder(tf.int32, shape=[None, seq_size], name="Indices")
        # [n, 2] correct answers will go here. 2 classifications T/F
        Y_ = tf.placeholder(tf.float32, [None, 2])
        # [n * seq_size, vocab_size]
        flat_indices = tf.reshape(indices, shape=[n * seq_size], name="Reshaped_Indices")

    with tf.name_scope('H1_Layer') as scope:
        # [vocab_size, h1_size]
        word_embeddings = tf.Variable(tf.random_uniform([vocab_size, h1_size], -1.0, 1.0), name="H1_Word_Embeddings")
        # [n, seq_size * h1_size]
        Y1 = tf.nn.embedding_lookup(word_embeddings, flat_indices, name="H1_Activations")
        Y1 = tf.reshape(Y1, shape=[n, seq_size * h1_size], name="Reshaped_H1_Activations")

    with tf.name_scope('H2_Layer') as scope:
        # [seq_size * h1_size, h2_size]
        W2 = tf.Variable(tf.truncated_normal([seq_size * h1_size, h2_size], stddev=0.1), name="H2_Weights")
        # [h2_size]
        B2 = tf.Variable(tf.zeros([h2_size]), name="H2_Bias")
        # [n, h2_size]
        Y2 = tf.nn.relu(tf.matmul(Y1, W2) + B2, name="H2_Activations")

    with tf.name_scope('Output_Layer') as scope:
        # [h2_size, 2]
        W3 = tf.Variable(tf.truncated_normal([h2_size, 2], stddev=0.1), name="Output_Weights")
        # [2]
        B3 = tf.Variable(tf.zeros([2]), name="Output_Bias")
        # [n,2]
        Ylogits = tf.matmul(Y2, W3) + B3
        # [n,2]
        Y = tf.nn.softmax(Ylogits, name="Output")

    with tf.name_scope('Stats') as scope:
        # cross entropy (scalar)
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y_, name="Cross_Entropy")
        cross_entropy = tf.reduce_mean(cross_entropy, name="Ave_Cross_Entropy")
        # accuracy of the trained model, between 0 (worst) and 1 (best)
        correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1), name="Accuracy")
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="Ave_Accuracy")

    with tf.name_scope('Training_Step') as scope:
        # training step
        train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)


    print("STARTING SESSION...")
    with tf.Session() as sess:
        # tensorboard stuff
        train_path = os.path.join(log_path, "{}-training".format(PREFIX))
        val_path = os.path.join(log_path, "{}-validation".format(PREFIX))
        summary_writer = tf.summary.FileWriter(train_path)
        validation_writer = tf.summary.FileWriter(val_path, sess.graph)

        # histograms
        word_embeddings_summary = tf.summary.histogram("word_embeddings", word_embeddings)
        W2_summary = tf.summary.histogram("W2", W2)
        B2_summary = tf.summary.histogram("B2", B2)
        W3_summary = tf.summary.histogram("W3", W3)
        B3_summary = tf.summary.histogram("B3", B3)

        # scalars
        loss_summary = tf.summary.scalar("batch_loss", cross_entropy)
        acc_summary = tf.summary.scalar("batch_accuracy", accuracy)

        # test and validation summaries
        summaries = tf.summary.merge([loss_summary, acc_summary])
        val_summaries = tf.summary.merge([
            loss_summary, acc_summary, word_embeddings_summary, W2_summary, B2_summary,
            W3_summary, B3_summary])

        # initialize
        init = tf.global_variables_initializer()

        # projector
        config = projector.ProjectorConfig()

        # You can add multiple embeddings. Here we add only one.
        embedding = config.embeddings.add()
        embedding.tensor_name = word_embeddings.name
        # Link this tensor to its metadata file (e.g. labels).
        embedding.metadata_path = vocab_path

        # The next line writes a projector_config.pbtxt in the LOG_DIR. TensorBoard will
        # read this file during startup.
        projector.visualize_embeddings(summary_writer, config)
        projector.visualize_embeddings(validation_writer, config)

        saver = tf.train.Saver()
        if RESTORE_SESSION:
            # saver = tf.train.import_meta_graph(meta_graph_path)
            saver.restore(sess, meta_graph_path)
            print("RESTORED:", meta_graph_path)
        else:
            sess.run(init)

        global_step = 0
        batch_count = 0

        for epoch in epochscount:
            with read_data_package(data_package_path) as (seqs_reader, vocab, probs):
                batch_gen = batch_generator(seqs_reader, probs, batch_size, vocab_size, seq_size)
                # create validation sets
                validation_set = [next(batch_gen) for i in range(val_size)]
                validation_set = {  "indices": np.vstack([b["indices"] for b in validation_set]),
                                    "Y_": np.vstack([b["Y_"] for b in validation_set]),
                                    "n": sum([b["n"] for b in validation_set])}

                for i, batch in enumerate(batch_gen):
                    if batches and batch_count >= batches:
                        print("REACHED {} BATCHES".format(batch_count))
                        return
                    global_step += batch["n"]
                    batch_count += 1
                    # validation
                    if i % val_period == 0:
                        feed_dict = {
                            indices: validation_set["indices"],
                            Y_: validation_set["Y_"],
                            n: validation_set["n"]}

                        a, c, smm, y = sess.run([accuracy, cross_entropy, val_summaries, Y], feed_dict=feed_dict)
                        validation_writer.add_summary(smm, global_step)

                        print("OUTPUT SAMPLE:")
                        for j in range(min(validation_set["n"], 50)):
                            seq = validation_set["indices"].tolist()[j]
                            actual_value = validation_set["Y_"].tolist()[j]
                            actual_value = (bool(actual_value[0]) and not bool(actual_value[1])) # T:[1,0] F:[0,1]
                            guess = [round(g) for g in y[j]]
                            guess = (guess[0] > guess[1]) # T:[1,0] F:[0,1]
                            confidence = (float(y[j][0]) if guess else float(y[j][1])) * 100
                            text = ""
                            for k, l in enumerate(seq):
                                text += " " if k > 0 else ""
                                if k == seq_size//2:
                                    text += (ANSI.GREEN if actual_value else ANSI.RED) + vocab[l] + ANSI.ENDC
                                else:
                                    text += vocab[l]
                            print_message = "TEXT: {0:50s} ACTUAL VALUE: {1:6s} GUESS: {2:6s} CONFIDENCE: {3:3.2f}%"\
                                .format(text, str(actual_value), str(guess), confidence)
                            print(print_message)

                        print("VALIDATION: ACCURACY:{0:7.4f} LOSS:{1:7.4f}"\
                                .format(a,c))

                    # forward pass
                    feed_dict = {
                        indices: batch["indices"],
                        Y_: batch["Y_"],
                        n: batch["n"]}

                    a, c, smm = sess.run([accuracy, cross_entropy, summaries], feed_dict=feed_dict)
                    summary_writer.add_summary(smm, global_step)
                    print("EPOCH:{0:3d} BATCH:{1:10d} ACCURACY:{2:8.4f} LOSS:{3:8.4f}"\
                        .format(epoch, i, a, c))

                    # backprop
                    sess.run(train_step, feed_dict=feed_dict)

                    # save checkpoint
                    if i % cp_period == 0:
                        # sess.run(assign_word_embedding)
                        save_path = saver.save(sess, os.path.join(log_path, "{}.ckpt".format(PREFIX)))#, global_step=global_step)
                        print(save_path)


def batch_generator(seqs_reader, probs, n, vocab_size, seq_size):
    """
    DESCRIPTION:
        generates the batch given the sequence reader

    ARGUMENTS:
        seqs_reader     A generator that produces sequences of word indices
        probs           A dictionary of probabilities of ocurance associated with word indices
        n               The desired size of the subsequences
        vocab_size      The vocabulary size
        seq_size        The size of the sub sequences
    """

    i = iter(sub_seqs_gen(seqs_reader, vocab_size, seq_size))
    while True:
        indices = np.array(list(islice(i, n)))
        size = indices.shape[0]
        Y_ = [[1,0]] * size # set all true by default
        for j in range(size):
            if bool(random.getrandbits(1)):
                Y_[j] = [0,1] # set y to false
                # replace middle index with random index
                rand_i = random_word_index(probs, indices[j][seq_size//2])
                indices[j][seq_size//2] = rand_i
        Y_ = np.array(Y_)

        if indices.size > 0:
            yield {"indices":indices, "Y_":Y_, "n":size}
        else: break

def sub_seqs_gen(seqs_reader, vocab_size, seq_size):
    """
    DESCRIPTION:
        generates sub sequences given the sequence reader

    ARGUMENTS:
        seqs_reader     A generator that produces sequences of word indices
        vocab_size      The vocabulary size
        seq_size        The size of the sub sequences
    """
    for seq in seqs_reader:
        # make sure the sequence is long enough to make a sub sequence of size seq_size
        if len(seq) >= seq_size:
            # loop through sub sequences
            for i in range(len(seq) - seq_size + 1):
                sub_seq = seq[i : i + seq_size]
                assert len(sub_seq) == seq_size, "not len(sub_seq) == seq_size"
                # make sure all words are in vocabulary of size vocab_size before appending
                if all([wi < vocab_size for wi in sub_seq]):
                    yield sub_seq

if __name__ == "__main__":
    data_package_path = None
    options = {}
    usage_str = "usage: python3 -m tml.learning.word_embeddings.random_or_not_nn <data_package_dir> [options]"
    try:
        data_package_path = sys.argv[1]
        opts, args = getopt.getopt(sys.argv[2:],"hl:g:e:b:",["vp=","cp=","bs=","vs=","ws=","ss=","h1=","h2=","lr="])
    except (IndexError, getopt.GetoptError):
        print(usage_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage_str + "\n" +
            """
            options:
            -h                      show help menu
            -l <log_dir>            the path to the log directory
            -g <graph_path>         the checkpoint date the nn should restore from
            -e <epochs>             number of epochs the nn should run
            -b <batches>            number of batches the nn should run

            -v <val_period>         how often to validate in batches per validation
            -c <cp_period>          how often to save checkpoints in number of batches per checkpoint

            --bs <batch_size>       batch size
            --vs <val_size>         validation set size in number of batches
            --ws <vocab_size>       vocabulary/word size
            --ss <seq_size>         sub sequence size
            --h1 <h1_size>          1st hidden layer size
            --h2 <h2_size>          2nd hidden layer size
            --lr <learning_rate>    learning rate
            """)
            sys.exit()
        elif opt == "-l":
            options["log_path"] = os.path.abspath(arg)
        elif opt == "-g":
            options["meta_graph_path"] = os.path.abspath(arg)
        elif opt == "-e":
            options["epochs"] = int(arg)
        elif opt == "-b":
            options["batches"] = int(arg)


        elif opt == "-v":
            options["val_period"] = int(arg)
        elif opt == "-c":
            options["cp_period"] = int(arg)

        elif opt == "--bs":
            options["batch_size"] = int(arg)
        elif opt == "--vs":
            options["val_size"] = int(arg)
        elif opt == "--ws":
            options["vocab_size"] = int(arg)
        elif opt == "--ss":
            options["seq_size"] = int(arg)
        elif opt == "--h1":
            options["h1_size"] = int(arg)
        elif opt == "--h2":
            options["h2_size"] = int(arg)
        elif opt == "--lr":
            options["learning_rate"] = int(arg)

    run_random_or_not_nn(data_package_path, **options)
