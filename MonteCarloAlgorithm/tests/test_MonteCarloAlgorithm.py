"""
Unit and regression test for the MonteCarloAlgorithm package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import MonteCarloAlgorithm


def test_MonteCarloAlgorithm_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "MonteCarloAlgorithm" in sys.modules
