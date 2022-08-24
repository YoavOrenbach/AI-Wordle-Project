from enum import Enum, IntEnum

Word = str
MAX = 0
MIN = 1
LETTERS_NUM = 5


class AlgorithmType(str, Enum):
    """An Enum for all the names of the implemented algorithms"""
    TotalRandom = "Total Random"
    Random = "Random"
    Minimax = "Minimax"
    AlphaBeta = "Alphabeta"
    Expectimax = "Expectimax"
    Entropy = "Entropy"
    Reinforcement = "Q-learning"


class GameType(str, Enum):
    """An Enum for all the names of the implemented games"""
    BasicWordle = "Wordle"
    Absurdle = "Absurdle"
    FakeVocabularyWordle = "Fake vocabulary"
    RealVocabularyWordle = "Real vocabulary"
    NoisyWordle = "Noisy Wordle"
    YellowWordle = "Yellow Wordle"


class Placing(IntEnum):
    """An Enum for representing the placing color of every letter"""
    correct = 0
    misplaced = 1
    incorrect = 2


WINNING_PATTERN = tuple([Placing.correct.value for _ in range(LETTERS_NUM)])
LOSING_PATTERN = tuple([Placing.incorrect.value]*LETTERS_NUM)
