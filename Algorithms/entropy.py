import math

from typing import Dict

from tqdm import tqdm

import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import Word
from game_visible_state import GameVisibleState


class Entropy(Algorithm):
    def __init__(self):
        super(Entropy, self).__init__("Entropy")

    def get_pattern_probs(self, word: Word, game_state: GameVisibleState, game_logic: AbstractWordleLogic) -> Dict[
        tuple, float]:
        pattern_counts = {pattern: 0 for pattern in game_logic.possible_patterns}
        possible_secret_words = game_logic.cur_possible_words
        for secret_word in possible_secret_words:
            pattern_counts[tuple(game_logic.get_pattern(word, secret_word))] += 1

        possible_words_num = len(possible_secret_words)
        pattern_probs = {k: v / possible_words_num for k, v in pattern_counts.items()}

        return pattern_probs

    def get_expected_info(self, word: Word, game_state: GameVisibleState, game_logic: AbstractWordleLogic) -> float:
        pattern_probs = self.get_pattern_probs(word, game_state, game_logic)
        return sum(
            pattern_probs[pattern] * math.log2(1 / pattern_probs[pattern]) if pattern_probs[pattern] != 0 else 0 for
            pattern in game_logic.possible_patterns)

    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        best_expected_info = -math.inf
        best_word = None

        for word in tqdm(game_logic.legal_words):
            expected_info = self.get_expected_info(word, game_state, game_logic)
            if expected_info > best_expected_info:
                best_expected_info = expected_info
                best_word = word

        # TODO: implement last guess strategy

        return best_word

    def reset(self):
        pass
