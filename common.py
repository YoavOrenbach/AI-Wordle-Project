from enum import Enum


class AlgorithmType(Enum):
    Random = "random"
    Minimax = "minimax"
    Expectimax = "expectimax"
    Entropy = "entropy"
    Reinforcement = "reinforcement"


class GameType(Enum):
    Wordle = "wordle"
    Absurdle = "absurdle"
    VocabWordle = "vocab_wordle"
    NoisyWordle = "noisy_wordle"
    YellowWordle = "yellow_wordle"
