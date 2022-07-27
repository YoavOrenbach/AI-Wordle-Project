from enum import Enum, IntEnum

Word = str
MAX = 0
MIN = 1
LETTERS_NUM = 5


class AlgorithmType(Enum):
    Random = "random"
    Minimax = "minimax"
    AlphaBeta = "alphabeta"
    Expectimax = "expectimax"
    Entropy = "entropy"
    Reinforcement = "reinforcement"


class GameType(Enum):
    BasicWordle = "wordle"
    Absurdle = "absurdle"
    VocabWordle = "vocab_wordle"
    NoisyWordle = "noisy_wordle"
    YellowWordle = "yellow_wordle"


class Placing(IntEnum):
    """An Enum for representing the placing color of every letter"""
    correct = 0
    misplaced = 1
    incorrect = 2


WINNING_PATTERN = tuple([Placing.correct for _ in range(LETTERS_NUM)])
