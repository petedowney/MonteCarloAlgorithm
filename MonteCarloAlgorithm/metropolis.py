

import isingHamiltonian as IsingHamiltonian
import numpy as np

def metropolis_montecarlo(hamiltonian : IsingHamiltonian, config, temperature=1, calc_sweep=1000, pre_calc_sweep=100):

    for x in range(pre_calc_sweep):
        config = hamiltonian.metropolis_sweep(config, temperature)

    energy_samples = np.zeros(calc_sweep)
    energy_samples[0] = np.array([hamiltonian.energy(config)])

    magnetization_samples = np.zeros(calc_sweep)
    magnetization_samples[0] = np.array([np.sum(2*config.string - 1)])


    for x in range(calc_sweep):
        config = hamiltonian.metropolis_sweep(config, temperature)
        energy_samples[x] = hamiltonian.energy(config)
        magnetization_samples[x] = np.sum(2*config.string - 1)

    energy_samples_squared = np.square(energy_samples)
    magnetization_samples_squared = np.square(magnetization_samples)

    average_energy_samples = np.zeros(len(energy_samples))
    average_energy_samples_squared = np.zeros(len(energy_samples))
    average_magnetization_samples = np.zeros(len(energy_samples))
    average_magnetization_samples_squared = np.zeros(len(energy_samples))

    for x in range(1, len(energy_samples)):
        average_energy_samples[x] = np.average(energy_samples[0:x])
        average_energy_samples_squared[x] = np.average(energy_samples_squared[0:x])
        average_magnetization_samples[x] = np.average(magnetization_samples[0:x])
        average_magnetization_samples_squared[x] = np.average(magnetization_samples_squared[0:x])

    return average_energy_samples, average_energy_samples_squared, \
        average_magnetization_samples, average_magnetization_samples_squared
