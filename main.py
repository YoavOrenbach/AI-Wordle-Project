from argparse import ArgumentParser
from algorithm import Random, MiniMax, Entropy, ReinforcementLearning
from game import Wordle, Absurdle, NoisyWordle, YellowWordle
from simulator import Simulator
import string
import itertools


def parse_args():
    """
    Parses the command line arguments to decide on various game features.
    :return: the Parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument('--word-list', type=str, default='word-list-all.txt', help='Used word list.')
    parser.add_argument('-n', '--num-games', type=int, default=20, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=True, help='show pygame interface')
    parser.add_argument('-g', '--game', type=str.lower, choices=['wordle', 'absurdle', 'vocab_wordle', 'noisy_wordle', 'yellow_wordle'],
                        default="wordle", help='which game to use')
    parser.add_argument('-a', '--algorithm', type=str.lower, choices=['random', 'minimax', 'entropy', 'learning'],
                        default='random', help='which algorithm to use')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()

    # Preprocess word list
    with open('word-list-all.txt', 'r') as f:
        word_list_large = f.read().splitlines()
    with open('word-list-solutions.txt', 'r') as f:
        word_list_small = f.read().splitlines()
    letters = [letter for letter in string.ascii_lowercase]

    # select policy
    if args.algorithm == 'random':
        algo = Random()
    elif args.algorithm == 'minimax':
        algo = MiniMax()
    elif args.algorithm == 'entropy':
        algo = Entropy()
    else:
        algo = ReinforcementLearning()

    # select game
    if args.game == 'wordle':
        game = Wordle(word_list_small)
    elif args.game == 'absurdle':
        game = Absurdle(word_list_small)
    elif args.game == 'vocab_wordle':
        game = Wordle([''.join(p) for p in itertools.product(letters, repeat=5)])
    elif args.game == 'noisy_wordle':
        game = NoisyWordle(word_list_small)
    else:
        game = YellowWordle(word_list_small)

    # Simulate games
    simulator = Simulator(game, algo, word_list_large)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
