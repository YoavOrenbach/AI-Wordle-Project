import random
from argparse import ArgumentParser

from Algorithms import Random, Minimax, AlphaBeta, Expectimax, Entropy, Reinforcement
from WordleGames import BasicWordleLogic, AbsurdleLogic, NoisyWordleLogic, YellowWordle, UnfilteredWordle
from WordleGames.vocabulary_wordle_logic import VocabularyWordleLogic
from common import AlgorithmType, GameType
from simulator import Simulator

DEFAULT_GAMES_NUM = 10
DEFAULT_IS_WITH_GUI = False


def parse_args():
    """
    Parses the command line arguments to decide on various game features.
    :return: the Parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument('-n', '--num-games', type=int, default=DEFAULT_GAMES_NUM, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=DEFAULT_IS_WITH_GUI, help='show pygame interface')
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

    # select game
    # TODO: create better factory
    if args.game == GameType.BasicWordle:
        game = BasicWordleLogic(secret_words, legal_words)
    elif args.game == GameType.Absurdle:
        game = AbsurdleLogic(secret_words, legal_words)
    elif args.game == GameType.FakeVocabularyWordle:
        game = VocabularyWordleLogic(vocabulary_size=12972, real_vocabulary=False)
    elif args.game == GameType.RealVocabularyWordle:
        game = VocabularyWordleLogic(vocabulary_size=1000, real_vocabulary=True, secret_words=secret_words,
                                     legal_words=legal_words)
    elif args.game == GameType.NoisyWordle:
        game = NoisyWordleLogic(secret_words, legal_words)
    elif args.game == GameType.YellowWordle:
        game = YellowWordle(secret_words, legal_words)
    elif args.game == GameType.UnfilteredWordle:
        game = UnfilteredWordle(secret_words, legal_words)
    else:
        raise Exception(f"{args.game} is not valid game")

    # select algorithm
    if args.algorithm == AlgorithmType.Random:
        algorithm = Random()
    elif args.algorithm == AlgorithmType.Minimax:
        algorithm = Minimax()
    elif args.algorithm == AlgorithmType.AlphaBeta:
        algorithm = AlphaBeta()
    elif args.algorithm == AlgorithmType.Expectimax:
        algorithm = Expectimax()
    elif args.algorithm == AlgorithmType.Entropy:
        algorithm = Entropy()
    else:
        algorithm = Reinforcement(game)

    # Simulate games
    simulator = Simulator(game, algorithm)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
