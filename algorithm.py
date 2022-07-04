from abc import ABC, abstractmethod
import random
import util
from game_state import GameState


class Algorithm(ABC):
    """An abstract class representing each algorithm used to solving the various games."""
    def __init__(self, name):
        super(Algorithm, self).__init__()
        self.name = name

    @abstractmethod
    def get_action(self, game_state: GameState):
        """Returns the next guess given the game state and the game being played."""
        pass

    @abstractmethod
    def reset(self):
        """Resets the algorithm."""
        pass


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__("Random")
        self.guess_count = 0

    def get_action(self, game_state):
        if self.guess_count == 0:
            self.guess_count += 1
            return random.choice(game_state.get_possible_guesses())
        self.guess_count += 1
        game_state.filter_wordle_guesses()
        return random.choice(game_state.get_possible_guesses())

    def reset(self):
        self.guess_count = 0


class MiniMax(Algorithm):
    def __init__(self):
        super(MiniMax, self).__init__("MiniMax")
        util.raiseNotDefined()

    def get_action(self, game_state):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()


class Entropy(Algorithm):
    def __init__(self):
        super(Entropy, self).__init__("Entropy")
        util.raiseNotDefined()

    def get_action(self, game_state):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()


class ReinforcementLearning(Algorithm):
    def __init__(self):
        super(ReinforcementLearning, self).__init__("Reinforcement learning")
        util.raiseNotDefined()

    def get_action(self, game_state):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()
