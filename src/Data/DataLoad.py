from scipy.io import loadmat
import numpy as np
import sys
import os

def load_data(key: str):
    if key not in ["MM_S1", "MT_S1", "MT_S2", "MT_S3"]:
        raise Exception(f"Key must be one of: \"MM_S1\", \"MT_S1\", \"MT_S2\", or \"MT_S3\", got \"{key}\"")
    raw_data = loadmat(os.path.abspath("../src/Data/" + key + "_raw.mat"))

    t = raw_data['cont']['t'][0][0][:,0]
    x_pos = raw_data['cont']['pos'][0][0][:,0]
    y_pos = raw_data['cont']['pos'][0][0][:,1]  
    x_vel = raw_data['cont']['vel'][0][0][:,0]
    y_vel = raw_data['cont']['vel'][0][0][:,1]
    x_acl = raw_data['cont']['acc'][0][0][:,0]
    y_acl = raw_data['cont']['acc'][0][0][:,1]
    
    spike_data = raw_data['PMd']['units'][0][0][0]
    spikes = []

    max_time = 0
    for i in range(len(spike_data)):
        spikes.append(spike_data[i]['ts'])
        if np.max(spikes[-1]) > max_time:
            max_time = np.max(spikes[-1])
    ts = np.zeros((int(max_time * 1000), len(spikes)))
    for i in range(ts.shape[1]):
        ts[:,i], _ = np.histogram(spikes[i], bins=np.arange(0, max_time, 0.001))
    return [ts, t, x_pos, y_pos, x_vel, y_vel, x_acl, y_acl]