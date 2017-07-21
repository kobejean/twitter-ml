#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/19/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for running the random or not neural net.                         #
################################################################################

if [ $# -eq 0 ]
    then
        echo "NO ARGUMENTS SUPPLIES"
        echo "SHOULD INCLUDE THE PATH TO THE DATA PACKAGE DIRECTORY"
        echo "./random_or_not_nn.sh path/to/data_package"

        exit 1
    else
        ABS_PATH=`cd "$1"; pwd`
        cd ../../

        echo "RUNNING RANDOM OR NOT NEURAL NET..."
        # assuming preprocessing has completed
        python3 -m tml.learning.word_embeddings.random_or_not_nn "$ABS_PATH" -l src/word_embeddings/log -e 1
        status=$?

        cd src/word_embeddings

        exit $status
fi
