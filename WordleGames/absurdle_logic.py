import util
from WordleGames.abstract_wordle_logic import AbstractWordleLogic


class AbsurdleLogic(AbstractWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(AbsurdleLogic, self).__init__("Absurdle", secret_words, legal_words, max_iter, word)

    def step(self, guess: str, secret_word: str):
        """Your code here"""
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()