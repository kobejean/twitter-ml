from datetime import datetime, timedelta
import random
import os
import re


# paths
this_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.abspath(os.path.join(this_path, os.pardir))
shared_data = os.path.join(parent_path, "shared_data")
data_path = os.path.join(this_path, "data")
write_path = os.path.join(data_path, "THE STREAM")
read_path = os.path.join(shared_data, "THE STREAM.csv")


print("READING TEXT...")
batch_size = 5000
tweet_texts = set([])

with open(read_path, "r") as file:
    for text in file:
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
            print("text:{0: <40}".format(text.rstrip("\n"))[:40], end="\r")

print("\n", len(tweet_texts),"TWEETS")
shuffle_tweet_texts = [text for text in tweet_texts]
# randomize order of tweets
random.shuffle(shuffle_tweet_texts)

print("\nCREATING BATCHES...")
batches = []
for i, text in enumerate(shuffle_tweet_texts):
    batch_num = i // batch_size
    print("i:{0} batch:{1} text:{2: <40}".format(i, batch_num, text.rstrip("\n"))[:40], end="\r")
    if i % batch_size == 0:
        batches.append([])
    batches[batch_num].append(text)

print("\nWRITING BATCHES...")
for i, batch in enumerate(batches):
    write_path = os.path.join(data_path, "THE TEXT " + str(i+1).zfill(4) + ".txt")
    with open(write_path, 'w') as write_file:
        for text in batch:
            print("batch:{0} text:{1: <40}".format(i, text.rstrip("\n"))[:40], end="\r")
            write_file.write(text) # python will convert \n to os.linesep

print("DONE")
