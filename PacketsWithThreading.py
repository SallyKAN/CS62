import threading as thr
import pyttsx3

from scapy.all import *

f = open("alexa.txt", "r")
language = 'en'
counter = 1
engine = pyttsx3.init()
changeName = 'sequence'
fs = open("cities.txt", "r")

def sniffPkts():
   tcp = sniff(iface="en0", session=TCPSession, timeout=30, monitor=True)
   _dir = 'CapTwo'
   name = str(changeName) + str(counter) +'.pcap'
   _dir = os.path.join(_dir, '%s' %changeName)
   if not os.path.exists(_dir):
      os.makedirs(_dir)
   _dir = os.path.join(_dir, '%s' % name)
   
   for pkt in tcp:
      #print(pkt.getlayer(Dot11Elt))
      # if (pkt.haslayer(Dot11QoS) or pkt.haslayer(Dot11ProbeReq) or pkt.haslayer(Dot11ProbeResp)):
      #  #print("got layers")
      #  if (pkt.getlayer(Dot11).addr1.__eq__("f4:f5:d8:d0:2d:b2") or
      #  pkt.getlayer(Dot11).addr2.__eq__("f4:f5:d8:d0:2d:b2") or
      #  pkt.getlayer(Dot11).addr3.__eq__("f4:f5:d8:d0:2d:b2") or
      #  pkt.getlayer(Dot11).addr1.__eq__("d0:73:d5:36:d7:f3") or
      #  pkt.getlayer(Dot11).addr2.__eq__("d0:73:d5:36:d7:f3") or
      #  pkt.getlayer(Dot11).addr3.__eq__("d0:73:d5:36:d7:f3") or
      #  pkt.getlayer(Dot11).addr1.__eq__("ac:84:c6:68:6a:ad") or
      #  pkt.getlayer(Dot11).addr2.__eq__("ac:84:c6:68:6a:ad") or
      #  pkt.getlayer(Dot11).addr3.__eq__("ac:84:c6:68:6a:ad") or
      #  pkt.getlayer(Dot11).addr1.__eq__("B0:C5:54:47:4E:96") or
      #  pkt.getlayer(Dot11).addr2.__eq__("B0:C5:54:47:4E:96") or
      #  pkt.getlayer(Dot11).addr3.__eq__("B0:C5:54:47:4E:96")):
      wrpcap(_dir, pkt, append=True)
   #  print(pkt)

def executeVoiceCmd():
   #print("executeVoiceCmd called")
   f = open("alexa.txt", "r")
   for cmd in f:
      if (counter%2 == 0):
         cmd = cmd + " off"
      else:
         cmd = cmd + " on"
      print(cmd)
      engine.say(cmd)
      engine.runAndWait()
      time.sleep(2)

while counter <= 200:
   t1 = thr.Thread(target=sniffPkts)
   t2 = thr.Thread(target=executeVoiceCmd)
   t1.start()
   t2.start()
   t1.join()
   t2.join()
   counter +=1
   time.sleep(5)
   f.close()

