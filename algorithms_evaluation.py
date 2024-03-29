import matplotlib.pyplot as plt
import numpy as np
import random

from WordleGames.abstract_wordle import AbstractWordle
from utils.common import AlgorithmType, GameType
from utils.simulator import Simulator
from utils.factory import load_word_lists, get_game_dictionary, get_algorithms_dictionary, get_game


def plot_avg_guesses(algorithm_names, avg_results, error, game_type, num_games):
    """Displays a bar graph of avg_results count from a list of algorithm_names and a game_type,
    over num_games games"""
    plt.style.use('seaborn-dark')
    plt.figure(figsize=(10, 6))
    ax = plt.bar(algorithm_names, avg_results, yerr=error, align='center', ecolor='black', capsize=10,
                 color='royalblue', zorder=3)
    text_kwargs = dict(fontsize=12, color='w')
    plt.bar_label(container=ax, label_type='center', **text_kwargs)
    plt.title(f"Algorithms average number of guesses on {game_type} game for {num_games} games",
              fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.grid(axis='y', zorder=0)
    plt.savefig(f"data/plots/{game_type}_avg_guesses")
    plt.show()


def plot_win_percentage(algorithm_names, win_percentage, game_type, num_games):
    """Displays a bar graph of win_percentage count from a list of algorithm_names and a game_type,
    over num_games games"""
    plt.style.use('seaborn-dark')
    plt.figure(figsize=(10, 6))
    plt.bar(algorithm_names, win_percentage, align='center', ecolor='black', capsize=10, color='firebrick', zorder=3)
    for i in range(len(algorithm_names)):
        plt.text(i, win_percentage[i], "{:.2f}%".format(win_percentage[i]), ha='center')
    plt.title(f"Algorithms win percentage on {game_type} game for {num_games} games", fontweight='bold', fontsize=14)
    plt.ylabel("win percentage", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.grid(axis='y', zorder=0)
    plt.savefig(f"data/plots/{game_type}_win_percentage")
    plt.show()


def plot_num_guesses(algorithm_names, num_guesses, error, game_type):
    """Displays a bar graph of num_guesses count from a list of algorithm_names and a game_type"""
    plt.style.use('seaborn-dark')
    plt.figure(figsize=(10, 6))
    ax = plt.bar(algorithm_names, num_guesses, yerr=error, align='center', ecolor='black', capsize=10,
                 color='forestgreen', zorder=3)
    text_kwargs = dict(fontsize=12, color='w')
    plt.bar_label(container=ax, label_type='center', **text_kwargs)
    plt.title(f"Algorithms number of guesses on {game_type} game", fontweight='bold', fontsize=14)
    plt.ylabel("Number of guesses", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.grid(axis='y', zorder=0)
    plt.savefig(f"data/plots/{game_type}_num_guesses")
    plt.show()


def plot_real_vs_fake(algorithm_names, results_real, error_real, results_fake, error_fake):
    """Displays a bar graph with the comparison of Real Vocab Wordle vs Fake Vocab Wordle based on results_real,
    results_fake results"""
    bar_width = 1 / 3
    plt.style.use('seaborn-dark')
    plt.subplots(figsize=(10, 6))

    # Set position of bar on X axis
    br1 = np.arange(len(results_real))
    br2 = [x + bar_width for x in br1]
    ax1 = plt.bar(br1, results_real, yerr=error_real, align='center', ecolor='black', capsize=10,
                  color='royalblue', zorder=3, width=bar_width, label='Real Vocabulary')
    text_kwargs = dict(fontsize=12, color='w')
    plt.bar_label(container=ax1, label_type='center', **text_kwargs)
    ax2 = plt.bar(br2, results_fake, yerr=error_fake, align='center', ecolor='black', capsize=10,
                  color='darkorange', zorder=3, width=bar_width, label='Fake Vocabulary')
    plt.bar_label(container=ax2, label_type='center', **text_kwargs)

    plt.title("Algorithms average number of guesses using real Vs fake vocabulary", fontweight='bold', fontsize=14)
    plt.xlabel("Algorithms", fontweight='bold', fontsize=14)
    plt.ylabel("Average number of guesses", fontweight='bold', fontsize=14)
    plt.xticks([r + bar_width / 2 for r in range(len(results_real))], algorithm_names)
    plt.grid(axis='y', zorder=0)
    plt.legend()
    plt.savefig("data/plots/real_vs_fake_avg_guesses")
    plt.show()


def evaluate_wordle(game: AbstractWordle, algorithms, algorithm_names, num_games, secret_words=None):
    """Calculate results (average number of turns and precentage of success) of algorithms over a game, when it's
    playing num_games games"""
    avg_results = []
    win_percentage = []
    error = []
    if game.get_type() != GameType.BasicWordle:
        if game.get_type() == GameType.FakeVocabularyWordle:
            with open('data/vocab_word_lists/fake_secret_12972.txt', 'r') as f:
                secret_words = f.read().splitlines()
            secret_words = random.sample(secret_words, num_games)

    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        cum_stats, all_stats = simulator.simulate_games(num_games=num_games, user_interface=False, secret_words=secret_words)
        avg_results.append(cum_stats[1] / num_games)
        win_percentage.append(100 * cum_stats[0] / num_games)
        error.append(all_stats.std(axis=0)[1])

    plot_avg_guesses(algorithm_names, avg_results, error, game.get_type().value, num_games)
    plot_win_percentage(algorithm_names, win_percentage, game.get_type().value, num_games)


def evaluate_absurdle(game: AbstractWordle, algorithms, algorithm_names):
    """Calculate number of turns of algorithms over a game, when played 100 games"""
    num_guesses = []
    error = []
    for algorithm in algorithms:
        simulator = Simulator(game, algorithm)
        if algorithm.type == AlgorithmType.Random:
            cum_stats, all_stats = simulator.simulate_games(num_games=1000, user_interface=False)
            num_guesses.append(cum_stats[1] / 1000)
            error.append(all_stats.std(axis=0)[1])
        else:
            cum_stats, all_stats = simulator.simulate_games(num_games=1, user_interface=False)
            num_guesses.append(cum_stats[1])
            error.append(all_stats.std(axis=0)[1])
    plot_num_guesses(algorithm_names, num_guesses, error, game.get_type().value)


def evaluate_vocab(secret_words, legal_words, algorithms):
    """
    Display a line graph of all algorithms
    X axis is the number of words in the possible words list
    Y axis is the average number of guess per game, when run over 100 games for each size
    Sized of the list of possible words start from 1000 to 12972 with 1000 difference each time
    """
    vocabulary_sizes = list(range(1000, 12001, 1000)) + [12972]
    for algorithm in algorithms:
        avg_results = []
        for vocab_size in vocabulary_sizes:
            vocab_wordle = get_game(secret_words, legal_words, GameType.RealVocabularyWordle, real_size=vocab_size)
            simulator = Simulator(vocab_wordle, algorithm)
            cum_stats, _ = simulator.simulate_games(num_games=100, user_interface=False)
            avg_results.append(cum_stats[1] / 100)
            print(algorithm.type.value, ",", vocab_size, ",", avg_results[-1])

        plt.plot(vocabulary_sizes, avg_results, label=algorithm.type.value)
    plt.title("Algorithms avg number of guesses as a function of the real vocabulary size")
    plt.ylabel("Avg number of guesses")
    plt.xlabel("Vocabulary size")
    plt.legend(loc='upper left')
    plt.savefig("data/plots/vocab_wordle_avg_guesses")
    plt.show()


def main():
    """Runs an evaluation as needed for the analisys of all algorithms and games"""
    secret_words, legal_words = load_word_lists()
    games_dictionary = get_game_dictionary(secret_words, legal_words)
    algorithms_dictionary = get_algorithms_dictionary(games_dictionary[GameType.BasicWordle.value])
    algorithms = [algorithm for algorithm in algorithms_dictionary.values() if
                  algorithm.type != AlgorithmType.TotalRandom and algorithm.type != AlgorithmType.Minimax]
    algorithm_names = [algorithm_type for algorithm_type in algorithms_dictionary if
                       algorithm_type != AlgorithmType.TotalRandom and algorithm_type != AlgorithmType.Minimax]
    wordle_game = games_dictionary[GameType.BasicWordle.value]
    evaluate_wordle(wordle_game, algorithms, algorithm_names, len(secret_words), secret_words)
    absurdle_game = games_dictionary[GameType.Absurdle.value]
    evaluate_absurdle(absurdle_game, algorithms, algorithm_names)
    yellow_game = games_dictionary[GameType.YellowWordle.value]
    evaluate_wordle(yellow_game, algorithms, algorithm_names, 100, secret_words)
    noisy_game = games_dictionary[GameType.NoisyWordle.value]
    evaluate_wordle(noisy_game, algorithms, algorithm_names, 100, secret_words)
    evaluate_vocab(secret_words, legal_words, algorithms)
    fake_game = games_dictionary[GameType.FakeVocabularyWordle.value]
    evaluate_wordle(fake_game, algorithms, algorithm_names, 100, secret_words)


if __name__ == '__main__':
    main()
