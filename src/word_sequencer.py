import os
from context import tml
from tml.learning.word_stats import *
from tml.utils.ansi import ANSI
from tml.utils.text_preprocessing import *

TEST_MODE = True

file_name = input("FILE NAME OF TXT FILE:") if not TEST_MODE else "THE STREAM.csv"
num_words = int(input("NUM WORDS:"))        if not TEST_MODE else 10000
words_per_training_case = 5
# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, file_name)
sequence_path = os.path.join(data_path, "SEQUENCE " + file_name)
vocab_path = os.path.join(data_path, "VOCAB " + file_name)

# word_counts = get_word_stats_from_file(read_path, num_words)
# print("WORD & COUNT")
# # print stats
# for word, count in word_counts:
#     print(ANSI.PURPLE + word.upper() + ": " + ANSI.ENDC + str(count))

texts = []
with open(read_path, "r") as file:
    lines = file.readlines()
    texts = [line.rstrip('\n') for line in lines]

tk = Tokenizer(
    num_words=None,
    filters="!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n",
    lower=True,
    split=" ",
    char_level=False
)
# texts = texts[:10000]
tk.fit_on_texts(texts)
vocab = dict((v,k) for k,v in tk.word_index.items())

text_seq = tk.texts_to_sequences(texts)
new_seq = []
for seq in text_seq:
    if len(seq) >= words_per_training_case:
        # print(seq)
        for i in range(len(seq) - words_per_training_case + 1):
            sub_seq = seq[i : i + words_per_training_case]
            assert len(sub_seq) == words_per_training_case, "not len(sub_seq) == words_per_training_case"

            if all([wi < num_words for wi in sub_seq]):
                # true if all words are in vocabulary of size num_words
                new_seq.append(sub_seq)

write_sequences(new_seq, sequence_path)
write_vocab(vocab, vocab_path, num_words)

# read sequence and print text
with open(sequence_path, "r") as file:
    seqs_reader = sequences_reader_from_file_reader(file)
    vocab = read_vocab(vocab_path)
    texts_reader = sequences_to_texts(seqs_reader, vocab)
    for text in texts_reader:
        print(text)
