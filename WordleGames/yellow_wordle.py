import itertools
from typing import List

import util
from WordleGames.abstract_wordle import AbstractWordle
from common import Placing, GameType, LETTERS_NUM, MAX


class YellowWordle(AbstractWordle):
    """Yellow Wordle game"""
    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[]):
        super(YellowWordle, self).__init__(secret_words, legal_words, max_iter, game_state,
            cur_possible_words, GameType.YellowWordle)
        self.all_patterns = [list(pattern) for pattern in
                             itertools.product([Placing.misplaced.value, Placing.incorrect.value], repeat=LETTERS_NUM)]

    def get_pattern(self, guess: str, secret_word: str):
        """Returns a legal pattern for a Yellow Wordle game according to the secret word"""
        target_word = list(secret_word)
        pattern = [Placing.incorrect for _ in range(LETTERS_NUM)]

        for i in range(LETTERS_NUM):
            if guess[i] in target_word:
                target_word.remove(guess[i])
                pattern[i] = Placing.misplaced

        return [int(elem) for elem in pattern]

    def successor_creator(self, agent_index=MAX, action=None):
        """Creates a successor game object for the adversarial algorithms."""
        return YellowWordle(self._secret_words, self.legal_words, self.max_iter, self.states.copy(),
                            self.cur_possible_words.copy())

    def filter_words(self) -> List[str]:
        """
        This method updates and returns the current words one can guess in a basic wordle game.
        There are 4 filters a word must pass to be considered possible:
        1. It must not contain grey (incorrect) letters that are not already green or yellow.
        2. It must NOT contain a yellow (misplaced) letter in the same spot as the last pattern, since we know it's not
           the right place, however, the letter must be present in the word.
        3. It must NOT contain more letters than the known amount (we can deduce the number of appearances of a letter
           in the secret word if a letter was green/yellow and also grey according to the official wordle rules).
        4. It must also NOT contain less letters than the known amount (if a letter is both green and yellow in
           different places it must appear at least twice).
        :param game_visible_state: the current state of the game containing a list of pairs of (guess, patterns)
        :return: the current list of legal words to guess: self.cur_legal_words
        """
        states = self.get_game_state()
        if not states:  # if no guess was made we return the list as is, since every word is possible.
            return self.cur_possible_words
        guess, pattern = states[-1]

        removed_letters, misplaced_letters = [], []  # lists to hold letters placing with indices.
        removed, misplaced = [], []  # lists to hold only letters placing.
        minimum_letters = util.Counter()  # Counter to hold the minimal number of letters appearances (filter 5)
        for idx, (letter, match) in enumerate(zip(guess, pattern)):
            if match == int(Placing.incorrect):
                removed_letters.append((idx, letter))
                removed.append(letter)
            else:
                misplaced_letters.append((idx, letter))
                misplaced.append(letter)
                minimum_letters[letter] += 1

        special_letters = util.Counter()  # special Counter to hold the maximal number of letter appearances (filter 4)
        for idx, letter in removed_letters:  # we are looking for grey letters that were also green or yellow.
            pop_flag = False
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
            if any((letter not in word) for idx, letter in misplaced_letters):
                return False

            # 3. remove words that contain more letters than the known amount
            for letter in special_letters:
                if word.count(letter) > special_letters[letter]:
                    return False

            # 4. remove words that contain less letters than the known amount
            for letter in minimum_letters:
                if word.count(letter) < minimum_letters[letter]:
                    return False

            return True

        return list(filter(should_keep_word, self.cur_possible_words))
