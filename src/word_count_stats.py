import os
from context import tml
from tml.utils.word_stats import *
from tml.utils.ansi import ANSI

TEST_MODE = False

file_name = input("FILE NAME OF TXT FILE:") if not TEST_MODE else "THE STREAM.csv"
num_words = int(input("NUM WORDS:"))        if not TEST_MODE else 10000
# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, file_name)

word_counts = get_word_stats_from_file(read_path, num_words)
print("WORD & COUNT")
# print stats
for word, count in word_counts:
    print(ANSI.PURPLE + word.upper() + ": " + ANSI.ENDC + str(count))
