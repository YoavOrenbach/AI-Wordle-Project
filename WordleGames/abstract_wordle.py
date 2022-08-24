import random
from abc import ABC, abstractmethod
from typing import List

import util
from utils.common import GameType, WINNING_PATTERN


class InvalidGuessException(ValueError):
    pass


class AbstractWordle(ABC):
    """An abstract class representing each Wordle type game"""

    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[], game_type=None):
        """
        Initializes an abstract wordle game with the list of secret words without knowing the secret word itself.
        In addition, it is receives the list of legal words for the algorithms to guess, the maximum game iterations,
        the previous game state, the previous possible words (matching previous patterns), and the game type.
        """
        super(AbstractWordle, self).__init__()
        self.type: GameType = game_type
        self._secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.done = False
        if not cur_possible_words:
            self.cur_possible_words = legal_words
        else:
            self.cur_possible_words = cur_possible_words
        self.all_patterns = []
        self.states = game_state  # contains pairs of (guess, pattern), namely a word and its resulting pattern.

    def get_type(self):
        """Retunrs the type of the game."""
        return self.type

    def get_all_patterns(self):
        """Returns all possible game patterns"""
        return self.all_patterns

    def get_done(self):
        """Returns if the game is over or not."""
        return self.done

    def get_game_state(self):
        """Returns the game state - a list of (guess, pattern) tuples."""
        return self.states

    def get_turn_num(self):
        """Returns the turn of the game."""
        return len(self.states) + 1

    def get_legal_words(self):
        """Returns the legal words list."""
        return self.legal_words

    def get_possible_words(self) -> List[str]:
        """Returns the possible words list (matching the previous guesses and patterns)."""
        return self.cur_possible_words

    def generate_secret_word(self):
        """Generates a random secret word."""
        return random.choice(self._secret_words)

    def step(self, guess: str, secret_word: str):
        """
        Performs a single step in the game following a guess. It updates the game state and the list of possible words.
        :return: the resulting pattern of the guess, a boolean flag - whether the game is done, a boolean flag -
        did the player win.
        """
        guess = guess.lower()
        if guess not in self.legal_words:
            raise InvalidGuessException('invalid word')

        self.cur_iter += 1

        pattern = self.get_pattern(guess, secret_word)
        self.states.append((guess, pattern))
        self.cur_possible_words = self.filter_words()
        is_win = (guess == secret_word) if self.type != GameType.Absurdle else (tuple(pattern) == WINNING_PATTERN)
        is_max_iter = (self.max_iter is not None and self.cur_iter >= self.max_iter)
        if is_win or is_max_iter:
            self.done = True

        return pattern, self.done, is_win

    def reset(self):
        """Resets the game."""
        self.cur_iter = 0
        self.done = False
        self.cur_possible_words = self.legal_words
        self.states.clear()

    def apply_action(self, action: str):
        """Applies agent action. The action is a word and it is added to the game state without a pattern."""
        self.states.append((action, []))

    def apply_opponent_action(self, action):
        """Applies the opponent action. The action is a pattern, so it updates the guess of the agent to have
         the pattern. In addition, it updates the possible words list for the next agent action."""
        guess, _ = self.states[-1]
        pattern = list(action)
        self.states[-1] = (guess, pattern)
        self.cur_possible_words = self.filter_words()

    def get_possible_patterns(self, guess):
        """This method returns all possible patterns for the opponent by generating patterns for all possible words.
        It enters them to a util.Counter so they can be used to calculate the expected score in Expectimax."""
        patterns_counter = util.Counter()
        for secret_word in self.cur_possible_words:
            patterns_counter[tuple(self.get_pattern(guess, secret_word))] += 1
        return patterns_counter

    @abstractmethod
    def filter_words(self):
        """Filters words from the possible words list according to the last guess and pattern."""
        pass

    @abstractmethod
    def get_pattern(self, guess: str, secret_word: str):
        """Returns a list containing the placing of each letter in the guess according to the secret word."""
        pass

    @abstractmethod
    def successor_creator(self):
        """Creates a successor game object for the adversarial algorithms."""
        pass
