import math
from typing import Dict

from tqdm import tqdm

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from WordleGames.utils import get_pattern_vanilla
from common import Word, GameType, AlgorithmType
from game_visible_state import GameVisibleState


class Entropy(Algorithm):
    opening_guesses = {GameType.BasicWordle: "tares", GameType.YellowWordle: "arise",
                       GameType.Absurdle: "tares"}  # these words were pre-computed using the same algorithm

    def __init__(self):
        super(Entropy, self).__init__(AlgorithmType.Entropy)

    def get_pattern(self, guess: Word, secret_word: Word, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        if game_logic.type in [GameType.Absurdle]:
            return get_pattern_vanilla(guess, secret_word)
        else:
            return game_logic.get_pattern(guess, secret_word, game_state)

    def get_pattern_probs(self, guess: Word, game_state: GameVisibleState, game_logic: AbstractWordleLogic) -> Dict[
        tuple, float]:
        pattern_counts = {pattern: 0 for pattern in game_logic.all_patterns}
        possible_secret_words = game_logic.cur_possible_words
        for secret_word in possible_secret_words:
            pattern_counts[tuple(self.get_pattern(guess, secret_word, game_state, game_logic))] += 1

        possible_words_num = len(possible_secret_words)
        pattern_probs = {k: v / possible_words_num for k, v in pattern_counts.items()}

        return pattern_probs

    def get_expected_info(self, guess: Word, game_state: GameVisibleState, game_logic: AbstractWordleLogic) -> float:
        pattern_probs = self.get_pattern_probs(guess, game_state, game_logic)
        return sum(
            pattern_probs[pattern] * math.log2(1 / pattern_probs[pattern]) if pattern_probs[pattern] != 0 else 0 for
            pattern in game_logic.all_patterns)

    def get_opening_guess(self, game_logic: AbstractWordleLogic) -> Word:
        return Entropy.opening_guesses[game_logic.type]

    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic) -> Word:
        if game_state.get_turn_num() == 1:
            return self.get_opening_guess(game_logic)

        best_expected_info = -math.inf
        best_word = None

        possible_words = game_logic.get_possible_words(game_state)  # TODO: maybe use all legal words?
        for word in possible_words:
            expected_info = self.get_expected_info(word, game_state, game_logic)
            if expected_info > best_expected_info:
                best_expected_info = expected_info
                best_word = word

        # TODO: implement "last guess" strategy
        return best_word

    def reset(self):
        pass
