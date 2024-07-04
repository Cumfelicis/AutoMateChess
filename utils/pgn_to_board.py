import game as g
import board_to_name as btn


def pgn_to_game(pgn="pgn.txt"):
    game = g.Game()
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
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower) == "legal move":
                                            game.get_board().redo_last_move(game.get_board().last_move)
                                            moves[x][0] = [k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower]
                                            game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]), i[-1].lower)
                                            break
                            else:
                                if k.name == "p":
                                    if btn.board_to_name(i[-3:-1]) in k.get_possible_moves() and \
                                            k.pos[1] == btn.file_to_name(i[0]):
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-3:-1]),
                                                                       i[-1].lower) == "legal move":
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
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
                                            game.get_board().redo_last_move(game.get_board().last_move)
                                            moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                            game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]))
                                            break

                            else:
                                if k.name == "p":
                                    if btn.board_to_name(i[-2:]) in k.get_possible_moves() and \
                                            k.pos[1] == btn.file_to_name(i[0]):
                                        if game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]),) == "legal move":
                                            game.get_board().redo_last_move(game.get_board().last_move)
                                            moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                            game.get_board().move_piece(k.pos, btn.board_to_name(i[-2:]))
                                            break
                        else:
                            continue
                        break
            elif i == "0-0":
                if game.get_players_move():
                    game.get_board().move_piece([7, 4], [7, 6])
                    moves[x][0] = [[7, 4], [7, 6], False]
                else:
                    game.get_board().move_piece([0, 4], [0, 6])
                    moves[x][0] = [[0, 4], [0, 6], False]
            elif i == "0-0-0":
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
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                            else:
                                if k.name == i[0].lower() and btn.file_to_name(i[1]) == k.pos[1]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
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
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                            else:
                                if k.name == i[0].lower() and k.pos[0] + 1 == i[1]:
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
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
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos,btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                            else:
                                if k.name == i[0].lower():
                                    if game.board.move_piece(k.pos, btn.board_to_name(i[-2:])) == "legal move":
                                        game.redo_last_move()
                                        moves[x][0] = [k.pos, btn.board_to_name(i[-2:]), False]
                                        game.board.move_piece(k.pos, btn.board_to_name(i[-2:]))
                                        break
                        else:
                            continue
                        break

        return moves, time_control
