import matplotlib.pyplot as plt
import numpy as np

from Algorithms import Random, Minimax, AlphaBeta, Expectimax, Entropy, Reinforcement
from WordleGames import BasicWordleLogic
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from common import AlgorithmType
from simulator import Simulator


def evaluate_algorithms(num_games, game: AbstractWordleLogic, secret_words=None):
    algorithms = [Random(), Minimax(), AlphaBeta(), Expectimax(), Entropy(), Reinforcement(game, train=False)]
    algorithm_names = [algorithm_type.value for algorithm_type in AlgorithmType]
    avg_results = []
    win_percentage = []

    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        results = simulator.simulate_games(num_games=num_games, user_interface=False, secret_words=secret_words)
        cum_stats = np.sum(results, axis=0)
        avg_results.append(cum_stats[1] / num_games)
        win_percentage.append(100 * cum_stats[0] / num_games)

    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, avg_results, color='royalblue')
    for i in range(len(algorithm_names)):
        plt.text(i, avg_results[i], "{:.2f}".format(avg_results[i]), ha='center')
    plt.title(f"Algorithms average number of guesses on {game.get_type().value} game for {num_games} games")
    plt.ylabel("Average number of guesses")
    plt.xlabel("Algorithms")
    plt.ylim([0, 6])
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, win_percentage, color='firebrick')
    for i in range(len(algorithm_names)):
        plt.text(i, win_percentage[i], "{:.2f}%".format(win_percentage[i]), ha='center')
    plt.title(f"Algorithms win percentage on {game.get_type().value} game for {num_games} games")
    plt.ylabel("win percentage")
    plt.xlabel("Algorithms")
    plt.show()


def evaluate_basic_wordle(secret_words, legal_words, num_games):
    game = BasicWordleLogic(secret_words, legal_words)
    evaluate_algorithms(num_games, game, secret_words)


def main():
    with open('legal_words.txt', 'r') as f:
        legal_words = f.read().splitlines()
    with open('secret_words.txt', 'r') as f:
        secret_words = f.read().splitlines()
    evaluate_basic_wordle(secret_words, legal_words, len(secret_words))


if __name__ == '__main__':
    main()
