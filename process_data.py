# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-8
import shutil
from pathlib import Path
import os
from scapy.all import *
import pickle


def write_pickle(filepath, outdir, average):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    packets = rdpcap(filepath)
    outfilename = filename + ".pkl"
    outfile = open(os.path.join(outdir, outfilename), 'wb')
    pkt_data = []
    num = 0
    flag = 0
    for p in packets:
        if num > int(average):
            break
        # count the number of packets
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

        # print("source MAC address: " + src)
        # print("destination MAC address: " + des)
        # print("packet size: " + str(size))
        # print("Polarity: " + str(DS))

        pkt_dict['No'] = num
        pkt_dict['src'] = src
        pkt_dict['des'] = des
        pkt_dict['size'] = size
        if str(DS) == 'to-DS':
            flag = -1
        else:
            flag = +1
        pkt_dict['polarity'] = flag

        pkt_data.append(pkt_dict)

    pickle.dump(pkt_data, outfile)


def get_average(dirname):
    average = {}
    for file in os.listdir(average_dir):
        if dirname in file:
            f = open(os.path.join(average_dir, file), "r")
            for line in f:
                (key, val) = line.split("=")
                average[key] = val
    return average


def make_directory(dirpath):
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
    p = Path(dirpath)
    p.mkdir(exist_ok=True, parents=True)


if __name__ == '__main__':
    data_dir = "/home/snape/Documents/comp5703/data"
    pickle_dir = "/home/snape/Documents/comp5703/data/pickle_data"
    dir_list = ["Amazon_Echo"]
    distance_dir_list = ["Captures_10m", "Captures_5m"]
    average_dir = "./Average_Num"
    # dir_list.append(subdir)
    average_dict = {}
    for dir in dir_list:
        for distance_dir in distance_dir_list:
            current_path = os.path.join(data_dir, dir, distance_dir)
            if os.path.isdir(current_path):
                print("Current path: " + current_path)
                # current_path = os.path.join(data_dir, dir)
                average_dict[dir] = get_average(dir)
                print(average_dict[dir])
                for command in os.listdir(current_path):
                    command_path = os.path.join(current_path, command)
                    out_dir = os.path.join(pickle_dir, dir, distance_dir, command)
                    print("creating " + out_dir)
                    make_directory(out_dir)
                    print("writing to " + out_dir)
                    for file in os.listdir(command_path):
                        filepath = os.path.join(command_path, file)
                        average = average_dict[dir][command]
                        # print(command + " average number is: " + average)
                        write_pickle(filepath, out_dir, average)
