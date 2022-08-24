from abc import ABC, abstractmethod

from WordleGames.abstract_wordle import AbstractWordle


class Algorithm(ABC):
    """An abstract class representing each algorithm used to solving the various games."""

    def __init__(self, type):
        """Initializes the algorithm class"""
        super(Algorithm, self).__init__()
        self.type = type

    @abstractmethod
    def get_action(self, game: AbstractWordle):
        """Returns the next guess given the game being played."""
        pass
