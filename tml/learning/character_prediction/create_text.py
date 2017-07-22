#!/usr/bin/env python3
"""
                            - Create Text -

PROGRAMMED BY: Jean Flaherty
DATE: 07/15/2017
DESCRIPTION:
    A script that reads from a text file and splits the text into batches. Files
    are written to src/character_prediction/data/{basename}/{basename} {i}.txt

    The path to the original text file can be passed as an argumant in
    command line like this:

        $ python3 create_text.py path/to/text_file.txt
"""

from datetime import datetime, timedelta
import random, os, re, sys

if __name__ == "__main__":
    read_path = None
    write_path = None
    options = {}
    usage_str = "usage: python3 -m tml.learning.character_prediction.create_text <text_file_path> <text_batches_dir>"
    try:
        read_path    = os.path.abspath(sys.argv[1])
        write_path = os.path.abspath(sys.argv[2])
    except IndexError:
        print(usage_str)
        sys.exit(2)


    # create directories if they do not exist
    if not os.path.exists(write_path):
        os.makedirs(write_path)

    print("READ PATH:", read_path)
    print("WRITE PATH:", write_path)

    read_basename = os.path.splitext(os.path.basename(read_path))[0]


    print("READING TEXT...")
    batch_size = 5000
    tweet_texts = set([])

    # read text
    with open(read_path, "r") as file:
        for i, text in enumerate(file):
            no_unknowns = True
            for c in text:
                a = ord(c)
                if a == 9:
                    continue
                if a == 10:
                    continue
                elif 32 <= a <= 126:
                    continue
                else:
                    no_unknowns = False
                    break

            if no_unknowns:
                tweet_texts.add(text)
                if i % 100 == 0:
                    print("TEXT: {0: <40}".format(text.rstrip("\n"))[:40], end="\r")
        print()

    print(len(tweet_texts),"TWEETS")
    shuffle_tweet_texts = [text for text in tweet_texts]
    # randomize order of tweets
    random.shuffle(shuffle_tweet_texts)
    print()

    print("CREATING BATCHES...")
    batches = []
    for i, text in enumerate(shuffle_tweet_texts):
        batch_num = i // batch_size
        if i % 100 == 0:
            print("I: {0} BATCH: {1} TEXT: {2: <40}".format(i, batch_num, text.rstrip("\n"))[:40], end="\r")
        if i % batch_size == 0:
            batches.append([])
        batches[batch_num].append(text)
    print()

    print("WRITING BATCHES...")
    for i, batch in enumerate(batches):
        write_file_path = os.path.join(write_path, read_basename + " " + str(i+1).zfill(4) + ".txt")
        with open(write_file_path, 'w') as write_file:
            for j, text in enumerate(batch):
                if (i*j) % 100 == 0:
                    print("BATCH: {0} TEXT: {1: <40}".format(i, text.rstrip("\n"))[:40], end="\r")
                write_file.write(text) # python will convert \n to os.linesep
    print()
    print("DONE")
