from typing import List, Tuple

from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import Placing
from game_visible_state import GameVisibleState
import util


class BasicWordleLogic(AbstractWordleLogic):
    """Classic Wordle game"""

    def __init__(self, secret_words, legal_words, max_iter=6):
        super(BasicWordleLogic, self).__init__("Wordle", secret_words, legal_words, max_iter)

    def get_pattern(self, guess: str, secret_word: str):
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
        return pattern

    def get_possible_words(self, game_visible_state: GameVisibleState) -> List[str]:
        states = game_visible_state.get_states()
        if not states:
            return self.cur_legal_words
        guess, pattern = states[-1]

        correct_letters, removed_letters, misplaced_letters = [], [], []
        correct, removed, misplaced = [], [], []
        minimum_letters = util.Counter()
        for idx, (letter, match) in enumerate(zip(guess, pattern)):
            if match == int(Placing.incorrect):
                removed_letters.append((idx, letter))
                removed.append(letter)
            elif match == int(Placing.correct):
                correct_letters.append((idx, letter))
                correct.append(letter)
                minimum_letters[letter] += 1
            else:
                misplaced_letters.append((idx, letter))
                misplaced.append(letter)
                minimum_letters[letter] += 1

        special_letters = util.Counter()
        for idx, letter in removed_letters:
            pop_flag = False
            if letter in correct:
                special_letters[letter] += correct.count(letter)
                misplaced_letters.append((idx, letter))
                pop_flag = True
            if letter in misplaced:
                special_letters[letter] += misplaced.count(letter)
                misplaced_letters.append((idx, letter))
                pop_flag = True
            if pop_flag:
                removed = list(filter((letter).__ne__, removed))

        def should_keep_word(word):
            # remove words with incorrect letters
            if any(letter in word for letter in removed):
                return False

            # remove words if they have misplaced letters in the wrong spot or misplaced letters are not in the word
            if any((word[idx] == letter or letter not in word) for idx, letter in misplaced_letters):
                return False

            # remove words that don't match correct letters
            if any((word[idx] != letter) for idx, letter in correct_letters):
                return False

            # remove words that contain more letters than the known amount
            for letter in special_letters:
                if word.count(letter) > special_letters[letter]:
                    return False

            # remove words that contain less letter than the known amount
            for letter in minimum_letters:
                if word.count(letter) < minimum_letters[letter]:
                    return False

            return True

        self.cur_legal_words = list(filter(should_keep_word, self.cur_legal_words))
        return self.cur_legal_words

    def reset(self):
        self.cur_iter = 0
        self.done = False
        self.cur_legal_words = self.legal_words
