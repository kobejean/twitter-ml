"""
                         - Word Processing -

PROGRAMMED BY: Jean Flaherty
DATE: 07/20/2017
DESCRIPTION:
    A host of word preprocessing functions.

FUNCTIONS:
    write_vocabulary
    read_vocabulary
    write_sequences
    read_sequences
    sequences_reader_from_file_reader
    sequences_to_texts
    write_probabilities
    read_probabilities
    random_word_index
    create_data_package
    read_data_package
"""
import csv, random, os
import numpy as np
from numpy.random import choice
from contextlib import contextmanager
from ...utils.generators import print_generator

SEQUENCE_FILENAME = "SEQUENCES.tsv"
VOCABULARY_FILENAME = "VOCABULARY.tsv"
PROBABILITIES_FILENAME = "PROBABILITIES.tsv"


def write_vocabulary(vocab, filepath, num_words=-1):
    with open(filepath, "w") as file:
        header = ["index","word"]
        writer = csv.writer(file, delimiter="\t", quotechar='"')
        writer.writerow(header)
        for index, word in list(vocab.items())[:num_words]:
            values = [index, word]
            writer.writerow(values)


def read_vocabulary(filepath):
    with open(filepath, "r") as file:
        reader = csv.reader(file, delimiter="\t", quotechar='"')
        next(reader)
        return {int(index) : str(word) for index, word in reader}


def write_sequences(seqs, filepath):
    with open(filepath, "w") as file:
        writer = csv.writer(file, delimiter="\t", quotechar='"')
        for seq in seqs:
            writer.writerow(seq)


def read_sequences(filepath):
    with open(filepath, "r") as file:
        seq_reader = sequences_reader_from_file_reader(file)
        return [seq for seq in seq_reader]


def sequences_reader_from_file_reader(file_reader):
    reader = csv.reader(file_reader, delimiter="\t", quotechar='"')
    return ([int(v) for v in r] for r in reader)


def sequences_to_texts(seqs, vocab):
    return (" ".join([vocab[i] for i in seq]) for seq in seqs)


def write_probabilities(probs, filepath):
    with open(filepath, "w") as file:
        header = ["index","prob"]
        writer = csv.writer(file, delimiter="\t", quotechar='"')
        writer.writerow(header)
        for index, prob in list(probs.items()):
            values = [index, prob]
            writer.writerow(values)


def read_probabilities(filepath):
    with open(filepath, "r") as file:
        reader = csv.reader(file, delimiter="\t", quotechar='"')
        next(reader)
        return {int(index) : float(prob) for index, prob in reader}


def random_word_index(probs, exclude=None):
    i = np.array(list(probs.keys()))
    p = np.array(list(probs.values()))
    c = choice(i, 1, p=p).item(0)
    # i = list(probs.keys())
    # c = random.choice(i) # without considering probability
    while c == exclude:
        c = choice(i, 1, p=p).item(0)
        # c = random.choice(i) # without considering probability
    return c


@contextmanager
def read_data_package(package_path):
    # paths
    sequence_path = os.path.join(package_path, SEQUENCE_FILENAME)
    vocab_path = os.path.join(package_path, VOCABULARY_FILENAME)
    probs_path = os.path.join(package_path, PROBABILITIES_FILENAME)

    sequence_file = open(sequence_path, "r")

    sequences = sequences_reader_from_file_reader(sequence_file)
    vocabulary = read_vocabulary(vocab_path)
    probabilities = read_probabilities(probs_path)

    yield sequences, vocabulary, probabilities
    sequence_file.close()
