python3 configruation.py

for file in ./apps/*.py
do
  nohup $file &
done