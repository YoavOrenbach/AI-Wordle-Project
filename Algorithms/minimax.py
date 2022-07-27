from builtins import str

import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic

# Added
from game_visible_state import GameVisibleState
from copy import deepcopy, copy

import collections
from tqdm import tqdm

class Minimax(Algorithm):
    def __init__(self, depth=1):
        super(Minimax, self).__init__("MiniMax")
        self.guess_count = 0
        self.depth = depth

    def generate_feedback(self, game_logic: AbstractWordleLogic, possible_soln, word):
        return game_logic.get_pattern(word, possible_soln)

    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        if len(game_state.get_states()) == 0:
            return "crane"
        if len(game_state.get_states()) == 1:
            return "yours"

        current_minimax = None
        current_minimax_word = None

        possible_words = game_logic.get_possible_words(game_state)

        for guess in tqdm(possible_words):
            # max loss for this guess
            maximum_remaining = None
            for possible_soln in possible_words: # TODO: change possible words
                # feedback guessing `guess` when the solution is `soln`
                pattern = self.generate_feedback(game_logic, possible_soln, guess)
                # how many words remain after incorporating this feedback
                remaining = len(list(filter(self.word_consistent(pattern, guess), possible_words)))

                # is this a new maximum loss?
                if maximum_remaining is None or remaining > maximum_remaining:
                    maximum_remaining = remaining

                if current_minimax is not None and maximum_remaining > current_minimax:
                    # the maximum for this guess is larger than the current minimax
                    # not possible that this word represents a minimax, we can break early
                    break

            if current_minimax is None or maximum_remaining < current_minimax:
                current_minimax = maximum_remaining
                current_minimax_word = guess

        return current_minimax_word

    def get_action(self):

    def reset(self):
        self.guess_count = 0
