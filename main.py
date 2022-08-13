import random
from argparse import ArgumentParser

from factory import load_word_lists, get_game, get_algorithm
from common import AlgorithmType, GameType
from simulator import Simulator

DEFAULT_GAMES_NUM = 100
DEFAULT_IS_WITH_GUI = False


def parse_args():
    """
    Parses the command line arguments to decide on various game features.
    :return: the Parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument('-n', '--num-games', type=int, default=DEFAULT_GAMES_NUM, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=DEFAULT_IS_WITH_GUI, help='show pygame interface')
    parser.add_argument('-g', '--game', type=str,
                        choices=[game_type.value for game_type in GameType],
                        default=GameType.RealVocabularyWordle.value, help='which game to use')
    parser.add_argument('-a', '--algorithm', type=str,
                        choices=[algorithm_type.value for algorithm_type in AlgorithmType],
                        default=AlgorithmType.Entropy.value, help='which algorithm to use')
    parser.add_argument('--seed', type=int, default=42, help='random seed. -1 for system time.')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()

    # seeding
    if args.seed != -1:
        random.seed(args.seed)

    # Preprocess word list
    secret_words, legal_words = load_word_lists()

    # select game
    game = get_game(secret_words, legal_words, args.game, real_size=12000)

    # select algorithm
    algorithm = get_algorithm(args.algorithm, game)

    # Simulate games
    simulator = Simulator(game, algorithm)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
