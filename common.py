from enum import Enum, IntEnum

Word = str
MAX = 0
MIN = 1
LETTERS_NUM = 5


class AlgorithmType(str, Enum):
    TotalRandom = "Total Random"
    Random = "Random"
    Minimax = "Minimax"
    AlphaBeta = "Alphabeta"
    Expectimax = "Expectimax"
    Entropy = "Entropy"
    Reinforcement = "Reinforcement"


class GameType(str, Enum):
    BasicWordle = "Wordle"
    Absurdle = "Absurdle"
    FakeVocabularyWordle = "Fake vocabulary"
    RealVocabularyWordle = "Real vocabulary"
    NoisyWordle = "Noisy"
    YellowWordle = "Yellow"


class Placing(IntEnum):
    """An Enum for representing the placing color of every letter"""
    correct = 0
    misplaced = 1
    incorrect = 2


WINNING_PATTERN = tuple([Placing.correct.value for _ in range(LETTERS_NUM)])
LOSING_PATTERN = tuple([Placing.incorrect.value]*LETTERS_NUM)
