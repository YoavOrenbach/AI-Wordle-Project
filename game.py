from abc import ABC, abstractmethod
from enum import IntEnum
import random
import util


class Placing(IntEnum):
    """An Enum for representing the placing color of every letter"""
    correct = 0
    misplaced = 1
    incorrect = 2


class Game(ABC):
    """An abstract class representing each Wordle type game"""
    def __init__(self, name):
        super(Game, self).__init__()
        self.name = name

    @abstractmethod
    def step(self, guess):
        """
        Performs a single step in the game following a guess.
        :return: the resulting pattern of each guess and a boolean flag if the game is done.
        """
        pass

    @abstractmethod
    def reset(self):
        """Resets the game state."""
        pass

    @abstractmethod
    def get_word_list(self):
        """Returns the large list of words used in the game."""
        pass


class Wordle(Game):
    """Classic Wordle game"""
    def __init__(self, secret_words, words_list, max_iter=6, word=None):
        super(Wordle, self).__init__("Wordle")
        self.secret_words = secret_words
        self.word_list = words_list
        self.max_iter = max_iter
        self.cur_iter = 0
        self.word = random.choice(self.secret_words) if word is None else word
        self.done = False

    def step(self, guess):
        guess = guess.lower()
        if guess not in self.word_list:
            raise ValueError('invalid word')

        if self.max_iter is not None and self.cur_iter >= self.max_iter:
            self.done = True
            return [], self.done

        self.cur_iter += 1

        target_word_copy = [letter for letter in self.word]
        pattern = [int(Placing.incorrect) for _ in range(5)]

        # first list out the correct letters in the correct spot
        for i in range(5):
            if target_word_copy[i] == guess[i]:
                target_word_copy[i] = "*"
                pattern[i] = int(Placing.correct)

        # check for letters in the incorrect spots
        for i in range(5):  # outer loop for the guessed word
            if pattern[i] != int(Placing.incorrect):  # skip this letter if it's already in correct spot
                continue
            for j in range(5):  # inner loop for the target word
                if i == j or target_word_copy[j] == "*":
                    continue
                if guess[i] == target_word_copy[j]:
                    target_word_copy[j] = "*"
                    pattern[i] = int(Placing.misplaced)
                    break
        if pattern.count(int(Placing.correct)) == len(pattern):
            self.done = True
        return pattern, self.done

    def reset(self, update_word=False):
        self.cur_iter = 0
        if update_word:
            self.word = random.choice(self.secret_words)
        self.done = False

    def get_word_list(self):
        return self.word_list


class Absurdle(Game):
    def __init__(self, secret_words, words_list, max_iter=6, word=None):
        super(Absurdle, self).__init__("Absurdle")
        self.secret_words = secret_words
        self.word_list = words_list
        self.max_iter = max_iter
        self.cur_iter = 0
        self.word = random.choice(self.secret_words) if word is None else word

    def step(self, guess):
        """Your code here"""
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()

    def get_word_list(self):
        return self.word_list


class NoisyWordle(Game):
    def __init__(self, secret_words, words_list, max_iter=6, word=None):
        super(NoisyWordle, self).__init__("Noisy Wordle")
        self.secret_words = secret_words
        self.word_list = words_list
        self.max_iter = max_iter
        self.cur_iter = 0
        self.word = random.choice(self.secret_words) if word is None else word

    def step(self, guess):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()

    def get_word_list(self):
        return self.word_list


class YellowWordle(Game):
    def __init__(self, secret_words, words_list, max_iter=6, word=None):
        super(YellowWordle, self).__init__("Yellow Wordle")
        self.secret_words = secret_words
        self.word_list = words_list
        self.max_iter = max_iter
        self.cur_iter = 0
        self.word = random.choice(self.secret_words) if word is None else word

    def step(self, guess):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()

    def get_word_list(self):
        return self.word_list
