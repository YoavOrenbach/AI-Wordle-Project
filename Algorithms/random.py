import random

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__(AlgorithmType.Random)
        self.guess_count = 0

    def get_action(self, game_logic: AbstractWordleLogic):
        self.guess_count += 1
        return random.choice(game_logic.get_possible_words())

    def reset(self):
        self.guess_count = 0
