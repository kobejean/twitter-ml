import os, random
from context import tml
from tml.utils.word_stats import *
from tml.utils.ansi import ANSI
from tml.utils.text_preprocessing import *

TEST_MODE = False

WORD_SIZE = 10000
SEQ_SIZE = 5

# paths
package_name = "THE STREAM"                if not TEST_MODE else "TEST THE STREAM"
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "THE STREAM.csv")
package_path = os.path.join(data_path, package_name)
sequence_path = os.path.join(package_path, "SEQUENCE.tsv")
vocab_path = os.path.join(package_path, "VOCAB.tsv")
vocab_meta_path = os.path.join(package_path, "VOCAB META.tsv")
probs_path = os.path.join(package_path, "PROBS.tsv")

if not os.path.exists(package_path):
    os.mkdir(package_path)

# read txt file
with open(read_path, "r") as file:
    texts = (line.rstrip('\n') for line in file)

    ################################################################################
    if TEST_MODE:
        # limit size for testing to save time
        texts = (t for t,_ in zip(texts, range(10000)))
    ################################################################################

    # keras text preprocessing
    tk = get_tokenizer_from_texts(texts, WORD_SIZE)

with open(read_path, "r") as file:
    texts = (line.rstrip('\n') for line in file)

    ################################################################################
    if TEST_MODE:
        # limit size for testing to save time
        texts = (t for t,_ in zip(texts, range(10000)))
    ################################################################################
    # create dicts
    vocab = dict([(v-1,k) for k,v in tk.word_index.items()])
    # for normalizing probability distribution so they add up to 1
    word_count_sum = sum(sorted([v for k,v in tk.word_counts.items()], reverse=True)[:WORD_SIZE])
    probs = dict(sorted([(tk.word_index[k]-1, float(v) / float(word_count_sum)) \
                    for k,v in tk.word_counts.items()])[:WORD_SIZE])

    ################################################################################
    if TEST_MODE:
        probs_sum = sum([v for k,v in probs.items()])
        assert abs(probs_sum-1) < 0.00005, "probs was not normalized:" + str(probs_sum)
        print(probs)
        print(vocab)
        for _ in range(100):
            print(random_word_index(probs))
    ################################################################################

    # i - 1 so that index z
    text_seq = [[i-1 for i in seq] for seq in tk.texts_to_sequences(texts)]

    # write files
    write_sequences(text_seq, sequence_path)
    write_vocab(vocab, vocab_path, WORD_SIZE)
    write_vocab_metadata(vocab, vocab_meta_path, WORD_SIZE)
    write_probs(probs, probs_path)

    show_seq = input("WOULD YOU LIKE TO SEE THE SUB SEQUENCES? (Y/N): ")
    if show_seq.upper().strip() == "Y":
        # read sequence and print text
        with open(sequence_path, "r") as file:
            seqs_reader = sequences_reader_from_file_reader(file)
            vocab = read_vocab(vocab_path)
            texts_reader = sequences_to_texts(seqs_reader, vocab)
            for text in texts_reader:
                print(text)
