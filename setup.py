import pathlib
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
      'numpy',
      'networkx'
]

setup(
    name='MonteCarloAlgorithm',
    version='',
    packages=['MonteCarloAlgorithm', 'MonteCarloAlgorithm.tests', 'MonteCarloAlgorithm.bitstring',
              'MonteCarloAlgorithm.metropolis', 'MonteCarloAlgorithm.isingHamiltonian'],
    url='',
    license='',
    author='peter',
    author_email='',
    #install_requires=INSTALL_REQUIRES,
    description=''
)
