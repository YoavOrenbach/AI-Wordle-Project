import util
from WordleGames.abstract_wordle import AbstractWordle


class NoisyWordle(AbstractWordle):
    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(NoisyWordle, self).__init__("Noisy Wordle", secret_words, legal_words, max_iter, word)

    def step(self, guess):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()
