# Load relevant libraries. If you have errors you probably need to install them into your conda env
#%matplotlib inline

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
# import montecarlo
import random
import networkx as nx
import random
import scipy
random.seed(2)

import metropolis
from MonteCarloAlgorithm.bitString import BitString
from MonteCarloAlgorithm.isingHamiltonian import IsingHamiltonian

# this is just included to fix a problem with printing later on
plt.bar(range(20), range(20));
plt.show()

# Number of nodes
N = 8

# Start by setting each edge to -1
Jval = 1


# Create graph
def build_1d_graph(N, Jval):
    """
    Build a 1D graph with a single J value (Jval)
    """
    G = nx.Graph()
    G.add_nodes_from([i for i in range(N)])
    G.add_edges_from([(i, (i + 1) % G.number_of_nodes()) for i in range(N)])
    # G.add_edge(2,5)
    # G.add_edge(4,8)
    # G.add_edge(4,0)
    for e in G.edges:
        G.edges[e]['weight'] = Jval
    return G


def draw_my_graph(G, conf=None, circ=True):
    """
    Draw our graph!
    """
    N = len(G.nodes())
    if conf == None:
        conf = BitString(np.zeros(N))


    plt.figure(1)
    # nx.draw(G, with_labels=True, font_weight='bold', pos=nx.circular_layout(G))

    pos = nx.spring_layout(G)
    if circ == True:
        pos = nx.circular_layout(G)

    # edge_labels = dict([((n1, n2), d['weight'])
    #                     for n1, n2, d in G.edges(data=True)])
    weights = [G[u][v]['weight'] for u, v in G.edges]

    nx.draw(
        G, pos, edge_color='black',
        # width=2,
        linewidths=2,
        node_size=200, node_color=conf.string, alpha=.5,
        labels={node: node for node in G.nodes()},
        width=weights
    )

    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # plt.figure(2)
    # nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


# Now let's define a function that converts a graph into a simpler IsingHamiltonian object
def get_IsingHamiltonian(G, mus=None):
    if mus == None:
        mus = np.zeros(len(G.nodes()))


    J = [[] for i in G.nodes()]
    for e in G.edges:
        J[e[0]].append((e[1], G.edges[e]['weight']))
        J[e[1]].append((e[0], G.edges[e]['weight']))
    return IsingHamiltonian(J, mus)


G = build_1d_graph(N, Jval)

# Now Draw the graph. First we will draw it with the nodes arranged on the circle, then we will draw the same graph
# with the position of the nodes optimized for easier visualization. Let's make a function for this
draw_my_graph(G)

ham = get_IsingHamiltonian(G, mus=[.1 for i in range(N)])

# Number of nodes
N = 8

# Start by setting each edge to -1
Jval = 1


# Create graph
def build_1d_graph(N, Jval):
    """
    Build a 1D graph with a single J value (Jval)
    """
    G = nx.Graph()
    G.add_nodes_from([i for i in range(N)])
    G.add_edges_from([(i, (i + 1) % G.number_of_nodes()) for i in range(N)])
    # G.add_edge(2,5)
    # G.add_edge(4,8)
    # G.add_edge(4,0)
    for e in G.edges:
        G.edges[e]['weight'] = Jval
    return G


def draw_my_graph(G, conf=BitString(np.zeros(N)), circ=True):
    """
    Draw our graph!
    """


    plt.figure(1)
    # nx.draw(G, with_labels=True, font_weight='bold', pos=nx.circular_layout(G))

    pos = nx.spring_layout(G)
    if circ == True:
        pos = nx.circular_layout(G)

    # edge_labels = dict([((n1, n2), d['weight'])
    #                     for n1, n2, d in G.edges(data=True)])
    weights = [G[u][v]['weight'] for u, v in G.edges]

    nx.draw(
        G, pos, edge_color='black',
        # width=2,
        linewidths=2,
        node_size=200, node_color=conf.string, alpha=.5,
        labels={node: node for node in G.nodes()},
        width=weights
    )

    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # plt.figure(2)
    # nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


# Now let's define a function that converts a graph into a simpler IsingHamiltonian object
def get_IsingHamiltonian(G, mus=None):
    if mus == None:
        mus = np.zeros(len(G.nodes()))

    J = [[] for i in G.nodes()]
    for e in G.edges:
        J[e[0]].append((e[1], G.edges[e]['weight']))
        J[e[1]].append((e[0], G.edges[e]['weight']))
    return IsingHamiltonian(J, mus)


G = build_1d_graph(N, Jval)

# Now Draw the graph. First we will draw it with the nodes arranged on the circle, then we will draw the same graph
# with the position of the nodes optimized for easier visualization. Let's make a function for this
draw_my_graph(G)

ham = get_IsingHamiltonian(G, mus=[.1 for i in range(N)])

conf = BitString(np.zeros(N))
conf.set_string([0, 0, 0, 0, 0, 0, 1, 1])
# conf.initialize(M=2)
draw_my_graph(G,conf=conf)

conf.set_string([0, 0, 0, 0, 0, 0, 1, 1])

Ei = ham.energy(conf)
Pi = np.e**(-Ei)
print(" Energy of      ", conf.string, " is ", Ei)
# print(" Probability of ", conf.config, " is ", Pi)
assert(abs(Ei-3.6) < 1e-12)

conf.set_int(106, 8)
print(" Index 16 = ", conf)
Ei = ham.energy(conf)
print(" Energy of      ", conf.string, " is ", Ei)
assert(abs(Ei+4.0) < 1e-12)

# Define a new configuration instance for a 6-site lattice
N = 6
conf = BitString(np.zeros(N))

# Define a new hamiltonian values
G = build_1d_graph(N, 2)
draw_my_graph(G, conf)
ham = get_IsingHamiltonian(G, mus=[1.1 for i in range(N)])

# Compute the average values for Temperature = 1
E, M, HC, MS = ham.compute_average_values(conf, temperature=1.0)


print(" E  = %12.8f" %E)
print(" M  = %12.8f" %M)
print(" HC = %12.8f" %HC)
print(" MS = %12.8f" %MS)

assert(np.isclose(E,  -11.90432015))
assert(np.isclose(M,  -0.02660820))
assert(np.isclose(HC, 0.59026994))
assert(np.isclose(MS, 0.05404295))

N = 8

# Initialize lists that we will fill with the property vs. temperature data
e_list = []
e2_list = []
m_list = []
m2_list = []
T_list = []

# Create BitString
conf = BitString(np.zeros(N))
print(" Number of configurations: ", 2**len(conf))

# Define a new hamiltonian values
G = build_1d_graph(N, 1)
draw_my_graph(G, conf)
ham = get_IsingHamiltonian(G, mus=[.1 for i in range(N)])

for Ti in range(1, 100):
    T = .1 * Ti

    E, M, HC, MS = ham.compute_average_values(conf, T)

    e_list.append(E)
    m_list.append(M)
    e2_list.append(HC)
    m2_list.append(MS)
    T_list.append(T)

plt.plot(T_list, e_list, label="energy");
plt.plot(T_list, m_list, label="magnetization");
plt.plot(T_list, m2_list, label="Susceptibility");
plt.plot(T_list, e2_list, label="Heat Capacity");
plt.legend();

Tc_ind = np.argmax(m2_list)
print(" Critical Temperature: %12.8f " % (T_list[Tc_ind]))
print("     E:  %12.8f" % (e_list[Tc_ind]))
print("     M:  %12.8f" % (m_list[Tc_ind]))
print("     HC: %12.8f" % (e2_list[Tc_ind]))
print("     MS: %12.8f" % (m2_list[Tc_ind]))
Tc2 = T_list[np.argmax(e2_list)]
print(" Critical Temperature: %12.8f" % (Tc2))

print(" E = %12.8f @ T = %12.8f" % (e_list[T_list.index(2.00)], 2.0))


print ("-----------------------------")
# Initialize BitString

conf = BitString(np.zeros(N))
conf = BitString([0, 1, 1, 0, 1, 1, 0, 0])

# run montecarlo
E, M, EE, MM = \
    metropolis.metropolis_montecarlo(ham, conf,
    temperature=2, calc_sweep=8000, pre_calc_sweep=2000)

HC = (EE[-1] - E[-1] * E[-1]) / T / T
MS = (MM[-1] - M[-1] * M[-1]) / T
print("     E:  %12.8f" % (E[-1]))
print("     M:  %12.8f" % (M[-1]))
print("     HC: %12.8f" % (HC))
print("     MS: %12.8f" % (MS))
# Exact values
# E:   -3.73231850
# M:    0.14658168
# EE:   1.64589165
# MM:   1.46663062

plt.plot(E, label="energy");
plt.plot([-3.73231850] * len(E), label="exact");
plt.legend();

# Eexact, M, HC, MS = ham1d.compute_average_values(conf, 2)
# print(Eexact)
# Eexact, M, HC, MS = ham.compute_average_values(conf, 2)
# print(Eexact)

def run_T_scan(ham, conf, Tstep=.1, Tmax=10, n_mc_steps=2000, n_burn=200):
    N = len(conf.config)

    T_range = []
    e_vs_T = []
    m_vs_T = []
    ee_vs_T = []
    mm_vs_T = []
    heat_cap_vs_T = []
    magn_sus_vs_T = []

    T = 1 * Tstep
    for Ti in range(int(Tmax / Tstep)):
        T += Tstep
        conf = BitString(np.zeros(N))
        conf.initialize(M=int(N / 2))
        # E, M, HC, MS = compute_montecarlo(ham, conf, T, n_mc_steps, n_burn, plot=False)
        e, m, ee, mm = \
    metropolis.metropolis_montecarlo(ham, conf,
    temperature=2, calc_sweep=8000, pre_calc_sweep=2000)
        T_range.append(T)

        e_vs_T.append(e[-1])
        m_vs_T.append(m[-1])
        ee_vs_T.append(ee[-1])
        mm_vs_T.append(mm[-1])

        E = e[-1]
        EE = ee[-1]
        M = m[-1]
        MM = mm[-1]
        heat_cap = (EE - E * E) / (T * T)
        magn_sus = (MM - M * M) / T
        heat_cap_vs_T.append(heat_cap)
        magn_sus_vs_T.append(magn_sus)

        # print("T= %12.8f E= %12.8f M=%12.8f Heat Capacity= %12.8f Mag. Suscept.=%12.8f" %(T, e[-1], m[-1], heat_cap, magn_sus))

    plt.plot(T_range, e_vs_T, label="Energy")
    plt.plot(T_range, m_vs_T, label="Magnetization")
    plt.plot(T_range, magn_sus_vs_T, label="Susceptibility")
    plt.plot(T_range, heat_cap_vs_T, label="Heat Capacity")
    plt.legend()
