import keras
from keras.preprocessing.text import Tokenizer
# from keras import backend as tf
# import numpy as np


def get_word_stats_from_file(file_path, num_words):
    tk = get_tokenizer_from_file(file_path, num_words)
    return sorted(list(tk.word_counts.items()), key=lambda item:item[1], reverse=True)[0:num_words]

def get_tokenizer_from_file(file_path, num_words):
    texts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        texts = [line.rstrip('\n') for line in lines]

    tk = Tokenizer(
        num_words=num_words,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        split=' ',
        char_level=False
    )
    tk.fit_on_texts(texts)
    return tk

def get_tokenizer_from_text(text, num_words):
    texts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        texts = [line.rstrip('\n') for line in lines]

    tk = Tokenizer(
        num_words=num_words,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        split=' ',
        char_level=False
    )
    tk.fit_on_texts(texts)
    return tk
