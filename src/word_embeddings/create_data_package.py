#!/usr/bin/env python3
"""
                           - Create Data Package -

PROGRAMMED BY: Jean Flaherty
DATE: 07/15/2017
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
import os, sys

# tml
from context import tml
from tml.utils.word_preprocessing import create_data_package, read_data_package, sequences_to_texts

this_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.abspath(os.path.join(this_path, os.pardir))
shared_data = os.path.join(parent_path, "shared_data")
data_path = os.path.join(this_path, "data")

# default read path
text_path = os.path.join(shared_data, "THE STREAM.csv")

# get path from command line arguments if passed
if len(sys.argv) >= 2:
    text_path = os.path.abspath(sys.argv[1])

package_name = os.path.splitext(os.path.basename(text_path))[0]
package_path = os.path.join(data_path, package_name)

if len(sys.argv) >= 3:
    package_path = os.path.abspath(sys.argv[2])

if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(package_path):
    os.mkdir(package_path)

print("READ TEXT PATH:", text_path)
print("PACKAGE PATH:", package_path)


create_data_package(text_path, package_path, vocabulary_size=10000)


# show_seq = input("WOULD YOU LIKE TO SEE THE TEXT SEQUENCES? (Y/N): ")
# if show_seq.upper().strip() == "Y":
#     # read sequence and print text
#     with read_data_package(package_path) as (seqs_reader, vocab, _):
#         # seqs_reader = sequences_reader_from_file_reader(file)
#         # vocab = read_vocabulary(vocab_path)
#         texts_reader = sequences_to_texts(seqs_reader, vocab)
#         for text in texts_reader:
#             print(text)
