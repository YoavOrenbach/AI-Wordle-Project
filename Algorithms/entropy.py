import math

import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import Word
from game_visible_state import GameVisibleState


class Entropy(Algorithm):
    def __init__(self):
        super(Entropy, self).__init__("Entropy")

    def get_expected_info(self, word: Word, game_state: GameVisibleState, game_logic: AbstractWordleLogic) -> float:
        return 0.0

    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        best_expected_info = -math.inf
        best_word = None

        for word in game_logic.legal_words:
            expected_info = self.get_expected_info(word, game_state, game_logic)
            if expected_info > best_expected_info:
                best_expected_info = expected_info
                best_word = word

        # TODO: implement last guess strategy

        return best_word

    def reset(self):
        pass
