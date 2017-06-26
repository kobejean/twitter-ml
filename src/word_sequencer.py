import os, random
from context import tml
from tml.learning.word_stats import *
from tml.utils.ansi import ANSI
from tml.utils.text_preprocessing import *

TEST_MODE = False

WORD_SIZE = 10000
SEQ_SIZE = 11

# paths
file_name = "THE STREAM"                if not TEST_MODE else "TEST THE STREAM"
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "THE STREAM.csv")
sequence_path = os.path.join(data_path, file_name + " SEQUENCE.csv")
vocab_path = os.path.join(data_path, file_name + " VOCAB.csv")
vocab_tsv_path = os.path.join(data_path, file_name + " VOCAB.tsv ")
probs_path = os.path.join(data_path, file_name + " PROBS.csv")

# read txt file
texts = []
with open(read_path, "r") as file:
    lines = file.readlines()
    texts = [line.rstrip('\n') for line in lines]

################################################################################
if TEST_MODE:
    # limit size for testing to save time
    texts = texts[:min(10000, len(texts))]
################################################################################

# keras text preprocessing
tk = Tokenizer(
    num_words=None,
    filters="!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n",
    lower=True,
    split=" ",
    char_level=False
)
tk.fit_on_texts(texts)

# create dicts
vocab = dict([(v,k) for k,v in tk.word_index.items()])
# for normalizing probability distribution so they add up to 1
word_count_sum = sum(sorted([v for k,v in tk.word_counts.items()], reverse=True)[:WORD_SIZE])
probs = dict(sorted([(tk.word_index[k], float(v) / float(word_count_sum)) \
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

text_seq = tk.texts_to_sequences(texts)
sub_seqs = []
for seq in text_seq:
    # make sure the sequence is long enough to make a sub sequence of size SEQ_SIZE
    if len(seq) >= SEQ_SIZE:
        # loop through sub sequences
        for i in range(len(seq) - SEQ_SIZE + 1):
            sub_seq = seq[i : i + SEQ_SIZE]
            assert len(sub_seq) == SEQ_SIZE, "not len(sub_seq) == SEQ_SIZE"
            # make sure all words are in vocabulary of size WORD_SIZE before appending
            if all([wi < WORD_SIZE for wi in sub_seq]):
                sub_seqs.append(sub_seq)

# random.shuffle(sub_seqs) # for randomizing order data

# write files
write_sequences(sub_seqs, sequence_path)
write_vocab(vocab, vocab_path, WORD_SIZE)
write_vocab_tsv(vocab, vocab_tsv_path, WORD_SIZE)
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
