'''
Generates tuning plots
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

CSV_FILE_PATH="/Users/anny/Code/Wat_ai/BCI-Signal-Decoding/Extracted_Data"

df = pd.read_csv('your_file.csv')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='Path to the file')
    args = parser.parse_args()
    
    print(f"File path provided: {args.file_path}")

if __name__ == "__main__":
    main()
