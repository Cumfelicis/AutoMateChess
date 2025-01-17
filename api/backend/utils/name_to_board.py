names = {
    "[7, 0]": "a1",
    "[6, 0]": "a2",
    "[5, 0]": "a3",
    "[4, 0]": "a4",
    "[3, 0]": "a5",
    "[2, 0]": "a6",
    "[1, 0]": "a7",
    "[0, 0]": "a8",

    "[7, 1]": "b1",
    "[6, 1]": "b2",
    "[5, 1]": "b3",
    "[4, 1]": "b4",
    "[3, 1]": "b5",
    "[2, 1]": "b6",
    "[1, 1]": "b7",
    "[0, 1]": "b8",

    "[7, 2]": "c1",
    "[6, 2]": "c2",
    "[5, 2]": "c3",
    "[4, 2]": "c4",
    "[3, 2]": "c5",
    "[2, 2]": "c6",
    "[1, 2]": "c7",
    "[0, 2]": "c8",

    "[7, 3]": "d1",
    "[6, 3]": "d2",
    "[5, 3]": "d3",
    "[4, 3]": "d4",
    "[3, 3]": "d5",
    "[2, 3]": "d6",
    "[1, 3]": "d7",
    "[0, 3]": "d8",

    "[7, 4]": "e1",
    "[6, 4]": "e2",
    "[5, 4]": "e3",
    "[4, 4]": "e4",
    "[3, 4]": "e5",
    "[2, 4]": "e6",
    "[1, 4]": "e7",
    "[0, 4]": "e8",

    "[7, 5]": "f1",
    "[6, 5]": "f2",
    "[5, 5]": "f3",
    "[4, 5]": "f4",
    "[3, 5]": "f5",
    "[2, 5]": "f6",
    "[1, 5]": "f7",
    "[0, 5]": "f8",

    "[7, 6]": "g1",
    "[6, 6]": "g2",
    "[5, 6]": "g3",
    "[4, 6]": "g4",
    "[3, 6]": "g5",
    "[2, 6]": "g6",
    "[1, 6]": "g7",
    "[0, 6]": "g8",

    "[7, 7]": "h1",
    "[6, 7]": "h2",
    "[5, 7]": "h3",
    "[4, 7]": "h4",
    "[3, 7]": "h5",
    "[2, 7]": "h6",
    "[1, 7]": "h7",
    "[0, 7]": "h8"
}


def name_to_board(name):
    try:
        return names[name]
    except KeyError:
        return [-1, -1]
