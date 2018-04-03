#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/15/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing the preprocessed scripts.                             #
################################################################################

TEXTPATH="tests/data/TEST STREAM.txt" # absolute path
OUTPATH="tests/data/TEST STREAM/"

echo "$TEXTPATH"

# echo "PREPROCESSING FOR CHARACTER PREDICTION..."
# python3 ../src/character_prediction/create_text.py data/TEST\ STREAM.txt data/TEST\ STREAM/
# status1=$?
#
# echo "PREPROCESSING FOR WORD EMBEDDINGS..."
# python3 ../src/word_embeddings/create_data_package.py data/TEST\ STREAM.txt data/TEST\ STREAM/
# status2=$?
cd ../

echo "PREPROCESSING FOR CHARACTER PREDICTION..."
python3 -m tml.learning.character_prediction.create_text "$TEXTPATH" "$OUTPATH"
status1=$?

echo "PREPROCESSING FOR WORD EMBEDDINGS..."
python3 -m tml.learning.word_embeddings.create_data_package "$TEXTPATH" "$OUTPATH"
status2=$?

cd tests

if [ $status1 -eq 0 ] && [ $status2 -eq 0 ]
    then
        exit 0
    else
        exit 1
fi
