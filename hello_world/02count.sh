#!/bin/bash

# sleep 10

echo
echo "----------------------------"
echo "| HELLO WORLD, this is OSG |" 
echo "----------------------------"

if [ $1 = 0 ]; then
    echo "I can't count :'("
    exit 1
else
    echo "Look, I can count to $1 :D"
fi


for i in $(seq $1); do
    echo "    $i"
done
 



