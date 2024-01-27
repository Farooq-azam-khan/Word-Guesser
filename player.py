import math
from pprint import pprint


def count_letter_in_word_list(letter, word_list):
    num_words_it_appears_in = 0
    for word in word_list:
        if letter in word:
            num_words_it_appears_in += 1
    return num_words_it_appears_in


def probability_of_letter(letter: str, word_list: list[str]):
    num_words_it_appears_in = count_letter_in_word_list(letter, word_list)
    return num_words_it_appears_in / len(word_list)


def entropy_of_letter(p_letter: float):
    return -p_letter * math.log2(p_letter)


def probability_of_letters(allowed: str, words: list[str]):
    prob_map = {}
    for letter in allowed:
        prob_map[letter] = probability_of_letter(letter, words)
    prob_map = sorted(prob_map.items(), key=lambda x: x[1], reverse=True)
    return prob_map


def entropy_of_letters(allowed: str, words: list[str]):
    entropy_map = {}
    for letter in allowed:
        count_letter = count_letter_in_word_list(letter, words)
        if count_letter == 0:
            continue
        p_letter = count_letter / len(words)
        entropy_map[letter] = entropy_of_letter(p_letter)
    entropy_map = sorted(entropy_map.items(), key=lambda x: x[1], reverse=True)
    return entropy_map


def filter_word_on_letter_occurence(word: str, pattern: str):
    # len of word and pattern guarenteed to be same length
    for wl, pl in zip(word, pattern):
        if pl != "*" and not (wl == pl):
            return False

    return True


def filter_words_on_pattern(pattern, words):
    filtered_words = []
    for word in words:
        if filter_word_on_letter_occurence(word, pattern):
            filtered_words.append(word)
    return filtered_words


def filter_words_on_previous_guess(
    previous_guesses: str, pattern: str, words: list[str]
):
    remaining_words = words[:]
    # IDEA: could make this faster by not looking at all previous guesses, but rather, the previous round guess.
    for letter in previous_guesses:
        if not (letter in pattern):
            # filter out words that were guessed wrong
            # TODO: check also the number of letters. They must also be equal
            remaining_words = list(
                filter(lambda word: not (letter in word), remaining_words)
            )

    return remaining_words


def filter_words_by_letter(letter, words):
    remaining_words = []
    for word in words:
        if letter not in word:
            remaining_words.append(word)
    return remaining_words


class Player:
    remaining_words = []
    allowed = ""
    words = []
    remaining_words_count_after_guess = []

    @staticmethod
    def start_game(words, allowed: str):
        Player.words = words[:]
        Player.allowed = allowed

    @staticmethod
    def next_word(length: int, allowed: str):
        # print()
        # print("PLAYER --- [START ROUND] ---")
        # print("BEFORE:", len(Player.words), end=" ")
        Player.remaining_words = list(
            filter(lambda word: len(word) == length, Player.words)
        )
        Player.allowed = allowed
        # print("AFTER:", len(Player.remaining_words))
        Player.remaining_words_count_after_guess = [len(Player.remaining_words)]

    @staticmethod
    def guess_letter(pattern, previous_guesses):
        is_there_one_word_that_can_be_guessed = len(Player.remaining_words) == 1
        if is_there_one_word_that_can_be_guessed:
            # print("\nFOUND WORD:")
            # print(Player.remaining_words_count_after_guess)
            secret_word_found = Player.remaining_words[0]
            for letter in secret_word_found:
                if not (letter in previous_guesses):
                    return letter

        # update remaining words
        # print(f"{pattern=}, {previous_guesses=}")
        # print("\nbefore filter #1", len(Player.remaining_words), end=" ")
        # 1. filter out words that were guessed wrong
        Player.remaining_words = filter_words_on_previous_guess(
            previous_guesses, pattern, Player.remaining_words
        )

        # 2. word does not match pattern exactly
        Player.remaining_words = filter_words_on_pattern(
            pattern, Player.remaining_words
        )
        # print("after", len(Player.remaining_words))
        # only non-guessed letters are allowed (does not matter if guess was wrong or right)
        Player.allowed = "".join(
            list(filter(lambda x: x not in previous_guesses, Player.allowed))
        )
        # print(f"allowed=", Player.allowed)

        # print("after filter #2", len(Player.remaining_words))

        def get_letter_frequency():
            freq = {}

            for letter in Player.allowed:
                freq[letter] = 0

            for word in Player.remaining_words:
                for letter in word:
                    if not (letter in previous_guesses) and letter in Player.allowed:
                        freq[letter] += 1
            return freq

        def guessing_based_on_frequency_algorithm():
            freq = get_letter_frequency()
            # print("PLAYER:", freq)

            max_letter = Player.allowed[0]
            max_val = freq[Player.allowed[0]]

            for letter, f_val in freq.items():
                if f_val > max_val:
                    max_val = f_val
                    max_letter = letter
            return max_letter

        def probability_mapping_algorithm():
            p_map = probability_of_letters(Player.allowed, Player.remaining_words)
            return p_map[0][0]

        def naive_alphabetical_guess():
            for letter in Player.allowed:
                if not (letter in previous_guesses):
                    return letter

        def use_entropy():
            entropy_map = entropy_of_letters(Player.allowed, Player.remaining_words)
            # print()
            # if len(entropy_map) >= 5:
            #     pprint(entropy_map[:5])
            # else:
            #     pprint(entropy_map)
            return entropy_map[0][0]

            # print(f'\nfiltered: {orig_len-len(Player.remaining_words)}, {len(Player.remaining_words)} left')

        prob_guess = probability_mapping_algorithm()
        freq_guess = guessing_based_on_frequency_algorithm()
        entropy_guess = use_entropy()

        guess_expected_reduction = sorted(
            [
                (
                    prob_guess,
                    len(
                        filter_words_by_letter(prob_guess, Player.remaining_words),
                    ),
                    "prob",
                ),
                (
                    freq_guess,
                    len(
                        filter_words_by_letter(freq_guess, Player.remaining_words),
                    ),
                    "freq",
                ),
                (
                    entropy_guess,
                    len(
                        filter_words_by_letter(entropy_guess, Player.remaining_words),
                    ),
                    "entropy",
                ),
            ],
            key=lambda x: x[1],
            reverse=False,
        )
        guess_map = guess_expected_reduction[0]
        # print(f"STRATEGY: {guess_map[2]}")
        Player.remaining_words_count_after_guess.append(
            (guess_map[2], len(Player.remaining_words))
        )

        return guess_map[0]
