#!/bin/sh
here="`dirname \"$0\"`"
cd "$here" || exit 1

python3 -i src/DataCollector.py
# python3 -i src/DataHandler.py
