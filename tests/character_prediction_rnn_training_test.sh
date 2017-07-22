#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/19/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing the random or not neural net.                         #
################################################################################

cd ../

# assuming preprocessing has completed
python3 -m tml.learning.character_prediction.rnn_train tests/data/THE\ STREAM/\*.txt tests/log/character_prediction/ tests/checkpoints -e 1 -b 200
status=$?

cd tests

exit $status
