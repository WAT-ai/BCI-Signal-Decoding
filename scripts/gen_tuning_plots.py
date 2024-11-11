'''
Generates tuning plots for pmd data

MM_S1-velocity
-> velocity_val: [neuron1, neuron2...]

'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

SOURCE_CSV_PATH="/Users/anny/Code/Wat_ai/BCI-Signal-Decoding/Extracted_Data"
DEST_CSV_PATH="/Users/anny/Code/Wat_ai/BCI-Signal-Decoding/processed_data/tuning_plots"
SESSIONS={
    # Session: [number of trials, number of neurons]
    "MM_S1": [496, 94],
    "MT_S1": [419, 49],
    "MT_S2": [646, 46],
    "MT_S3": [652, 57]
    }


def plot_diagram(neuron_num, monkey, independent_var):
    df_kinematics = pd.read_csv(f"{DEST_CSV_PATH}/{independent_var}_{monkey}.csv")
    df_neuron = pd.read_csv(f"{DEST_CSV_PATH}/pmd_{monkey}.csv")
    
    # Scatter plot
    plt.scatter(df_kinematics, df_neuron[f"Neuron{neuron_num}"]) 
    plt.title(f"Tuning plot: Neuron{neuron_num} + {independent_var}")
    plt.xlabel(independent_var)
    plt.ylabel('activation')
    plt.show()

    
# Generates CSV pairings for the tuning plots
def process_data(num_bins):

    for session, details in SESSIONS.items():
        
        base_path = SOURCE_CSV_PATH + "/" + session
        pmd_path = base_path + "/neural_data_PMd"
        kinematics_path = base_path + "/kinematic_data"
        num_trials = details[0]
        num_neurons = details[1]
        
        velocity_list = []
        acceleration_list = []
        neurons_list = [[] for i in range(num_neurons + 1)] # 1 indexed
        
        for i in range(1, num_trials + 1):
            kinematic_data = pd.read_csv(f"{kinematics_path}/reach{i}.csv")
            neuron_data = pd.read_csv(f"{pmd_path}/neural_data_PMd_reach{i}.csv")
            
            total_velocity = (kinematic_data['x_velocity']**2 + kinematic_data['y_velocity']**2)**0.5
            velocity_list.append(total_velocity)
            total_acceleration = (kinematic_data['x_acceleration']**2 + kinematic_data['y_acceleration']**2)**0.5
            acceleration_list.append(total_acceleration)
            
            for neuron_num in range (1, num_neurons + 1):
                neurons_list[neuron_num].append(neuron_data[f"Neuron{neuron_num}"])
            
        result_velocities = pd.concat(velocity_list, ignore_index=True)
        result_acceleration = pd.concat(velocity_list, ignore_index=True)
        result_neurons_list = [pd.concat(neurons_list[i], ignore_index=True) for i in range(1, num_neurons + 1)]
        result_neurons = pd.DataFrame()
        for i in range(num_neurons):
            result_neurons[f"Neuron{i+1}"] = result_neurons_list[i]
        
        
        result_velocities.to_csv(f"{DEST_CSV_PATH}/velocity_{session}.csv", index=False)
        result_acceleration.to_csv(f"{DEST_CSV_PATH}/acceleration_{session}.csv", index=False)
        result_neurons.to_csv(f"{DEST_CSV_PATH}/pmd_{session}.csv", index=False)

        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--combine-bins', type=int, help='Compress bins')
    parser.add_argument('--neuron', type=int)
    parser.add_argument('--monkey', type=str)
    parser.add_argument('-a', action='store_true')
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()
    
    if args.neuron and args.monkey and (args.a or args.v):
        if args.a:
            independent_var = "acceleration"
        elif args.v:
            independent_var = "velocity"
        plot_diagram(args.neuron, args.monkey, independent_var)
    else:
        num_bins = 1
        if args.combine_bins:
            num_bins = args.combine_bins
        process_data(num_bins)


if __name__ == "__main__":
    main()
