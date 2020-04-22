# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-22
import os

from scapy.all import rdpcap


def get_stats(dir):
    instance_sum = 0
    pkt_sum = 0
    for root, dirs, files in os.walk(dir):
        instance_sum += len(files)
        for file in files:
            filepath = root + "/" + file
            print("process " + filepath)
            if not file.endswith(".pcap"):
                continue
            packets = rdpcap(filepath)
            pkt_sum += len(packets)
    mean = pkt_sum / instance_sum
    return instance_sum, pkt_sum, mean


if __name__ == "__main__":
    # Change to your own path where you put the original data
    data_dir = "/home/snape/Documents/comp5703/data"
    for device_dir in os.listdir(data_dir):
        print(device_dir)
        first_path = os.path.join(data_dir, device_dir)
        for distance_dir in os.listdir(first_path):
            print(distance_dir)
            second_path = os.path.join(first_path, distance_dir)
            instance_sum, pkt_sum, mean = get_stats(second_path)
            print("statics of " + device_dir + "_" + distance_dir + " :")
            print("instance_sum: " + str(instance_sum))
            print("packet_sum: " + str(pkt_sum))
            print("mean: " + str(mean) + "\n")
