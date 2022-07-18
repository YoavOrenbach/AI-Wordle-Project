from typing import List, Tuple


class GameVisibleState:
    """A class for representing the game state"""

    def __init__(self, current_game_state=[]):
        self.states: List[Tuple] = current_game_state  # contains pairs of (guess, pattern), namely a word and its resulting pattern.

    def get_states(self):
        return self.states

    def add_state(self, guess, pattern):
        self.states.append((guess, pattern))
