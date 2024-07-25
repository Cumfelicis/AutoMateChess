from chess import game as g
from utils import board_to_name as btn
import zstandard as zstd


def pgn_to_game(pgn="pgn.txt"):
    game = g.Game(real_game=False)
    game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    time_control_found = False
    time_control = []
    n = 1
    move = []
    moves = []
    time_found = False
    first_move_found = False
    second_move_found = False
    with open(pgn, "r") as file:
        for i in file.readlines():
            for j in i.split():
                if j == "[TimeControl":
                    time_control_found = True
                    continue
                if time_control_found:
                    time_control_found = False
                    time = ""
                    t_or_i = True
                    inkrement = ""
                    for k in j[1:-2]:
                        if k == "+":
                            t_or_i = False
                            continue
                        elif t_or_i:
                            time += k
                        else:
                            inkrement += k
                    time_control.append(int(time))
                    time_control.append(int(inkrement))
                if j == f"{n}" + ".":
                    first_move_found = True
                    continue
                elif j == f"{n}" + "...":
                    second_move_found = True
                    n += 1
                    continue
                if first_move_found:
                    move.append(j)
                    first_move_found = False
                elif second_move_found:
                    second_move_found = False
                    move.append(j)
                if j == "[%clk":
                    time_found = True
                    continue
                if time_found:
                    move.append(j[:-1])
                    moves.append(move)
                    move = []
                    time_found = False
        for x, i in enumerate(moves):
            i = i[0].replace("?", "").replace("!", "").replace("+", "")
            if not i[0].isupper() and not i[0].isnumeric():
                if i[-1].isalpha():
                    for j in game.board.squares:
                        for k in j:
                            if game.get_players_move():
                                if k.name == "P":
                                    if btn.board_to_name(i[-3:-1]) in k.get_possible_moves() and \
                                            k.pos[1] == btn.file_to_name(i[0]):
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower):
                                            game.get_board().redo_last_move(game.get_board().last_move)
                                            moves[x][0] = [k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower]
                                            game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower)
                                            break
                            else:
                                if k.name == "p":
                                    if btn.board_to_name(i[-3:-1]) in k.get_possible_moves() and \
                                            k.pos[1] == btn.file_to_name(i[0]):
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]),
                                                                       i[-1].lower):
                                            game.get_board().redo_last_move(game.get_board().last_move)
                                            moves[x][0] = [k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower]
                                            game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower)
                                            break
                        else:
                            continue
                        break
                else:
                    for j in game.board.squares:
                        for k in j:
                            if game.get_players_move():
                                if btn.board_to_name(i[-2:]) in k.get_possible_moves() and \
                                        k.pos[1] == btn.file_to_name(i[0]):
                                    if game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.get_board().redo_last_move(game.get_board().last_move)
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break

                            else:
                                if k.name == "p":
                                    if btn.board_to_name(i[-2:]) in k.get_possible_moves() and \
                                            k.pos[1] == btn.file_to_name(i[0]):
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:])):
                                            game.get_board().redo_last_move(game.get_board().last_move)
                                            moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                            game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]))
                                            break
                        else:
                            continue
                        break
            elif i == "O-O":
                if game.get_players_move():
                    game.get_board().move_piece([7, 4], [7, 6])
                    moves[x][0] = [[7, 4], [7, 6], False]
                else:
                    game.get_board().move_piece([0, 4], [0, 6])
                    moves[x][0] = [[0, 4], [0, 6], False]
            elif i == "O-O-O":
                if game.get_players_move():
                    game.get_board().move_piece([7, 4], [7, 2])
                    moves[x][0] = [[7, 4], [7, 2], False]
                else:
                    game.get_board().move_piece([0, 4], [0, 2])
                    moves[x][0] = [[0, 4], [0, 2], False]
            else:
                if i[1].isalpha() and not i[1] == "x" and i[2].isalpha():
                    for j in game.board.squares:
                        for k in j:
                            if game.get_players_move():
                                if k.name == i[0] and btn.file_to_name(i[1]) == k.pos[1]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                            else:
                                if k.name == i[0].lower() and btn.file_to_name(i[1]) == k.pos[1]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                        else:
                            continue
                        break
                elif i[1].isnumeric():
                    for j in game.board.squares:
                        for k in j:
                            if game.get_players_move():
                                if k.name == i[0] and abs(k.pos[0] - 8) == i[1]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                            else:
                                if k.name == i[0].lower() and k.pos[0] + 1 == i[1]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                        else:
                            continue
                        break
                else:
                    for j in game.board.squares:
                        for k in j:
                            if game.get_players_move():
                                if k.name == i[0]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                            else:
                                if k.name == i[0].lower():
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                        else:
                            continue
                        break

        return moves, time_control


def game_from_lines(lines, game):
    game = game
    game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    time_control_found = False
    time_control = []
    last_clock_white = 0
    last_clock_black = 0
    time, inkrement = 0, 0
    n = 1
    move = []
    moves = []
    times = []
    positions = []
    time_found = False
    first_move_found = False
    second_move_found = False
    white_elo = 0
    black_elo = 0
    white_elo_found = False
    black_elo_found = False
    for i in lines:
        for j in i.split():
            if j == '[WhiteElo':
                white_elo_found = True
                continue
            if j == '[BlackElo':
                black_elo_found = True
                continue

            if white_elo_found:
                white_elo = int(j[:-1].strip('"'))
                white_elo_found = False
            if black_elo_found:
                black_elo = int(j[:-1].strip('"'))
                black_elo_found = False
            if j == "[TimeControl":
                time_control_found = True
                continue
            if time_control_found:
                if j == '"-"]':
                    return [], [], [], []
                time, inkrement = map(lambda e: int(e.strip('"')), j[:-1].split('+'))
                time_control.append(time)
                time_control.append(inkrement)
                last_clock_white = time_control[0]
                last_clock_black = time_control[0]
                time_control_found = False
            if j == f"{n}" + ".":
                first_move_found = True
                continue
            elif j == f"{n}" + "...":
                second_move_found = True
                n += 1
                continue
            if first_move_found:
                move.append(j)
                # first_move_found = False

            elif second_move_found:
                move.append(j)
                # second_move_found = False
            if j == "[%clk":
                time_found = True
                continue
            if time_found:
                move.append(j[:-1])
                moves.append(move)
                move = []
                time_in_seconds = time_to_seconds(j[:-1])
                if first_move_found:
                    times.append(abs(last_clock_white - time_in_seconds))
                    last_clock_white = time_in_seconds + inkrement
                    first_move_found = False
                else:
                    times.append(abs(last_clock_black - time_in_seconds))
                    last_clock_black = time_in_seconds + inkrement
                    second_move_found = False
                time_found = False
    for x, i in enumerate(moves):
        i = i[0].replace('?', '').replace('!', '').replace('+', '').replace('x', '').replace('#', '')
        if not i[0].isupper() and not i[0].isnumeric():
            if i[-1].isalpha():  # promotion
                for j in game.board.squares:
                    for k in j:
                        if game.get_players_move():
                            if k.name == "P":  # white pawn moves
                                if btn.board_to_name(i[-4:-2]) in k.get_possible_moves() and \
                                        k.pos[1] == btn.file_to_name(i[0]):
                                    temp_k_pos = k.pos.copy()
                                    if game.get_board().move_piece(k.pos, btn.board_to_name(i[-4:-2]),
                                                                   promotion=i[-1].upper()):
                                        game.get_board().redo_last_move(game.get_board().last_move)
                                        moves[x][0] = [temp_k_pos, btn.board_to_name(i[-4:-2]), i[-1].upper()]
                                        positions.append(game.get_board().board_to_string())
                                        game.get_board().move_piece(temp_k_pos, btn.board_to_name(i[-4:-2]),
                                                                    promotion=i[-1].upper())
                                        break
                        else:
                            if k.name == "p":  # black pawn moves
                                if btn.board_to_name(i[-4:-2]) in k.get_possible_moves() and \
                                        k.pos[1] == btn.file_to_name(i[0]):
                                    temp_k_pos = k.pos.copy()
                                    if game.get_board().move_piece(k.pos, btn.board_to_name(i[-4:-2]),
                                                                   promotion=i[-1].lower()):
                                        game.get_board().redo_last_move(game.get_board().last_move)
                                        moves[x][0] = [temp_k_pos, btn.board_to_name(i[-4:-2]), i[-1].lower()]
                                        positions.append(game.get_board().board_to_string())
                                        game.get_board().move_piece(temp_k_pos, btn.board_to_name(i[-4:-2]),
                                                                    promotion=i[-1].lower())
                                        break
                    else:
                        continue
                    break

            else:  # pawn moves no promotion
                for j in game.board.squares:
                    for k in j:
                        if game.get_players_move():
                            if k.name == 'P':
                                if btn.board_to_name(i[-2:]) in k.get_possible_moves() and \
                                        k.pos[1] == btn.file_to_name(i[0]):
                                    if game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.get_board().redo_last_move(game.get_board().last_move)
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        positions.append(game.get_board().board_to_string())
                                        game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break

                        else:
                            if k.name == "p":
                                if btn.board_to_name(i[-2:]) in k.get_possible_moves() and \
                                        k.pos[1] == btn.file_to_name(i[0]):
                                    if game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:])):
                                        game.get_board().redo_last_move(game.get_board().last_move)
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        positions.append(game.get_board().board_to_string())
                                        game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                    else:
                        continue
                    break
        elif i == "O-O":  # castling moves
            if game.get_players_move():
                positions.append(game.get_board().board_to_string())
                game.get_board().move_piece([7, 4], [7, 6])
                moves[x][0] = [[7, 4], [7, 6], False]
                continue
            else:
                positions.append(game.get_board().board_to_string())
                game.get_board().move_piece([0, 4], [0, 6])
                moves[x][0] = [[0, 4], [0, 6], False]
                continue
        elif i == "O-O-O":
            if game.get_players_move():
                positions.append(game.get_board().board_to_string())
                game.get_board().move_piece([7, 4], [7, 2])
                moves[x][0] = [[7, 4], [7, 2], False]
                continue
            else:
                positions.append(game.get_board().board_to_string())
                game.get_board().move_piece([0, 4], [0, 2])
                moves[x][0] = [[0, 4], [0, 2], False]
                continue
        else:
            if i[1].isalpha() and not i[1] == "x" and i[2].isalpha():
                for j in game.board.squares:
                    for k in j:
                        if game.get_players_move():
                            if k.name == i[0] and btn.file_to_name(i[1]) == k.pos[1]:
                                if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                    game.redo_last_move()
                                    moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                    positions.append(game.get_board().board_to_string())
                                    game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                    break
                        else:
                            if k.name == i[0].lower() and btn.file_to_name(i[1]) == k.pos[1]:
                                if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                    game.redo_last_move()
                                    moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                    positions.append(game.get_board().board_to_string())
                                    game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                    break
                    else:
                        continue
                    break
            elif i[1].isnumeric():  # specified move rank
                for j in game.board.squares:
                    for k in j:
                        if game.get_players_move():
                            if k.name == i[0] and 8 - k.pos[0] == int(i[1]):
                                if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                    game.redo_last_move()
                                    moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                    positions.append(game.get_board().board_to_string())
                                    game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                    break
                        else:
                            if k.name == i[0].lower() and 8 - k.pos[0] == int(i[1]):
                                if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                    game.redo_last_move()
                                    moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                    positions.append(game.get_board().board_to_string())
                                    game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                    break
                    else:
                        continue
                    break
            else:
                for j in game.board.squares:
                    for k in j:
                        if game.get_players_move():
                            if k.name == i[0]:
                                if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                    game.redo_last_move()
                                    moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                    positions.append(game.get_board().board_to_string())
                                    game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                    break
                        else:
                            if k.name == i[0].lower():
                                if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])):
                                    game.redo_last_move()
                                    moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                    positions.append(game.get_board().board_to_string())
                                    game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                    break
                    else:
                        continue
                    break
        if not isinstance(moves[x][0], list):
            raise Exception('illegal move in PGN')
    return time_control, positions, times, [white_elo, black_elo]


def time_to_seconds(time_str):
    # Split the time string into hours, minutes, and seconds
    h, m, s = map(int, time_str.split(':'))

    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s
    print

    return total_seconds


if __name__ == '__main__':
    with open('pgn.txt', 'r') as file:
        print(game_from_lines(file.readlines(), g.Game(real_game=False)))
