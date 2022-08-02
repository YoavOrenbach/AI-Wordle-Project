import random
from abc import ABC, abstractmethod
from typing import List

from common import GameType, MAX, MIN, WINNING_PATTERN


class InvalidGuessException(ValueError):
    pass


class AbstractWordleLogic(ABC):
    """An abstract class representing each Wordle type game"""

    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[], game_type=None):
        super(AbstractWordleLogic, self).__init__()
        self.type: GameType = game_type
        self._secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.done = False
        if not cur_possible_words:
            self.cur_possible_words = legal_words
        else:
            self.cur_possible_words = cur_possible_words
        self.all_patterns = []
        self.states = game_state  # contains pairs of (guess, pattern), namely a word and its resulting pattern.

    def get_type(self):
        return self.type

    def get_all_patterns(self):
        return self.all_patterns

    def get_done(self):
        return self.done

    def get_game_state(self):
        return self.states

    def get_turn_num(self):
        return len(self.states) + 1

    def get_legal_words(self):
        return self.legal_words

    def get_possible_words(self) -> List[str]:
        return self.cur_possible_words

    def generate_secret_word(self):
        return random.choice(self._secret_words)

    def step(self, guess: str, secret_word: str):
        """
        Performs a single step in the game following a guess.
        :return: the resulting pattern of the guess, a boolean flag - whether the game is done, a boolean flag -
        did the player win.
        """
        guess = guess.lower()
        if guess not in self.legal_words:
            raise InvalidGuessException('invalid word')

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word)
        self.states.append((guess, pattern))
        self.cur_possible_words = self.filter_words()
        is_win = (guess == secret_word) if self.type != GameType.Absurdle else (tuple(pattern) == WINNING_PATTERN)
        is_max_iter = (self.max_iter is not None and self.cur_iter >= self.max_iter)
        if is_win or is_max_iter:
            self.done = True

        return pattern, self.done, is_win

    def reset(self):
        """Resets the game state."""
        self.cur_iter = 0
        self.done = False
        self.cur_possible_words = self.legal_words
        self.states = []

    def apply_action(self, action: str):
        self.states.append((action, []))

    def apply_opponent_action(self, action):
        guess, _ = self.states[-1]
        self.states[-1] = (guess, action)
        self.cur_possible_words = self.filter_words()

    def get_possible_patterns(self, guess):
        return list(set(tuple(self.get_pattern(guess, secret_word)) for secret_word in self.cur_possible_words))

    @abstractmethod
    def filter_words(self):
        pass

    @abstractmethod
    def get_pattern(self, guess: str, secret_word: str):
        """Returns a list containing the placing of each letter in the guess."""
        pass

    @abstractmethod
    def successor_creator(self):
        pass
