!#/bin/bash

for file in *.py
do
  nohup python3 $file &
done