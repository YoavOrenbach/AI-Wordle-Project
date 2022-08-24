import itertools
import random
import string
import os

from WordleGames import BasicWordle
from common import LETTERS_NUM, GameType


class VocabularyWordle(BasicWordle):
    """A Vocabulary Wordle game class extending the basic Wordle game."""
    def __init__(self, vocabulary_size: int, real_vocabulary: bool, secret_words=None, legal_words=None):
        """Initializing the vocabulary Wordle object with a vocabulary size and a boolean flag indicationg if the"""
        self._real_secret_path = f'data/vocab_word_lists/real_secret_{vocabulary_size}.txt'
        self._real_legal_path = f'data/vocab_word_lists/real_legal_{vocabulary_size}.txt'
        self._fake_secret_path = f'data/vocab_word_lists/fake_secret_{vocabulary_size}.txt'
        self._fake_legal_path = f'data/vocab_word_lists/fake_legal_{vocabulary_size}.txt'
        self.vocab_size = vocabulary_size

        if not self.check_word_lists(real_vocabulary):
            self.create_word_list(vocabulary_size, real_vocabulary, secret_words, legal_words)
        secret_words, legal_words = self.load_word_list(real_vocabulary)

        super().__init__(secret_words, legal_words)
        if real_vocabulary:
            self.type = GameType.RealVocabularyWordle
        else:
            self.type = GameType.FakeVocabularyWordle

    def get_vocab_size(self):
        """Returns the vocabulary size"""
        return self.vocab_size

    def check_word_lists(self, real_vocabulary):
        """Checks if the word list of the real vocabulary already exists."""
        if real_vocabulary:
            if not os.path.isfile(self._real_secret_path) or not os.path.isfile(self._real_legal_path):
                return False
        else:
            if not os.path.isfile(self._fake_secret_path) or not os.path.isfile(self._fake_legal_path):
                return False
        return True

    def create_word_list(self, vocabulary_size, real_vocabulary, secret_words, legal_words):
        """Creates a word list of the given vocabulary size according to the ratio of the secret words."""
        REAL_SECRET_RATIO = 5.603
        secret_vocabulary_size = max([round(vocabulary_size / REAL_SECRET_RATIO), 1])
        if real_vocabulary:
            sampled_secret_words = random.sample(secret_words, secret_vocabulary_size)
            legal_non_secret_words = set(legal_words).difference(set(secret_words))
            sampled_legal_non_secret_words = random.sample(legal_non_secret_words, vocabulary_size - secret_vocabulary_size)
            sampled_legal_words = sampled_secret_words + sampled_legal_non_secret_words
            write_list_to_file(self._real_secret_path, sampled_secret_words)
            write_list_to_file(self._real_legal_path, sampled_legal_words)
        else:
            all_words = [''.join(word_letters) for word_letters in
                         itertools.product(list(string.ascii_lowercase), repeat=LETTERS_NUM)]
            sampled_legal_words = random.sample(all_words, vocabulary_size)
            sampled_secret_words = random.sample(sampled_legal_words, secret_vocabulary_size)
            write_list_to_file(self._fake_secret_path, sampled_secret_words)
            write_list_to_file(self._fake_legal_path, sampled_legal_words)

    def load_word_list(self, real_vocabulary):
        if real_vocabulary:
            sampled_secret_words = read_list_from_file(self._real_secret_path)
            sampled_legal_words = read_list_from_file(self._real_legal_path)
        else:
            sampled_secret_words = read_list_from_file(self._fake_secret_path)
            sampled_legal_words = read_list_from_file(self._fake_legal_path)
        return sampled_secret_words, sampled_legal_words


def write_list_to_file(file_path, word_list):
    with open(file_path, 'w') as f:
        for word in word_list:
            f.write(word + '\n')


def read_list_from_file(file_path):
    with open(file_path, 'r') as f:
        word_list = f.read().splitlines()
    return word_list
