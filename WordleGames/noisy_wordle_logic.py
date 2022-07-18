from typing import List
import random
import util
from common import Placing
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from game_visible_state import GameVisibleState


class NoisyWordleLogic(AbstractWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6):
        super(NoisyWordleLogic, self).__init__("Noisy Wordle", secret_words, legal_words, max_iter)

    @staticmethod
    def weight_placing(real_placing):
        return [real_placing] * 85 + [Placing.correct] * 4 + [Placing.misplaced] * 8 + [Placing.incorrect] * 3

    def get_pattern(self, guess: str, secret_word: str):
        # First, get the real pattern
        pool = {}
        for g, s in zip(guess, secret_word):
            if g == s:
                continue
            if s in pool:
                pool[s] += 1
            else:
                pool[s] = 1

        pattern = []
        for guess_letter, solution_letter in zip(guess, secret_word):
            if guess_letter == solution_letter:
                pattern.append(int(Placing.correct))
            elif guess_letter in secret_word and guess_letter in pool and pool[guess_letter] > 0:
                pattern.append(int(Placing.misplaced))
                pool[guess_letter] -= 1
            else:
                pattern.append(Placing.incorrect)

        return [random.choice(NoisyWordleLogic.weight_placing(c)) for c in pattern]
    
    def get_possible_words(self, game_visible_state: GameVisibleState) -> List[str]:
        return self.cur_possible_words

    def reset(self):
        self.cur_iter = 0
        self.done = False
        self.cur_possible_words = self.legal_words
