# import os
# from context import tml
# from tml.utils.word_preprocessing import *
#
# TEST_MODE = False
#
# package_name = "THE STREAM"                if not TEST_MODE else "TEST THE STREAM"
# abs_path = os.path.abspath(os.path.dirname(__file__))
# data_path = os.path.join(abs_path, "data")
# text_path = os.path.join(data_path, "THE STREAM.csv")
# package_path = os.path.join(data_path, package_name)
#
# if not os.path.exists(package_path):
#     print("PACKAGE PATH {} DOES NOT EXIST... CREATING DIRECTORY...".format(package_path))
#     os.mkdir(package_path)
#
# create_data_package(text_path, package_path, vocabulary_size=10000)
#
#
# show_seq = input("WOULD YOU LIKE TO SEE THE TEXT SEQUENCES? (Y/N): ")
# if show_seq.upper().strip() == "Y":
#     # read sequence and print text
#     with read_data_package(package_path) as seqs_reader, vocab, _:
#         # seqs_reader = sequences_reader_from_file_reader(file)
#         # vocab = read_vocabulary(vocab_path)
#         texts_reader = sequences_to_texts(seqs_reader, vocab)
#         for text in texts_reader:
#             print(text)
