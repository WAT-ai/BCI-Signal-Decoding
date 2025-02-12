# Important libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio

def GetDataAndBin(monkey_id):
    mat_contents = sio.loadmat(r"..\\..\\Data Extraction\\"+monkey_id+"_raw.mat")
    
    acceleration_data = mat_contents["cont"]["acc"].item()
    position_data = mat_contents["cont"]["pos"].item()
    vel_data = mat_contents["cont"]["vel"].item()
    timepoints_data = mat_contents["cont"]["t"].item().squeeze()
    
    spiking_timepoints = mat_contents["PMd"]["units"].item()["ts"].squeeze()
    n_neurons = len(spiking_timepoints)
    
    # Binning Spike Data
    start_time = timepoints_data[0] 
    end_time = timepoints_data[-1]
    bin_size = 0.01

    edges=np.arange(start_time, end_time, bin_size) #Get edges of time bins
    num_bins= edges.shape[0]-1 #Number of bins

    neural_data=np.empty([num_bins, n_neurons]) #Initialize array for binned neural data

    #Count number of spikes in each bin for each neuron, and put in array
    for i in range(n_neurons):
        neural_data[:,i]=np.histogram(spiking_timepoints[i].squeeze(), edges)[0]
        
        
        
    downsample_idxs = np.arange(0 , timepoints_data.shape[0], 10) #Get the idxs of values we are going to include after downsampling

    # Binning Kinematic Data
    downsampled_acc = vel_data[downsample_idxs,:] #Get the downsampled outputs
    downsampled_time = timepoints_data[downsample_idxs] #Get the downsampled output times

    output_dim = 2  # Kin (x,y)
    outputs_binned = np.empty([num_bins, output_dim]) #Initialize matrix of binned outputs

    #Loop through bins, and get the mean outputs in those bins
    for i in range(num_bins): #Loop through bins
        
            idxs=np.where( (downsampled_time>=edges[i]) & (downsampled_time<edges[i+1]) )[0] # Getting any time samples from [ edges[i], edges[i+1] )
            
            for j in range(output_dim): #Loop through output features
                
                if len(idxs)<=1:
                    outputs_binned[i,j] = downsampled_acc[i,j]
                else:
                    outputs_binned[i,j] = np.mean(downsampled_acc[idxs,j])


    return neural_data, outputs_binned, n_neurons