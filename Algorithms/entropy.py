import math
from typing import Dict

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle import AbstractWordle
from WordleGames.utils import get_pattern_vanilla
from common import Word, GameType, AlgorithmType

from tqdm import tqdm


class Entropy(Algorithm):
    def __init__(self):
        super(Entropy, self).__init__(AlgorithmType.Entropy)
        # these guesses were pre-computed using the same algorithm
        self.opening_guesses = {GameType.BasicWordle: "tares", GameType.YellowWordle: "arise",
                                GameType.NoisyWordle: "tares",
                                GameType.Absurdle: "tares", GameType.FakeVocabularyWordle: "lxpyn",
                                GameType.RealVocabularyWordle: {1000: "rates",
                                                                2000: "tares",
                                                                3000: "tares",
                                                                4000: "soare",
                                                                5000: "tares",
                                                                6000: "lares",
                                                                7000: "tares",
                                                                8000: "lares",
                                                                9000: "tares",
                                                                10000: "tares",
                                                                11000: "tares",
                                                                12000: "tares",
                                                                12972: "tares"}}

    def get_pattern(self, guess: Word, secret_word: Word, game: AbstractWordle):
        if game.type in [GameType.Absurdle, GameType.NoisyWordle]:  # this is mainly for faster run
            return get_pattern_vanilla(guess, secret_word)
        else:
            return game.get_pattern(guess, secret_word)

    def get_pattern_probs(self, guess: Word, game: AbstractWordle) -> Dict[tuple, float]:
        pattern_counts = {tuple(pattern): 0 for pattern in game.get_all_patterns()}
        possible_secret_words = game.get_possible_words()
        for secret_word in possible_secret_words:
            pattern_counts[tuple(self.get_pattern(guess, secret_word, game))] += 1

        possible_words_num = len(possible_secret_words)
        pattern_probs = {k: v / possible_words_num for k, v in pattern_counts.items()}

        return pattern_probs

    def get_expected_info(self, guess: Word, game: AbstractWordle) -> float:
        pattern_probs = self.get_pattern_probs(guess, game)
        return sum(prob * math.log2(1 / prob) if prob!=0 else 0 for prob in pattern_probs.values())

    def get_action(self, game: AbstractWordle) -> Word:
        if game.get_turn_num() == 1:
            if game.get_type() != GameType.RealVocabularyWordle:
                return self.opening_guesses[game.get_type()]
            else:
                return self.opening_guesses[game.get_type()][game.get_vocab_size()]

        best_expected_info = -math.inf
        best_word = None

        possible_words = game.get_possible_words()
        for word in (possible_words):
            expected_info = self.get_expected_info(word, game)
            if expected_info > best_expected_info:
                best_expected_info = expected_info
                best_word = word
        return best_word
