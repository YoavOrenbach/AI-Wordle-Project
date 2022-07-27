from argparse import ArgumentParser
from WordleGames import BasicWordleLogic, AbsurdleLogic, NoisyWordleLogic, YellowWordle
from Algorithms import Random, Minimax, AlphaBeta, Expectimax, Entropy, Reinforcement
from common import AlgorithmType, GameType, LETTERS_NUM
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
    parser.add_argument('-n', '--num-games', type=int, default=1, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=False, help='show pygame interface')
    parser.add_argument('-g', '--game', type=str.lower,
                        choices=[game_type.value for game_type in GameType],
                        default=GameType.Absurdle.value, help='which game to use')
    parser.add_argument('-a', '--algorithm', type=str.lower,
                        choices=[algorithm_type.value for algorithm_type in AlgorithmType],
                        default=AlgorithmType.Minimax.value, help='which algorithm to use')
    parser.add_argument('--seed', type=int, default=42, help='random seed. -1 for system time.')
    return parser.parse_args()


def get_vocabulary_list(secret_words):
    letters = [letter for letter in string.ascii_lowercase]
    all_combos = [''.join(p) for p in itertools.product(letters, repeat=LETTERS_NUM)]
    vocab = set(secret_words.copy())
    vocab.update(set(random.sample(all_combos, 100000)))
    return list(vocab)


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

    # select game
    # TODO: create better factory
    if args.game == 'wordle':
        game = BasicWordleLogic(secret_words, legal_words)
    elif args.game == 'absurdle':
        game = AbsurdleLogic(secret_words, legal_words)
    elif args.game == 'vocab_wordle':
        vocab = get_vocabulary_list(secret_words)
        game = BasicWordleLogic(secret_words, vocab)
    elif args.game == 'noisy_wordle':
        game = NoisyWordleLogic(secret_words, legal_words)
    else:
        game = YellowWordle(secret_words, legal_words)

    # select algorithm
    if args.algorithm == "random":
        algorithm = Random()
    elif args.algorithm == "minimax":
        algorithm = Minimax()
    elif args.algorithm == "alphabeta":
        algorithm = AlphaBeta()
    elif args.algorithm == "expectimax":
        algorithm = Expectimax()
    elif args.algorithm == "entropy":
        algorithm = Entropy()
    else:
        algorithm = Reinforcement(game)

    # Simulate games
    simulator = Simulator(game, algorithm)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
