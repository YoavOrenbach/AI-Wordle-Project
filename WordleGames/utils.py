from common import Placing, Word


def get_pattern_vanilla(guess: Word, secret_word: Word):
    """Returns a list containing the placing of each letter in the guess according to the secret word
    like basic Wordle"""
    pool = {}
    for g, s in zip(guess, secret_word):
        if g == s:
            continue
        if s in pool:
            pool[s] += 1
        else:
            pool[s] = 1

    pattern = []
    for guess_letter, solution_letter in zip(guess, secret_word):
        if guess_letter == solution_letter:
            pattern.append(int(Placing.correct))
        elif guess_letter in secret_word and guess_letter in pool and pool[guess_letter] > 0:
            pattern.append(int(Placing.misplaced))
            pool[guess_letter] -= 1
        else:
            pattern.append(int(Placing.incorrect))
    return pattern
