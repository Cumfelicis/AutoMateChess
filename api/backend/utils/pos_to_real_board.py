from ..config import config


def get_pos(index, axis):
    if axis:
        return int((index + 0.5) * config['BOARD_SQUARE_SIZE'])
    else:
        return int((index + 0.5) * config['BOARD_SQUARE_SIZE'])
