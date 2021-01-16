import string
import random


def open_file(source):
    BeeMovie = source
    # write = open("BeeMovie.txt", "w")
    BeeMovie = BeeMovie.replace(";", "")
    BeeMovie = " ".join(BeeMovie.split())
    BeeMovieList = BeeMovie.split(" ")
    return BeeMovieList


def create_nodes(title):
    BeeMovieList = open_file(title)
    i = 1
    past_j = 0
    j = random.randint(1, 30)
    finalCSV = ""
    while j < len(BeeMovieList):
        finalCSV += str(i) + "," + ";".join(BeeMovieList[past_j: j]) + "\n"
        past_j = j
        j += random.randint(1, 30)
        i += 1
    return finalCSV


def max_edge_count(size):
    if size > 2:
        return size * 4
    elif size <= 1:
        return 0
    elif size == 2:
        return 2


def create_edges(content):
    node_count = len(content.split("\n"))
    past_edges = {}
    j = 0
    finalEdgeCSV = ""
    while j < max_edge_count(node_count):
        randomFrom = random.randint(1, node_count)
        randomTo = random.randint(1, node_count)
        if randomTo != randomFrom and (randomTo, randomFrom) not in past_edges:
            past_edges[randomTo, randomFrom] = True
            finalEdgeCSV += str(randomFrom) + "," + str(randomTo) + "\n"
        j += 1
    return finalEdgeCSV


def create_node_edge(title):
    create_nodes(title)
    print("created nodes csv!")
    create_edges(title)
    print("created edges csv!")


# create_node_edge(sys.argv[0])
