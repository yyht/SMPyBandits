# -*- coding: utf-8 -*-
""" CentralizedMultiplePlay: a multi-player policy where ONE policy is used by a centralized agent; asking the policy to select nbPlayers arms at each step.
"""

__author__ = "Lilian Besson"
__version__ = "0.2"

from .BaseMPPolicy import BaseMPPolicy
from .ChildPointer import ChildPointer


# --- Class for a child player

class CentralizedChildPointer(ChildPointer):
    """ Centralized version of the ChildPointer class."""
    def __init__(self, mother, playerId):
        super(CentralizedChildPointer, self).__init__(mother, playerId)

    def __str__(self):   # Better to recompute it automatically
        return "#{}<CentralizedMultiplePlay: {}>".format(self.playerId + 1, self.mother.player)

    def __repr__(self):  # Better to recompute it automatically
        return "CentralizedMultiplePlay: {}".format(self.mother.player)


# --- Class for the mother

class CentralizedMultiplePlay(BaseMPPolicy):
    """ CentralizedMultiplePlay: a multi-player policy where ONE policy is used by a centralized agent; asking the policy to select nbPlayers arms at each step.
    """

    def __init__(self, nbPlayers, playerAlgo, nbArms, *args, **kwargs):
        """
        - nbPlayers: number of players to create (in self._players).
        - playerAlgo: class to use for every players.
        - nbArms: number of arms, given as first argument to playerAlgo.
        - `*args`, `**kwargs`: arguments, named arguments, given to playerAlgo.

        Examples:

        >>> s = CentralizedMultiplePlay(10, TakeFixedArm, 14)
        >>> s = CentralizedMultiplePlay(NB_PLAYERS, Softmax, nbArms, temperature=TEMPERATURE)

        - To get a list of usable players, use s.childs.
        - Warning: s._players is for internal use ONLY!
        """
        assert nbPlayers > 0, "Error, the parameter 'nbPlayers' for CentralizedMultiplePlay class has to be > 0."
        self.nbPlayers = nbPlayers
        self.player = playerAlgo(nbArms, *args, **kwargs)  # Only one policy
        self.childs = [None] * nbPlayers  # But nbPlayers children
        for playerId in range(nbPlayers):
            self.childs[playerId] = CentralizedChildPointer(self, playerId)
            print(" - One new child, of index {}, and class {} ...".format(playerId, self.childs[playerId]))  # DEBUG
        self.nbArms = nbArms

    def __str__(self):
        return "CentralizedMultiplePlay({} x {})".format(self.nbPlayers, str(self.player))

    # --- Proxy methods

    def _startGame_one(self, playerId):
        if playerId == 0:  # For the first player, run the method
            self.player.startGame()
        # For the other players, nothing to do? Yes

    def _getReward_one(self, playerId, arm, reward):
        self.player.getReward(arm, reward)
        if playerId != 0:  # We have to be sure that the internal player.t is not messed up
            if hasattr(self.player, 't'):
                self.player.t -= 1

    def _choice_one(self, playerId):
        if playerId == 0:  # For the first player, run the method
            self.choices = self.player.choiceMultiple(self.nbPlayers)
            # print("At time t = {} the {} centralized policy chosed arms = {} ...".format(self.player.t, self, self.choices))  # DEBUG
        # For the all players, use the pre-computed result
        return self.choices[playerId]

    def _handleCollision_one(self, playerId, arm):
        raise ValueError("Error: a CentralizedMultiplePlay policy should always aim at orthogonal arms, so no collision should be observed.")
