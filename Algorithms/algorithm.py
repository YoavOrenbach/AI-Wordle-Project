from abc import ABC, abstractmethod

from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from game_visible_state import GameVisibleState


class Algorithm(ABC):
    """An abstract class representing each algorithm used to solving the various games."""

    def __init__(self, type):
        super(Algorithm, self).__init__()
        self.type = type

    @abstractmethod
    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        """Returns the next guess given the game state and the game being played."""
        pass

    @abstractmethod
    def reset(self):
        """Resets the algorithm."""
        pass