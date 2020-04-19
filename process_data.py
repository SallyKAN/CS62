# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-8
import shutil
from pathlib import Path
from scapy.all import *
import pickle


def transform_data(pkt_instance, filepath, average):
    file = os.path.basename(filepath)
    if not file.endswith(".pcap"):
        return
    # filename = os.path.splitext(file)[0]
    print("process " + file)
    packets = rdpcap(filepath)
    num = 0
    flag = 0
    size = 0
    for p in packets:
        pkt_row = []
        if num > int(average):
            break
        # count the number of packets
        num = num + 1
        # To store the packet info
        # pkt_instance = []
        # Source MAC address
        # src = p.addr2
        # Destination MAC address
        # des = p.addr1

        # Packet size
        size = len(p)
        # Polarity flag derived from the QS status, 'to-DS' indicates STA to AP, 'from-DS' indicates AP to STA
        DS = p.FCfield & 0x3

        # print("source MAC address: " + src)
        # print("destination MAC address: " + des)
        # print("packet size: " + str(size))
        # print("Polarity: " + str(DS))

        # pkt_dict['No'] = num
        # pkt_dict['src'] = src
        # pkt_dict['des'] = des
        # pkt_dict['size'] = size
        if str(DS) == 'to-DS':
            flag = -1
        else:
            flag = +1
        pkt_row.append(flag)
        pkt_row.append(size)
        pkt_instance.append(pkt_row)
    if num < int(average):
        for i in range(int(average) - num):
            pkt_instance.append([flag, size])


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


"""
The data under `data_dir` is structured as below:

├── Amazon_Echo
│   ├── Captures_10m
│   │   ├── alarm
│   │   ├── fact
│   │   ├── joke
│   │   ├── smart_bulb
│   │   ├── smart_plug
│   │   ├── time
│   │   ├── timer
│   │   └── weather
│   └── Captures_5m
│       ├── alarm
│       ├── fact
│       ├── joke
│       ├── smart_bulb
│       ├── smart_plug
│       ├── time
│       ├── timer
│       └── weather
├── Google_Home
│   └── Captures_5m
│       ├── alarm
│       ├── fact
│       ├── joke
│       ├── music_play
│       ├── music_stop
│       ├── smart_bulb
│       ├── smart_plug
│       ├── time
│       ├── timer
│       └── weather

"""

if __name__ == '__main__':
    data_dir = "/home/snape/Documents/comp5703/data"
    pickle_dir = "/home/snape/Documents/comp5703/data/pickle_data"
    dir_list = ["Amazon_Echo", "Google_Home"]
    distance_dir_list = ["Captures_10m", "Captures_5m"]
    average_dir = "./Average_Num"
    average_dict = {}

    # Iterate through the data directory by smart speaker type: Google_Home, Amazon_Echo
    for dir in dir_list:
        # Iterate through the distance subdirectory of each data directory: Captures_10m, Captures_5m
        for distance_dir in distance_dir_list:
            current_path = os.path.join(data_dir, dir, distance_dir)
            if os.path.isdir(current_path):
                print("Current path: " + current_path)

                # for each subdirectory,
                # get the average packet size from pre-calculated results put under `./Average_Num` directory
                average_dict[dir] = get_average(dir)
                print(average_dict[dir])

                for command in os.listdir(current_path):
                    command_path = os.path.join(current_path, command)
                    # Create the output direcory of generated pickle files
                    out_dir = os.path.join(pickle_dir, dir, distance_dir, command)
                    print("creating " + out_dir)
                    make_directory(out_dir)
                    print("writing to " + out_dir)
                    average = average_dict[dir][command]
                    print(command + " average number is: " + average)
                    pkt_data = []
                    for file in os.listdir(command_path):
                        filepath = os.path.join(command_path, file)
                        # For each file under command subdirectory
                        # process packets and write as pickle file when the packet number is not greater than the average number
                        transform_data(pkt_data, filepath, average)

                    outfilename = command + ".pkl"
                    outfile = open(os.path.join(out_dir, outfilename), 'wb')
                    pickle.dump(pkt_data, outfile)
