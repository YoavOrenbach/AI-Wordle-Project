from enum import Enum, IntEnum

Word = str
MAX = 0
MIN = 1
LETTERS_NUM = 5


class AlgorithmType(str, Enum):
    """An Enum for all the names of the implemented algorithms"""
    TotalRandom = "Total-Random"
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
    FakeVocabularyWordle = "Fake-vocabulary"
    RealVocabularyWordle = "Real-vocabulary"
    NoisyWordle = "Noisy-Wordle"
    YellowWordle = "Yellow-Wordle"


class Placing(IntEnum):
    """An Enum for representing the placing color of every letter"""
    correct = 0
    misplaced = 1
    incorrect = 2


WINNING_PATTERN = tuple([Placing.correct.value for _ in range(LETTERS_NUM)])
LOSING_PATTERN = tuple([Placing.incorrect.value]*LETTERS_NUM)

def get_pattern_vanilla(guess: Word, secret_word: Word):
    """Returns a list containing the placing of each letter in the guess according to the secret word
    like basic Wordle"""
    pool = {}
    for g, s in zip(guess, secret_word):
        if g == s:
            continue
        if s in pool:
            pool[s] += 1
        else:
            pool[s] = 1

    pattern = []
    for guess_letter, solution_letter in zip(guess, secret_word):
        if guess_letter == solution_letter:
            pattern.append(int(Placing.correct))
        elif guess_letter in secret_word and guess_letter in pool and pool[guess_letter] > 0:
            pattern.append(int(Placing.misplaced))
            pool[guess_letter] -= 1
        else:
            pattern.append(int(Placing.incorrect))
    return pattern
