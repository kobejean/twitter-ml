import csv, random
import numpy as np
from numpy.random import choice
from contextlib import contextmanager
import os, random
from ..utils.ansi import ANSI

# TEST_MODE = True

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


def create_data_package(text_path, package_path, vocabulary_size=10000, show_progress=False):
    import keras
    from keras.preprocessing.text import Tokenizer
    # paths
    sequence_path = os.path.join(package_path, SEQUENCE_FILENAME)
    vocab_path = os.path.join(package_path, VOCABULARY_FILENAME)
    probs_path = os.path.join(package_path, PROBABILITIES_FILENAME)

    # read txt file
    with open(text_path, "r") as file:
        texts = (line.rstrip('\n') for line in file)

        ################################################################################
        # if TEST_MODE:
        #     # limit size for testing to save time
        #     texts = (t for t,_ in zip(texts, range(10000)))
        ################################################################################
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

        ################################################################################
        # if TEST_MODE:
        #     # limit size for testing to save time
        #     texts = (t for t,_ in zip(texts, range(10000)))
        ################################################################################
        print("CREATING VOCABULARY...")
        # create dicts
        vocab = dict([(v-1,k) for k,v in tk.word_index.items()])
        # for normalizing probability distribution so they add up to 1
        print("CREATING PROBABILITIES...")
        word_count_sum = sum(sorted([v for k,v in tk.word_counts.items()], reverse=True)[:vocabulary_size])
        probs = dict(sorted([(tk.word_index[k]-1, float(v) / float(word_count_sum)) \
                        for k,v in tk.word_counts.items()])[:vocabulary_size])

        ################################################################################
        # if TEST_MODE:
        #     probs_sum = sum([v for k,v in probs.items()])
        #     assert abs(probs_sum-1) < 0.00005, "probabilities were not normalized:" + str(probs_sum)
        #     print(probs)
        #     print(vocab)
        #     for _ in range(100):
        #         print(random_word_index(probs))
        ################################################################################
        print("CREATING SEQUENCES...")
        # i - 1 so that index z
        text_seq = ([i-1 for i in seq] for seq in tk.texts_to_sequences(texts))

        # write files
        print("WRITING SEQUENCES...")
        write_sequences(text_seq, sequence_path)
        print("WRITING VOCABULARY...")
        write_vocabulary(vocab, vocab_path, vocabulary_size)
        print("WRITING PROBABILITIES...")
        write_probabilities(probs, probs_path)
        print("DONE!")

        ################################################################################
        # if TEST_MODE:
        #     show_seq = input("WOULD YOU LIKE TO SEE THE TEXT SEQUENCES? (Y/N): ")
        #     if show_seq.upper().strip() == "Y":
        #         # read sequence and print text
        #         with open(sequence_path, "r") as file:
        #             seqs_reader = sequences_reader_from_file_reader(file)
        #             vocab = read_vocabulary(vocab_path)
        #             texts_reader = sequences_to_texts(seqs_reader, vocab)
        #             for text in texts_reader:
        #                 print(text)

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

# if __name__ == "__main__":
#     package_name = "THE STREAM"                if not TEST_MODE else "TEST THE STREAM"
#     abs_path = os.path.abspath(os.path.dirname(__file__))
#     data_path = os.path.join(abs_path, "data")
#     text_path = os.path.join(data_path, "THE STREAM.csv")
#     package_path = os.path.join(data_path, package_name)
#     create_data_package(text_path, package_path, vocabulary_size=10000)
