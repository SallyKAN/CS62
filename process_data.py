# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-8
import shutil
from pathlib import Path
from scapy.all import *
import pickle


def transform_data(filepath, average):
    file = os.path.basename(filepath)
    if not file.endswith(".pcap"):
        return
    # filename = os.path.splitext(file)[0]
    print("process " + file)
    packets = rdpcap(filepath)
    num = 0
    flag = 0
    size = 0
    pkt_row = []
    for p in packets:
        num = num + 1
        if num > int(average):
            break
        # count the number of packets
        # Packet size
        size = len(p)
        # Polarity flag derived from the QS status, 'to-DS' indicates STA to AP, 'from-DS' indicates AP to STA
        DS = p.FCfield & 0x3
        if str(DS) == 'to-DS':
            flag = -1
        else:
            flag = 1
        # pkt_row.append(flag * size)
        pkt_row.append(flag * size)
    if num < int(average):
        for i in range(int(average) - num):
            pkt_row.append(flag * size)
    return pkt_row


#
# def get_average(dirname):
#     average = {}
#     for file in os.listdir(average_dir):
#         if dirname in file:
#             f = open(os.path.join(average_dir, file), "r")
#             for line in f:
#                 (key, val) = line.split("=")
#                 average[key] = val
#     return average


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
        'Amazon_Echo_Captures_5m': 101,
        'Amazon_Echo_Captures_10m': 107,
        'Google_Home_Captures_5m': 366
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
        device_path = os.path.join(data_dir, device_dir)
        for distance_dir in os.listdir(device_path):
            current_path = os.path.join(device_path, distance_dir)
            print("current path: " + current_path)
            average_name = device_dir + "_" + distance_dir
            average = average_dict[average_name]
            print("average number of " + average_name + " is : " + str(average))
            X_training = []
            y_training = []
            # Create the output direcory of generated pickle files
            out_dir = os.path.join(pickle_dir, device_dir, distance_dir)
            print("creating " + out_dir)
            make_directory(out_dir)
            # print("writing to " + out_dir)
            for command in os.listdir(current_path):
                command_path = os.path.join(current_path, command)
                # average = average_dict[dir][command]
                # print(command + " average number is: " + average)
                for file in os.listdir(command_path):
                    filepath = os.path.join(command_path, file)
                    # For each file under command subdirectory
                    # process packets and write as pickle file when the packet number is not greater than the average number
                    pkt_row = transform_data(filepath, average)
                    X_training.append(pkt_row)
                    y_training.append(label_dict[command])

            X_training_outfile = open(os.path.join(out_dir, "X_training.pkl"), 'wb')
            pickle.dump(X_training, X_training_outfile)

            y_training_outfile = open(os.path.join(out_dir, "y_training.pkl"), 'wb')
            pickle.dump(y_training, y_training_outfile)
