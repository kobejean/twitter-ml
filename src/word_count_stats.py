import os
from context import tml
from tml.utils.ansi import ANSI

TEST_MODE = False

file_name = input("FILE NAME OF TXT FILE:") if not TEST_MODE else "THE STREAM.csv"
vocabulary_size = int(input("VOCABULARY SIZE:"))        if not TEST_MODE else 10000
# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, file_name)

texts = []
with open(file_path, "r") as file:
    lines = file.readlines()
    texts = [line.rstrip('\n') for line in lines]

tk = Tokenizer(
    num_words=vocabulary_size,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    lower=True,
    split=' ',
    char_level=False
)
tk.fit_on_texts(texts)

word_counts = sorted(list(tk.word_counts.items()), key=lambda item:item[1], reverse=True)[0:vocabulary_size]

print("WORD & COUNT")
# print stats
for word, count in word_counts:
    print(ANSI.PURPLE + word.upper() + ": " + ANSI.ENDC + str(count))
