# CS62
Capstone Project
(Keep updating)

## Requirements
`git clone https://github.com/SallyKAN/CS62.git`

`cd ./CS62`

`pip install requirements.txt`
## Dataset
The original traffic traces (in pcap format) can be download from here:
[link](https://drive.google.com/open?id=1eqSQzm2VUNQwtWhknwd-AzdB4GGxsZ2D)

The processed data for training and testing (in pickle format) can be download from here:
  
### Dataset Structure

The original traffic traces

```
data
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
```
The processed data
```
pickle_data
├── Amazon_Echo
│   ├── Captures_10m
│       ├── X_training.pkl
│       ├── y_training.pkl
│       ├── X_test.pkl
│       ├── y_test.pkl
│   └── Captures_5m
│       ├── X_training.pkl
│       ├── y_training.pkl
│       ├── X_test.pkl
│       ├── y_test.pkl
├── Google_Home
│   └── Captures_5m
│       ├── X_training.pkl
│       ├── y_training.pkl
│       ├── X_test.pkl
│       ├── y_test.pkl

```
### Dataset Description
```
X_<type of evaluation>.pkl : Packet's assigned polarity with packet size sequence
y_<type of evaluation>.pkl : Corresponding activity's classes sequece
```

## Running and Reproduce
1. Download the original data: [link](https://drive.google.com/open?id=1eqSQzm2VUNQwtWhknwd-AzdB4GGxsZ2D)
2. Unzip the data to somewhere /the/path/to/data/
3. Change the data path in `process_data.py`

```
# Change to your own path where you put the original data
data_dir = "/the/path/to/data/"
# Change to your own path where you put the generated pickle data
pickle_dir = "/the/path/to/data/"
```
4. run `python prceoss_data.py`