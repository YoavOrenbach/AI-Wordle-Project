import random

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__("Random")
        self.guess_count = 0

    def get_action(self, game_state, game_logic: AbstractWordleLogic):
        self.guess_count += 1
        return random.choice(game_logic.get_possible_words(game_state))

    def reset(self):
        self.guess_count = 0
