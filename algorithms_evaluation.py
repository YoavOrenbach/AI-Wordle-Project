import matplotlib.pyplot as plt
import numpy as np

from Algorithms import Random, Minimax, AlphaBeta, Expectimax, Entropy, Reinforcement
from WordleGames import BasicWordleLogic, AbsurdleLogic, NoisyWordleLogic, YellowWordle
from WordleGames.vocabulary_wordle_logic import VocabularyWordleLogic
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType, GameType
from simulator import Simulator


def evaluate_algorithms(num_games, game: AbstractWordleLogic):
    algorithms = [Random(), Minimax(), AlphaBeta(), Expectimax(), Entropy(), Reinforcement(game)]
    algorithm_names = [algorithm_type.value for algorithm_type in AlgorithmType]
    avg_results = []

    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        results = simulator.simulate_games(num_games=num_games, user_interface=False)
        cum_stats = np.sum(results, axis=0)
        avg_results.append(cum_stats[1] / num_games)

    plt.bar(algorithm_names, avg_results)
    for i in range(len(algorithm_names)):
        plt.text(i, avg_results[i], "{:.2f}".format(avg_results[i]), ha='center')
    plt.title(f"Algorithms average number guesses on {game.get_type().value} for {num_games} games")
    plt.ylabel("Average number of guesses")
    plt.xlabel("Algorithms")
    plt.show()


def evaluate_games(secret_words, legal_words, num_games):
    games = {GameType.BasicWordle.value: BasicWordleLogic(secret_words, legal_words),
             GameType.Absurdle.value: AbsurdleLogic(secret_words, legal_words),
             GameType.FakeVocabularyWordle.value: VocabularyWordleLogic(vocabulary_size=12972, real_vocabulary=False),
             GameType.RealVocabularyWordle.value: VocabularyWordleLogic(vocabulary_size=1000, real_vocabulary=True, secret_words=secret_words,
                 legal_words=legal_words),
             GameType.NoisyWordle.value: NoisyWordleLogic(secret_words, legal_words),
             GameType.YellowWordle.value: YellowWordle(secret_words, legal_words)}

    game_names = [game_type.value for game_type in GameType]
    for game in games.values():
        evaluate_algorithms(num_games, game)
        break


def main():
    with open('legal_words.txt', 'r') as f:
        legal_words = f.read().splitlines()
    with open('secret_words.txt', 'r') as f:
        secret_words = f.read().splitlines()
    num_games = 100
    evaluate_games(secret_words, legal_words, num_games)

if __name__ == '__main__':
    main()
