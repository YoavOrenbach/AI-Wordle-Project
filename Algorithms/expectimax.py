import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType


class Expectimax(Algorithm):
    def __init__(self):
        super(Expectimax, self).__init__(AlgorithmType.Expectimax)
        util.raiseNotDefined()

    def get_action(self, game_state, game_logic: AbstractWordleLogic):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()
