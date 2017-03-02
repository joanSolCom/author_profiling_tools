#!/bin/bash

while true; do
echo "-------------------"
echo "waking up."
ps -aux | grep -c "python ./parser_client/parse.py"
if [ $? -eq 2 ]; then
  echo "Process is running."
else
  echo "Process is not running."
  echo "Will now reactivate."
  python ./parser_client/parse.py
fi
echo "Sleeping for a minute."
sleep 60

done