import random


def generate_random_number(digits):
    digits = [str(random.randint(0, 9)) for _ in range(digits)]
    random_number = int(''.join(digits))
    return random_number


def split_sentence(sentence, delimiter=None):
    if delimiter is None:
        # If no delimiter is specified, default to splitting by spaces
        words = sentence.split()
    else:
        words = sentence.split(delimiter)
    return words
