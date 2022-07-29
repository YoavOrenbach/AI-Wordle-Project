import numpy as np
from abc import abstractmethod

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType

import random
from common import MAX, MIN
from tqdm import tqdm


class AdversarialAgent(Algorithm):
    def __init__(self, algorithm_type, depth=1):
        super(AdversarialAgent, self).__init__(algorithm_type)
        self.depth = depth

    @abstractmethod
    def adversarial_search(self, curr_depth, game_logic: AbstractWordleLogic, player_id, alpha=0, beta=0):
        pass

    def get_action(self, game_logic: AbstractWordleLogic):
        possible_words = game_logic.get_possible_words()
        best_action = random.choice(possible_words)
        high_score = -np.inf
        for word in tqdm(possible_words):
            successor_game = game_logic.generate_successor(agent_index=MAX, action=word)
            minimax_score = self.adversarial_search(1, successor_game, MIN, -np.inf, np.inf)
            if high_score < minimax_score:
                high_score = minimax_score
                best_action = word
        print(best_action)
        return best_action


class Minimax(AdversarialAgent):
    def __init__(self):
        super(Minimax, self).__init__(AlgorithmType.Minimax)

    def adversarial_search(self, curr_depth, game_logic: AbstractWordleLogic, player_id, alpha=0, beta=0):
        legal_actions = game_logic.get_legal_actions(player_id)
        if curr_depth == self.depth * 2 or game_logic.get_done() or not legal_actions:
            return evaluation_function(game_logic)

        result_lst = []
        for i, action in enumerate(legal_actions):
            successor_game = game_logic.generate_successor(agent_index=player_id, action=action)
            if player_id == MAX:
                result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MIN))
            else:
                result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MAX))
        return max(result_lst) if player_id == MAX else min(result_lst)


class AlphaBeta(AdversarialAgent):
    def __init__(self):
        super(AlphaBeta, self).__init__(AlgorithmType.AlphaBeta)

    def adversarial_search(self, curr_depth, game_logic: AbstractWordleLogic, player_id, alpha=0, beta=0):
        legal_actions = game_logic.get_legal_actions(player_id)
        if curr_depth == self.depth * 2 or game_logic.get_done() or not legal_actions:
            return evaluation_function(game_logic)

        if player_id == MAX:
            for i, action in enumerate(legal_actions):
                successor_game = game_logic.generate_successor(agent_index=MAX, action=action)
                result = self.adversarial_search(curr_depth + 1, successor_game, MIN, alpha, beta)
                alpha = max(alpha, result)
                if beta <= alpha:
                    break
            return alpha
        else:
            for i, action in enumerate(legal_actions):
                successor_game = game_logic.generate_successor(agent_index=MAX, action=action)
                result = self.adversarial_search(curr_depth + 1, successor_game, MAX, alpha, beta)
                beta = min(beta, result)
                if beta <= alpha:
                    break
            return beta


class Expectimax(AdversarialAgent):
    def __init__(self):
        super(Expectimax, self).__init__(AlgorithmType.Expectimax)

    def adversarial_search(self, curr_depth, game_logic: AbstractWordleLogic, player_id, alpha=0, beta=0):
        legal_actions = game_logic.get_legal_actions(player_id)
        if curr_depth == self.depth * 2 or game_logic.get_done() or not legal_actions:
            return evaluation_function(game_logic)

        result_lst = []
        for i, action in enumerate(legal_actions):
            successor_game = game_logic.generate_successor(agent_index=player_id, action=action)
            if player_id == MAX:
                result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MIN))
            else:
                result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MAX))
        return max(result_lst) if player_id == MAX else sum(result_lst) / len(legal_actions)


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
