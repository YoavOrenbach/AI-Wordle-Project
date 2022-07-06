from Algorithms import Random, Minimax, Expectimax, Entropy, Reinforcement
from common import AlgorithmType


def get_algorithm(algorithm_type: AlgorithmType):
    type_to_algorithm = {AlgorithmType.Random: Random,
                         AlgorithmType.Minimax: Minimax,
                         AlgorithmType.Expectimax: Expectimax,
                         AlgorithmType.Entropy: Entropy,
                         AlgorithmType.Reinforcement: Reinforcement}
    return type_to_algorithm[algorithm_type]()
