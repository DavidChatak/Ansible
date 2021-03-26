#!/bin/bash
x=1
touch logs.txt
while  true;
do
#  echo "Welcome $x times"
  echo "Welcome $x times" >> logs.txt
  x=$(( $x + 1 ))
	sleep 3
done

# cat logs.txt
