"""
Unit and regression test for the MonteCarloAlgorithm package.
"""

# Import package, test suite, and other packages as needed
import sys

import MonteCarloAlgorithm.bitstring.bitString as Bitstring
import MonteCarloAlgorithm.metropolis.metropolis as Metropolis
import MonteCarloAlgorithm.isingHamiltonian.isingHamiltonian as IsingHamiltonian

import networkx as nx
import numpy as np

import MonteCarloAlgorithm


def test_MonteCarloAlgorithm_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "MonteCarloAlgorithm" in sys.modules

def test_energy_correct():

    graph = build_1d_graph(6, 1)
    hamiltonian = get_IsingHamiltonian(graph, mus=[.0 for i in range(6)])
    test = Bitstring.BitString([0, 1, 0, 1, 0, 1])
    energy = hamiltonian.energy(test)
    assert(energy == -6)

    test = Bitstring.BitString([0, 1, 1, 1, 1, 1])
    energy = hamiltonian.energy(test)
    assert (energy == 2)

    hamiltonian = get_IsingHamiltonian(graph, mus=[.1 for i in range(6)])
    test = Bitstring.BitString([0, 1, 0, 1, 0, 1])
    energy = hamiltonian.energy(test)
    assert (energy == -6)

    test = Bitstring.BitString([0, 1, 1, 1, 1, 1])
    energy = hamiltonian.energy(test)
    assert (energy == 2.4)

def test_average_calculation():

    graph = build_1d_graph(6, 1)
    hamiltonian = get_IsingHamiltonian(graph, mus=[.0 for i in range(6)])
    test = Bitstring.BitString([0, 1, 0, 1, 0, 1])

    e, m, hc, ms, = hamiltonian.compute_average_values(test, 1.0)

    assert (abs(e) - 5.11 < .01)
    assert (abs(m)  < .00001)
    assert (abs(ms) - .55 < .01)
    assert (abs(hc) - 2.89 < .01)

    e, m, hc, ms, = hamiltonian.compute_average_values(test, 2.0)

    assert (abs(e) - 2.87 < .01)
    assert (abs(m)  < .00001)
    assert (abs(ms) - 1.08 < .01)
    assert (abs(hc) - 1.36 < .01)

    graph = build_1d_graph(8, 1)
    hamiltonian = get_IsingHamiltonian(graph, mus=[.1 for i in range(8)])
    test = Bitstring.BitString([0, 1, 1, 1, 0, 1, 0, 0])

    e, m, hc, ms, = hamiltonian.compute_average_values(test, 2.0)

    assert (abs(e) - 3.73 < .01)
    assert (abs(m) -.15 < .01)
    assert (abs(ms) - 1.47 < .01)
    assert (abs(hc) - 1.65 < .01)


# sometimes fails just cause it probability based
def test_metropolis_sweep():
    graph = build_1d_graph(8, 1)
    hamiltonian = get_IsingHamiltonian(graph, mus=[0.0 for i in range(8)])
    test = Bitstring.BitString([0, 1, 1, 0, 1, 1, 0, 0])

    e, m, hc, ms, = hamiltonian.compute_average_values(test, 2.0)
    el, ml, hcl, msl = Metropolis.metropolis_montecarlo(hamiltonian, test,
                                                        temperature=2.0, calc_sweep=20000, pre_calc_sweep=5000)
    e2, m2, hc2, ms2 = Metropolis.metropolis_to_end_values(el, ml, hcl, msl, 2.0)

    assert(abs(e - e2) < .05)
    assert (abs(m - m2) < .05)
    assert (abs(hc - hc2) < .05)
    assert (abs(ms - ms2) < .05)

    graph = build_1d_graph(8, 1)
    hamiltonian = get_IsingHamiltonian(graph, mus=[0.1 for i in range(8)])
    test = Bitstring.BitString([0, 1, 1, 0, 1, 1, 0, 0])

    e, m, hc, ms, = hamiltonian.compute_average_values(test, 1.0)
    el, ml, hcl, msl = Metropolis.metropolis_montecarlo(hamiltonian, test,
                                                        temperature=1.0, calc_sweep=100000, pre_calc_sweep=5000)
    e2, m2, hc2, ms2 = Metropolis.metropolis_to_end_values(el, ml, hcl, msl, 1.0)

    assert (abs(e - e2) < .05)
    assert (abs(m - m2) < .05)
    assert (abs(hc - hc2) < .05)
    assert (abs(ms - ms2) < .05)



# copied from the jupyter-notebook
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


def get_IsingHamiltonian(G, mus=None):
    if mus == None:
        mus = np.zeros(len(G.nodes()))


    J = [[] for i in G.nodes()]
    for e in G.edges:
        J[e[0]].append((e[1], G.edges[e]['weight']))
        J[e[1]].append((e[0], G.edges[e]['weight']))
    return IsingHamiltonian.IsingHamiltonian(J, mus)
