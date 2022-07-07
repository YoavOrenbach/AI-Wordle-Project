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
        target_word_letters = [letter for letter in secret_word]
        pattern = [int(Placing.incorrect) for _ in range(5)]

        # first list out the correct letters in the correct spot
        for i in range(5):
            if target_word_letters[i] == guess[i]:
                target_word_letters[i] = "*"
                pattern[i] = int(Placing.correct)

        # check for letters in the incorrect spots
        for i in range(5):  # outer loop for the guessed word
            if pattern[i] != int(Placing.incorrect):  # skip this letter if it's already in correct spot
                continue
            for j in range(5):  # inner loop for the target word
                if i == j or target_word_letters[j] == "*":
                    continue
                if guess[i] == target_word_letters[j]:
                    target_word_letters[j] = "*"
                    pattern[i] = int(Placing.misplaced)
                    break
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


    def step(self, guess, secret_word):
        guess = guess.lower()
        if guess not in self.legal_words:
            raise ValueError('invalid word')

        if self.max_iter is not None and self.cur_iter >= self.max_iter:
            self.done = True
            return [], self.done

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word)

        if pattern.count(int(Placing.correct)) == len(pattern):
            self.done = True

        return pattern, self.done

    def reset(self):
        self.cur_iter = 0
        self.done = False
        self.cur_legal_words = self.legal_words
