import math
from typing import Dict
import json
import numpy as np
from scipy.stats import entropy

from tqdm import tqdm

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle import AbstractWordle
from WordleGames.utils import get_pattern_vanilla
from common import Word, GameType, AlgorithmType

WORD_FREQ_MAP_FILE = "data/freq_map.json"


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
        if game.type in [GameType.Absurdle, GameType.NoisyWordle]:
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
        return sum(prob * math.log2(1 / prob) if prob != 0 else 0 for prob in pattern_probs.values())

    def get_action(self, game: AbstractWordle) -> Word:
        if game.get_turn_num() == 1:
            if game.get_type() != GameType.RealVocabularyWordle:
                return self.opening_guesses[game.get_type()]
            else:
                return self.opening_guesses[game.get_type()][game.get_vocab_size()]

        best_expected_info = -math.inf
        best_word = None

        possible_words = game.get_possible_words()
        for word in possible_words:
            expected_info = self.get_expected_info(word, game)
            if expected_info > best_expected_info:
                best_expected_info = expected_info
                best_word = word
        return best_word


class EntropyFrequency(Entropy):
    def __init__(self):
        super(EntropyFrequency, self).__init__()
        self.priors = get_frequency_based_priors()

    def get_pattern_freq_probs(self, guess: Word, game: AbstractWordle, word_to_prob) -> Dict[tuple, float]:
        pattern_probs = {tuple(pattern): 0 for pattern in game.get_all_patterns()}
        possible_secret_words = game.get_possible_words()
        for secret_word in possible_secret_words:
            pattern_probs[tuple(self.get_pattern(guess, secret_word, game))] += word_to_prob[secret_word]
        return pattern_probs

    def get_expected_freq_info(self, guess: Word, game: AbstractWordle, word_to_prob) -> float:
        pattern_probs = self.get_pattern_freq_probs(guess, game, word_to_prob)
        return entropy(list(pattern_probs.values()), base=2)

    def get_action(self, game: AbstractWordle) -> Word:
        if game.get_turn_num() == 1:
            if game.get_type() != GameType.RealVocabularyWordle:
                return self.opening_guesses[game.get_type()]
            else:
                return self.opening_guesses[game.get_type()][game.get_vocab_size()]

        best_expected_info = math.inf
        best_word = None

        possible_words = game.get_possible_words()
        weights = get_weights(possible_words, self.priors)
        distribution_entropy = entropy_of_distributions(weights)
        word_to_weight = dict(zip(possible_words, weights))
        for word in (possible_words):
            expected_info = self.get_expected_freq_info(word, game, word_to_weight)
            prob = word_to_weight[word]
            expected_score = get_expected_scores(prob, distribution_entropy, expected_info)
            if expected_score < best_expected_info:
                best_expected_info = expected_score
                best_word = word
        return best_word


def get_word_frequencies():
    with open(WORD_FREQ_MAP_FILE) as fp:
        result = json.load(fp)
    return result


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def get_frequency_based_priors(n_common=3000, width_under_sigmoid=10):
    """
    We know that that list of wordle answers was curated by some human
    based on whether they're sufficiently common. This function aims
    to associate each word with the likelihood that it would actually
    be selected for the final answer.

    Sort the words by frequency, then apply a sigmoid along it.
    """
    freq_map = get_word_frequencies()
    words = np.array(list(freq_map.keys()))
    freqs = np.array([freq_map[w] for w in words])
    arg_sort = freqs.argsort()
    sorted_words = words[arg_sort]

    # We want to imagine taking this sorted list, and putting it on a number
    # line so that it's length is 10, situating it so that the n_common most common
    # words are positive, then applying a sigmoid
    x_width = width_under_sigmoid
    c = x_width * (-0.5 + n_common / len(words))
    xs = np.linspace(c - x_width / 2, c + x_width / 2, len(words))
    priors = dict()
    for word, x in zip(sorted_words, xs):
        priors[word] = sigmoid(x)
    return priors

def get_weights(words, priors):
    frequencies = np.array([priors[word] for word in words])
    total = frequencies.sum()
    if total == 0:
        return np.zeros(frequencies.shape)
    return frequencies / total


def entropy_of_distributions(distributions, atol=1e-12):
    axis = len(distributions.shape) - 1
    return entropy(distributions, base=2, axis=axis)


def entropy_to_expected_score(ent):
    """
    Based on a regression associating entropies with typical scores
    from that point forward in simulated games, this function returns
    what the expected number of guesses required will be in a game where
    there's a given amount of entropy in the remaining possibilities.
    """
    # Assuming you can definitely get it in the next guess,
    # this is the expected score
    min_score = 2**(-ent) + 2 * (1 - 2**(-ent))

    # To account for the likely uncertainty after the next guess,
    # and knowing that entropy of 11.5 bits seems to have average
    # score of 3.5, we add a line to account
    # we add a line which connects (0, 0) to (3.5, 11.5)
    return min_score + 1.5 * ent / 11.5


def get_expected_scores(prob, h0, h1):
    # If this guess is the true answer, score is 1. Otherwise, it's 1 plus
    # the expected number of guesses it will take after getting the corresponding
    # amount of information.
    return prob + (1 - prob) * (1 + abs(h0-h1))


