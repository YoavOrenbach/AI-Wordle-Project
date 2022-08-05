from Algorithms import Random, TotalRandom, Minimax, AlphaBeta, Expectimax, Entropy, Reinforcement
from WordleGames import BasicWordle, Absurdle, NoisyWordle, YellowWordle
from WordleGames.vocabulary_wordle import VocabularyWordle
from WordleGames.abstract_wordle import AbstractWordle
from common import AlgorithmType, GameType


def load_word_lists():
    with open('data/legal_words.txt', 'r') as f:
        legal_words = f.read().splitlines()
    with open('data/secret_words.txt', 'r') as f:
        secret_words = f.read().splitlines()
    return secret_words, legal_words


def get_game(secret_words, legal_words, game_type: GameType):
    if game_type == GameType.BasicWordle:
        game = BasicWordle(secret_words, legal_words)
    elif game_type == GameType.Absurdle:
        game = Absurdle(secret_words, legal_words)
    elif game_type == GameType.FakeVocabularyWordle:
        game = VocabularyWordle(vocabulary_size=12972, real_vocabulary=False)
    elif game_type == GameType.RealVocabularyWordle:
        game = VocabularyWordle(vocabulary_size=1000, real_vocabulary=True, secret_words=secret_words,
                                legal_words=legal_words)
    elif game_type == GameType.NoisyWordle:
        game = NoisyWordle(secret_words, legal_words)
    elif game_type == GameType.YellowWordle:
        game = YellowWordle(secret_words, legal_words)
    else:
        raise Exception(f"{game_type} is not valid game")
    return game


def get_algorithm(algorithm_type: AlgorithmType, game: AbstractWordle):
    if algorithm_type == AlgorithmType.Random:
        algorithm = Random()
    elif algorithm_type == AlgorithmType.TotalRandom:
        algorithm = TotalRandom()
    elif algorithm_type == AlgorithmType.Minimax:
        algorithm = Minimax()
    elif algorithm_type == AlgorithmType.AlphaBeta:
        algorithm = AlphaBeta()
    elif algorithm_type == AlgorithmType.Expectimax:
        algorithm = Expectimax()
    elif algorithm_type == AlgorithmType.Entropy:
        algorithm = Entropy()
    elif algorithm_type == AlgorithmType.Reinforcement:
        algorithm = Reinforcement(game, train=False)
    else:
        raise Exception(f"{algorithm_type} is not valid algorithm")
    return algorithm


def get_game_dictionary(secret_words, legal_words):
    games_dic = {}
    for game_type in GameType:
        games_dic[game_type.value] = get_game(secret_words, legal_words, game_type)
    return games_dic


def get_algorithms_dictionary(game: AbstractWordle):
    algos_dic = {}
    for algo_type in AlgorithmType:
        algos_dic[algo_type.value] = get_algorithm(algo_type, game)
    return algos_dic
