import numpy as np
import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType

import random
from common import Placing, MAX, MIN


class Minimax(Algorithm):
    def __init__(self, depth=1):
        super(Minimax, self).__init__(AlgorithmType.Minimax)
        self.depth = depth

    def minimax_val(self, curr_depth, game_logic: AbstractWordleLogic, player_id):
        legal_actions = game_logic.get_legal_actions(player_id)
        if curr_depth == self.depth * 2 or game_logic.done or not legal_actions:
            return evaluation_function(game_logic)

        result_lst = []
        for i, action in enumerate(legal_actions):
            successor_game = game_logic.generate_successor(agent_index=MAX, action=action)
            if player_id == MAX:
                result_lst.append(self.minimax_val(curr_depth + 1, successor_game, MIN))
            else:
                result_lst.append(self.minimax_val(curr_depth + 1, successor_game, MAX))
        return max(result_lst) if player_id == MAX else min(result_lst)

    def get_action(self, game_logic: AbstractWordleLogic):
        possible_words = game_logic.get_possible_words()
        best_action = random.choice(possible_words)
        high_score = -np.inf
        for word in possible_words:
            successor_game = game_logic.generate_successor(agent_index=MAX, action=word)
            minimax_score = self.minimax_val(1, successor_game, MIN)
            if high_score < minimax_score:
                high_score = minimax_score
                best_action = word

        return best_action


class AlphaBeta(Algorithm):
    def __init__(self, depth=2):
        super(AlphaBeta, self).__init__(AlgorithmType.AlphaBeta)
        self.depth = depth

    def alphabeta_val(self, curr_depth, game_logic: AbstractWordleLogic, alpha, beta, player_id):
        legal_actions = game_logic.get_legal_actions(player_id)
        if curr_depth == self.depth * 2 or game_logic.done or not legal_actions:
            return evaluation_function(game_logic)

        if player_id == MAX:
            for i, action in enumerate(legal_actions):
                successor_game = game_logic.generate_successor(agent_index=MAX, action=action)
                result = self.alphabeta_val(curr_depth + 1, successor_game, alpha, beta, MIN)
                alpha = max(alpha, result)
                if beta <= alpha:
                    break
            return alpha
        else:
            for i, action in enumerate(legal_actions):
                successor_game = game_logic.generate_successor(agent_index=MAX, action=action)
                result = self.alphabeta_val(curr_depth + 1, successor_game, alpha, beta, MAX)
                beta = min(beta, result)
                if beta <= alpha:
                    break
            return beta

    def get_action(self, game_logic: AbstractWordleLogic):
        possible_words = game_logic.get_possible_words()
        best_action = random.choice(possible_words)
        high_score = -np.inf
        for word in possible_words:
            successor_game = game_logic.generate_successor(agent_index=MAX, action=word)
            minimax_score = self.alphabeta_val(1, successor_game, -np.inf, np.inf, MIN)
            if high_score < minimax_score:
                high_score = minimax_score
                best_action = word
        return best_action


class Expectimax(Algorithm):
    def __init__(self, depth=2):
        super(Expectimax, self).__init__(AlgorithmType.Expectimax)
        self.depth = depth

    def expectimax_val(self, curr_depth, game_logic: AbstractWordleLogic, player_id):
        legal_actions = game_logic.get_legal_actions(player_id)
        if curr_depth == self.depth * 2 or game_logic.done or not legal_actions:
            return evaluation_function(game_logic)

        result_lst = []
        for i, action in enumerate(legal_actions):
            successor_game = game_logic.generate_successor(agent_index=MAX, action=action)
            if player_id == MAX:
                result_lst.append(self.expectimax_val(curr_depth + 1, successor_game, MIN))
            else:
                result_lst.append(self.expectimax_val(curr_depth + 1, successor_game, MAX))
        return max(result_lst) if player_id == MAX else sum(result_lst)/len(legal_actions)

    def get_action(self, game_logic: AbstractWordleLogic):
        possible_words = game_logic.get_possible_words()
        best_action = random.choice(possible_words)
        high_score = -np.inf
        for word in possible_words:
            successor_game = game_logic.generate_successor(agent_index=MAX, action=word)
            minimax_score = self.expectimax_val(1, successor_game, MIN)
            if high_score < minimax_score:
                high_score = minimax_score
                best_action = word
        print(best_action)
        return best_action


def evaluation_function(game_logic: AbstractWordleLogic):
    """
    score = 0
    for guess, pattern in game_logic.get_game_state():
        for placing in pattern:
            if placing == Placing.correct.value:
                score += (game_logic.max_iter-game_logic.get_turn_num()+1) * 10
            elif placing == Placing.misplaced.value:
                score += (game_logic.max_iter-game_logic.get_turn_num()+1) * 5
            else:
                score -= (game_logic.get_turn_num()+1) * 5
    return score
    """
    remaining_words = len(game_logic.get_possible_words())
    return -remaining_words


