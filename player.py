class Player:

    remianing_words = []
    allowed = ''

    @staticmethod
    def start_game(words, allowed):
        Player.remianing_words = words

        Player.allowed = allowed

    @staticmethod
    def next_word(length):
        def filter_word_length(word):
            return len(word) == length
        Player.remianing_words = list(
            filter(filter_word_length, Player.remianing_words))

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

        def guessing_algorithm():
            freq = {}

            max_freq_letter = ''

            for letter in Player.allowed:
                if not (letter in previous_guesses):
                    freq[letter] = 0
                    max_freq_letter = letter

            for word in Player.remianing_words:
                for letter in word:
                    if not (letter in previous_guesses):
                        freq[letter] += 1

            max_freq_val = freq[max_freq_letter]
            for letter, freq_val in freq.items():
                if freq_val > max_freq_val:
                    max_freq_letter = letter
                    max_freq_val = freq_val
            return max_freq_letter

        # print(f'\nfiltered: {orig_len-len(Player.remianing_words)}, {len(Player.remianing_words)} left')
        return guessing_algorithm()
