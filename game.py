from abc import ABC, abstractmethod
import random


class Game(ABC):
    def __init__(self):
        super(Game, self).__init__()

    @abstractmethod
    def guess(self, word):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_word_list(self):
        pass


class Wordle(Game):
    def __init__(self, words, max_iter=6, word=None):
        super(Wordle, self).__init__()
        self.word_list = words
        self.max_iter = max_iter
        self.cur_iter = 0
        self.word = random.choice(self.word_list) if word is None else word

    def guess(self, word):
        word = word.lower()

        if word not in self.word_list:
            raise ValueError('invalid word')

        if self.max_iter is not None and self.cur_iter >= self.max_iter:
            return None

        self.cur_iter += 1

        ans = []
        for idx, letter in enumerate(word):

            if letter == self.word[idx]:
                ans.append('CORRECT')
            elif letter in self.word:
                ans.append('MISPLACED')
            else:
                ans.append('INCORRECT')

        return ans

    def reset(self, update_word=False):
        self.cur_iter = 0
        if update_word:
            self.word = random.choice(self.word_list)

    def get_word_list(self):
        return self.word_list
