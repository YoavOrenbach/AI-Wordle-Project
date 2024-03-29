import time
import numpy as np
from tqdm import tqdm

from utils.common import Placing
from utils.first_gui import GraphicalInterface


class Simulator:
    """A class for simulating wordle games given a game and algorithm objects"""

    def __init__(self, game, algo):
        self.game = game
        self.algo = algo

    def simulate_games(self, num_games, user_interface=True, secret_words=None):
        """
        This method simulates a given number of game can show a pygame graphical interface
        :param num_games: the number of games to simulate
        :param user_interface: a boolean flag that determines if to show graphical interface or not.
        :param secret_words: a list of words to be used as secret words
        """
        results = []
        start = time.time()
        for i in tqdm(range(num_games)):
            secret_word = self.game.generate_secret_word() if secret_words is None else secret_words[i]
            results.append(list(self.simulate_game(secret_word, user_interface)))
            self.game.reset()
        end = time.time()
        self.print_simulation_results(np.array(results), num_games, (end - start))
        cum_stats = np.sum(results, axis=0)
        return cum_stats, np.array(results)

    def simulate_game(self, secret_word, user_interface=True):
        """
        This method simulates a single game
        :return: the stats for the game.
        """
        done = False
        correct_answer = False
        num_guesses = 0
        num_letters_guessed = 0
        num_correct_letters_guessed = 0
        num_misplaced_letters_guessed = 0
        num_incorrect_letters_guessed = 0

        if user_interface:
            gi = GraphicalInterface(secret_word)

        while not done:
            guess = self.algo.get_action(self.game)
            pattern, done, is_win = self.game.step(guess, secret_word)
            num_guesses += 1
            num_letters_guessed += len(guess)
            num_correct_letters_guessed += pattern.count(int(Placing.correct))
            num_misplaced_letters_guessed += pattern.count(int(Placing.misplaced))
            num_incorrect_letters_guessed += pattern.count(int(Placing.incorrect))
            if is_win:
                correct_answer = True

            if user_interface:
                gi.event_handler(guess, pattern)
                time.sleep(0.5)

        if user_interface:
            gi.load_ending_screen(win=correct_answer)

        return correct_answer, num_guesses, num_letters_guessed, num_correct_letters_guessed, \
               num_misplaced_letters_guessed, num_incorrect_letters_guessed

    def print_simulation_results(self, all_stats, num_games, duration):
        """
        This method prints all the stats for the number of simulated wordle games.
        :param all_stats: all the stats recorded during each game in the method simulate_game
        :param num_games: the number of played games.
        :param duration: the duration of the simulated games.
        """
        cum_stats = np.sum(all_stats, axis=0)
        sub_six = (all_stats[:, 1] <= 6).sum() / num_games * 100.0

        print(f'Results for {self.game.type} game with {self.algo.type} algorithm:')
        print('# Games: {}'.format(num_games))
        print('# Wins:  {}'.format(cum_stats[0]))
        print('% <= 6 Guesses:    {:.3f}'.format(sub_six))
        print('Avg Time per Game: {:.3f} sec'.format(duration / num_games))
        print('Max # Guesses:     {:}'.format(all_stats[:, 1].max()))
        print('Min # Guesses:     {:}'.format(all_stats[:, 1].min()))
        print('Avg. # Guesses:    {:}'.format(cum_stats[1] / num_games))
        print('Median # Guesses:  {:}'.format(np.median(all_stats[:, 1])))
        print('Std. Dev. Guesses: {:.3f}'.format(all_stats.std(axis=0)[1]))
        print('% Correct Letters:   {:.3f}'.format(float(cum_stats[3]) / cum_stats[2] * 100))
        print('% Misplaced Letters: {:.3f}'.format(float(cum_stats[4]) / cum_stats[2] * 100))
        print('% Incorrect Letters: {:.3f}'.format(float(cum_stats[5]) / cum_stats[2] * 100))
