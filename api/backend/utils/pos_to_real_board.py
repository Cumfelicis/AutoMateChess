from ..config import config


def get_pos(index, axis):
    if axis:
        return int((index) * config['BOARD_SQUARE_SIZE'])
    else:
        return 8750 - int((index) * config['BOARD_SQUARE_SIZE'])
