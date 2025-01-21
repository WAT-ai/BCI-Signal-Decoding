'''
This file combines all time bin based data from a dataset (MM_S1_processed, MT_S1_processed, MT_S2_processed, or MT_S3_processed)
It will concatenate all of the time bins for all reaches in the dataset, each being their own row
This includes the time of bin, neuron firing data per neuron, kinematic data (location, velocity, acceleration), and whether or not the target was on
Exports to "time_bin_info.csv" in your current folder
'''



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

time_datasets = [
    "timestamps_data", "neural_data_PMd", 
     "kinematic_data", "target_on"
]

dataset_path = "Data Extraction/Extracted Data/MM_S1_processed"

time_dfs = []

for dataset in time_datasets:
    directory = f"{dataset_path}/{dataset}"

    # Get a sorted list of CSV files in numerical order
    files = sorted(
        [file for file in os.listdir(directory) if file.endswith(".csv")],
        key=lambda x: int(x.split('reach')[1].split('.csv')[0])
    )

    # List to store each dataframe
    dataframes = []

    # Loop through each file in the sorted list
    for file in files:
        file_path = os.path.join(directory, file)
        # Read CSV and add to the list
        dataframes.append(pd.read_csv(file_path))

    # Concatenate all dataframes in the list into a single dataframe
    time_dfs.append(pd.concat(dataframes, ignore_index=True))

time_bin_df = pd.concat(time_dfs, axis=1)

time_bin_df = time_bin_df.drop("time_stamps", axis=1)

time_bin_df.to_csv("time_bin_info2.csv", index=False)