import sys, os
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(parent, 'risk'))

import numpy as np
import pytest

import risk_utils


def test_diceroll_1vs1():
    iterations = 100_000
    defender_wins = 0
    for i in range(iterations):
        attacker, defender = risk_utils.diceroll(2, 1)
        if defender == 1:
            defender_wins += 1

    # 21/36 means defender wins in 21 cases out of 36 with 1 dice vs 1 dice
    np.testing.assert_almost_equal(float(defender_wins)/iterations,
                                   21/36., decimal=2)


def test_diceroll_2vs1():
    # defender wins probablity 0.4212962962962963
    iterations = 100_000
    defender_wins = 0
    for i in range(iterations):
        attacker, defender = risk_utils.diceroll(3, 1)
        if defender == 1:
            defender_wins += 1

    # 21/36 means defender wins in 21 cases out of 36 with 1 dice vs 1 dice
    np.testing.assert_almost_equal(float(defender_wins)/iterations,
                                   0.4212962962962963,
                                   decimal=2)


def test_diceroll_3vs1():
    # defender wins probablity 0.3402777777777778
    iterations = 100_000
    defender_wins = 0
    for i in range(iterations):
        attacker, defender = risk_utils.diceroll(4, 1)
        if defender == 1:
            defender_wins += 1

    # 21/36 means defender wins in 21 cases out of 36 with 1 dice vs 1 dice
    np.testing.assert_almost_equal(float(defender_wins)/iterations,
                                   0.3402777777777778,
                                   decimal=2)


def test_diceroll_1vs2():
    # defender wins probablity 0.3402777777777778
    iterations = 100_000
    defender_wins = 0
    for i in range(iterations):
        attacker, defender = risk_utils.diceroll(2, 2)
        if defender == 2:
            defender_wins += 1

    # 21/36 means defender wins in 21 cases out of 36 with 1 dice vs 1 dice
    np.testing.assert_almost_equal(float(defender_wins)/iterations,
                                   0.7454,
                                   decimal=2)

def test_diceroll_not_enough_attacker_troops():
    with pytest.raises(ValueError):
        assert risk_utils.diceroll(1, 1)


def test_diceroll_not_defenders():
    with pytest.raises(ValueError):
        assert risk_utils.diceroll(2, 0)