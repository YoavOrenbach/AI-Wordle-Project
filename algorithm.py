from abc import ABC, abstractmethod
import random
import util
from game import Pattern


class Algorithm(ABC):
    """An abstract class representing each algorithm used to solving the various games."""
    def __init__(self, name):
        super(Algorithm, self).__init__()
        self.name = name

    @abstractmethod
    def next_guess(self, game_state, game):
        """Returns the next guess given the game state and the game being played."""
        pass

    @abstractmethod
    def reset(self):
        """Resets the algorithm."""
        pass


class Random(Algorithm):
    def __init__(self):
        super(Random, self).__init__("Random")
        self.guess_count = 0
        self.possible_guesses = []

    def next_guess(self, game_state, game):
        if self.guess_count == 0:
            self.possible_guesses = game.get_word_list().copy()
            self.guess_count += 1
            return random.choice(self.possible_guesses)
        self.guess_count += 1
        self.possible_guesses = filter_words(game_state[-1], self.possible_guesses)
        return random.choice(self.possible_guesses)

    def reset(self):
        self.guess_count = 0


class MiniMax(Algorithm):
    def __init__(self):
        super(MiniMax, self).__init__("MiniMax")
        util.raiseNotDefined()

    def next_guess(self, game_state, game):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()


class Entropy(Algorithm):
    def __init__(self):
        super(Entropy, self).__init__("Entropy")
        util.raiseNotDefined()

    def next_guess(self, game_state, game):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()


class ReinforcementLearning(Algorithm):
    def __init__(self):
        super(ReinforcementLearning, self).__init__("Reinforcement learning")
        util.raiseNotDefined()

    def next_guess(self, game_state, game):
        util.raiseNotDefined()

    def reset(self):
        util.raiseNotDefined()


def filter_words(last_state, word_list):
    """
    This function filters words from the word list given the last state of the game
    :param last_state: the last state of the game containing the last guess and last pattern received.
    :param word_list: The current word list to be filtered.
    :return: A filtered word list with words that can match the last pattern.
    """
    guess, result = last_state

    correct_letters, removed_letters, misplaced_letters = [], [], []
    correct, removed, misplaced = [], [], []
    for idx, (letter, match) in enumerate(zip(guess, result)):
        if match == int(Pattern.incorrect):
            removed_letters.append((idx, letter))
            removed.append(letter)
        elif match == int(Pattern.correct):
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

    new_possible_guesses = list(filter(should_keep_word, word_list))
    return new_possible_guesses