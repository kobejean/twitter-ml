from datetime import datetime, timedelta
import random
import os
import re

from context import tml
from tml.collection.data_handler import DataHandler


# paths
abs_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(abs_path, "data")
read_path = os.path.join(data_path, "THE STREAM.csv")

# initialization
dat_hand = DataHandler(file_path=read_path)
# print data
dat_hand.display()

batches = []
batch_size = 5000
tweet_texts = set([])
for entry in dat_hand.data:
    # replace urls with generic url
    text = entry.get("text","")
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

    if not "\n" in text and no_unknowns:
        text = re.sub('¥', '', text, re.MULTILINE)
        # text = re.sub('https?\:\/\/t\.co\/.{10}', 'https://t.co/XXXXXXXXXX', text, re.MULTILINE)
        text = re.sub('https?\:\/\/t\.co\/.{10}', '¥', text, re.MULTILINE)
        tweet_texts.add(text)

print(len(tweet_texts),"tweets")
shuffle_tweet_texts = [text for text in tweet_texts]
# randomize order of tweets
random.shuffle(shuffle_tweet_texts)

for i, text in enumerate(shuffle_tweet_texts):
    batch_num = i // batch_size
    if i % batch_size == 0:
        batches.append([])

    batches[batch_num].append(text)

for i, batch in enumerate(batches):
    write_path = os.path.join(data_path, "THE TEXT " + str(i+1).zfill(4) + ".txt")
    write_file = open(write_path, 'w')
    for text in batch:
        write_file.write(text+"\n") # python will convert \n to os.linesep

    write_file.close()
