import random
from abc import ABC, abstractmethod


class AbstractWordleLogic(ABC):
    """An abstract class representing each Wordle type game"""

    def __init__(self, name, secret_words, legal_words, max_iter=6, word=None):
        super(AbstractWordleLogic, self).__init__()
        self.name = name
        self.secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.done = False

    def generate_secret_word(self):
        return random.choice(self.secret_words)

    @abstractmethod
    def step(self, guess: str, secret_word: str):
        """
        Performs a single step in the game following a guess.
        :return: the resulting pattern of each guess and a boolean flag if the game is done.
        """
        pass

    @abstractmethod
    def reset(self):
        """Resets the game state."""
        pass

    def get_legal_words(self):
        """Returns the large list of words used in the game."""
        return self.legal_words