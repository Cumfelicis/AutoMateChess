def get_pos(index, axis):
    if axis:
        return int((index + 0.5) * 312 * 0.8)
    else:
        return int((index + 2.5) * 312 * 0.8)
