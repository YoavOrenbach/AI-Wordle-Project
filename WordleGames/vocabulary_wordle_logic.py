import itertools
import random

from WordleGames import BasicWordleLogic
from WordleGames.utils import get_all_letters
from common import LETTERS_NUM, GameType


class VocabularyWordleLogic(BasicWordleLogic):
    def __init__(self, vocabulary_size: int, real_vocabulary: bool):
        secret_words, legal_words = VocabularyWordleLogic.get_words(vocabulary_size, real_vocabulary)
        super().__init__(secret_words, legal_words)
        self.type = GameType.VocabularyWordle

    @classmethod
    def get_words(cls, vocabulary_size, real_vocabulary):
        REAL_SECRET_RATIO = 5.603
        secret_vocabulary_size = max([round(vocabulary_size / REAL_SECRET_RATIO), 1])
        if real_vocabulary:
            raise NotImplemented  # TODO
        else:
            all_words = [''.join(word_letters) for word_letters in
                         itertools.product(get_all_letters(), repeat=LETTERS_NUM)]
            legal_words = random.sample(all_words, vocabulary_size)
            secret_words = random.sample(legal_words, secret_vocabulary_size)
        return secret_words, legal_words
