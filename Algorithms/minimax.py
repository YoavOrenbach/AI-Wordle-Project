import numpy as np
from abc import abstractmethod

from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle import AbstractWordle
from utils.common import AlgorithmType
from utils import util

import random
from utils.common import MAX, MIN, GameType, Placing


def generate_successor(game: AbstractWordle, agent_index=MAX, action=None):
    """
    Returns a game logic successor after a player turn was complete.
    """
    successor = game.successor_creator()
    if agent_index == MAX:
        successor.apply_action(action)  # action = guess
    elif agent_index == MIN:
        successor.apply_opponent_action(action)  # action = pattern
    else:
        raise Exception("illegal agent index.")
    return successor


def get_legal_actions(game: AbstractWordle, agent_index=MAX):
    """
    Returns legal action for each player.
    For MAX player, this function returns a new list of possible words.
    For Min player, this function returns a list of new possible patterns
    """
    if agent_index == MAX:
        return game.get_possible_words()
    elif agent_index == MIN:
        guess, _ = game.states[-1]
        return game.get_possible_patterns(guess)
    else:
        raise Exception("illegal agent index.")


class AdversarialAgent(Algorithm):
    """An abstract class representing each adversarial type agent"""
    def __init__(self, algorithm_type, depth=1):
        """Initializes the adversarial agent class, which contains the depth at which the agents will run"""
        super(AdversarialAgent, self).__init__(algorithm_type)
        self.depth = depth
        self.opening_guesses = None
        self.absurdle_computed_second_guess = ""

    @abstractmethod
    def adversarial_search(self, curr_depth, game: AbstractWordle, player_id, alpha=0.0, beta=0.0):
        """simulating the game as a two player game, and returning a score based on the agent logic"""
        pass

    def get_action(self, game: AbstractWordle):
        """Returns the adversarial agent action using self.depth"""
        if game.get_turn_num() == 1:
            if game.get_type() != GameType.RealVocabularyWordle:
                return self.opening_guesses[game.get_type()]
            else:
                return self.opening_guesses[game.get_type()][game.get_vocab_size()]
        elif game.get_type() == GameType.Absurdle and game.get_turn_num() == 2:
            return self.absurdle_computed_second_guess

        possible_words = game.get_possible_words()
        best_action = random.choice(possible_words)
        high_score = -np.inf
        for word in (possible_words):
            successor_game = generate_successor(game, agent_index=MAX, action=word)
            minimax_score = self.adversarial_search(1, successor_game, MIN, -np.inf, np.inf)
            if high_score < minimax_score:
                high_score = minimax_score
                best_action = word
        return best_action


class Minimax(AdversarialAgent):
    """Classing minimax agent"""
    def __init__(self, algorithm_type=AlgorithmType.Minimax):
        """Initializes the Minimax agent class"""
        super(Minimax, self).__init__(algorithm_type)
        self.opening_guesses = {GameType.BasicWordle: "serai", GameType.YellowWordle: "arise",
                                GameType.NoisyWordle: "stoae", GameType.Absurdle: "serai",
                                GameType.FakeVocabularyWordle: "zpnoy",
                                GameType.RealVocabularyWordle: {1000: "aeros",
                                                                2000: "lanes",
                                                                3000: "soare",
                                                                4000: "serai",
                                                                5000: "nears",
                                                                6000: "reans",
                                                                7000: "serai",
                                                                8000: "reais",
                                                                9000: "serai",
                                                                10000: "serai",
                                                                11000: "serai",
                                                                12000: "serai",
                                                                12972: "serai"}}
        self.absurdle_computed_second_guess = "bludy"


    def adversarial_search(self, curr_depth, game: AbstractWordle, player_id, alpha=0.0, beta=0.0):
            """simulating the game as a two player game, and returning a score based on the minimax logic"""
            legal_actions = get_legal_actions(game, player_id)
            if curr_depth == self.depth * 2 or game.get_done() or not legal_actions:
                return evaluation_function(game)

            result_lst = []
            for i, action in enumerate(legal_actions):
                successor_game = generate_successor(game, agent_index=player_id, action=action)
                if player_id == MAX:
                    result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MIN))
                else:
                    result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MAX))
            return max(result_lst) if player_id == MAX else min(result_lst)


class AlphaBeta(Minimax):
    """Minimax with alpha-beta pruning agent"""
    def __init__(self):
        """Initializes the Minimax with alpha-beta agent class"""
        super(AlphaBeta, self).__init__(AlgorithmType.AlphaBeta)

    def adversarial_search(self, curr_depth, game: AbstractWordle, player_id, alpha=0.0, beta=0.0):
        """simulating the game as a two player game, and returning a score based on the minimax with alpha-beta logic"""
        legal_actions = get_legal_actions(game, player_id)
        if curr_depth == self.depth * 2 or game.get_done() or not legal_actions:
            return evaluation_function(game)

        if player_id == MAX:
            for i, action in enumerate(legal_actions):
                successor_game = generate_successor(game, agent_index=player_id, action=action)
                result = self.adversarial_search(curr_depth + 1, successor_game, MIN, alpha, beta)
                alpha = max(alpha, result)
                if beta <= alpha:
                    break
            return alpha
        else:
            for i, action in enumerate(legal_actions):
                successor_game = generate_successor(game, agent_index=player_id, action=action)
                result = self.adversarial_search(curr_depth + 1, successor_game, MAX, alpha, beta)
                beta = min(beta, result)
                if beta <= alpha:
                    break
            return beta


class Expectimax(AdversarialAgent):
    """Expectimax agent"""
    def __init__(self):
        """Initializes the Expectimax agent class"""
        super(Expectimax, self).__init__(AlgorithmType.Expectimax)
        self.opening_guesses = {GameType.BasicWordle: "lares", GameType.YellowWordle: "arise",
                                GameType.NoisyWordle: "lares", GameType.Absurdle: "lares",
                                GameType.FakeVocabularyWordle: "oydpn",
                                GameType.RealVocabularyWordle: {1000: "rates",
                                                                2000: "tares",
                                                                3000: "tares",
                                                                4000: "soare",
                                                                5000: "tares",
                                                                6000: "lares",
                                                                7000: "rales",
                                                                8000: "lares",
                                                                9000: "lares",
                                                                10000: "lares",
                                                                11000: "lares",
                                                                12000: "lares",
                                                                12972: "lares"}}
        self.absurdle_computed_second_guess = "mount"

    def adversarial_search(self, curr_depth, game: AbstractWordle, player_id, alpha=0.0, beta=0.0):
        """simulating the game as a two player game, and returning a score based on the expectimax logic"""
        legal_actions = get_legal_actions(game, player_id)
        if curr_depth == self.depth * 2 or game.get_done() or not legal_actions:
            return evaluation_function(game)

        result_lst = []
        result_counter = util.Counter()
        for i, action in enumerate(legal_actions):
            successor_game = generate_successor(game, agent_index=player_id, action=action)
            if player_id == MAX:
                result_lst.append(self.adversarial_search(curr_depth + 1, successor_game, MIN))
            else:
                result_counter[tuple(action)] = (self.adversarial_search(curr_depth + 1, successor_game, MAX))
        return max(result_lst) if player_id == MAX else compute_expected_min(result_counter, legal_actions)


def compute_expected_min(result_counter, patterns_counter):
    """Returns expected result, used by the Expectimax agent"""
    return (patterns_counter * result_counter) / patterns_counter.totalCount()


def evaluation_function(game: AbstractWordle):
    """
    The evaluation function used by all adverserial agents, baes on the number of the remaining words.
    Returns the number of remaining words * (-1)
    """
    remaining_words = len(game.get_possible_words())
    return -remaining_words


def evaluation_function_turn_num(game: AbstractWordle):
    """Alternative evaluation function, based on the number of turns that are played."""
    return -game.get_turn_num()


def evaluation_function_game_score(game: AbstractWordle):
    """Alternative evaluation function, based on the pattern return by the game."""
    score = 0
    game_state = game.get_game_state()
    for _, pattern in game_state:
        for placing in pattern:
            if placing == Placing.correct.value:
                score += 10
            elif placing == Placing.misplaced.value:
                score += 5
            else:
                score += 1
    return score
