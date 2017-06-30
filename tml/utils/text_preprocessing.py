import csv, random
import numpy as np
from numpy.random import choice

def write_vocab(vocab, filepath, num_words=-1):
    with open(filepath, "w") as file:
        header = ["index","word"]
        writer = csv.writer(file, delimiter="\t", quotechar='"')
        writer.writerow(header)
        for index, word in list(vocab.items())[:num_words]:
            values = [index, word]
            writer.writerow(values)

def write_vocab_metadata(vocab, filepath, num_words=-1):
    with open(filepath, "w") as file:
        header = ["word","index"]
        writer = csv.writer(file, delimiter="\t", quotechar='"')
        writer.writerow(header)
        for index, word in list(vocab.items())[:num_words]:
            values = [word, index]
            writer.writerow(values)

# def write_vocab_tsv(vocab, filepath, num_words=-1):
#     with open(filepath, "w") as file:
#         # header
#         file.write("{}\t{}\n".format("word","index"))
#         for index, word in list(vocab.items())[:num_words]:
#             values = [index, word]
#             file.write("{}\t{}\n".format(word,index))


def read_vocab(filepath):
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

# def sequence_to_words(seq, vocab):
#     return [vocab[i] for i in seq]

def write_probs(probs, filepath):
    with open(filepath, "w") as file:
        header = ["index","prob"]
        writer = csv.writer(file, delimiter="\t", quotechar='"')
        writer.writerow(header)
        for index, prob in list(probs.items()):
            values = [index, prob]
            writer.writerow(values)

def read_probs(filepath):
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
