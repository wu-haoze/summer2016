#!/bin/bash

for file in f4/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*