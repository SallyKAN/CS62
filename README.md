# CS62
Capstone Project

## Reuqirements
- Install aircrack-ng

`sudo apt-get update`

`sudo apt-get install -y aircrack-ng`
- Install vlc

`sudo apt-get install vlc`

`sed -i 's/geteuid/getppid/' /usr/bin/vlc`

## Run script

Create a directory for puting command audio files

`mkdir ./audios` 

Change the wireless network configuration to your own configuration in the script

`INTERFACE="wlp3s0"
 INTERFACE_MON="wlp3s0mon"
 MAC_ADDR="88:10:8f:61:e3:f1"
 CHANNEL="1"
`

Change the excuteable permission

`chmod +x ./capture.sh`

Run as root

`sudo su`

`./capture.sh`
