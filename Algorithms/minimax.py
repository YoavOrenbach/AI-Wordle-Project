from builtins import str

import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic

# Added
from game_visible_state import GameVisibleState
from copy import deepcopy, copy

import time

class Minimax(Algorithm):
    def __init__(self, depth=2):
        super(Minimax, self).__init__("MiniMax")
        self.guess_count = 0
        self.depth = depth

    def evaluation_function(self, game_state):
        if not game_state.get_states:
            return 0
        action, pattern = game_state.get_states()[-1]
        reward = 0
        turn = len(game_state.get_states())
        for placing in pattern:
            if placing == 0:
                reward += (6 - turn) * 10
            elif placing == 1:
                reward += (6 - turn) * 5
            else:
                reward -= (turn + 1) * 5
        return reward

    def generate_successor(self, agent_index=0, action="crane"):
        successor = GameVisibleState(current_game_state)
        if agent_index == 0:
            successor.apply_action(action)
        elif agent_index == 1:
            successor.apply_opponent_action(action)
        else:
            raise Exception("illegal agent index.")
        return successor

    def MiniMaxVal(self, curr_depth, game_logic, game_state, player_id, done):
        legal_words = game_logic.get_possible_words(game_state)
        if curr_depth == self.depth * 2 or not legal_words or done:
            return self.evaluation_function(game_state)

        result_lst = []
        for i, word in enumerate(legal_words):
            game_logic_copy = deepcopy(game_logic)
            game_state_copy = deepcopy(game_state)
            pattern, done = game_logic_copy.step(word)
            game_state_copy.add_state(word, pattern)
            if player_id == 0:
                result_lst.append(self.MiniMaxVal(curr_depth + 1, game_logic_copy, game_state_copy, 1, done))
            else:
                result_lst.append(self.MiniMaxVal(curr_depth + 1, game_logic_copy, game_state_copy, 0, done))
        return max(result_lst) if player_id == 0 else min(result_lst)

    def get_action(self, game_state: GameVisibleState, game_logic: AbstractWordleLogic):
        best_move = "crane"
        game_logic_copy = deepcopy(game_logic)
        game_state_copy = deepcopy(game_state)
        possible_words = game_logic_copy.get_possible_words(game_state_copy)
        high_score = float("-inf")
        for word in possible_words:
            pattern, done = game_logic_copy.step(word)
            game_state_copy.add_state(word, pattern)
            minimax_score = self.MiniMaxVal(1, game_logic_copy, game_state_copy, 1, 0)
            if high_score < minimax_score:
                high_score = minimax_score
                best_move = word
        self.guess_count += 1
        return best_move

    def reset(self):
        self.guess_count = 0
