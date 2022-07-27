import random
from typing import List

import util
from WordleGames.abstract_wordle_logic import AbstractWordleLogic, InvalidGuessException
from WordleGames.utils import get_pattern_vanilla
from common import Word, Placing, WINNING_PATTERN, GameType


class AbsurdleLogic(AbstractWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[]):
        super(AbsurdleLogic, self).__init__(GameType.Absurdle, secret_words, legal_words, max_iter,
            game_state, cur_possible_words)

    def generate_secret_word(self):
        return None

    def step(self, guess: str, secret_word: str = None):
        """Your code here"""
        guess = guess.lower()
        if guess not in self.legal_words:
            raise InvalidGuessException('invalid word')

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word, game_state)

        is_win = (tuple(pattern) == WINNING_PATTERN)
        is_max_iter = (self.max_iter is not None and self.cur_iter >= self.max_iter)
        if is_win or is_max_iter:
            self.done = True

        return pattern, self.done, is_win

    def filter_words(self) -> List[Word]:
        return None

    def get_pattern(self, guess: str, secret_word: str = None):
        """Returns a list containing the placing of each letter in the guess."""
        all_patterns = AbstractWordleLogic.all_patterns
        pattern_words_count = {pattern: 0 for pattern in all_patterns}
        possible_words = set(self.get_possible_words())
        possible_secret_words = [word for word in self._secret_words if word in possible_words]
        for word in possible_secret_words:  # TODO: should iterate only over the secret possible words
            word_pattern = tuple(get_pattern_vanilla(guess, word))
            pattern_words_count[word_pattern] += 1
        if len(possible_secret_words) == 1 and pattern_words_count[WINNING_PATTERN] == 1:
            best_pattern = WINNING_PATTERN
        else:
            max_count = max(pattern_words_count.values())
            best_patterns = [k for k, v in pattern_words_count.items() if v == max_count and k != WINNING_PATTERN]
            best_pattern = random.choice(best_patterns)
        return list(best_pattern)
