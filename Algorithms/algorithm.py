from abc import ABC, abstractmethod

from game_state import GameVisibleState


class Algorithm(ABC):
    """An abstract class representing each algorithm used to solving the various games."""

    def __init__(self, name):
        super(Algorithm, self).__init__()
        self.name = name

    @abstractmethod
    def get_action(self, game_state: GameVisibleState):
        """Returns the next guess given the game state and the game being played."""
        pass

    @abstractmethod
    def reset(self):
        """Resets the algorithm."""
        pass