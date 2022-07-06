import random

from Algorithms.algorithm import Algorithm


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__("Random")
        self.guess_count = 0

    def get_action(self, game_state):
        if self.guess_count == 0:
            self.guess_count += 1
            return random.choice(game_state.get_possible_guesses())
        self.guess_count += 1
        game_state.filter_wordle_guesses()
        return random.choice(game_state.get_possible_guesses())

    def reset(self):
        self.guess_count = 0
