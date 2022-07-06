import random

from Algorithms.abstract_wordle import AbstractWordle
from common import Placing


class BasicWordle(AbstractWordle):
    """Classic Wordle game"""

    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(BasicWordle, self).__init__("Wordle", secret_words, legal_words, max_iter, word)

    def step(self, guess):
        guess = guess.lower()
        if guess not in self.legal_words:
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
        return self.legal_words
