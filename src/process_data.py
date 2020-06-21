# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-8
import shutil
from binascii import crc32
from pathlib import Path

from scapy.all import *
import pickle

from scapy.layers.dot11 import Dot11


def is_badFCS(p):
    crc = crc32(bytes(p[Dot11])[:-4]) & 0xFFFFFFFF
    badFCS = (crc != p.fcs)
    return badFCS


def transform_data(filepath, average):
    packets = rdpcap(filepath)
    num = 0
    flag = 0
    size = 0
    pkt_row = []
    for p in packets:
        if is_badFCS(p):
            # num = num + 1
            print("packet " + str(num) + " in " + filepath + ": badFCS")
            break

        # count the number of packets
        num = num + 1
        if num > int(average):
            break
        # Packet size
        size = len(p)
        # Polarity flag derived from the QS status, 'to-DS' indicates STA to AP, 'from-DS' indicates AP to STA
        DS = p.FCfield & 0x3
        if str(DS) == 'to-DS':
            flag = -1
        else:
            flag = 1
        pkt_row.append(flag * size)
    if num < int(average):
        for i in range(int(average) - num):
            pkt_row.append(flag * size)
    return pkt_row


def make_directory(dirpath):
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
    p = Path(dirpath)
    p.mkdir(exist_ok=True, parents=True)


"""
The data under `data_dir` is structured as below:

├── Amazon_Echo
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
├── Google_Home
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
    # Change to your own path where you put the original data
    data_dir = "/home/snape/Documents/comp5703/data/Google_Home/May22"
    # Change to your own path where you put the generated pickle data
    pickle_dir = "/home/snape/Documents/comp5703/pickle_data"

    device_list = ['Amazon_Echo', 'Google_Home']
    average_dict = {
        'Amazon_Echo': 300,
        'Google_Home': 600
    }
    label_dict = {
        'alarm': 0,
        'fact': 1,
        'joke': 2,
        'smart_bulb': 3,
        'smart_plug': 4,
        'time': 5,
        'timer': 6,
        'weather': 7,
        'music_stop': 8,
        'music_play': 9
    }

    for device_dir in device_list:
        if device_dir == 'Amazon_Echo':
            continue
        # device_path = os.path.join(data_dir, device_dir)
        # for distance_dir in os.listdir(device_path):
        #     current_path = os.path.join(device_path, distance_dir)
        print("current path: " + data_dir)
        average_name = device_dir
        average = average_dict[average_name]
        print("average number of " + average_name + " is : " + str(average))

        # Training data
        data = []

        # Training label
        labels = []

        # Create the output directory of generated pickle files
        date = os.path.basename(data_dir)
        out_dir = os.path.join(pickle_dir, device_dir, date)
        print("creating " + out_dir)
        make_directory(out_dir)

        for command in os.listdir(data_dir):
            print("process " + command + "...")
            command_path = os.path.join(data_dir, command)
            for file in os.listdir(command_path):
                filepath = os.path.join(command_path, file)
                pkt_row = transform_data(filepath, average)
                data.append(pkt_row)
                labels.append(label_dict[command])

        data_outfile = open(os.path.join(out_dir, "data.pkl"), 'wb')
        pickle.dump(data, data_outfile)

        labels_outfile = open(os.path.join(out_dir, "labels.pkl"), 'wb')
        pickle.dump(labels, labels_outfile)
