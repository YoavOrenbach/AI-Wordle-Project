from argparse import ArgumentParser
from WordleGames import BasicWordleLogic, AbsurdleLogic, NoisyWordleLogic, YellowWordle
from common import AlgorithmType, GameType, LETTERS_NUM
from factories import get_algorithm
from simulator import Simulator
import string
import itertools
import random


def parse_args():
    """
    Parses the command line arguments to decide on various game features.
    :return: the Parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument('-n', '--num-games', type=int, default=5, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=True, help='show pygame interface')
    parser.add_argument('-g', '--game', type=str.lower,
                        choices=[game_type.value for game_type in GameType],
                        default=GameType.BasicWordle.value, help='which game to use')
    parser.add_argument('-a', '--algorithm', type=str.lower,
                        choices=[algorithm_type.value for algorithm_type in AlgorithmType],
                        default=AlgorithmType.Random.value, help='which algorithm to use')
    parser.add_argument('--seed', type=int, default=42, help='random seed. -1 for system time.')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()

    # seeding
    if args.seed != -1:
        random.seed(args.seed)

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
        game = BasicWordleLogic(secret_words, legal_words)
    elif args.game == 'absurdle':
        game = AbsurdleLogic(secret_words, legal_words)
    elif args.game == 'vocab_wordle':
        game = BasicWordleLogic(secret_words, [''.join(p) for p in itertools.product(letters, repeat=LETTERS_NUM)])
    elif args.game == 'noisy_wordle':
        game = NoisyWordleLogic(secret_words, legal_words)
    else:
        game = YellowWordle(secret_words, legal_words)

    # Simulate games
    simulator = Simulator(game, algorithm)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
