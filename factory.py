from Algorithms import Random, Minimax, AlphaBeta, Expectimax, Entropy, Reinforcement
from WordleGames import BasicWordleLogic, AbsurdleLogic, NoisyWordleLogic, YellowWordle
from WordleGames.vocabulary_wordle_logic import VocabularyWordleLogic
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType, GameType


def load_word_lists():
    with open('legal_words.txt', 'r') as f:
        legal_words = f.read().splitlines()
    with open('secret_words.txt', 'r') as f:
        secret_words = f.read().splitlines()
    return secret_words, legal_words


def get_game(secret_words, legal_words, game_type: GameType):
    if game_type == GameType.BasicWordle:
        game = BasicWordleLogic(secret_words, legal_words)
    elif game_type == GameType.Absurdle:
        game = AbsurdleLogic(secret_words, legal_words)
    elif game_type == GameType.FakeVocabularyWordle:
        game = VocabularyWordleLogic(vocabulary_size=12972, real_vocabulary=False)
    elif game_type == GameType.RealVocabularyWordle:
        game = VocabularyWordleLogic(vocabulary_size=1000, real_vocabulary=True, secret_words=secret_words,
                                     legal_words=legal_words)
    elif game_type == GameType.NoisyWordle:
        game = NoisyWordleLogic(secret_words, legal_words)
    else:
        game = YellowWordle(secret_words, legal_words)
    return game


def get_algorithm(algorithm_type: AlgorithmType, game: AbstractWordleLogic):
    if algorithm_type == AlgorithmType.Random:
        algorithm = Random()
    elif algorithm_type == AlgorithmType.Minimax:
        algorithm = Minimax()
    elif algorithm_type == AlgorithmType.AlphaBeta:
        algorithm = AlphaBeta()
    elif algorithm_type == AlgorithmType.Expectimax:
        algorithm = Expectimax()
    elif algorithm_type == AlgorithmType.Entropy:
        algorithm = Entropy()
    else:
        algorithm = Reinforcement(game, train=False)
    return algorithm


def get_game_dictionary(secret_words, legal_words):
    games_dic = {}
    for game_type in GameType:
        games_dic[game_type.value] = get_game(secret_words, legal_words, game_type)
    return games_dic


def get_algorithms_dictionary(game: AbstractWordleLogic):
    algos_dic = {}
    for algo_type in AlgorithmType:
        algos_dic[algo_type.value] = get_algorithm(algo_type, game)
    return algos_dic
