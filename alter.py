# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-8

from scapy.all import *
import pickle


packets = rdpcap('fact1.pcap')
outfile = open("test.pkl", 'wb')


pkt_data = []
num = 0

for p in packets:
    #count the number of packets
    num = num + 1
    # To store the packet info
    pkt_dict = {}
    # Source MAC address
    src = p.addr2
    # Destination MAC address
    des = p.addr1
    # Packet size
    size = len(p)
    # Polarity flag derived from the QS status, 'to-DS' indicates STA to AP, 'from-DS' indicates AP to STA
    DS = p.FCfield & 0x3

    print("source MAC address: " + src)
    print("destination MAC address: " + des)
    print("packet size: " + str(size))
    print("Polarity: " + str(DS))

    pkt_dict['No'] = num
    pkt_dict['src'] = src
    pkt_dict['des'] = des
    pkt_dict['size'] = size
    pkt_dict['polarity'] = str(DS)

    pkt_data.append(pkt_dict)

pickle.dump(pkt_data, outfile)

# # read python dict back from the file
# test_file = open('test.pkl', 'rb')
# test_data = pickle.load(pkl_file)
# pkl_file.close()

# print(test_data)