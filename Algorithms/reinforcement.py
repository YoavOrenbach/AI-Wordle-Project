from utils import util
from Algorithms.algorithm import Algorithm
from WordleGames.abstract_wordle import AbstractWordle
from utils.common import Placing, AlgorithmType, GameType
from tqdm import tqdm
import random
import pickle


# Rewards for the placing of each letter in a guess:
GREEN_REWARD = 10
YELLOW_REWARD = 5
GREY_REWARD = -5

# Features for approximate Q Learning:
MATCHES = 0
DIFFERENCES = 1


class QLearningAgent:
    """Classic Q-learning agent"""
    def __init__(self):
        """Initializing Q-values table."""
        self.Q_values = util.Counter()

    def get_q_value(self, state, action):
        """Returns the Q-value of a given (state, action) pair."""
        return self.Q_values[(state, action)]

    def get_value(self, state, actions):
        """Returns the action with the maximal Q-value of a given state over the legal actions."""
        if not actions:
            return 0.0
        max_action = float('-inf')
        for action in actions:
            if max_action < self.get_q_value(state, action):
                max_action = self.get_q_value(state, action)
        return max_action

    def get_policy(self, state, actions):
        """Computes the best action to take in a given state over the legal actions."""
        max_action = float('-inf')
        actions_lst = []
        for action in actions:
            if max_action < self.get_q_value(state, action):
                max_action = self.get_q_value(state, action)
                actions_lst = [action]
            elif max_action == self.get_q_value(state, action):
                actions_lst.append(action)
        return random.choice(actions_lst)

    def get_q_action(self, state, actions, epsilon):
        """Computes the best action to take in a given state by using epsilon to govern exploration vs exploitation"""
        if not actions:
            return None
        if util.flipCoin(epsilon):
            return random.choice(actions)
        return self.get_policy(state, actions)

    def update(self, state, action, next_state, reward, alpha, discount, actions):
        """Updates the Q-table given the current state, the action to take, the new state and the hyper-parameters."""
        self.Q_values[(state, action)] = self.Q_values[(state, action)] + alpha * \
                                         (reward+discount*self.get_value(next_state, actions)-self.Q_values[(state, action)])

    def save_agent(self, game_type: GameType):
        agent_game = 'wordle' if game_type != GameType.FakeVocabularyWordle else 'fake'
        with open(f'Algorithms/saved_rl_agents/{agent_game}.pkl', 'wb') as f:
            pickle.dump(self.Q_values, f)

    def load_agent(self, game_type: GameType):
        agent_game = 'wordle' if game_type != GameType.FakeVocabularyWordle else 'fake'
        with open(f'Algorithms/saved_rl_agents/{agent_game}.pkl', 'rb') as f:
            self.Q_values = pickle.load(f)


class ApproximateQAgent(QLearningAgent):
    """Approximate Q-learning agent."""
    def __init__(self, get_pattern_func):
        """Initializing the weights and a function to calculate patterns of guesses."""
        super(ApproximateQAgent, self).__init__()
        self.weights = util.Counter()
        self.get_pattern = get_pattern_func

    def get_features(self, state, action):
        """Returns the features of a given (state, action) pair by calculating the pattern of the action, and
         comparing it to the pattern of the current state"""

        features = util.Counter()
        features[MATCHES] = 0
        features[DIFFERENCES] = 0

        if not state:
            return features

        guess, pattern = state
        next_pattern = self.get_pattern(guess, action)
        for placing1, placing2 in zip(pattern, next_pattern):
            if placing1 == placing2:
                features[MATCHES] += 1
            else:
                features[DIFFERENCES] += 1

        features.divideAll(5.0)
        return features

    def get_q_value(self, state, action):
        """Returns the approximate Q-value of a given (state, action) pair by computing the dot product between
         the features and the weights."""
        return self.get_features(state, action) * self.weights

    def update(self, state, action, next_state, reward, alpha, discount, legal_actions):
        """Updates the current weights given the current state, the action to take and the new state."""
        features = self.get_features(state, action)
        correction = reward + discount * self.get_value(next_state, legal_actions) - self.get_q_value(state, action)
        for i in features:
            self.weights[i] = self.weights[i] + alpha * correction * features[i]

    def save_agent(self, game_type: GameType):
        with open('Algorithms/saved_rl_agents/approximate.pkl', 'wb') as f:
            pickle.dump(self.weights, f)

    def load_agent(self, game_type: GameType):
        with open('Algorithms/saved_rl_agents/approximate.pkl', 'rb') as f:
            self.weights = pickle.load(f)


class Reinforcement(Algorithm):
    """A reinforcement algorithm to play a Wordle type game"""
    def __init__(self, game: AbstractWordle, train=False, approximate=False):
        """
        Initializes the algorithm guess count, game type, the agent being used (approximate or not), and trains for a
        fixed number of episodes.
        :param game: An AbstractWordleLogic type game to simulate training and decide on the type of agent to use.
        """
        super(Reinforcement, self).__init__(AlgorithmType.Reinforcement)
        self.game = game
        self.approximate = approximate

        if not self.approximate:
            self.agent = QLearningAgent()
        else:
            self.agent = ApproximateQAgent(game.get_pattern)

        if train:
            self.train()
        else:
            self.agent.load_agent(self.game.get_type())

    def train(self):
        """Trains the agent for a given number of episodes.
        Decides on the hyper-parameters, simulates games, calculates rewards and updates the agent."""
        # hyper-parameters
        alpha = 0.2
        discount = 0.8
        epsilon = 1.0
        epsilon_min = 0.05
        epsilon_decay = 0.9999 if not self.approximate else 0.995
        num_episodes = 40000 if not self.approximate else 1000

        for _ in tqdm(range(num_episodes)):
            secret_word = self.game.generate_secret_word()
            legal_actions = self.game.get_possible_words()
            done = False
            state = 0 if not self.approximate else ()

            while not done:
                action = self.agent.get_q_action(state, legal_actions, epsilon)
                pattern, done, _ = self.game.step(action, secret_word)
                reward = constant_rewards(pattern)
                legal_actions = self.game.get_possible_words()
                next_state = 0 if not self.approximate else (action, pattern)
                self.agent.update(state, action, next_state, reward, alpha, discount, legal_actions)
                state = next_state

            # Decrease epsilon
            epsilon = max(epsilon_min, epsilon*epsilon_decay)
            self.game.reset()
        self.agent.save_agent(self.game.get_type())
        print(f"Training completed over {num_episodes} episodes")

    def get_action(self, game: AbstractWordle):
        """Returns the next guess given the game being played, according to the agent type (classic vs approximate)"""
        actions = game.get_possible_words()
        if not self.approximate:
            return self.agent.get_policy(0, actions)
        state = ()
        if game.get_game_state():
            guess, pattern = game.get_game_state()[-1]
            state = (guess, pattern)
        return self.agent.get_policy(state, actions)


def constant_rewards(pattern):
    """Returns rewards according to the given pattern. green is 10, yellow is 5, and grey is -5."""
    reward = 0
    for placing in pattern:
        if placing == Placing.correct.value:
            reward += GREEN_REWARD
        elif placing == Placing.misplaced.value:
            reward += YELLOW_REWARD
        else:
            reward += GREY_REWARD
    return reward


def turn_rewards(pattern, turn_num):
    """Returns rewards according to the given pattern and the game's turn number. Since the goal is to guess in as
    fewer guesses as possible, a lower turn results in more rewards."""
    reward = 0
    for placing in pattern:
        if placing == Placing.correct.value:
            reward += (7-turn_num)*GREEN_REWARD
        elif placing == Placing.misplaced.value:
            reward += (7-turn_num)*YELLOW_REWARD
        else:
            reward += turn_num*GREY_REWARD
    return reward
