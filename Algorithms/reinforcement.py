import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle_logic import AbstractWordleLogic
from WordleGames.basic_wordle_logic import BasicWordleLogic
from game_visible_state import GameVisibleState
from tqdm import tqdm
import random


class Reinforcement(Algorithm):
    def __init__(self):
        super(Reinforcement, self).__init__("Reinforcement learning")
        self.Q_values = util.Counter()
        self.guess_count = 0

        with open('word-list-all.txt', 'r') as f:
            word_list_large = f.read().splitlines()
        with open('word-list-solutions.txt', 'r') as f:
            word_list_small = f.read().splitlines()

        game = BasicWordleLogic(word_list_small, word_list_large)
        self.train(game)

    def train(self, game_logic: AbstractWordleLogic):
        # hyperparameters
        alpha = 0.2
        discount = 0.8
        epsilon = 1.0
        epsilon_decay = 0.9995  # 0.995 for secret list
        epsilon_min = 0.05

        # training variables
        num_episodes = 20000

        for _ in tqdm(range(num_episodes)):
            game_state = GameVisibleState()
            secret_word = game_logic.generate_secret_word()
            done = False
            state = 0

            while not done:
                action = self.get_q_action(state, game_logic.get_possible_words(game_state), epsilon)
                pattern, done = game_logic.step(action, secret_word)
                reward = 0
                for placing in pattern:
                    if placing == 0:
                        reward += (6-state)*10
                    elif placing == 1:
                        reward += (6-state)*5
                    else:
                        reward -= (state+1)*5
                game_state.add_state(action, pattern)
                actions = game_logic.get_possible_words(game_state)
                next_state = (state + 1) % 6
                self.update(state, action, next_state, reward, alpha, discount, actions)
                state = next_state

            # Decrease epsilon
            epsilon = max(epsilon_min, epsilon*epsilon_decay)
            game_logic.reset()

        print(f"Training completed over {num_episodes} episodes")

    def get_q_Value(self, state, action, actions):
        return self.Q_values[(state, action)]

    def get_value(self, state, actions):
        if not actions:
            return 0.0
        max_action = float('-inf')
        for action in actions:
            if max_action < self.get_q_Value(state, action, actions):
                max_action = self.get_q_Value(state, action, actions)
        return max_action

    def get_policy(self, state, actions):
        max_action = float('-inf')
        actions_lst = []
        for action in actions:
            if max_action < self.get_q_Value(state, action, actions):
                max_action = self.get_q_Value(state, action, actions)
                actions_lst = [action]
            elif max_action == self.get_q_Value(state, action, actions):
                actions_lst.append(action)
        return random.choice(actions_lst)

    def get_q_action(self, state, legalActions, epsilon):
        if not legalActions:
            return None
        if util.flipCoin(epsilon):
            return random.choice(legalActions)
        return self.get_policy(state, actions=legalActions)

    def update(self, state, action, next_state, reward, alpha, discount, actions):
        self.Q_values[(state, action)] = self.Q_values[(state, action)] + alpha * \
                                         (reward+discount*self.get_value(next_state, actions)-self.Q_values[(state, action)])

    def get_action(self, game_state, game_logic: AbstractWordleLogic):
        self.guess_count += 1
        actions = game_logic.get_possible_words(game_state)
        return self.get_policy(self.guess_count-1, actions=actions)

    def reset(self):
        self.guess_count = 0
