# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-8
import shutil
from pathlib import Path

import numpy as np
from scapy.all import *
import pickle
from sklearn.model_selection import train_test_split


def transform_data(filepath, average):
    file = os.path.basename(filepath)
    # if not file.endswith(".pcap"):
    #     print(filepath)
    #     return [0] * average
    packets = rdpcap(filepath)
    num = 0
    flag = 0
    size = 0
    pkt_row = []
    for p in packets:
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
    # Change to your own path where you put the original data
    data_dir = "/home/snape/Documents/comp5703/data"
    # Change to your own path where you put the generated pickle data
    pickle_dir = "/home/snape/Documents/comp5703/pickle_data"

    average_dict = {
        'Amazon_Echo_Captures_5m': 120,
        'Amazon_Echo_Captures_10m': 120,
        'Google_Home_Captures_5m': 600
    }
    label_dict = {
        'alarm': 1,
        'fact': 2,
        'joke': 3,
        'smart_bulb': 4,
        'smart_plug': 5,
        'time': 6,
        'timer': 7,
        'weather': 8,
        'music_stop': 9,
        'music_play': 10
    }

    for device_dir in os.listdir(data_dir):
        if device_dir != 'Google_Home':
            continue
        device_path = os.path.join(data_dir, device_dir)
        for distance_dir in os.listdir(device_path):
            current_path = os.path.join(device_path, distance_dir)
            print("current path: " + current_path)
            average_name = device_dir + "_" + distance_dir
            average = average_dict[average_name]
            print("average number of " + average_name + " is : " + str(average))

            # Training data
            data = []

            # Training label
            labels = []

            # Create the output directory of generated pickle files
            out_dir = os.path.join(pickle_dir, device_dir, distance_dir)
            print("creating " + out_dir)
            make_directory(out_dir)

            for command in os.listdir(current_path):
                print("process " + command + "...")
                command_path = os.path.join(current_path, command)
                for file in os.listdir(command_path):
                    filepath = os.path.join(command_path, file)
                    pkt_row = transform_data(filepath, average)
                    data.append(pkt_row)
                    labels.append(label_dict[command])

            data_outfile = open(os.path.join(out_dir, "data.pkl"), 'wb')
            pickle.dump(data, data_outfile)

            labels_outfile = open(os.path.join(out_dir, "labels.pkl"), 'wb')
            pickle.dump(labels, labels_outfile)

            # create_dataset(data, labels, out_dir)
