import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic

# Added
from game_visible_state import GameVisibleState


class Minimax(Algorithm):
    def __init__(self):
        super(Minimax, self).__init__("MiniMax")
        self.guess_count = 0

    def get_action(self, game_state, game_logic: AbstractWordleLogic):
        """comments for myself:
        game state is """
        game_state = GameVisibleState()
        high_score = float('-inf')


    def reset(self):
        util.raiseNotDefined()
