#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/20/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for creating the data package.                                    #
################################################################################

if [ $# -eq 0 ]
    then
        echo "NO ARGUMENTS SUPPLIES"
        echo "SHOULD INCLUDE THE PATH TO THE TEXT FILE"
        echo "./create_data_package.sh path/to/text_file.txt"

        exit 1
    else

        DIRPATH="${1%/*}"
        DIRPATH="$(cd "$DIRPATH"; pwd)"
        BASENAME="${1##*/}"
        BASENAME="${BASENAME%.*}"
        EXTENSION="${1##*.}"

        TEXTPATH="$DIRPATH/$BASENAME.$EXTENSION" # absolute path
        DATAPATH="$(pwd)/data/$BASENAME"

        if [ $# -ge 2 ]
            then
                DATAPATH="$(pwd)/$2"
        fi


        cd ../../

        echo "CREATING DATA PACKAGE..."
        # assuming preprocessing has completed
        python3 -m tml.learning.word_embeddings.create_data_package "$TEXTPATH" "$DATAPATH" --ws 10000
        status=$?

        cd src/word_embeddings

        exit $status
fi
