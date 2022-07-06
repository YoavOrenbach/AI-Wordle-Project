import util
from Algorithms.basic_wordle import BasicWordle


class YellowWordle(BasicWordle):
    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(YellowWordle, self).__init__("Yellow Wordle", secret_words, legal_words, max_iter, word)

    def step(self, guess):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()

    def get_word_list(self):
        return self.word_list
