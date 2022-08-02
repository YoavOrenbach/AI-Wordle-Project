from typing import List

from WordleGames import BasicWordleLogic
from common import Word, WINNING_PATTERN, GameType, MAX


class AbsurdleLogic(BasicWordleLogic):
    def __init__(self, secret_words, legal_words, should_filter=True, max_iter=None, game_state=[], cur_possible_words=[]):
        super(AbsurdleLogic, self).__init__(secret_words, legal_words, should_filter, max_iter,
            game_state, cur_possible_words, GameType.Absurdle)
        self._possible_secret_words = secret_words

    def successor_creator(self, successor=None, agent_index=MAX, action=None):
        return AbsurdleLogic(self._possible_secret_words.copy(), self.legal_words, self.should_filter, self.max_iter,
            self.states.copy(), self.cur_possible_words.copy())

    def filter_words(self) -> List[Word]:
        filtered_words = super(AbsurdleLogic, self).filter_words()
        self._possible_secret_words = [word for word in self._possible_secret_words if word in filtered_words]
        return filtered_words

    def get_pattern(self, guess: str, secret_word: str):
        """Returns a list containing the placing of each letter in the guess."""
        pattern_words_count = {tuple(pattern): 0 for pattern in self.all_patterns}
        for word in self._possible_secret_words:
            word_pattern = tuple(super(AbsurdleLogic, self).get_pattern(guess, word))
            pattern_words_count[word_pattern] += 1
        if len(self._possible_secret_words) == 1 and pattern_words_count[WINNING_PATTERN] == 1:
            best_pattern = WINNING_PATTERN
        else:
            max_count = max(pattern_words_count.values())
            best_patterns = [k for k, v in pattern_words_count.items() if v == max_count and k != WINNING_PATTERN]
            max_pattern_sum = 0
            best_pattern = best_patterns[-1]
            for pattern in best_patterns:  # Todo: make sure best pattern is like the original absurdle
                if sum(pattern) > max_pattern_sum:
                    max_pattern_sum = sum(pattern)
                    best_pattern = pattern
        return best_pattern

    def reset(self):
        super(AbsurdleLogic, self).reset()
        self._possible_secret_words = self._secret_words
