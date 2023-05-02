import copy
import math
import random
import numpy as np;
from MonteCarloAlgorithm.bitString.bitString import BitString
class IsingHamiltonian:

    """
    creates the ising hamiltonian
    node connections = the weights of the node connections
    outside affect = the affect of outside bias on nodal connections
    """
    def __init__(self, node_connections=[[()]], outside_affect=np.zeros(1)):

        assert(len(node_connections) == len(outside_affect))
        self.nodeConnections = node_connections
        self.outsideAffect = outside_affect

    """
    calculates the energy of the system given the configuration
    config = a bit string
    """
    def energy(self, config : BitString):
        assert (len(config) == len(self.nodeConnections), "config length does not match")

        energy = np.dot(self.outsideAffect, 2*config.string-1)
        # adds the energy of the effects of each other
        for node in range(len(config)):
            for n in self.nodeConnections[node]:
                if n[0] < node:
                    energy += n[1] * (1 if (config.string[node] == config.string[n[0]]) else -1)


        return energy

    """
    calculates how energy
    """
    def energy_change(self, config : BitString, flipped_index : int, old_energy=float('nan')):

        origin_energy = old_energy if not math.isnan(old_energy) else self.energy(config);
        config.flip(flipped_index);
        new_energy = self.energy(config)
        return new_energy - origin_energy, config, new_energy
    def metropolis_sweep(self, config, temperature=1.0):

        orgEnergy = self.energy(config);

        for sweep in random.sample(list(range(len(config))), len(config)):
            delta_energy, potential_new_config, potential_new_energy = \
                self.energy_change(copy.deepcopy(config), sweep, old_energy=orgEnergy)
            if IsingHamiltonian.make_change(delta_energy, temperature):
                orgEnergy = potential_new_energy
                config = potential_new_config

        return config

    def compute_average_values(self, config : BitString, temperature=1.0):
        energy_sum = 0.0
        energy_squared_sum = 0.0
        magnetization_sum = 0.0
        magnetization_squared_sum = 0.0
        Z_sum = 0.0
        # is Z probability?

        for x in range(2**len(config)):
            config.set_int(x, digits=len(config))
            energy = self.energy(config)
            Z = np.exp(-energy/temperature)
            energy_sum += Z * energy
            energy_squared_sum += energy * energy * Z
            magnetization = np.sum(2*config.string - 1)
            magnetization_sum += magnetization * Z
            magnetization_squared_sum += magnetization * magnetization * Z
            Z_sum += Z

        energy_average = energy_sum / Z_sum
        energy_squared_average = energy_squared_sum / Z_sum
        magnetization_average = magnetization_sum / Z_sum
        magnetization_squared_average = magnetization_squared_sum / Z_sum

        heat_capacity = (energy_squared_average - energy_average**2)/(temperature**2)
        magnetic_susceptibility = (magnetization_squared_average - magnetization_average**2)/(temperature)

        return energy_average, magnetization_average, heat_capacity, magnetic_susceptibility




    @staticmethod
    def make_change(energy_change, temperature):
        return energy_change <= 0 or (np.exp(-energy_change / temperature) > random.random())





