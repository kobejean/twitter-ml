#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/15/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing the preprocessed scripts                              #
################################################################################


echo "PREPROCESSING FOR CHARACTER PREDICTION..."
python3 ../src/character_prediction/create_text.py data/THE\ STREAM.txt data/THE\ STREAM/

echo "PREPROCESSING FOR WORD EMBEDDINGS..."
python3 ../src/word_embeddings/create_data_package.py data/THE\ STREAM.txt data/THE\ STREAM/

rm -r data/THE\ STREAM/
