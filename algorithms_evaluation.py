import matplotlib.pyplot as plt
import random

from WordleGames.abstract_wordle import AbstractWordle
from common import AlgorithmType, GameType
from simulator import Simulator
from factory import load_word_lists, get_game_dictionary, get_algorithms_dictionary


def plot_avg_guesses(algorithm_names, avg_results, game_type, num_games):
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, avg_results, color='royalblue')
    for i in range(len(algorithm_names)):
        plt.text(i, avg_results[i], "{:.2f}".format(avg_results[i]), ha='center')
    plt.title(f"Algorithms average number of guesses on {game_type.value} game for {num_games} games",
              fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.savefig(f"data/plots/{game_type.value}_avg_guesses")
    plt.show()


def plot_win_percentage(algorithm_names, win_percentage, game_type, num_games):
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, win_percentage, color='firebrick')
    for i in range(len(algorithm_names)):
        plt.text(i, win_percentage[i], "{:.2f}%".format(win_percentage[i]), ha='center')
    plt.title(f"Algorithms win percentage on {game_type.value} game for {num_games} games", fontweight='bold', fontsize=14)
    plt.ylabel("win percentage", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.savefig(f"data/plots/{game_type.value}_win_percentage")
    plt.show()


def plot_num_guesses(algorithm_names, num_guesses, game_type):
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, num_guesses, color='forestgreen')
    for i in range(len(algorithm_names)):
        plt.text(i, num_guesses[i], "{:.2f}".format(num_guesses[i]), ha='center')
    plt.title(f"Algorithms number of guesses on {game_type.value} game", fontweight='bold', fontsize=14)
    plt.ylabel("Number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.savefig(f"data/plots/{game_type.value}_num_guesses")
    plt.show()


def evaluate_wordle(game: AbstractWordle, algorithms, algorithm_names, num_games, secret_words=None):
    avg_results = []
    win_percentage = []
    if game.get_type() == GameType.YellowWordle or game.get_type() == GameType.NoisyWordle:
        secret_words = random.sample(secret_words, num_games)

    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        cum_stats = simulator.simulate_games(num_games=num_games, user_interface=False, secret_words=secret_words)
        avg_results.append(cum_stats[1] / num_games)
        win_percentage.append(100 * cum_stats[0] / num_games)

    plot_avg_guesses(algorithm_names, avg_results, game.get_type(), num_games)
    plot_win_percentage(algorithm_names, win_percentage, game.get_type(), num_games)


def evaluate_absurdle(game: AbstractWordle, algorithms, algorithm_names):
    num_guesses = []
    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        if algorithm.type == AlgorithmType.Random:
            cum_stats = simulator.simulate_games(num_games=100, user_interface=False)
            num_guesses.append(cum_stats[1] / 100)
        else:
            cum_stats = simulator.simulate_games(num_games=1, user_interface=False)
            num_guesses.append(cum_stats[1])
    plot_num_guesses(algorithm_names, num_guesses, game.get_type())


def main():
    random.seed(42)
    secret_words, legal_words = load_word_lists()
    games_dictionary = get_game_dictionary(secret_words, legal_words)
    algorithms_dictionary = get_algorithms_dictionary(games_dictionary[GameType.BasicWordle.value])
    algorithms = [algorithm for algorithm in algorithms_dictionary.values() if algorithm.type != AlgorithmType.Minimax]
    algorithm_names = [algorithm_type.value for algorithm_type in AlgorithmType if
                       algorithm_type != AlgorithmType.Minimax]
    wordle_game = games_dictionary[GameType.BasicWordle.value]
    evaluate_wordle(wordle_game, algorithms, algorithm_names, len(secret_words), secret_words)
    absurdle_game = games_dictionary[GameType.Absurdle.value]
    evaluate_absurdle(absurdle_game, algorithms, algorithm_names)
    yellow_game = games_dictionary[GameType.YellowWordle.value]
    evaluate_wordle(yellow_game, algorithms, algorithm_names, 100, secret_words)
    noisy_game = games_dictionary[GameType.NoisyWordle.value]
    evaluate_wordle(noisy_game, algorithms, algorithm_names, 100, secret_words)


if __name__ == '__main__':
    main()
