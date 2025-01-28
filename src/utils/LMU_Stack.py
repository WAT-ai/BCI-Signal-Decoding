from nengo.networks import EnsembleArray
from nengo.connection import Connection
from nengo.network import Network
from nengo.node import Node
from nengo.utils.filter_design import cont2discrete
import numpy as np

class LMUStack(Network):
    def __init__(self, dim, order = 4, window = 1, n_per_order = 50, dt=0.001):
        # Parameters
        self.dim = dim
        self.q = order
        self.theta = window
        self.n_per_order = n_per_order


        # Complicated LMU Math
        A = np.zeros((self.q, self.q))
        B = np.zeros((self.q, 1))
        for i in range(self.q):
            B[i] = (-1.)**i * (2*i+1)
            for j in range(self.q):
                A[i,j] = (2*i+1)*(-1 if i<j else (-1.)**(i-j+1)) 
        A = A / self.theta
        B = B / self.theta  

        # State-Space Conversion
        self.A_p = A * 0.1 + np.eye(self.q)
        self.B_p = B * 0.1

        # Network Construction
        self.input = Node(size_in=dim)
        self.output = Node(size_in=dim*order)
        self.LMU_ensembles = EnsembleArray(n_neurons=order*n_per_order, 
                                           n_ensembles=dim,
                                           ens_dimensions=order)

        for ens_i, ens in enumerate(self.LMU_ensembles.all_ensembles):
            Connection(self.input[ens_i], ens, transform=self.B_p, synapse=0.1)
            Connection(ens, ens, transform=self.A_p, synapse=0.1)
            Connection(ens, self.output[ens_i * self.q:(ens_i + 1) * self.q])
