# encoding: UTF-8
# Copyright 2017 Google.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf
from tensorflow.contrib import layers
from tensorflow.contrib import rnn  # rnn stuff temporarily in contrib, moving back to code in TF 1.1
import os, sys, getopt, time, math
import numpy as np
from . import preprocessing as txt
tf.set_random_seed(0)

# model parameters
#
# Usage:
#   Training only:
#         Leave all the parameters as they are
#         Disable validation to run a bit faster (set validation=False below)
#         You can follow progress in Tensorboard: tensorboard --log-dir=log
#   Training and experimentation (default):
#         Keep validation enabled
#         You can now play with the parameters anf follow the effects in Tensorboard
#         A good choice of parameters ensures that the testing and validation curves stay close
#         To see the curves drift apart ("overfitting") try to use an insufficient amount of
#         training data (shakedir = "shakespeare/t*.txt" for example)
#
ALPHASIZE = txt.ALPHASIZE


def train(text_files, log_path, checkpoints_path,
          nb_epochs = 1,
          nb_batches = None,

          sequence_size = 30,
          batch_size = 100,
          internal_size = 512,
          n_layers = 3,
          learning_rate = 0.001,  # fixed learning rate
          dropout_pkeep = 1.0    # no dropout
          ):
    print("TEXT FILES:", text_files)
    print("LOG PATH:", log_path)
    print("CHECKPOINTS PATH:", checkpoints_path)
    testlen, vali_len, codetext, vali_text, bookranges = txt.read_data_files(text_files, validation=True, nb_epochs=nb_epochs)
    
    # display some stats on the data
    epoch_size = testlen // (batch_size * sequence_size)
    txt.print_data_stats(testlen, vali_len, epoch_size)

    #
    # the model (see FAQ in README.md)
    #
    lr = tf.placeholder(tf.float32, name='lr')  # learning rate
    pkeep = tf.placeholder(tf.float32, name='pkeep')  # dropout parameter
    dynamic_batch_size = tf.placeholder(tf.int32, name='dynamic_batch_size')

    # inputs
    X = tf.placeholder(tf.uint8, [None, None], name='X')    # [ batch_size, sequence_size ]
    Xo = tf.one_hot(X, ALPHASIZE, 1.0, 0.0)                 # [ batch_size, sequence_size, ALPHASIZE ]
    # expected outputs = same sequence shifted by 1 since we are trying to predict the next character
    Y_ = tf.placeholder(tf.uint8, [None, None], name='Y_')  # [ batch_size, sequence_size ]
    Yo_ = tf.one_hot(Y_, ALPHASIZE, 1.0, 0.0)               # [ batch_size, sequence_size, ALPHASIZE ]
    # input state
    Hin = tf.placeholder(tf.float32, [None, internal_size*n_layers], name='Hin')  # [ batch_size, internal_size * n_layers]

    # using a n_layers=3 layers of GRU cells, unrolled sequence_size=30 times
    # dynamic_rnn infers sequence_size from the size of the inputs Xo
    gruCellsWithDropout = [rnn.DropoutWrapper(rnn.GRUCell(internal_size), input_keep_prob=pkeep) for _ in range(n_layers)]
    multicell = rnn.MultiRNNCell(gruCellsWithDropout, state_is_tuple=False)
    multicell = rnn.DropoutWrapper(multicell, output_keep_prob=pkeep)
    Yr, H = tf.nn.dynamic_rnn(multicell, Xo, dtype=tf.float32, initial_state=Hin)
    # Yr: [ batch_size, sequence_size, internal_size ]
    # H:  [ batch_size, internal_size*n_layers ] # this is the last state in the sequence

    H = tf.identity(H, name='H')  # just to give it a name

    # Softmax layer implementation:
    # Flatten the first two dimension of the output [ batch_size, sequence_size, ALPHASIZE ] => [ batch_size x sequence_size, ALPHASIZE ]
    # then apply softmax readout layer. This way, the weights and biases are shared across unrolled time steps.
    # From the readout point of view, a value coming from a cell or a minibatch is the same thing

    Yflat = tf.reshape(Yr, [-1, internal_size])    # [ batch_size x sequence_size, internal_size ]
    Ylogits = layers.linear(Yflat, ALPHASIZE)     # [ batch_size x sequence_size, ALPHASIZE ]
    Yflat_ = tf.reshape(Yo_, [-1, ALPHASIZE])     # [ batch_size x sequence_size, ALPHASIZE ]
    loss = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Yflat_)  # [ batch_size x sequence_size ]
    loss = tf.reshape(loss, [dynamic_batch_size, -1])      # [ batch_size, sequence_size ]
    Yo = tf.nn.softmax(Ylogits, name='Yo')        # [ batch_size x sequence_size, ALPHASIZE ]
    Y = tf.argmax(Yo, 1)                          # [ batch_size x sequence_size ]
    Y = tf.reshape(Y, [dynamic_batch_size, -1], name="Y")  # [ batch_size, sequence_size ]
    train_step = tf.train.AdamOptimizer(lr).minimize(loss)

    # stats for display
    seqloss = tf.reduce_mean(loss, 1)
    batchloss = tf.reduce_mean(seqloss)
    accuracy = tf.reduce_mean(tf.cast(tf.equal(Y_, tf.cast(Y, tf.uint8)), tf.float32))
    loss_summary = tf.summary.scalar("batch_loss", batchloss)
    acc_summary = tf.summary.scalar("batch_accuracy", accuracy)
    summaries = tf.summary.merge([loss_summary, acc_summary])

    # Init Tensorboard stuff. This will save Tensorboard information into a different
    # folder at each run named 'log/<timestamp>/'. Two sets of data are saved so that
    # you can compare training and validation curves visually in Tensorboard.
    timestamp = str(math.trunc(time.time()))
    summary_path = os.path.join(log_path, timestamp + "-training")
    summary_writer = tf.summary.FileWriter(summary_path)
    validation_path = os.path.join(log_path, timestamp + "-validation")
    validation_writer = tf.summary.FileWriter(validation_path)

    # Init for saving models. They will be saved into a directory named 'checkpoints'.
    # Only the last checkpoint is kept.
    if not os.path.exists(checkpoints_path):
        os.mkdir(checkpoints_path)
    saver = tf.train.Saver(max_to_keep=1)

    # for display: init the progress bar
    DISPLAY_FREQ = 50
    _50_BATCHES = DISPLAY_FREQ * batch_size * sequence_size
    progress = txt.Progress(DISPLAY_FREQ, size=111+2, msg="Training on next "+str(DISPLAY_FREQ)+" batches")

    # init
    istate = np.zeros([batch_size, internal_size*n_layers])  # initial zero input state
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    step = 0

    # create validation minibatch
    vali_sequence_size = 1*1024  # Sequence length for validation. State will be wrong at the start of each sequence.
    vali_batch_size = vali_len // vali_sequence_size
    vali_x, vali_y, _ = next(txt.rnn_minibatch_sequencer(vali_text, epoch_size, vali_batch_size, vali_sequence_size, 1))  # all data in 1 batch


    # training loop
    for x, y_, epoch in txt.rnn_minibatch_sequencer(codetext, epoch_size, batch_size, sequence_size, nb_epochs=nb_epochs, nb_batches=nb_batches):

        # train on one minibatch
        feed_dict = {X: x, Y_: y_, Hin: istate, lr: learning_rate, pkeep: dropout_pkeep, dynamic_batch_size: batch_size}
        _, y, ostate, smm = sess.run([train_step, Y, H, summaries], feed_dict=feed_dict)

        # save training data for Tensorboard
        summary_writer.add_summary(smm, step)

        # display a visual validation of progress (every 50 batches)
        if step % _50_BATCHES == 0:
            feed_dict = {X: x, Y_: y_, Hin: istate, pkeep: 1.0, dynamic_batch_size: batch_size}  # no dropout for validation
            y, l, bl, acc = sess.run([Y, seqloss, batchloss, accuracy], feed_dict=feed_dict)
            txt.print_learning_learned_comparison(x, y, l, bookranges, bl, acc, epoch_size, step, epoch)

        # run a validation step every 50 batches
        # The validation text should be a single sequence but that's too slow (1s per 1024 chars!),
        # so we cut it up and batch the pieces (slightly inaccurate)
        # tested: validating with 5K sequences instead of 1K is only slightly more accurate, but a lot slower.
        if step % _50_BATCHES == 0 and len(vali_text) > 0:
            txt.print_validation_header(testlen, bookranges)
            vali_nullstate = np.zeros([vali_batch_size, internal_size*n_layers])
            feed_dict = {X: vali_x, Y_: vali_y, Hin: vali_nullstate, pkeep: 1.0,  # no dropout for validation
                         dynamic_batch_size: vali_batch_size}
            ls, acc, smm = sess.run([batchloss, accuracy, summaries], feed_dict=feed_dict)
            txt.print_validation_stats(ls, acc)
            # save validation data for Tensorboard
            validation_writer.add_summary(smm, step)

        # display a short text generated with the current weights and biases (every 150 batches)
        if step // 3 % _50_BATCHES == 0:
            txt.print_text_generation_header()
            ry = np.array([[txt.convert_from_alphabet(ord("\n"))]])
            rh = np.zeros([1, internal_size * n_layers])
            for k in range(1000):
                ryo, rh = sess.run([Yo, H], feed_dict={X: ry, pkeep: 1.0, Hin: rh, dynamic_batch_size: 1})
                rc = txt.sample_from_probabilities(ryo, topn=10 if epoch <= 1 else 2)
                print(chr(txt.convert_to_alphabet(rc)), end="")
                ry = np.array([[rc]])
            txt.print_text_generation_footer()

        # save a checkpoint (every 500 batches)
        if step // 10 % _50_BATCHES == 0:
            save_path = os.path.join(checkpoints_path, 'rnn_train_' + timestamp)
            saver.save(sess, save_path, global_step=step)

        # display progress bar
        progress.step(reset=step % _50_BATCHES == 0)

        # loop state around
        istate = ostate
        step += batch_size * sequence_size

    # all runs: sequence_size = 30, batch_size = 100, ALPHASIZE = 98, internal_size = 512, n_layers = 3
    # run 1477669632 decaying learning rate 0.001-0.0001-1e7 dropout 0.5: not good
    # run 1477670023 lr=0.001 no dropout: very good

    # Tensorflow runs:
    # 1485434262
    #   trained on shakespeare/t*.txt only. Validation on 1K sequences
    #   validation loss goes up from step 5M
    # 1485436038
    #   trained on shakespeare/t*.txt only. Validation on 5K sequences
    #   On 5K sequences validation accuracy is slightly higher and loss slightly lower
    #   => sequence breaks do introduce inaccuracies but the effect is small
    # 1485437956
    #   Trained on shakespeare/*.txt only. Validation on 1K sequences
    #   On this much larger dataset, validation loss still decreasing after 6 epochs (step 35M)
    # 1485440785
    #   Dropout = 0.5 - Trained on shakespeare/*.txt only. Validation on 1K sequences
    #   Much worse than before. Not very surprising since overfitting was not apparent
    #   on the validation curves before so there is nothing for dropout to fix.

if __name__ == "__main__":
    text_files = None
    log_path = None
    checkpoints_path = None

    options = {}
    usage_str = "usage: python3 -m tml.learning.character_prediction.rnn_train <text_files> <log_path> <checkpoints_path> [options]"
    try:
        text_files = sys.argv[1]
        log_path = sys.argv[2]
        checkpoints_path = sys.argv[3]
        opts, args = getopt.getopt(sys.argv[4:],"he:b:",["bs=","ss=","is=","nl=","lr=","dp="])
    except (IndexError, getopt.GetoptError):
        print(usage_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage_str + "\n" +
            """
            options:
            -h                      show help menu
            -e <epochs>             number of epochs the nn should run
            -b <batches>            number of batches the nn should run

            --bs <batch_size>       batch size
            --ss <seq_size>         sub sequence size
            --is <internal_size>    number of neurons per hidden layer
            --nl <n_layers>         number of hidden layers
            --lr <learning_rate>    learning rate
            --dp <dropout_pkeep>    dropout probability
            """)
            sys.exit()
        elif opt == "-e":
            options["nb_epochs"] = int(arg)
        elif opt == "-b":
            options["nb_batches"] = int(arg)

        elif opt == "--bs":
            options["batch_size"] = int(arg)
        elif opt == "--ss":
            options["seq_size"] = int(arg)
        elif opt == "--is":
            options["internal_size"] = int(arg)
        elif opt == "--nl":
            options["n_layers"] = int(arg)
        elif opt == "--lr":
            options["learning_rate"] = int(arg)
        elif opt == "--dp":
            options["dropout_pkeep"] = float(arg)


    train(text_files, log_path, checkpoints_path, **options)
