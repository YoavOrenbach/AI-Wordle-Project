from abc import ABC, abstractmethod
import random


class Algorithm(ABC):
    def __init__(self, name):
        super(Algorithm, self).__init__()
        self.name = name

    @abstractmethod
    def next_guess(self, game_state, game):
        pass

    @abstractmethod
    def reset(self):
        pass


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__("random")
        self.guess_count = 0
        self.possible_guesses = []

    def next_guess(self, game_state, game):
        if self.guess_count == 0:
            self.possible_guesses = game.get_word_list().copy()
            self.guess_count += 1
            return random.choice(self.possible_guesses)
        self.guess_count += 1
        self.possible_guesses = remove_impossible_words(game_state[-1], self.possible_guesses)
        return random.choice(self.possible_guesses)

    def reset(self):
        self.guess_count = 0


def remove_impossible_words(last_state, word_list):
    guess, result = last_state

    # correct letters, keep these
    correct_letters = [(idx, l) for idx, (l, c) in enumerate(zip(guess, result)) if c == 'CORRECT']

    # remove words with these letters in them
    removed_letters = [l for l, c in zip(guess, result) if c == 'INCORRECT']

    # these letters can't be in these positions
    misplaced_letters = [(idx, l) for idx, (l, c) in enumerate(zip(guess, result)) if c == 'MISPLACED']

    # filter test func
    def should_keep_word(word):
        # remove words with incorrect letters
        if any(letter in word for letter in removed_letters):
            return False

        # remove words if they have misplaced letters in the wrong spot
        if any( (word[idx] == letter) for idx, letter in misplaced_letters ):
            return False

        # remove words that don't match correct letters
        if any( (word[idx] != letter) for idx, letter in correct_letters ):
            return False

        return True

    new_possible_guesses = list( filter(should_keep_word, word_list) )

    total_removed = len(word_list) - len(new_possible_guesses)
    return new_possible_guesses