from gtts import gTTS
from playsound import playsound
import time
from scapy.all import *
import sys
import pyshark
from scapy.layers.inet import IP
import pyttsx3

#import vlc

f = open("alexa.txt", "r")
language = 'en'
counter = 1
engine = pyttsx3.init()
changeName = 'alarm'
nameBla = 0;
fs = open("cities.txt", "r")

while counter <= 1000:
	#	print(mytext)
	print("woke up")
	nameBla = 0;
	f = open("alexa.txt", "r")
	cities = fs.readline()
	for cmd in f:
		time.sleep(0)
		nameBla += 1
		print(cities)
		print(nameBla)
		print(changeName)
		if nameBla == 1:
			changeName = 'alarm'
			cmd = cmd + str(counter%12) + "am"
		elif nameBla == 2:
			changeName = 'weather'
			cmd = cmd + cities
		elif nameBla == 3:
			changeName = 'joke'
		elif nameBla == 4:
			changeName = 'music'
		elif nameBla == 5:
			changeName = 'timer'
			cmd = cmd + str(counter%24) + "hours"
		elif nameBla == 6:
			changeName = 'fact'
		elif nameBla == 7:
			changeName = 'smart_plug'
			if (counter%2 == 0):
				cmd = cmd + " off"
			else:
				cmd = cmd + " on"
		elif nameBla == 8:
			changeName == 'time'
			cmd = cmd + cities
		name = str(changeName) + str(counter) +'.pcap'
		_dir = 'Captures'
		_dir = os.path.join(_dir, '%s' %changeName)	
		if not os.path.exists(_dir):
			os.makedirs(_dir)
		_dir = os.path.join(_dir, '%s' % name)
		engine.say(cmd)
		engine.setProperty('rate',200)  #120 words per minute
		engine.setProperty('volume',0.9) 
		engine.runAndWait()
		tcp = sniff(session=TCPSession, timeout=10)
		
		print(_dir)
		for pkt in tcp:
			#print(pkt.getlayer(Dot11Elt))
				if (pkt.haslayer(Dot11QoS) or pkt.haslayer(Dot11ProbeReq) or pkt.haslayer(Dot11ProbeResp)):
					if (pkt.getlayer(Dot11).addr1.__eq__("68:54:fd:e5:b9:dd") or
					pkt.getlayer(Dot11).addr2.__eq__("68:54:fd:e5:b9:dd") or
					pkt.getlayer(Dot11).addr3.__eq__("68:54:fd:e5:b9:dd")):
						wrpcap(_dir, pkt, append=True)
			#	if pkt.subtype == 8 and str(pkt.addr1) == '68:54:fd:e5:b9:dd':
			#		print(pkt.show())
			#	print(pkt.getlayer(Dot11).addr1)
			#	print(pkt.getlayer(Dot11).addr2)
			#	print(pkt.getlayer(Dot11).addr3)
			#	
			#		print("if done")
			#		wrpcap("captured.pcap", pkt, append=True)
			#print(type(pkt))
			#print(pkt.show())
			#if (pkt.getlayer(Dot11).addr1.__eq__("172.20.10.1") or
			#	pkt.getlayer(Dot11).addr2.__eq__("172.20.10.1")):
			#	print(pkt.summary())
	counter +=1
	print("sleeping now")
	#time.sleep(5)
		
	
	

	

f.close()
#player = vlc.MediaPlayer()
#player.play()
#68:54:FD:E5:B9:DD



