#!/bin/bash
DIRECTORY="/home/snape/Downloads/Google_home"

#echo "cd $DIRECTORY"
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
	RESULT=$(echo "$packets/$number" | bc -l)
	echo "$data_set average is $RESULT"
	echo " "
	cd - >/dev/null 
done

