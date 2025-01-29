import time
import numpy as np
from scipy.interpolate import make_splrep
from scipy.io import loadmat
import nengo
import numpy as np
import pandas as pd
from nengo.ensemble import Ensemble
from nengo.connection import Connection
from nengo.node import Node

# Model Information
dt = 0.001
dti = 1/dt

# Model Parameters
n_neurons = 49
n_ensemble_neurons = 3000
ensemble_radius = 1     # ? Represents the range of values for the neurons?
ensemble_synapse = 0.025
probe_synapse = 0.01
running_time = 19
training_time = 0.8*running_time # WHen does the model stop learning


with nengo.Network() as model:
    in_node = nengo.Node([0]*n_neurons)
    
    target_node = nengo.Node([0]*2) # expected kinematic output
    inhib_node = nengo.Node(output=lambda t: t >= training_time)

    rep_ens = nengo.Ensemble(n_ensemble_neurons, n_neurons, ensemble_radius)
    recurr_ens = nengo.Ensemble(n_ensemble_neurons, n_neurons, ensemble_radius)
    out_ens = nengo.Ensemble(n_ensemble_neurons, 2, ensemble_radius)
    err_ens = nengo.Ensemble(n_ensemble_neurons, 2, ensemble_radius)

    in_rep_con = nengo.Connection(in_node, rep_ens, ensemble_synapse) # Acts as a low-pass for the spike input
    in_rec_con = nengo.Connection(in_node, recurr_ens, ensemble_synapse)
    rec_rec_con = nengo.Connection(recurr_ens, recurr_ens, synapse=ensemble_synapse, transform=1) # putting transform=-1 bc??
    rec_out_con = nengo.Connection(recurr_ens, out_ens, function=lambda x: [0, 0], learning_rule_type=nengo.PES(learning_rate=2e-4))
    rep_out_con = nengo.Connection(rep_ens, out_ens, function=lambda x: [0, 0], learning_rule_type=nengo.PES(learning_rate=2e-4))
    out_err_con = nengo.Connection(out_ens, err_ens)
    tar_err_con = nengo.Connection(target_node, err_ens, transform=-1)
    err_rep_lrn_con = nengo.Connection(err_ens, rep_out_con.learning_rule) # Connects error ensemble value to learning rule -- analogous to how backprop uses error to follow stochastic gradient in training
    err_rec_lrn_con = nengo.Connection(err_ens, rec_out_con.learning_rule)
    inhib_lrn_con = nengo.Connection(inhib_node, err_ens.neurons, transform=-20 * np.ones((err_ens.n_neurons, 1))) # Inhibit error ensemble once training is done to prevent weight changes after training_time

    p_out = nengo.Probe(out_ens, synapse=probe_synapse)
    p_err = nengo.Probe(err_ens, synapse=probe_synapse)
    
with nengo.Simulator(model, dt=dt, seed=0) as sim:
    sim.run(running_time)
