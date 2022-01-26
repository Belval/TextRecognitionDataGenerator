#!/usr/bin/env bash

rm -rf faults
mkdir faults
python3 run.py -na 2 -rs -c 1000000 --output_dir train
rm -rf faults
mkdir faults
python3 run.py -na 2 -rs -c 100 --output_dir val

rm -rf faults
mkdir faults

python3 run.py -na 2 -rs -c 1000 --output_dir test

zip dataset.zip -r train val test

