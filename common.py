from enum import Enum, IntEnum

Word = str
MAX = 0
MIN = 1
LETTERS_NUM = 5


class AlgorithmType(str, Enum):
    Random = "random"
    Minimax = "minimax"
    AlphaBeta = "alphabeta"
    Expectimax = "expectimax"
    Entropy = "entropy"
    Reinforcement = "reinforcement"


class GameType(str, Enum):
    BasicWordle = "wordle"
    Absurdle = "absurdle"
    FakeVocabularyWordle = "fake_vocabulary"
    RealVocabularyWordle = "real_vocabulary"
    NoisyWordle = "noisy"
    YellowWordle = "yellow"


class Placing(IntEnum):
    """An Enum for representing the placing color of every letter"""
    correct = 0
    misplaced = 1
    incorrect = 2


WINNING_PATTERN = tuple([Placing.correct.value for _ in range(LETTERS_NUM)])
LOSING_PATTERN = [Placing.incorrect.value]*LETTERS_NUM
