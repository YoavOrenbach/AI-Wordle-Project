from typing import List

import util
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from WordleGames.utils import get_pattern_vanilla
from common import Placing, Word, GameType, MAX, MIN


class BasicWordleLogic(AbstractWordleLogic):
    """Classic Wordle game"""

    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[], game_type=GameType.BasicWordle):
        super(BasicWordleLogic, self).__init__(secret_words, legal_words, max_iter, game_state, cur_possible_words, game_type)

    def get_pattern(self, guess: Word, secret_word: Word):
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
                pattern.append(int(Placing.incorrect))
        return pattern

    def get_possible_patterns(self, guess: str):
        return [self.get_pattern(guess, self._secret_word)]

    def successor_creator(self, successor=None, agent_index=MAX, action=None):
        return BasicWordleLogic(self._secret_words, self.legal_words, self.max_iter,
            self.states.copy(), self.cur_possible_words.copy())

    def filter_words(self) -> List[Word]:
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
        states = self.states
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
            if any((word[idx]==letter or letter not in word) for idx, letter in misplaced_letters):
                return False

            # 3. remove words that don't match correct letters
            if any((word[idx]!=letter) for idx, letter in correct_letters):
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

        return list(filter(should_keep_word, self.cur_possible_words))
