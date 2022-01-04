with open("./dictionary.csv", "r") as words:
    word_set = set(list(map(lambda w: w[:-1], words.readlines())))


def find_possible_words(letters, curr_word, word_set, possible):
    if curr_word in word_set and curr_word not in possible:
        possible.add(curr_word)
    for i in range(len(letters)):
        find_possible_words(letters[:i] + letters[i + 1:], curr_word + letters[i], word_set, possible)


def solver(letters):
    possible = set()
    find_possible_words(letters, "", word_set, possible)
    possible = list(possible)
    possible.sort(key=len, reverse=True)
    return possible
