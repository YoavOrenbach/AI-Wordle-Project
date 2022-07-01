from argparse import ArgumentParser
from algorithm import Random
from game import Wordle
from simulator import Simulator


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--word-list', type=str, default='word-list-all.txt', help='Used word list.')
    parser.add_argument('-n', '--num-games', type=int, default=20, help='# of games to simulate')
    parser.add_argument('-u', '--user-interface', type=bool, default=True, help='show pygame interface')
    parser.add_argument('-g', '--game', type=str.lower, choices=['wordle', 'absurdle', 'all_words', 'noisy_wordle', 'yellow_wordle'],
                        default="wordle", help='which game to use')
    parser.add_argument('-a', '--algorithm', type=str.lower, choices=['random', 'minimax', 'entropy', 'learning'],
                        default='random', help='which algorithm to use')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()

    # Preprocess word list
    with open(args.word_list, 'r') as f:
        word_list = f.read().splitlines()

    # select policy
    algo = None
    if args.algorithm == 'random':
        algo = Random()

    # select game
    game = None
    if args.game == "wordle":
        game = Wordle(word_list)

    # Simulate games
    simulator = Simulator(game, algo)
    simulator.simulate_games(num_games=args.num_games, user_interface=args.user_interface)


if __name__ == '__main__':
    main()
