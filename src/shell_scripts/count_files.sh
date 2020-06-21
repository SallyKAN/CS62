#!/bin/bash
DIR=$1
cd $DIR
total=0

for dir in $(find . -maxdepth 1 -mindepth 1 -type d)
do
  sub=$(find "$dir" -type f | wc -l)
  echo "$dir:  $sub"
  total=`expr $total + $sub`
done

echo "total: $total"
