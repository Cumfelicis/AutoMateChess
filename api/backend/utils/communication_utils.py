from .name_to_board import name_to_board as ntb

def generate_json_from_move(move):
    _move = f'{ntb(f"{move[0]}")}{ntb(f"{move[1]}")}'
    return {
        'move': _move,
        'player': move[-1]
    }
