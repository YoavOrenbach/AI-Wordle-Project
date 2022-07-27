from abc import ABC, abstractmethod

from WordleGames.abstract_wordle_logic import AbstractWordleLogic


class Algorithm(ABC):
    """An abstract class representing each algorithm used to solving the various games."""

    def __init__(self, type):
        super(Algorithm, self).__init__()
        self.type = type

    @abstractmethod
    def get_action(self, game_logic: AbstractWordleLogic):
        """Returns the next guess given the game state and the game being played."""
        pass
