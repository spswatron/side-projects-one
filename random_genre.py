import pandas as pd
import random
from termcolor import cprint


def random_genre():
    random_dict = {}
    words = ""
    df = pd.read_csv('yob2019.txt', sep=",", header=None, nrows=200)
    df.columns = ["name", "gender", "total"]
    # two_k_nineteen_names['total'] = two_k_nineteen_names.apply(lambda row: int(row.total), axis=1)
    # two_k_nineteen_names.sort_values(by=['total'], inplace=True, ascending=False)
    # two_k_nineteen_names.to_csv('yob2019.txt', index=False, header=False)
    local = {}
    local['prev'] = 'M'
    local['prev_color'] = 'alkjaslkdjfkasd'

    genres = open("genres.txt", "r")
    wikipedia_genres = open("wikipedia_genres.txt", "r")
    genres = genres.read().split('\n')
    wikipedia_genres = wikipedia_genres.read().split('\n')

    lst = ["red", "green", "yellow",
           "blue", "magenta", "cyan"]

    def rand_color():
        choice = random.choice(lst)
        if choice != local['prev_color']:
            local['prev_color'] = choice
            return choice
        return rand_color()

    # name_hash = {}
    # def names_to_hash():
    #     global prev
    #     global name_hash
    #     for index, row in two_k_nineteen_names.iterrows():
    #         name_hash[row['name']] = row['total']

    genre_hash = {}
    wiki_genre_hash = {}

    def genre_to_hash():
        for genre in genres:
            genre_hash[genre] = 1

    genre_to_hash()

    def wiki_genre_to_hash():
        for genre in wikipedia_genres:
            wiki_genre_hash[genre] = 1

    wiki_genre_to_hash()

    def rand_name():
        name_row = df.sample()
        df.drop(name_row.index)
        gender = ''.join(name_row['gender'].values)
        if local['prev'] != gender:
            local['prev'] = gender
            return ''.join(name_row['name'].values)
        return rand_name()

    def rand_genre():
        random_genre = random.choice(list(genre_hash.keys()))
        del genre_hash[random_genre]
        return random_genre

    def rand_wiki_genre():
        random_genre = random.choice(list(wiki_genre_hash.keys()))
        del wiki_genre_hash[random_genre]
        return random_genre

    def fix_string_space(uneven):
        uneven = list(uneven)
        uneven = uneven + [' '] * (15 - len(uneven))
        return ''.join(uneven)

    local['prev_num'] = float('inf')

    def random_number(max_num):
        random_num = random.choice(list(range(max_num)))
        if random_num != local['prev_num']:
            local['prev_num'] = random_num
            return random_num + 2
        return random_number(max_num)

    # for i in range(5):
    #     # cprint(rand_name(), rand_color())
    #     name = fix_string_space(rand_name())
    #     print(name + '\t' + '\t' + rand_genre())
    # print()
    print()
    num_rand = 6
    for i in range(num_rand):
        # cprint(rand_name(), rand_color())
        name = fix_string_space(rand_name())
        id = len(random_dict)
        random_dict[id] = {}
        # words += "Genre: " + rand_wiki_genre()
        random_dict[id]["Genre"] = rand_wiki_genre()
        # words += "Form: " + rand_genre()
        random_dict[id]["Form"] = rand_genre()
        num = random_number(3)
        names = ''
        for j in range(num):
            names += rand_name()
            if j < num - 1:
                names += ', '
        random_dict[id]["Characters"] = names
        words += "Form: " + "Characters: " + names
        words += "\n"
        # if i != num_rand - 1:
        #     print()
    # return words
    return random_dict


random_genre()
