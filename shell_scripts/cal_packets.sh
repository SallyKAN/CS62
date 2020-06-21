#!/bin/bash
DIRECTORY=$1
OUT_DIR=$2

cal_per_command(){
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
	average=$1"_"$2
	#echo $average
	echo "$data_set=$RESULT" >> $OUT_DIR/$average.txt
done
}

rm -rf $OUT_DIR/*
echo "rm -rf $OUT_DIR/*" 

cd $DIRECTORY
echo "cd $DIRECTORY"

for device_dataset in $(ls ./);
do
	cd $device_dataset
	echo "cd $device_dataset"
	for distance_dataset in $(ls ./);
	do
		cd $distance_dataset
		echo "cd $distance_dataset"
		cal_per_command $device_dataset $distance_dataset
		cd ..
	done
	cd $DIRECTORY
done
