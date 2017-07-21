#!/usr/bin/env python3
"""
                           - Create Data Package -

PROGRAMMED BY: Jean Flaherty
DATE: 07/20/2017
DESCRIPTION:
    A script that reads from a text file and generates a preprocessed data
    package for word based natural language processing. Files include:

        VOCABULARY.tsv    - A table of word indices to word strings.
        PROBABILITIES.tsv - A table of word indices to probabilities based of
                            of their frequencies.
        SEQUENCES.tsv     - A lists of sequences of word indices.

    These files are written to src/word_embeddings/data/{basename}/

    The path to the original text file can be passed as an argumant in
    command line like this:

        $ python3 create_data_package.py path/to/text_file.txt
"""
import os, sys, getopt

from .preprocessing import *
from ...utils.generators import print_generator

def create_data_package(text_path, package_path, vocabulary_size=10000):
    import keras
    from keras.preprocessing.text import Tokenizer
    # paths
    sequence_path = os.path.join(package_path, SEQUENCE_FILENAME)
    vocab_path = os.path.join(package_path, VOCABULARY_FILENAME)
    probs_path = os.path.join(package_path, PROBABILITIES_FILENAME)

    # read txt file
    with open(text_path, "r") as file:
        texts = (line.rstrip('\n') for line in file)
        texts = print_generator("TEXT:", texts, 100, "\r")

        print("TOKENIZING...")
        # keras text preprocessing
        tk = Tokenizer(
            num_words=vocabulary_size,
            filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
            lower=True,
            split=' ',
            char_level=False
        )
        tk.fit_on_texts(texts)

    with open(text_path, "r") as file:
        texts = (line.rstrip('\n') for line in file)
        texts = print_generator("TEXT:", texts, 100, "\r")

        # create dicts
        print("CREATING VOCABULARY...")
        vocab = {v-1: k for k,v in tk.word_index.items()}
        # for normalizing probability distribution so they add up to 1
        print("CREATING PROBABILITIES...")
        word_count_sum = sum(sorted([v for k,v in tk.word_counts.items()], reverse=True)[:vocabulary_size])
        probs = dict(sorted([(tk.word_index[k]-1, float(v) / float(word_count_sum)) \
                        for k,v in tk.word_counts.items()])[:vocabulary_size])
        print("CREATING SEQUENCES...")
        # i - 1 so that index z
        text_seq = ([i-1 for i in seq] for seq in tk.texts_to_sequences(texts))
        text_seq = print_generator("SEQUENCE:", text_seq, 100, "\r")

        # write files
        print("WRITING SEQUENCES...")
        write_sequences(text_seq, sequence_path)
        print("WRITING VOCABULARY...")
        write_vocabulary(vocab, vocab_path, vocabulary_size)
        print("WRITING PROBABILITIES...")
        write_probabilities(probs, probs_path)
        print("DONE!")

if __name__ == "__main__":
    text_file_path = None
    data_package_path = None
    options = {}
    usage_str = "usage: python3 -m tml.learning.word_embeddings.create_data_package <text_file_path> <data_package_dir> [options]"
    try:
        text_file_path    = os.path.abspath(sys.argv[1])
        data_package_path = os.path.abspath(sys.argv[2])
        opts, args = getopt.getopt(sys.argv[3:],"h",["ws="])
    except (IndexError, getopt.GetoptError):
        print(usage_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage_str + "\n" +
            """
            options:
            -h                      show help menu
            --ws <vocab_size>       vocabulary/word size (10000 by default)
            """)
            sys.exit()
        elif opt == "-ws":
            options["vocabulary_size"] = int(arg)

    if not os.path.exists(data_package_path):
        os.makedirs(data_package_path)

    print("READ TEXT PATH:", text_file_path)
    print("WRITE DATA PACKAGE PATH:", data_package_path)

    create_data_package(text_file_path, data_package_path, **options)
