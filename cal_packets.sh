#!/bin/bash
DIRECTORY=$1
OUT_DIR=$2

echo "cd $DIRECTORY"

cd $DIRECTORY
for data_set in $(ls ./);
do
	echo "calculating $data_set..."
	cd $data_set
	if [ -f all.pcap ]; 
	then 
		rm all.pcap
	fi
	number=`ls |wc -l`
	echo "The number of pcap files: $number"
	mergecap -w all.pcap *.pcap
	packets=`capinfos all.pcap|grep -e "Number of packets ="|awk '{print $5}'`
	echo "The total packets number: $packets"
	RESULT=$(echo "$packets/$number"|bc)
	echo "$data_set average is $RESULT"
	echo " "
	rm all.pcap
	cd - >/dev/null
	average=$(basename $(dirname $DIRECTORY))"_"$(basename $DIRECTORY)
	#echo $average
	echo "$data_set=$RESULT" >> $OUT_DIR/$average.txt
done

