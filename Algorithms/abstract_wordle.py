import random
from abc import ABC, abstractmethod


class AbstractWordle(ABC):
    """An abstract class representing each Wordle type game"""

    def __init__(self, name, secret_words, legal_words, max_iter=6, word=None):
        super(AbstractWordle, self).__init__()
        self.name = name
        self.secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.word = random.choice(self.secret_words) if word is None else word
        self.done = False

    @abstractmethod
    def step(self, guess):
        """
        Performs a single step in the game following a guess.
        :return: the resulting pattern of each guess and a boolean flag if the game is done.
        """
        pass

    @abstractmethod
    def reset(self):
        """Resets the game state."""
        pass

    @abstractmethod
    def get_word_list(self):
        """Returns the large list of words used in the game."""
        pass