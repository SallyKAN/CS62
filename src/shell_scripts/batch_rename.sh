#!/bin/bash
DIR=$1
cd $DIR
total=0

for dir in $(find . -maxdepth 1 -mindepth 1 -type d)
do
  #echo "$dir"
  sub=$(find "$dir" -type f)
  for name in $(basename -a $sub)
  do
	declare result=($(grep -Eo '[^0-9]+|[0-9]+' <<< $name))
#	number=${result[1]}
	number=`expr ${result[1]} + 1000`
        rename=${result[0]}$number${result[2]}
	echo "$name  $rename"
	mv $dir/$name $dir/$rename 
#	if [ -f $dir/$name ];then
#		echo "true"
#	else
#		echo "false"
#	fi
  done	
done

#echo "total: $total"
