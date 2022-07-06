import util
from common import Placing


class GameState:
    """A class for representing the game state"""

    def __init__(self, word_list):
        self.possible_guesses = word_list
        self.states = []  # contains pairs of (guess, pattern), namely a word and its resulting pattern.

    def get_possible_guesses(self):
        return self.possible_guesses

    def get_states(self):
        return self.states

    def add_state(self, guess, pattern):
        self.states.append((guess, pattern))

    def filter_wordle_guesses(self, ):
        guess, pattern = self.states[-1]

        correct_letters, removed_letters, misplaced_letters = [], [], []
        correct, removed, misplaced = [], [], []
        for idx, (letter, match) in enumerate(zip(guess, pattern)):
            if match == int(Placing.incorrect):
                removed_letters.append((idx, letter))
                removed.append(letter)
            elif match == int(Placing.correct):
                correct_letters.append((idx, letter))
                correct.append(letter)
            else:
                misplaced_letters.append((idx, letter))
                misplaced.append(letter)

        special_letters = util.Counter()
        for idx, letter in removed_letters:
            pop_flag = False
            if letter in correct:
                special_letters[letter] += 1 + correct.count(letter)
                misplaced_letters.append((idx, letter))
                pop_flag = True
            if letter in misplaced:
                special_letters[letter] += 1 + misplaced.count(letter)
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
                if word.count(letter) >= special_letters[letter]:
                    return False

            return True

        self.possible_guesses = list(filter(should_keep_word, self.possible_guesses))
