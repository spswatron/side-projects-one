class Trie:
    def __init__(self):
        self.children = {}
        self.visited = False
        self.word_end = False


def add_word(node: Trie, word: str):
    for letter in word:
        if letter not in node.children:
            node.children[letter] = Trie()
        node = node.children[letter]
    node.word_end = True


root = Trie()
with open("./dictionary.csv", "r") as words:
    for dict_word in words:
        add_word(root, dict_word[:-1])


def find_possible_words(letters, curr_word, node, possible):
    if curr_word in possible or node is None or node.visited:
        return
    node.visited = True
    if node.word_end:
        node.word_end = False
        possible.add(curr_word)
    for i in range(len(letters)):
        new_letters = letters[:i] + letters[i + 1:]
        new_curr_word = curr_word + letters[i]
        new_node = node.children[letters[i]] if letters[i] in node.children else None
        find_possible_words(new_letters, new_curr_word, new_node, possible)


def solver(letters):
    possible = set()
    find_possible_words(letters, "", root, possible)
    possible = list(possible)
    possible.sort(key=len, reverse=True)
    for word in possible:
        print(word)
    return possible
