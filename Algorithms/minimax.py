from builtins import str

import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic

# Added
from game_visible_state import GameVisibleState
from copy import deepcopy, copy

import collections

GREEN_PLAC = 2
YELLOW_PLAC = 1
GREY_PLAC = 0

WORD_LEN = 5


class Minimax(Algorithm):
    def __init__(self, depth=1):
        super(Minimax, self).__init__("MiniMax")
        self.guess_count = 0
        self.depth = depth

    def generate_feedback(self, game_logic: AbstractWordleLogic, possible_soln, word):
        game_logic_copy = deepcopy(game_logic)
        game_logic_copy.set_secret_word(possible_soln)
        pattern, done = game_logic_copy.step(word)
        return pattern

    def word_consistent(self, pattern, guess):
        def pred(word):
            # count the letters in word
            letter_counts = collections.Counter()
            for letter in word:
                letter_counts[letter] += 1

            for i in range(WORD_LEN):
                if pattern[i] == GREEN_PLAC:
                    # green pair does not match
                    if word[i] != guess[i]:
                        return False
                    # green letters "use up" one of the solution letters
                    else:
                        letter_counts[guess[i]] -= 1

                if pattern[i] == YELLOW_PLAC:
                    # letter does match, but it shouldn't
                    if word[i] == guess[i]:
                        return False
                    # contain letter l somewhere, aside from a green space
                    else:
                        if letter_counts[guess[i]] <= 0:
                            return False
                        else:
                            letter_counts[guess[i]] -= 1

                if pattern[i] == GREY_PLAC:
                    # contain no gray letters
                    if letter_counts[guess[i]] != 0:
                        return False
            return True

        return pred

    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        current_minimax = None
        current_minimax_word = None

        possible_words = game_logic.get_possible_words(game_state)

        for guess in possible_words:
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

    def reset(self):
        self.guess_count = 0
