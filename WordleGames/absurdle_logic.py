import random
from typing import List

import util
from WordleGames.abstract_wordle_logic import AbstractWordleLogic, InvalidGuessException
from WordleGames.utils import get_pattern_vanilla
from common import Word, Placing, WINNING_PATTERN
from game_visible_state import GameVisibleState


class AbsurdleLogic(AbstractWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6):
        super(AbsurdleLogic, self).__init__("Absurdle", secret_words, legal_words, max_iter)

    def generate_secret_word(self):
        return None

    def step(self, guess: str, secret_word: str, game_state: GameVisibleState):
        """Your code here"""
        guess = guess.lower()
        if guess not in self.legal_words:
            raise InvalidGuessException('invalid word')

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word, game_state)

        is_win = (guess == WINNING_PATTERN)
        is_max_iter = (self.max_iter is not None and self.cur_iter >= self.max_iter)
        if is_win or is_max_iter:
            self.done = True

        return pattern, self.done, is_win

    def get_possible_words(self, game_visible_state: GameVisibleState) -> List[Word]:
        # TODO: this is code duplication
        """
                This method updates and returns the current words one can guess in a basic wordle game.
                There are 5 filters a word must pass to be considered possible:
                1. It must not contain grey (incorrect) letters that are not already green or yellow.
                2. It must NOT contain a yellow (misplaced) letter in the same spot as the last pattern, since we know it's not
                   the right place, however, the letter must be present in the word.
                3. It must contain EXACTLY green (correct) letters in the same place as the last pattern.
                4. It must NOT contain more letters than the known amount (we can deduce the number of appearances of a letter
                   in the secret word if a letter was green/yellow and also grey according to the official wordle rules).
                5. It must also NOT contain less letters than the known amount (if a letter is both green and yellow in
                   different places it must appear at least twice).
                :param game_visible_state: the current state of the game containing a list of pairs of (guess, patterns)
                :return: the current list of legal words to guess: self.cur_legal_words
                """
        states = game_visible_state.get_states()
        if not states:  # if no guess was made we return the list as is, since every word is possible.
            return self.cur_possible_words
        guess, pattern = states[-1]

        correct_letters, removed_letters, misplaced_letters = [], [], []  # lists to hold letters placing with indices.
        correct, removed, misplaced = [], [], []  # lists to hold only letters placing.
        minimum_letters = util.Counter()  # Counter to hold the minimal number of letters appearances (filter 5)
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

        special_letters = util.Counter()  # special Counter to hold the maximal number of letter appearances (filter 4)
        for idx, letter in removed_letters:  # we are looking for grey letters that were also green or yellow.
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
                removed = list(filter((letter).__ne__, removed))  # we remove a special letter from the removed list

        def should_keep_word(word):
            # 1. remove words with incorrect letters
            if any(letter in word for letter in removed):
                return False

            # 2. remove words if they have misplaced letters in the wrong spot or misplaced letters are not in the word
            if any((word[idx] == letter or letter not in word) for idx, letter in misplaced_letters):
                return False

            # 3. remove words that don't match correct letters
            if any((word[idx] != letter) for idx, letter in correct_letters):
                return False

            # 4. remove words that contain more letters than the known amount
            for letter in special_letters:
                if word.count(letter) > special_letters[letter]:
                    return False

            # 5. remove words that contain less letters than the known amount
            for letter in minimum_letters:
                if word.count(letter) < minimum_letters[letter]:
                    return False

            return True

        self.cur_possible_words = list(filter(should_keep_word, self.cur_possible_words))
        return self.cur_possible_words

    def get_pattern(self, guess: str, secret_word: str, game_state: GameVisibleState):
        """Returns a list containing the placing of each letter in the guess."""
        all_patterns = AbstractWordleLogic.all_patterns
        pattern_words_count = {pattern: 0 for pattern in all_patterns}
        possible_words = self.get_possible_words(game_state)
        for word in possible_words:
            word_pattern = tuple(get_pattern_vanilla(guess, word))
            pattern_words_count[word_pattern] += 1
        max_count = max(pattern_words_count.values())
        if max_count == 0:
            best_pattern = tuple(WINNING_PATTERN)
        else:
            best_patterns = [k for k, v in pattern_words_count.items() if v == max_count and k != WINNING_PATTERN]
            best_pattern = random.choice(best_patterns)
        return list(best_pattern)
