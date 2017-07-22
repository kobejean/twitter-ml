#!/usr/bin/env bash

################################################################################
# PROGRAMMED BY: Jean Flaherty                                                 #
# DATE: 07/19/2017                                                             #
# DESCRIPTION:                                                                 #
#   A script for testing everything.                                           #
################################################################################

echo "RUNNING: collector_test.py"
python3 collector_test.py
status1=$?
echo "EXITED WITH STATUS CODE: $status1"

echo "RUNNING: preprocessing_test.sh"
./preprocessing_test.sh
status2=$?
echo "EXITED WITH STATUS CODE: $status2"

echo "RUNNING: random_or_not_nn_test.sh"
./random_or_not_nn_test.sh
status3=$?
echo "EXITED WITH STATUS CODE: $status3"

echo "RUNNING: character_prediction_rnn_training_test.sh"
./character_prediction_rnn_training_test.sh
status4=$?
echo "EXITED WITH STATUS CODE: $status4"

echo "CLEANING UP..."
rm -r data/THE\ STREAM
rm -r log
rm -r checkpoints

echo "DONE"

if [ $status1 -eq 0 ] && [ $status2 -eq 0 ] && [ $status3 -eq 0 ] && [ $status4 -eq 0 ]
    then
        exit 0
    else
        exit 1
fi
