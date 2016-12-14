# -*- coding: utf-8 -*-
""" Base class for any policy.

- If rewards are not in [0, 1], be sure to give the lower value and the amplitude. Eg, if rewards are in [-3, 3], lower = -3, amplitude = 6.
"""

__author__ = "Lilian Besson"
__version__ = "0.3"

import numpy as np


class BasePolicy(object):
    """ Base class for any policy."""

    def __init__(self, nbArms, lower=0., amplitude=1.):
        self.nbArms = nbArms
        self.lower = lower
        self.amplitude = amplitude
        self.t = -1
        self.pulls = np.zeros(nbArms, dtype=int)
        self.rewards = np.zeros(nbArms)

    def __str__(self):
        return self.__class__.__name__

    def startGame(self):
        self.t = 0
        self.pulls.fill(0)
        self.rewards.fill(0)

    def getReward(self, arm, reward):
        self.t += 1
        self.pulls[arm] += 1
        self.rewards[arm] += (reward - self.lower) / self.amplitude

    def choice(self):
        raise NotImplementedError("This method choice() has to be implemented in the child class inheriting from BasePolicy.")

    def choiceWithRank(self, rank=1):
        raise NotImplementedError("This method choiceWithRank(rank) has to be implemented in the child class inheriting from BasePolicy.")