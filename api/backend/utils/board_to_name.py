names = {
    "a1": [7, 0],
    "a2": [6, 0],
    "a3": [5, 0],
    "a4": [4, 0],
    "a5": [3, 0],
    "a6": [2, 0],
    "a7": [1, 0],
    "a8": [0, 0],

    "b1": [7, 1],
    "b2": [6, 1],
    "b3": [5, 1],
    "b4": [4, 1],
    "b5": [3, 1],
    "b6": [2, 1],
    "b7": [1, 1],
    "b8": [0, 1],

    "c1": [7, 2],
    "c2": [6, 2],
    "c3": [5, 2],
    "c4": [4, 2],
    "c5": [3, 2],
    "c6": [2, 2],
    "c7": [1, 2],
    "c8": [0, 2],

    "d1": [7, 3],
    "d2": [6, 3],
    "d3": [5, 3],
    "d4": [4, 3],
    "d5": [3, 3],
    "d6": [2, 3],
    "d7": [1, 3],
    "d8": [0, 3],

    "e1": [7, 4],
    "e2": [6, 4],
    "e3": [5, 4],
    "e4": [4, 4],
    "e5": [3, 4],
    "e6": [2, 4],
    "e7": [1, 4],
    "e8": [0, 4],

    "f1": [7, 5],
    "f2": [6, 5],
    "f3": [5, 5],
    "f4": [4, 5],
    "f5": [3, 5],
    "f6": [2, 5],
    "f7": [1, 5],
    "f8": [0, 5],

    "g1": [7, 6],
    "g2": [6, 6],
    "g3": [5, 6],
    "g4": [4, 6],
    "g5": [3, 6],
    "g6": [2, 6],
    "g7": [1, 6],
    "g8": [0, 6],

    "h1": [7, 7],
    "h2": [6, 7],
    "h3": [5, 7],
    "h4": [4, 7],
    "h5": [3, 7],
    "h6": [2, 7],
    "h7": [1, 7],
    "h8": [0, 7]
}

file_names = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}


def board_to_name(name):
    try:
        return names[name]
    except KeyError:
        return [-1, -1]


def file_to_name(file):
    try:
        return file_names[file]
    except KeyError:
        return -1
