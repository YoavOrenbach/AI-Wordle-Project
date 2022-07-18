import util
# from WordleGames.basic_wordle_logic import BasicWordleLogic
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from typing import List
from common import Placing
from game_visible_state import GameVisibleState


class YellowWordle(AbstractWordleLogic):
    def __init__(self, secret_words, legal_words, max_iter=6):
        super(YellowWordle, self).__init__("Yellow Wordle", secret_words, legal_words, max_iter)

    def get_pattern(self, guess: str, secret_word: str) -> List[int]:
        target_word = list(secret_word)
        pattern = [Placing.incorrect for _ in range(5)]

        for i in range(5):
            if guess[i] in target_word:
                target_word.remove(guess[i])
                pattern[i] = Placing.misplaced

        return [int(elem) for elem in pattern]

    def reset(self):
        self.cur_iter = 0
        self.done = False
        self.cur_legal_words = self.legal_words

    def get_possible_words(self, game_visible_state: GameVisibleState) -> List[str]:
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
        if not states: # if no guess was made we return the list as is, since every word is possible.
            return self.cur_legal_words
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

            # 3. remove words that don't match correct letters
            # if any((word[idx] != letter) for idx, letter in correct_letters):
            #    return False

            # 4. remove words that contain more letters than the known amount
            for letter in special_letters:
                if word.count(letter) > special_letters[letter]:
                    return False

            # 5. remove words that contain less letters than the known amount
            for letter in minimum_letters:
                if word.count(letter) < minimum_letters[letter]:
                    return False

            return True

        self.cur_legal_words = list(filter(should_keep_word, self.cur_legal_words))
        return self.cur_legal_words