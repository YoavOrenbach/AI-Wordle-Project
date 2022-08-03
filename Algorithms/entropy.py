import math
from typing import Dict

from tqdm import tqdm

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from WordleGames.utils import get_pattern_vanilla
from common import Word, GameType, AlgorithmType


class Entropy(Algorithm):
    opening_guesses = {GameType.BasicWordle: "tares", GameType.YellowWordle: "arise", GameType.NoisyWordle: "tares",
                       GameType.Absurdle: "tares", GameType.FakeVocabularyWordle: "lxpyn"}

    # these words were pre-computed using the same algorithm

    def __init__(self):
        super(Entropy, self).__init__(AlgorithmType.Entropy)

    def get_pattern(self, guess: Word, secret_word: Word, game_logic: AbstractWordleLogic):
        if game_logic.type in [GameType.Absurdle]:
            return get_pattern_vanilla(guess, secret_word)
        else:
            return game_logic.get_pattern(guess, secret_word)

    def get_pattern_probs(self, guess: Word, game_logic: AbstractWordleLogic) -> Dict[tuple, float]:
        pattern_counts = {tuple(pattern): 0 for pattern in game_logic.get_all_patterns()}
        possible_secret_words = game_logic.get_possible_words()
        for secret_word in possible_secret_words:
            pattern_counts[tuple(self.get_pattern(guess, secret_word, game_logic))] += 1

        possible_words_num = len(possible_secret_words)
        pattern_probs = {k: v / possible_words_num for k, v in pattern_counts.items()}

        return pattern_probs

    def get_expected_info(self, guess: Word, game_logic: AbstractWordleLogic) -> float:
        pattern_probs = self.get_pattern_probs(guess, game_logic)
        return sum(prob * math.log2(1 / prob) if prob != 0 else 0 for prob in pattern_probs.values())

    def get_opening_guess(self, game_logic: AbstractWordleLogic) -> Word:
        return Entropy.opening_guesses[game_logic.get_type()]

    def get_action(self, game_logic: AbstractWordleLogic) -> Word:
        if game_logic.get_turn_num() == 1:
            if game_logic.get_type() in self.opening_guesses:
                return self.get_opening_guess(game_logic)

        best_expected_info = -math.inf
        best_word = None

        possible_words = game_logic.get_possible_words()
        for word in tqdm(possible_words):
            expected_info = self.get_expected_info(word, game_logic)
            if expected_info > best_expected_info:
                best_expected_info = expected_info
                best_word = word
        return best_word
