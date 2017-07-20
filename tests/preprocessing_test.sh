#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/15/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing the preprocessed scripts.                             #
################################################################################


echo "PREPROCESSING FOR CHARACTER PREDICTION..."
python3 ../src/character_prediction/create_text.py data/THE\ STREAM.txt data/THE\ STREAM/
status1=$?

echo "PREPROCESSING FOR WORD EMBEDDINGS..."
python3 ../src/word_embeddings/create_data_package.py data/THE\ STREAM.txt data/THE\ STREAM/
status2=$?

if [ $status1 -eq 0 ] && [ $status2 -eq 0 ]
# if [ $status1 -eq 0 ]
    then
        exit 0
    else
        exit 1
fi
