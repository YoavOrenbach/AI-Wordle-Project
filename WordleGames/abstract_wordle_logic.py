import itertools
import random
from abc import ABC, abstractmethod
from typing import List
from typing import List, Tuple

from common import Placing, LETTERS_NUM, GameType, MAX, MIN


class InvalidGuessException(ValueError):
    pass


class AbstractWordleLogic(ABC):
    """An abstract class representing each Wordle type game"""
    all_patterns = [pattern for pattern in
                    itertools.product([placing.value for placing in Placing], repeat=LETTERS_NUM)]

    def __init__(self, secret_words, legal_words, max_iter=6, game_state=[], cur_possible_words=[], game_type=None):
        super(AbstractWordleLogic, self).__init__()
        if cur_possible_words is None:
            cur_possible_words = []
        if game_state is None:
            game_state = []
        self.type: GameType = game_type
        self._secret_words = secret_words
        self.legal_words = legal_words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.done = False
        if not cur_possible_words:
            self.cur_possible_words = legal_words  # TODO: move to game visible state
        else:
            self.cur_possible_words = cur_possible_words
        self._secret_word = random.choice(self._secret_words)
        self.states = game_state  # contains pairs of (guess, pattern), namely a word and its resulting pattern.

    def apply_action(self, action: str):
        self.states.append((action, ()))

    def apply_opponent_action(self, guess, action):
        self.states[-1] = (guess, action)
        self.cur_possible_words = self.filter_words()

    def generate_successor(self, agent_index=MAX, action=None):
        successor = self.successor_creator()
        if agent_index == MAX:
            successor.apply_action(action)  # action = guess
        elif agent_index == MIN:
            guess, _ = self.states[-1]
            successor.apply_opponent_action(guess, action)  # action = pattern
        else:
            raise Exception("illegal agent index.")
        return successor

    def get_legal_actions(self, agent_index=MAX):
        if agent_index == MAX:
            return self.get_possible_words()
        elif agent_index == MIN:
            guess, _ = self.states[-1]
            return self.get_possible_patterns(guess)
        else:
            raise Exception("illegal agent index.")

    def get_game_state(self):
        return self.states

    def get_turn_num(self):
        return len(self.states) + 1

    def generate_secret_word(self):
       # self._secret_word = random.choice(self._secret_words)
       return self._secret_word

    def get_legal_words(self):
        return self.legal_words

    def step(self, guess: str, secret_word: str):
        """
        Performs a single step in the game following a guess.
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

        is_win = (guess==secret_word)
        is_max_iter = (self.max_iter is not None and self.cur_iter >= self.max_iter)
        if is_win or is_max_iter:
            self.done = True

        return pattern, self.done, is_win

    def reset(self):
        """Resets the game state."""
        self.cur_iter = 0
        self.done = False
        self.cur_possible_words = self.legal_words
        self.states = []
        self._secret_word = random.choice(self._secret_words)

    def get_possible_words(self) -> List[str]:
        return self.cur_possible_words

    @abstractmethod
    def filter_words(self):
        pass

    @abstractmethod
    def get_pattern(self, guess: str, secret_word: str):
        """Returns a list containing the placing of each letter in the guess."""
        pass

    @abstractmethod
    def get_possible_patterns(self, guess: str):
        pass

    @abstractmethod
    def successor_creator(self):
        pass

    @property
    def secret_word(self):
        return self._secret_word
