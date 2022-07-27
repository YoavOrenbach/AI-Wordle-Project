from enum import Enum, IntEnum

Word = str

LETTERS_NUM = 5


class AlgorithmType(Enum):
    Random = "random"
    Minimax = "minimax"
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


WINNING_PATTERN = tuple([Placing.correct for _ in range(LETTERS_NUM)])
