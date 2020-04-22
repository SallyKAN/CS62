#!/bin/bash

#The wireless network interface name, check with `iwconfig`
INTERFACE="wlp3s0"

#The wireless network interface name after enabling the monitor mode
INTERFACE_MON="wlp3s0mon"

#The MAC address of the smart device
MAC_ADDR="88:10:8f:61:e3:f1"

#The wifi channel
CHANNEL="1"

#The directory used to store audio files
audios=$(ls ./audio)

#The repeat times of playing command
REPEAT_TIMES=5

#Enable the monitor mode of the wireless driver
airmon-ng start $INTERFACE $CHANNEL

for audio in $audios; do
    filename="${audio%.*}"
    extention=".pcap"
    tcpdump -i $INTERFACE_MON -w $filename$extention wlan host $MAC_ADDR &
    echo "Playing $audio"
    for((i=1;i<=$REPEAT_TIMES;i++)); do
        #If it says "VLC is not supposed to be run as root. Sorry", try `sed -i 's/geteuid/ge	     tppid/' /usr/bin/vlc`, see more at https://unix.stackexchange.com/questions/125546/ho	  w-to-run-vlc-player-in-root
	cvlc --play-and-exit ./audio/$audio 
    	sleep 5
    done

    #Once the command is done, stop the capturing.
    pid=$(ps -e | pgrep tcpdump)  
    echo $pid  
    #interrupt it:  
    sleep 3
    kill -2 $pid
done

#Disable the monitor mode of the wireless driver
airmon-ng stop $INTERFACE_MON

