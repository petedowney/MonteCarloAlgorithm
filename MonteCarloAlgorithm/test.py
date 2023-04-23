import random

import networkx as nx;
import numpy as np;
import metropolis
from MonteCarloAlgorithm.bitString import BitString
import matplotlib.pyplot as plt

from MonteCarloAlgorithm.isingHamiltonian import IsingHamiltonian

# Number of nodes
N = 8

# Start by setting each edge to -1
Jval = 1

def build_1d_graph(N, Jval):
    """
    Build a 1D graph with a single J value (Jval)
    """
    G = nx.Graph()
    G.add_nodes_from([i for i in range(N)])
    G.add_edges_from([(i,(i+1)% G.number_of_nodes() ) for i in range(N)])
    # G.add_edge(2,5)
    # G.add_edge(4,8)
    # G.add_edge(4,0)
    for e in G.edges:
        G.edges[e]['weight'] = Jval
    return G

def get_IsingHamiltonian(G, mus=None):
    if mus == None:
        mus = np.zeros(len(G.nodes()))

    J = [[] for i in G.nodes()]
    for e in G.edges:
        J[e[0]].append((e[1], G.edges[e]['weight']))
        J[e[1]].append((e[0], G.edges[e]['weight']))
    return IsingHamiltonian(J,mus)


if __name__ == "__main__":
    G = build_1d_graph(N, 1)

    temp = 2.0
    # Now Draw the graph. First we will draw it with the nodes arranged on the circle, then we will draw the same graph
    # with the position of the nodes optimized for easier visualization. Let's make a function for this
    ham = get_IsingHamiltonian(G, mus=[0.1 for i in range(N)])

    config = BitString([0,0,0,0,0,0,0,0])

    energy, energyS, magnet, magnetS = \
        metropolis.metropolis_montecarlo(ham, config,
        temperature=temp, calc_sweep=16000, pre_calc_sweep=2000)

    heat_cap = (energyS - np.square(energy)) / temp**2
    mag_sus = (magnetS - np.square(magnet)) / temp

    fig = plt.figure()
    ax = fig.add_axes([.1, .1, .8, .8])

    ax.plot(range(0, len(heat_cap), 1), energy, label="energy");
    ax.plot(range(0, len(heat_cap), 1), magnet, label="magnetization");
    ax.plot(range(0, len(heat_cap), 1), heat_cap, label="heat capacity");
    ax.plot(range(0, len(heat_cap), 1), mag_sus, label="magnetic sus");
    ax.legend()
    plt.show()

    e, m, hc, ms = ham.compute_average_values(config, temperature=temp)
    print("average energy: simulated: " + str(energy[-1]) + " actual: " + str(e))
    print("average magnetization: simulated: " + str(magnet[-1]) + " actual: " + str(m))
    print("average heat capacity: simulated: " + str(heat_cap[-1]) + " actual: " + str(hc))
    print("average magnetic susceptibility: simulated: " + str(mag_sus[-1]) + " actual: " + str(ms))



