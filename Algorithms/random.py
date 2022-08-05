import random

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle import AbstractWordle
from common import AlgorithmType


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__(AlgorithmType.Random)

    def get_action(self, game: AbstractWordle):
        return random.choice(game.get_possible_words())


class TotalRandom(Algorithm):
    def __init__(self):
        super(TotalRandom, self).__init__(AlgorithmType.TotalRandom)

    def get_action(self, game: AbstractWordle):
        return random.choice(game.get_legal_words())
