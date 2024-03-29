import random
from WordleGames import BasicWordle
from utils.common import Placing, GameType, LETTERS_NUM, MAX, Word, LOSING_PATTERN
from utils import util


class NoisyWordle(BasicWordle):
    """Noisy Wordle game"""
    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[]):
        super(NoisyWordle, self).__init__(secret_words, legal_words, max_iter,
                                          game_state, cur_possible_words, GameType.NoisyWordle)

    @staticmethod
    def weight_placing(real_placing):
        """Returning one of three color with equal chance"""
        return [real_placing] * 1 + [Placing.correct.value] * 33 + [Placing.misplaced.value] * 33 + \
               [Placing.incorrect.value] * 33

    def successor_creator(self, successor=None, agent_index=MAX, action=None):
        """Creates a successor game object for the adversarial algorithms."""
        return NoisyWordle(self._secret_words, self.legal_words, self.max_iter,
                           self.states.copy(), self.cur_possible_words.copy())

    def get_pattern(self, guess: str, secret_word: Word):
        """Returns a legal pattern for a Noisy Wordle game according to the secret word"""
        pattern = super(NoisyWordle, self).get_pattern(guess, secret_word)
        chosen_square = random.randrange(LETTERS_NUM)
        pattern[chosen_square] = random.choice(NoisyWordle.weight_placing(pattern[chosen_square]))
        return pattern

    def get_possible_patterns(self, guess):
        """Returns the losing pattern"""
        patterns_counter = util.Counter()
        patterns_counter[LOSING_PATTERN] = 1
        return patterns_counter

    def filter_words(self):
        """
        Filters words from the possible words list according to the last guess and pattern.
        In Noisy Wordle, the filtering is like basic Wordle, however the patterns are 11 different possible patterns
        """
        if not self.get_game_state():
            return self.cur_possible_words
        guess, original_pattern = self.get_game_state()[-1]
        all_patterns = noisy_patterns(original_pattern)
        unified_words = set()
        for pattern in all_patterns:
            self.states[-1] = (guess, pattern)
            unified_words = unified_words.union(set(super(NoisyWordle, self).filter_words()))
        self.states[-1] = (guess, original_pattern)
        return list(unified_words)


def noisy_patterns(pattern):
    """Returns 11 possible noisy patterns"""
    all_patterns = [pattern]
    for i, placing in enumerate(pattern):
        possible_pattern1 = pattern.copy()
        possible_pattern2 = pattern.copy()
        if placing == Placing.correct.value:
            possible_pattern1[i] = Placing.misplaced.value
            all_patterns.append(possible_pattern1)
            possible_pattern2[i] = Placing.incorrect.value
            all_patterns.append(possible_pattern2)
        elif placing == Placing.misplaced.value:
            possible_pattern1[i] = Placing.correct.value
            all_patterns.append(possible_pattern1)
            possible_pattern2[i] = Placing.incorrect.value
            all_patterns.append(possible_pattern2)
        else:
            possible_pattern1[i] = Placing.correct.value
            all_patterns.append(possible_pattern1)
            possible_pattern2[i] = Placing.misplaced.value
            all_patterns.append(possible_pattern2)
    return all_patterns
