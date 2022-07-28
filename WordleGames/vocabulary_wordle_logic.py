import itertools
import random
import string

from WordleGames import BasicWordleLogic
from common import LETTERS_NUM, GameType


class VocabularyWordleLogic(BasicWordleLogic):
    def __init__(self, vocabulary_size: int, real_vocabulary: bool, secret_words=None, legal_words=None):
        secret_words, legal_words = VocabularyWordleLogic.get_words(vocabulary_size, real_vocabulary, secret_words,
                                                                    legal_words)
        super().__init__(secret_words, legal_words)
        if real_vocabulary:
            self.type = GameType.RealVocabularyWordle
        else:
            self.type = GameType.FakeVocabularyWordle

    @classmethod
    def get_words(cls, vocabulary_size, real_vocabulary, secret_words, legal_words):
        REAL_SECRET_RATIO = 5.603
        secret_vocabulary_size = max([round(vocabulary_size / REAL_SECRET_RATIO), 1])
        if real_vocabulary:
            sampled_secret_words = random.sample(secret_words, secret_vocabulary_size)
            legal_non_secret_words = set(legal_words).difference(set(secret_words))
            sampled_legal_non_secret_words = random.sample(legal_non_secret_words, vocabulary_size - secret_vocabulary_size)
            sampled_legal_words = sampled_secret_words + sampled_legal_non_secret_words
        else:
            all_words = [''.join(word_letters) for word_letters in
                         itertools.product(list(string.ascii_lowercase), repeat=LETTERS_NUM)]
            sampled_legal_words = random.sample(all_words, vocabulary_size)
            sampled_secret_words = random.sample(sampled_legal_words, secret_vocabulary_size)
        return sampled_secret_words, sampled_legal_words
