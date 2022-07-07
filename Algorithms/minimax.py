import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic


class Minimax(Algorithm):
    def __init__(self):
        super(Minimax, self).__init__("MiniMax")
        util.raiseNotDefined()

    def get_action(self, game_state, game_logic: AbstractWordleLogic):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()
