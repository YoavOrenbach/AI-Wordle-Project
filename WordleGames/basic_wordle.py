import random

from WordleGames.abstract_wordle import AbstractWordle
from common import Placing


class BasicWordle(AbstractWordle):
    """Classic Wordle game"""

    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(BasicWordle, self).__init__("Wordle", secret_words, legal_words, max_iter, word)

    def get_pattern(self, guess: str, secret_word: str):
        target_word_letters = [letter for letter in secret_word]
        pattern = [int(Placing.incorrect) for _ in range(5)]

        # first list out the correct letters in the correct spot
        for i in range(5):
            if target_word_letters[i] == guess[i]:
                target_word_letters[i] = "*"
                pattern[i] = int(Placing.correct)

        # check for letters in the incorrect spots
        for i in range(5):  # outer loop for the guessed word
            if pattern[i] != int(Placing.incorrect):  # skip this letter if it's already in correct spot
                continue
            for j in range(5):  # inner loop for the target word
                if i == j or target_word_letters[j] == "*":
                    continue
                if guess[i] == target_word_letters[j]:
                    target_word_letters[j] = "*"
                    pattern[i] = int(Placing.misplaced)
                    break
        return pattern

    def step(self, guess, secret_word):
        guess = guess.lower()
        if guess not in self.legal_words:
            raise ValueError('invalid word')

        if self.max_iter is not None and self.cur_iter >= self.max_iter:
            self.done = True
            return [], self.done

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word)

        if pattern.count(int(Placing.correct)) == len(pattern):
            self.done = True

        return pattern, self.done

    def reset(self):
        self.cur_iter = 0
        self.done = False
