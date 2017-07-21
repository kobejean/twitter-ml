#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/20/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for running the charachter prediction recurrent neural net.       #
################################################################################

if [ $# -eq 0 ]
    then
        echo "NO ARGUMENTS SUPPLIES"
        echo "SHOULD INCLUDE THE PATH TO THE TEXT FILES"
        echo "./run_rnn_train.sh path/to/text_file_*.txt"

        exit 1
    else
        DIRPATH="${1%/*}"
        DIRPATH="$(cd "$DIRPATH"; pwd)"
        BASENAME="${1##*/}"

        TEXTPATH="$DIRPATH/"$BASENAME"" # absolute path

        cd ../../

        # assuming preprocessing has completed
        python3 -m tml.learning.character_prediction.rnn_train "$TEXTPATH" src/character_prediction/log/ src/character_prediction/checkpoints
        status=$?

        cd src/character_prediction

        exit $status
fi
