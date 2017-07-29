from context import tml
from tml.learning.word_embeddings.preprocessing import read_vocabulary
import getopt, sys, os

import tensorflow as tf
from tensorflow.contrib.learn import KMeansClustering

def main(k, graph_path, vocab_path, vocab_size=10000, word_vector_size=200, relative_tolerance=1e-20):
    vocab = read_vocabulary(vocab_path)
    # print(vocab)

    # Create some variables.

    word_embeddings = tf.Variable(tf.zeros(shape=[vocab_size,word_vector_size]), name="Word_Embeddings")


    # Add ops to save and restore all the variables.

    # Later, launch the model, use the saver to restore variables from disk, and
    # do some work with the model.
    with tf.Session() as sess:
        saver = tf.train.Saver({"H1_Layer/H1_Word_Embeddings": word_embeddings})
        saver.restore(sess, graph_path)

        restored_word_embeddings = sess.run(word_embeddings)


    def input_fn():
        return tf.constant(restored_word_embeddings, tf.float32), None

    tf.logging.set_verbosity(tf.logging.DEBUG)
    kmeans = KMeansClustering(
        num_clusters=k,
        relative_tolerance=relative_tolerance,
        # kmeans_plus_plus_num_retries=5
        )
    _ = kmeans.fit(input_fn=input_fn)

    clusters = kmeans.clusters()
    assignments = list(kmeans.predict_cluster_idx(input_fn=input_fn))

    clustered_words = {}
    for i, idx in enumerate(assignments):
        if not idx in clustered_words.keys():
            clustered_words[idx] = []
        clustered_words[idx].append(vocab[i])

    # clustered_words = {(idx, vocab[i]) for i, idx in enumerate(assignments)}
    # clustered_words = sorted(clustered_words)
    # for idx, word in clustered_words:
    #     print(idx, "\t", word)
    while True:
        search = int(input("SEARCH: "))
        print(clustered_words[search])
        # for word in clustered_words[search]:
        #     print(word)



if __name__ == "__main__":
    options = {}
    usage_str = "usage: python3 kmeans.py [options]"
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hk:g:v:")
    except (getopt.GetoptError):
        print(usage_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage_str + "\n" +
            """
            options:
            -h                      show help menu
            -k <k>                  the number of means
            -g <graph_path>         the checkpoint date the nn should restore from
            -v <vocab_path>         the path to the vocabulary file
            """)
            sys.exit()
        elif opt == "-k":
            options["k"] = int(arg)
        elif opt == "-g":
            options["graph_path"] = os.path.abspath(arg)
        elif opt == "-v":
            options["vocab_path"] = os.path.abspath(arg)


    main(**options)
