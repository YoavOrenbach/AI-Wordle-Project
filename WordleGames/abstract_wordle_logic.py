import itertools
import random
from abc import ABC, abstractmethod
from typing import List

from common import Placing, LETTERS_NUM, GameType
from game_visible_state import GameVisibleState


class InvalidGuessException(ValueError):
    pass


class AbstractWordleLogic(ABC):
    """An abstract class representing each Wordle type game"""
    all_patterns = [pattern for pattern in
                    itertools.product([placing.value for placing in Placing], repeat=LETTERS_NUM)]

    def __init__(self, type, secret_words, legal_words, max_iter=6):
        super(AbstractWordleLogic, self).__init__()
        self.type: GameType = type
        self._secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.done = False
        self.cur_possible_words = legal_words  # TODO: move to game visible state

    def generate_secret_word(self):
        return random.choice(self._secret_words)

    def get_legal_words(self):
        return self.legal_words

    def step(self, guess: str, secret_word: str, game_state: GameVisibleState):
        """
        Performs a single step in the game following a guess.
        :return: the resulting pattern of the guess, a boolean flag - whether the game is done, a boolean flag -
        did the player win.
        """
        guess = guess.lower()
        if guess not in self.legal_words:
            raise InvalidGuessException('invalid word')

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word, game_state)

        is_win = (guess == secret_word)
        is_max_iter = (self.max_iter is not None and self.cur_iter >= self.max_iter)
        if is_win or is_max_iter:
            self.done = True

        return pattern, self.done, is_win

    def reset(self):
        """Resets the game state."""
        self.cur_iter = 0
        self.done = False
        self.cur_possible_words = self.legal_words

    @abstractmethod
    def get_possible_words(self, game_visible_state: GameVisibleState) -> List[str]:
        pass

    @abstractmethod
    def get_pattern(self, guess: str, secret_word: str, game_state: GameVisibleState):
        """Returns a list containing the placing of each letter in the guess."""
        pass
