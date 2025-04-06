storage = {
    "K": [7, 0],
    "Q": [7, 1],
    "R": [6, 1],
    "N": [5, 1],
    "B": [4, 1],
    "P": [0, 1],
    "k": [7, 1],
    "q": [7, 0],
    "r": [6, 0],
    "n": [5, 0],
    "b": [4, 0],
    "p": [0, 0]
}


def piece_to_storage(piece):
    try:
        return storage[piece].copy()
    except KeyError:
        print("not a piece")
        return False
