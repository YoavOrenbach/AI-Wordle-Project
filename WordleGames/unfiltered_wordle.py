from WordleGames import BasicWordleLogic
from common import GameType, MAX, LOSING_PATTERN


class UnfilteredWordle(BasicWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[]):
        super(UnfilteredWordle, self).__init__(secret_words, legal_words, max_iter,
                                            game_state, cur_possible_words, GameType.UnfilteredWordle)

    def successor_creator(self, successor=None, agent_index=MAX, action=None):
        return UnfilteredWordle(self._secret_words, self.legal_words, self.max_iter,
                                self.states.copy(), self.cur_possible_words.copy())

    def filter_words(self):
        return self.cur_possible_words
