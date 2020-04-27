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
[link](https://drive.google.com/file/d/1R8ArcEs1Tfqdz4lBKazP0VyzQINaksna/view?usp=sharing)
  
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
│   │   ├── data.pkl
│   │   ├── labels.pkl
│   │   ├── X_test.pkl
│   │   ├── X_training.pkl
│   │   ├── X_val.pkl
│   │   ├── y_test.pkl
│   │   ├── y_training.pkl
│   │   └── y_val.pkl
│   └── Captures_5m
│       ├── data.pkl
│       ├── labels.pkl
│       ├── X_test.pkl
│       ├── X_training.pkl
│       ├── X_val.pkl
│       ├── y_test.pkl
│       ├── y_training.pkl
│       └── y_val.pkl
└── Google_Home
    └── Captures_5m
        ├── data.pkl
        ├── labels.pkl
        ├── X_test.pkl
        ├── X_training.pkl
        ├── X_val.pkl
        ├── y_test.pkl
        ├── y_training.pkl
        └── y_val.pkl
```
### Dataset Description
```
data.pkl : Packet's assigned polarity with packet size sequence
labels.pkl : Corresponding activity's classes sequece
```

## Running
### Reproduce processed dataset
1. Download the original data: [link](https://drive.google.com/open?id=1eqSQzm2VUNQwtWhknwd-AzdB4GGxsZ2D)
2. Unzip the data to somewhere /the/path/to/data/
3. Change the data path in `process_data.py`

```
# Change to your own path where you put the original data
data_dir = "/the/path/to/data/"
# Change to your own path where you put the generated pickle data
pickle_dir = "/the/path/to/pickle_data/"
```
4. Run `python prceoss_data.py`
5. The dataset should be generated as:
```
/the/path/to/pickle_data/
├── Amazon_Echo
│   ├── Captures_10m
│   │   ├── data.pkl
│   │   ├── labels.pkl
│   └── Captures_5m
│       ├── data.pkl
│       ├── labels.pkl
└── Google_Home
    └── Captures_5m
        ├── data.pkl
        ├── labels.pkl
```
### Split dataset into train, validation, test
1. Change the data path in the `utils.py`
```
    aamazon5_data_dir = "/the/path/to/pickle_data/Amazon_Echo/Captures_5m"
    create_dataset(aamazon5_data_dir)

    amazon10_data_dir = "/the/path/to/pickle_data/Amazon_Echo/Captures_10m"
    create_dataset(amazon10_data_dir)

    google_out_dir = "/the/path/to/pickle_data/Google_Home/Captures_5m"
    create_dataset(google_out_dir)
```
2. Run `python utils.py`
3. The dataset should be generated as:
```
/the/path/to/pickle_data/
├── Amazon_Echo
│   ├── Captures_10m
│   │   ├── data.pkl
│   │   ├── labels.pkl
│   │   ├── X_test.pkl
│   │   ├── X_training.pkl
│   │   ├── X_val.pkl
│   │   ├── y_test.pkl
│   │   ├── y_training.pkl
│   │   └── y_val.pkl
│   └── Captures_5m
│       ├── data.pkl
│       ├── labels.pkl
│       ├── X_test.pkl
│       ├── X_training.pkl
│       ├── X_val.pkl
│       ├── y_test.pkl
│       ├── y_training.pkl
│       └── y_val.pkl
└── Google_Home
    └── Captures_5m
        ├── data.pkl
        ├── labels.pkl
        ├── X_test.pkl
        ├── X_training.pkl
        ├── X_val.pkl
        ├── y_test.pkl
        ├── y_training.pkl
        └── y_val.pkl
```
### Training 
1. Change the data path in the `training.py`
```
   # Training Google_Home dataset
   dataset_dir = "/the/path/to/pickle_data/Google_Home/Captures_5m/"
```
2. Run `python training.py`
