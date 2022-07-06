from argparse import ArgumentParser

from WordleGames import BasicWordle, Absurdle, NoisyWordle, YellowWordle
from common import AlgorithmType
from factories import get_algorithm
from simulator import Simulator
import string
import itertools


def parse_args():
    """
    Parses the command line arguments to decide on various game features.
    :return: the Parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument('-n', '--num-games', type=int, default=20, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=True, help='show pygame interface')
    parser.add_argument('-g', '--game', type=str.lower,
                        choices=['wordle', 'absurdle', 'vocab_wordle', 'noisy_wordle', 'yellow_wordle'],
                        default="wordle", help='which game to use')
    parser.add_argument('-a', '--algorithm', type=str.lower, choices=['random', 'minimax', 'entropy', 'learning'],
                        default='random', help='which algorithm to use')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()

    # Preprocess word list
    with open('legal_words.txt', 'r') as f:
        legal_words = f.read().splitlines()
    with open('secret_words.txt', 'r') as f:
        secret_words = f.read().splitlines()
    letters = [letter for letter in string.ascii_lowercase]

    # select algorithm
    algorithm = get_algorithm(AlgorithmType(args.algorithm))

    # select game
    # TODO: create better factory
    if args.game == 'wordle':
        game = BasicWordle(secret_words, legal_words)
    elif args.game == 'absurdle':
        game = Absurdle(secret_words, legal_words)
    elif args.game == 'vocab_wordle':
        game = BasicWordle(secret_words, [''.join(p) for p in itertools.product(letters, repeat=5)])
    elif args.game == 'noisy_wordle':
        game = NoisyWordle(secret_words, legal_words)
    else:
        game = YellowWordle(secret_words, legal_words)

    # Simulate games
    simulator = Simulator(game, algorithm)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
