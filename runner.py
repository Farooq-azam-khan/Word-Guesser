from tqdm import trange
from player import Player
import random
import sys

import logging

log = logging.getLogger(__name__)


def get_words(filename="words.txt"):
    words = []
    with open(filename, "r") as f:
        for word in f:
            words.append(word.rstrip("\n"))
    return words


def main(verbose, seed, rounds):
    # constants
    ROUNDS = rounds
    SEED = seed
    VERBOSE = verbose
    random.seed(SEED)

    if VERBOSE:
        print("verbose mode is on")

    MINLENGTH = 5
    MAXLENGTH = 15
    ALLOWED = "abcdefghijklmnopqrstuvwxyz"
    BLANK = "*"

    words = get_words()
    words = list(
        filter(
            lambda x: len(x) >= MINLENGTH
            and len(x) <= MAXLENGTH
            and filter_characters(x, ALLOWED),
            words,
        )
    )
    if VERBOSE:
        print(f"Read in {len(words)} words")
    Player.start_game(words, ALLOWED)
    if VERBOSE:
        print(f"Using seed {SEED}")

    total_misses = 0
    range_fn = trange if not VERBOSE else range
    for _ in range_fn(ROUNDS):
        current_misses = 0
        previous_guesses = ""
        secret_word = random.choice(words)
        previous_correct = -1
        if VERBOSE:
            print(f"Secret Word: {secret_word}: ", end="")
        Player.next_word(len(secret_word), ALLOWED)

        while current_misses < len(ALLOWED):
            pattern = ""
            correct = 0

            # check guess and make the pattern
            for letter in secret_word:
                if letter in previous_guesses:
                    pattern += letter
                    correct += 1
                else:
                    pattern += BLANK

            # guessed the word
            if correct == len(secret_word):
                break
            # got a wrong guess
            if correct == previous_correct:
                current_misses += 1
                if VERBOSE:
                    print("!", end="")

            guess = Player.guess_letter(pattern, previous_guesses)
            if VERBOSE:
                print(guess, end="")
            previous_correct = correct
            previous_guesses += guess

        total_misses += current_misses
        if VERBOSE:
            print(f" ({current_misses})")
    print(
        f"Made a total of {total_misses} misses over {ROUNDS} rounds with seed {SEED}."
    )
    # logging.log(level='log'
    #             msg=f'Made a total of {total_misses} misses over {ROUNDS} rounds with seed {SEED}.')


def filter_characters(word, allowed_chars):
    for letter in word:
        if not (letter in allowed_chars):
            return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python runner.py [seed] [rounds] [verbose(true/false)]")
    else:
        VERBOSE = False
        if sys.argv[3] == "true" or sys.argv[3] == "True":
            VERBOSE = True

        ROUNDS = int(sys.argv[2])
        SEED = int(sys.argv[1])

        main(verbose=VERBOSE, rounds=ROUNDS, seed=SEED)
