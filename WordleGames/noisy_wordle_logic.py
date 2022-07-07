import util
from WordleGames.abstract_wordle_logic import AbstractWordleLogic


class NoisyWordleLogic(AbstractWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(NoisyWordleLogic, self).__init__("Noisy Wordle", secret_words, legal_words, max_iter, word)

    def step(self, guess: str, secret_word: str):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()
