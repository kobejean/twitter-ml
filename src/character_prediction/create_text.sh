#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/21/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for creating the text batches.                                    #
################################################################################

if [ $# -eq 0 ]
    then
        echo "NO ARGUMENTS SUPPLIES"
        echo "SHOULD INCLUDE THE PATH TO THE TEXT FILE"
        echo "./create_text.sh path/to/text_file.txt"

        exit 1
    else

        DIRPATH="${1%/*}"
        DIRPATH="$(cd "$DIRPATH"; pwd)"
        BASENAME="${1##*/}"
        BASENAME="${BASENAME%.*}"
        EXTENSION="${1##*.}"

        TEXTPATH="$DIRPATH/$BASENAME.$EXTENSION" # absolute path
        BATCHESPATH="$(pwd)/data/$BASENAME"

        if [ $# -ge 2 ] # if second arg is passed use as output path
            then
                BATCHESPATH="$(pwd)/$2"
        fi


        cd ../../

        echo "CREATING DATA PACKAGE..."
        # assuming preprocessing has completed
        python3 -m tml.learning.character_prediction.create_text "$TEXTPATH" "$BATCHESPATH"
        status=$?

        cd src/character_prediction

        exit $status
fi
