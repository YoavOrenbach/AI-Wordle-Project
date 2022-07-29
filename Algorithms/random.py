import random

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__(AlgorithmType.Random)

    def get_action(self, game_logic: AbstractWordleLogic):
        return random.choice(game_logic.get_possible_words())
