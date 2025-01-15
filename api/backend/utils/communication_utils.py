from .name_to_board import name_to_board as ntb

def generate_json_from_move(move):
    _move = f'{ntb(f"{move[0]}")}{{ntb(f"{move[1]}")}}'
    if move[3] is not False: _move += move[3]
    return {
        'move': _move
    }
