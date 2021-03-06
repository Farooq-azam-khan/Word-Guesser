import math


class Player:

    remianing_words = []
    allowed = ''
    words = []

    @staticmethod
    def start_game(words, allowed):
        Player.words = words[:]
        Player.allowed = allowed

    @staticmethod
    def next_word(length, allowed):
        def filter_word_length(word):
            return len(word) == length

        Player.remianing_words = list(
            filter(filter_word_length, Player.words))
        Player.allowed = allowed

    @staticmethod
    def guess_letter(pattern, previous_guesses):
        if len(Player.remianing_words) == 1:
            secret_word_found = Player.remianing_words[0]
            # check the previous gesses and guess the letter not in there
            for letter in secret_word_found:
                if not (letter in previous_guesses):
                    return letter

        # orig_len = len(Player.remianing_words)

        def filter_word_on_letter_occurence(word, pattern):
            for wl, pl in zip(word, pattern):
                if pl != '*' and not(wl == pl):
                    return False

            return True

        Player.remianing_words = list(filter(lambda word: filter_word_on_letter_occurence(word, pattern),
                                             Player.remianing_words))

        for letter in previous_guesses:
            if not(letter in pattern):
                # filter out words that were guessed wrong
                Player.remianing_words = list(filter(lambda word: not(letter in word),
                                                     Player.remianing_words))

        def get_letter_frequency():
            freq = {}
            Player.allowed = ''.join(
                list(filter(lambda x: x not in previous_guesses, Player.allowed)))

            for letter in Player.allowed:
                freq[letter] = 0

            for word in Player.remianing_words:
                for letter in word:
                    if not (letter in previous_guesses):
                        freq[letter] += 1
            return freq

        def guessing_based_on_frequency_algorithm():
            freq = get_letter_frequency()

            max_letter = Player.allowed[0]
            max_val = freq[Player.allowed[0]]

            for letter, f_val in freq.items():
                if f_val > max_val:
                    max_val = f_val
                    max_letter = letter
            return max_letter

        def naive_alphabetical_guess():
            for letter in Player.allowed:
                if not (letter in previous_guesses):
                    return letter

        def use_entropy():
            freq = get_letter_frequency()
            n = len(Player.remianing_words)
            # print(freq)
            # entropy = -1*sum([(val/n)*math.log2(val/n) for _, val in freq.items()])
            entropy = 0
            for _, val in freq.items():
                if (val/n) == 0:
                    entropy += (val/n)*math.log(abs(0.00001))
                else:
                    entropy += (val/n)*math.log(abs(val/n))
            entropy *= -1

            bitGain = {}
            for l, p in freq.items():
                bitGain[l] = ((-1*entropy)/(10-(p/n)*10/10)) * \
                    (p/n)*10/10*(p/n)*10/10

            max_letter = Player.allowed[0]
            max_val = bitGain[Player.allowed[0]]

            for letter, f_val in bitGain.items():
                if f_val < max_val:
                    max_val = f_val
                    max_letter = letter
            return max_letter

            # print(f'\nfiltered: {orig_len-len(Player.remianing_words)}, {len(Player.remianing_words)} left')
        return guessing_based_on_frequency_algorithm()
        # return use_entropy() # not fully developed
        # return naive_alphabetical_guess()
