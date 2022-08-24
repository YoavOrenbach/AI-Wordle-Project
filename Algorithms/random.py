import random

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle import AbstractWordle
from common import AlgorithmType


class Random(Algorithm):
    """Random agent"""
    def __init__(self):
        """Initializes the Random agent class"""
        super(Random, self).__init__(AlgorithmType.Random)

    def get_action(self, game: AbstractWordle):
        """Returns the Random agent action"""
        return random.choice(game.get_possible_words())


class TotalRandom(Algorithm):
    """Total Random agent"""
    def __init__(self):
        """Initializes the Total Random agent class"""
        super(TotalRandom, self).__init__(AlgorithmType.TotalRandom)

    def get_action(self, game: AbstractWordle):
        """Returns the Total Random agent action"""
        return random.choice(game.get_legal_words())
