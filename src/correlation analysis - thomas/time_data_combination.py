import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

time_datasets = [
    "timestamps_data", "neural_data_PMd", 
     "kinematic_data", "target_on"
]

time_dfs = []

for dataset in time_datasets:
    directory = f"../../Data Extraction/Extracted Data/MM_S1_processed/{dataset}"

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

time_bin_df.to_csv("time_bin_info.csv", index=False)