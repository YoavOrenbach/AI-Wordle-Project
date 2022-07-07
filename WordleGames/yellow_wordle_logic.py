import util
from WordleGames.basic_wordle_logic import BasicWordleLogic


class YellowWordle(BasicWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6, word=None):
        super(YellowWordle, self).__init__("Yellow Wordle", secret_words, legal_words, max_iter, word)

    def step(self, guess: str, secret_word: str):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()
