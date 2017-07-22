#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/20/2017                                                             #
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
        DIRPATH="${1%/*}"
        DIRPATH="$(cd "$DIRPATH"; pwd)"
        BASENAME="${1##*/}"
        BASENAME="${BASENAME%.*}"
        EXTENSION="${1##*.}"

        TEXTPATH="$DIRPATH/$BASENAME.$EXTENSION" # absolute path

        echo "PREPROCESSING FOR CHARACTER PREDICTION..."
        cd character_prediction
        ./create_text.sh "$TEXTPATH"
        cd ../

        echo "PREPROCESSING FOR WORD EMBEDDINGS..."
        cd word_embeddings
        ./create_data_package.sh "$TEXTPATH"
        cd ../

        exit 0
fi
