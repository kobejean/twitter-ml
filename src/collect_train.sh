##########################################################################################
# AUTHOR: Jake Jongewaard                                                               #
#                                                                                       #
# DESCRIPTION:Script for simplifying the execution of the data gathering and training   #
# processes.                                                                            #
#########################################################################################
#!/usr/bin/env bash

echo Executing collection_program.py
python3 collection_program.py

echo Executing create_text.py
echo What would you like to name the files?
read filename
echo What would you like to name the directory to store the files?
read training_directory
python3 create_text.py $training_directory $filename

echo Executing rnn_train.py
echo What is the name of the directory where the training files are stored?
read $training_directory
mkdir data/$training_directory
python3 learning_example/rnn_train.py $training_directory