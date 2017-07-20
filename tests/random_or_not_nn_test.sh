#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/19/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing the random or not neural net.                         #
################################################################################

cd ../

echo "RUNNING RANDOM OR NOT NEURAL NET..."
# assuming preprocessing has completed
python3 -m tml.learning.word_embeddings.random_or_not_nn -d tests/data/THE\ STREAM -l tests/log/word_embeddings/ -b 1000
status=$?

cd tests

exit $status
