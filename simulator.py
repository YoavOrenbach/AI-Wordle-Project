import time
import numpy as np
from graphical_interface import GraphicalInterface


class Simulator:
    def __init__(self, game, algo):
        self.game = game
        self.algo = algo

    def simulate_games(self, num_games, user_interface=True):
        results = []
        start = time.time()
        for _ in range(num_games):
            results.append(list(self.simulate_game(user_interface)))
            self.game.reset(update_word=True)
            self.algo.reset()
        end = time.time()
        self.print_simulation_results(np.array(results), num_games, (end-start))

    def simulate_game(self, user_interface=True):
        game_state = []
        keep_guessing = True
        num_guesses = 0
        correct_answer = False
        num_letters_guessed = 0
        num_correct_letters_guessed = 0
        num_misplaced_letters_guessed = 0
        num_incorrect_letters_guessed = 0

        if user_interface:
            gi = GraphicalInterface(self.game.word)

        while keep_guessing:
            guess = self.algo.next_guess(game_state, self.game)
            result = self.game.guess(guess)
            game_state.append((guess, result))
            num_guesses += 1
            if result is None:
                break
            num_letters_guessed += len(guess)
            num_correct_letters_guessed += result.count('CORRECT')
            num_misplaced_letters_guessed += result.count('MISPLACED')
            num_incorrect_letters_guessed += result.count('INCORRECT')
            if result.count('CORRECT') == len(result):
                keep_guessing = False
                correct_answer = True

            if user_interface:
                gi.event_handler(guess)
                time.sleep(0.5)

        if user_interface:
            gi.load_ending_screen(win=correct_answer)

        return correct_answer, num_guesses, num_letters_guessed, num_correct_letters_guessed, \
               num_misplaced_letters_guessed, num_incorrect_letters_guessed

    def print_simulation_results(self, all_stats, num_games, duration):
        cum_stats = np.sum(all_stats, axis=0)
        sub_six = (all_stats[:, 1] <= 6).sum() / num_games * 100.0

        print(f'Results for {self.game.name} game with {self.algo.name} algorithm:')
        print('# Games: {}'.format(num_games))
        print('# Wins:  {}'.format(cum_stats[0]))
        print('% <= 6 Guesses:    {:.3f}'.format(sub_six))
        print('Avg Time per Game: {:.3f} sec'.format(duration/num_games))
        print('Max # Guesses:     {:}'.format(all_stats[:, 1].max()))
        print('Min # Guesses:     {:}'.format(all_stats[:, 1].min()))
        print('Avg. # Guesses:    {:}'.format(cum_stats[1] / num_games))
        print('Median # Guesses:  {:}'.format(np.median(all_stats[:, 1])))
        print('Std. Dev. Guesses: {:.3f}'.format(all_stats.std(axis=0)[1]))
        print('% Correct Letters:   {:.3f}'.format(float(cum_stats[3]) / cum_stats[2] * 100))
        print('% Misplaced Letters: {:.3f}'.format(float(cum_stats[4]) / cum_stats[2] * 100))
        print('% Incorrect Letters: {:.3f}'.format(float(cum_stats[5]) / cum_stats[2] * 100))

