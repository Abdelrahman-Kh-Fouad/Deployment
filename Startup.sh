#!/bin/bash
python3 configuration.py
for file in ./apps/*.py
do
  echo $file
done

for file in apps/*.py
do
  nohup python3 $file &
done