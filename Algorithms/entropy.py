import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic


class Entropy(Algorithm):
    def __init__(self):
        super(Entropy, self).__init__("Entropy")
        util.raiseNotDefined()

    def get_action(self, game_state, game_logic: AbstractWordleLogic):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()