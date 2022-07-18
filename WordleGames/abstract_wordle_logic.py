import random
from abc import ABC, abstractmethod

from typing import List
from common import Placing

from game_visible_state import GameVisibleState
from copy import deepcopy

class InvalidGuessException(ValueError):
    pass


class AbstractWordleLogic(ABC):
    """An abstract class representing each Wordle type game"""

    def __init__(self, name, secret_words, legal_words, max_iter=6):
        super(AbstractWordleLogic, self).__init__()
        self.name = name
        self._secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.done = False
        self.cur_legal_words = legal_words
        self._secret_word = ''

    def generate_secret_word(self):
        self._secret_word = random.choice(self._secret_words)
        return self._secret_word

    def get_legal_words(self):
        return self.legal_words

    def step(self, guess: str, secret_word=None):
        """
        Performs a single step in the game following a guess.
        :return: the resulting pattern of each guess and a boolean flag if the game is done.
        """
        if not secret_word:
            secret_word = self._secret_word

        guess = guess.lower()
        if guess not in self.legal_words:
            raise InvalidGuessException('invalid word')

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word)

        if pattern.count(int(Placing.correct)) == len(pattern) or (
                self.max_iter is not None and self.cur_iter >= self.max_iter):
            self.done = True

        return pattern, self.done

    @abstractmethod
    def reset(self):
        """Resets the game state."""
        pass

    @abstractmethod
    def get_possible_words(self, game_visible_state: GameVisibleState) -> List[str]:
        pass

    @abstractmethod
    def get_pattern(self, guess: str, secret_word: str):
        """Returns a list containing the placing of each letter in the guess."""
        pass