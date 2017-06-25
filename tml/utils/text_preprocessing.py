import csv

def write_vocab(vocab, filepath, num_words=-1):
    with open(filepath, "w") as file:
        for index, word in list(vocab.items())[:num_words]:
            writer = csv.writer(file)
            values = [index, word]
            writer.writerow(values)


def read_vocab(filepath):
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        return {v[0] : v[1] for v in reader}

def write_sequences(seqs, filepath):
    with open(filepath, "w") as file:
        writer = csv.writer(file)
        for seq in seqs:
            writer.writerow(seq)

def read_sequences(filepath):
    with open(filepath, "r") as file:
        seq_reader = sequences_reader_from_file_reader(file)
        return [seq for seq in seq_reader]

def sequences_reader_from_file_reader(file_reader):
    reader = csv.reader(file_reader)
    return reader

def sequences_to_texts(seqs, vocab):
    return (" ".join([vocab[i] for i in seq]) for seq in seqs)
