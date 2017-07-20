#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/15/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for creating the preprocessed data from a text file               #
################################################################################

if [ $# -eq 0 ]
    then
        echo "NO ARGUMENTS SUPPLIES"
        echo "SHOULD INCLUDE THE FILE PATH TO THE TEXT FILE"
        echo "./preprocessing file/to/text_file.csv"

        exit 1
    else
        ABS_PATH=`cd "$1"; pwd`
        echo "PREPROCESSING FOR CHARACTER PREDICTION..."
        python3 character_prediction/create_text.py "$ABS_PATH"

        echo "PREPROCESSING FOR WORD EMBEDDINGS..."
        python3 word_embeddings/create_data_package.py "$ABS_PATH"

        exit 0
fi
