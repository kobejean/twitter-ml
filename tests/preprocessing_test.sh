#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/15/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing the preprocessed scripts.                             #
################################################################################

TEXTPATH="../../tests/data/THE STREAM.txt" # absolute path
OUTPATH="../../tests/data/THE STREAM/"

echo "$TEXTPATH"

# echo "PREPROCESSING FOR CHARACTER PREDICTION..."
# python3 ../src/character_prediction/create_text.py data/THE\ STREAM.txt data/THE\ STREAM/
# status1=$?
#
# echo "PREPROCESSING FOR WORD EMBEDDINGS..."
# python3 ../src/word_embeddings/create_data_package.py data/THE\ STREAM.txt data/THE\ STREAM/
# status2=$?
cd ../src/character_prediction

echo "PREPROCESSING FOR CHARACTER PREDICTION..."
python3 create_text.py "$TEXTPATH" "$OUTPATH"
status1=$?

cd ../word_embeddings

echo "PREPROCESSING FOR WORD EMBEDDINGS..."
./create_data_package.sh "$TEXTPATH" "$OUTPATH"
status2=$?
cd ../../tests

if [ $status1 -eq 0 ] && [ $status2 -eq 0 ]
# if [ $status1 -eq 0 ]
    then
        exit 0
    else
        exit 1
fi
