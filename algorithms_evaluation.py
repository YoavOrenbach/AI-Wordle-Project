import matplotlib.pyplot as plt
import numpy as np
import random

from WordleGames.abstract_wordle import AbstractWordle
from common import AlgorithmType, GameType
from simulator import Simulator
from factory import load_word_lists, get_game_dictionary, get_algorithms_dictionary, get_game


def plot_avg_guesses(algorithm_names, avg_results, game_type, num_games):
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, avg_results, color='royalblue')
    for i in range(len(algorithm_names)):
        plt.text(i, avg_results[i], "{:.2f}".format(avg_results[i]), ha='center')
    plt.title(f"Algorithms average number of guesses on {game_type} game for {num_games} games",
              fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.savefig(f"data/plots/{game_type}_avg_guesses")
    plt.show()


def plot_win_percentage(algorithm_names, win_percentage, game_type, num_games):
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, win_percentage, color='firebrick')
    for i in range(len(algorithm_names)):
        plt.text(i, win_percentage[i], "{:.2f}%".format(win_percentage[i]), ha='center')
    plt.title(f"Algorithms win percentage on {game_type} game for {num_games} games", fontweight='bold', fontsize=14)
    plt.ylabel("win percentage", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.savefig(f"data/plots/{game_type}_win_percentage")
    plt.show()


def plot_num_guesses(algorithm_names, num_guesses, game_type):
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, num_guesses, color='forestgreen')
    for i in range(len(algorithm_names)):
        plt.text(i, num_guesses[i], "{:.2f}".format(num_guesses[i]), ha='center')
    plt.title(f"Algorithms number of guesses on {game_type} game", fontweight='bold', fontsize=14)
    plt.ylabel("Number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.savefig(f"data/plots/{game_type}_num_guesses")
    plt.show()


def plot_real_vs_fake(algorithm_names, results_real, results_fake):
    bar_width = 1/3
    plt.subplots(figsize=(10, 6))

    # Set position of bar on X axis
    br1 = np.arange(len(results_real))
    br2 = [x + bar_width for x in br1]

    plt.bar(br1, results_real, color='royalblue', width=bar_width, edgecolor='grey', label='Real Vocabulary')
    for i in range(len(results_real)):
        plt.text(i, results_real[i], "{:.2f}".format(results_real[i]), ha='center')
    plt.bar(br2, results_fake, color='darkorange', width=bar_width, edgecolor='grey', label='Fake Vocabulary')
    for i in range(len(results_fake)):
        plt.text(i+0.333, results_fake[i], "{:.2f}".format(results_fake[i]), ha='center')

    plt.title("Algorithms average number of guesses using real Vs fake vocabulary", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xticks([r + bar_width/2 for r in range(len(results_real))], algorithm_names)
    plt.legend()
    plt.savefig("data/plots/real_vs_fake_avg_guesses")
    plt.show()


def plot_reinforcement_results():
    plt.figure(figsize=(10, 6))
    methods = ["Approximate Q-learning", "Q-learning with\nstate=turn", "Q-learning with\nstate=0"]
    results = [4.9, 3.84, 3.8]
    plt.bar(methods, results, color='royalblue')
    for i in range(len(results)):
        plt.text(i, results[i], "{:.2f}".format(results[i]), ha='center')
    plt.title("Different RL methods results on Wordle game",fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Reinforcement techniques", fontweight='bold', fontsize=14)
    plt.ylim([0,6])
    plt.savefig(f"data/plots/Reinforcement_results")
    plt.show()


def plot_entropy_results():
    plt.figure(figsize=(10, 6))
    methods = ["Max entropy", "Min expected score"]
    results = [3.75, 3.86]
    plt.bar(methods, results, color='royalblue')
    for i in range(len(results)):
        plt.text(i, results[i], "{:.2f}".format(results[i]), ha='center')
    plt.title("Entropy based techniques results on Wordle game",fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Reinforcement techniques", fontweight='bold', fontsize=14)
    plt.ylim([0,6])
    plt.savefig(f"data/plots/Entropy_results")
    plt.show()


def plot_adversarial_results():
    methods = ["Number of remaining words", "Game turn number", "Summing the game score"]
    minimax_results = [3.9, 3.99, 4.08]
    expectimax_results = [3.86, 3.84, 3.93]
    bar_width = 1/3
    plt.subplots(figsize=(10, 6))

    # Set position of bar on X axis
    br1 = np.arange(len(minimax_results))
    br2 = [x + bar_width for x in br1]

    plt.bar(br1, minimax_results, color='royalblue', width=bar_width, edgecolor='grey', label='Minimax')
    for i in range(len(minimax_results)):
        plt.text(i, minimax_results[i], "{:.2f}".format(minimax_results[i]), ha='center')
    plt.bar(br2, expectimax_results, color='darkorange', width=bar_width, edgecolor='grey', label='Expectimax')
    for i in range(len(expectimax_results)):
        plt.text(i+0.333, expectimax_results[i], "{:.2f}".format(expectimax_results[i]), ha='center')

    plt.title("Algorithms average number of guesses using real Vs fake vocabulary", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xticks([r + bar_width/2 for r in range(len(minimax_results))], methods)
    plt.ylim([0,6])
    plt.legend()
    plt.savefig("data/plots/Adversarial_guesses")
    plt.show()


def evaluate_wordle(game: AbstractWordle, algorithms, algorithm_names, num_games, secret_words=None):
    avg_results = []
    win_percentage = []
    if game.get_type() != GameType.BasicWordle:
        if game.get_type() == GameType.FakeVocabularyWordle:
            with open('data/vocab_word_lists/fake_secret_12972.txt', 'r') as f:
                secret_words = f.read().splitlines()
            secret_words = random.sample(secret_words, num_games)

    algorithms = [algorithms[-2]]
    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        cum_stats = simulator.simulate_games(num_games=num_games, user_interface=False, secret_words=secret_words)
        avg_results.append(cum_stats[1] / num_games)
        win_percentage.append(100 * cum_stats[0] / num_games)

    # plot_avg_guesses(algorithm_names, avg_results, game.get_type(), num_games)
    # plot_win_percentage(algorithm_names, win_percentage, game.get_type(), num_games)


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


def evaluate_vocab(secret_words, legal_words, algorithms):
    vocabulary_sizes = list(range(1000, 12001, 1000)) + [12972]
    num_games = 100
    plt.figure(figsize=(10, 6))
    for algorithm in algorithms:
        avg_results = []
        for vocab_size in vocabulary_sizes:
            vocab_wordle = get_game(secret_words, legal_words, GameType.RealVocabularyWordle, real_size=vocab_size)
            simulator = Simulator(vocab_wordle, algorithm)
            cum_stats = simulator.simulate_games(num_games=num_games, user_interface=False)
            avg_results.append(cum_stats[1] / num_games)
            print(algorithm.type.value, ",", vocab_size, ",", avg_results[-1])

        plt.plot(vocabulary_sizes, avg_results, label=algorithm.type.value)
    plt.title("Algorithms avg number of guesses as a function of the real vocabulary size")
    plt.ylabel("Avg number of guesses")
    plt.xlabel("Vocabulary size")
    plt.legend(loc='upper left')
    plt.savefig("data/plots/vocab_wordle_avg_guesses")
    plt.show()


def main():
    random.seed(42)
    secret_words, legal_words = load_word_lists()
    games_dictionary = get_game_dictionary(secret_words, legal_words)
    algorithms_dictionary = get_algorithms_dictionary(games_dictionary[GameType.BasicWordle.value])
    algorithms = [algorithm for algorithm in algorithms_dictionary.values() if algorithm.type != AlgorithmType.Minimax]
    algorithm_names = [algorithm_type.value for algorithm_type in AlgorithmType if
                       algorithm_type != AlgorithmType.Minimax]
    # wordle_game = games_dictionary[GameType.BasicWordle.value]
    # evaluate_wordle(wordle_game, algorithms, algorithm_names, len(secret_words), secret_words)
    # absurdle_game = games_dictionary[GameType.Absurdle.value]
    # evaluate_absurdle(absurdle_game, algorithms, algorithm_names)
    yellow_game = games_dictionary[GameType.YellowWordle.value]
    evaluate_wordle(yellow_game, algorithms, algorithm_names, 100, secret_words)
    # noisy_game = games_dictionary[GameType.NoisyWordle.value]
    # evaluate_wordle(noisy_game, algorithms, algorithm_names, 100, secret_words)
    # evaluate_vocab(secret_words, legal_words, algorithms)
    # fake_game = games_dictionary[GameType.FakeVocabularyWordle.value]
    # evaluate_wordle(fake_game, algorithms, algorithm_names, 10, secret_words)


def plot():
    # algorithm_names = ["Random", "Minimax with\nAlphaBeta pruning", "Expectimax", "Entropy", "Reinforcement"]
    # avg_results_real = [4.73, 3.97, 3.92, 3.86, 3.79]
    # avg_results_fake = [4.9, 5.1, 4.9, 4.48, 4.38]
    # plot_real_vs_fake(algorithm_names, avg_results_real, avg_results_fake)
    plot_reinforcement_results()
    plot_entropy_results()
    plot_adversarial_results()


if __name__ == '__main__':
    main()
