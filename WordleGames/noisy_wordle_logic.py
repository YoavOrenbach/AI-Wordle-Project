import random
from WordleGames import BasicWordleLogic
from common import Placing, GameType, LETTERS_NUM, MAX, Word


class NoisyWordleLogic(BasicWordleLogic):
    def __init__(self, secret_words, legal_words, should_filter=True, max_iter=6, game_state=[], cur_possible_words=[]):
        super(NoisyWordleLogic, self).__init__(secret_words, legal_words, should_filter, max_iter,
            game_state, cur_possible_words, GameType.NoisyWordle)

    @staticmethod
    def weight_placing(real_placing):
        return [real_placing] * 1 + [Placing.correct.value] * 33 + [Placing.misplaced.value] * 33 + [
            Placing.incorrect.value] * 33  # TODO: change weighting choice

    def successor_creator(self, successor=None, agent_index=MAX, action=None):
        return NoisyWordleLogic(self._secret_words, self.legal_words, self.should_filter, self.max_iter,
            self.states.copy(), self.cur_possible_words.copy())

    def get_pattern(self, guess: str, secret_word: Word):
        pattern = super(NoisyWordleLogic, self).get_pattern(guess, secret_word)
        chosen_square = random.randrange(LETTERS_NUM)
        pattern[chosen_square] = random.choice(NoisyWordleLogic.weight_placing(pattern[chosen_square]))
        return pattern

    def filter_words(self):
        if not self.get_game_state():
            return self.cur_possible_words
        guess, original_pattern = self.get_game_state()[-1]
        all_patterns = noisy_patterns(original_pattern)
        unified_words = set()
        for pattern in all_patterns:
            self.states[-1] = (guess, pattern)
            unified_words = unified_words.union(set(super(NoisyWordleLogic, self).filter_words()))
        self.states[-1] = (guess, original_pattern)
        return list(unified_words)


def noisy_patterns(pattern):
    """Returns 11 possible noisy patterns"""
    all_patterns = [pattern]
    for i, placing in enumerate(pattern):
        possible_pattern1 = pattern.copy()
        possible_pattern2 = pattern.copy()
        if placing == Placing.correct.value:
            possible_pattern1[i] = Placing.misplaced.value
            all_patterns.append(possible_pattern1)
            possible_pattern2[i] = Placing.incorrect.value
            all_patterns.append(possible_pattern2)
        elif placing == Placing.misplaced.value:
            possible_pattern1[i] = Placing.correct.value
            all_patterns.append(possible_pattern1)
            possible_pattern2[i] = Placing.incorrect.value
            all_patterns.append(possible_pattern2)
        else:
            possible_pattern1[i] = Placing.correct.value
            all_patterns.append(possible_pattern1)
            possible_pattern2[i] = Placing.misplaced.value
            all_patterns.append(possible_pattern2)
    return all_patterns
