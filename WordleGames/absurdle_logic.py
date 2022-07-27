import random
from typing import List

import util
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from WordleGames import BasicWordleLogic
from common import Word, Placing, WINNING_PATTERN, GameType, MAX


class AbsurdleLogic(BasicWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=None, secret_word='', game_state=[], cur_possible_words=[]):
        super(AbsurdleLogic, self).__init__(secret_words, legal_words, max_iter, secret_word,
            game_state, cur_possible_words, GameType.Absurdle)
        self.possible_secret_words = self._secret_words

    def generate_secret_word(self):
        return None

    def successor_creator(self, successor=None, agent_index=MAX, action=None):
        return AbsurdleLogic(self._secret_words, self.legal_words, self.max_iter, self._secret_word,
            self.states.copy(), self.cur_possible_words.copy())

    def filter_words(self) -> List[Word]:
        filtered_words = super(AbsurdleLogic, self).filter_words()
        self.possible_secret_words = [word for word in self._secret_words if word in filtered_words]
        return filtered_words

    def get_pattern(self, guess: str, secret_word: str = None):
        """Returns a list containing the placing of each letter in the guess."""
        # all_patterns = AbstractWordleLogic.all_patterns
        # pattern_words_count = {pattern: 0 for pattern in all_patterns}
        # #possible_words = set(self.get_possible_words())
        # #possible_secret_words = [word for word in self._secret_words if word in possible_words]
        # for word in self.possible_secret_words:  # TODO: should iterate only over the secret possible words
        #     word_pattern = tuple(super(AbsurdleLogic, self).get_pattern(guess, word))
        #     pattern_words_count[word_pattern] += 1
        # if len(self.possible_secret_words) == 1 and pattern_words_count[WINNING_PATTERN] == 1:
        #     best_pattern = WINNING_PATTERN
        # else:
        #     max_count = max(pattern_words_count.values())
        #     best_patterns = [k for k, v in pattern_words_count.items() if v == max_count and k != WINNING_PATTERN]
        best_patterns = self.get_possible_patterns(guess)
        best_pattern = random.choice(best_patterns)
        return best_pattern

    def get_possible_patterns(self, guess: str):
        all_patterns = AbstractWordleLogic.all_patterns
        pattern_words_count = {pattern: 0 for pattern in all_patterns}
        for word in self.possible_secret_words:
            word_pattern = tuple(super(AbsurdleLogic, self).get_pattern(guess, word))
            pattern_words_count[word_pattern] += 1
        if len(self.possible_secret_words) == 1 and pattern_words_count[WINNING_PATTERN] == 1:
            best_patterns = [WINNING_PATTERN]
        else:
            max_count = max(pattern_words_count.values())
            best_patterns = [k for k, v in pattern_words_count.items() if v == max_count and k != WINNING_PATTERN]
        return best_patterns
