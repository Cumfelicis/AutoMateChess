import time
import copy

import pygame as py
import math
import pygame.display
import sys
import board_to_name
import name_to_board
from Pieces import Bishop, Pawn, Queen, King, Knight, Rook, No
import arduino_communication
import pos_to_real_board as ptrb
from piece_to_storage import piece_to_storage
import piece_detector


class Board:
    def __init__(self, setup, alignment, pos_x, pos_y, window, size, stepper_x=False, stepper_y=False, magnet=False,
                 real_board=False):
        self.setup = setup
        self.real_board = real_board
        self.alignment = alignment
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = (pos_x, pos_y)
        self.window = window
        self.size = size
        self.between_squares = int(162 * 0.8)
        if self.real_board:
            self.stepper_x = stepper_x
            self.stepper_y = stepper_y
            self.magnet = magnet
            self.multistepper = arduino_communication.Multistepper()
            self.multistepper.add_stepper(self.stepper_x)
            self.multistepper.add_stepper(self.stepper_y)
        #  self.piece_detector = piece_detector.PieceDetector()
        self.white_pieces = ["K", "Q", "R", "B", "N", "P"]
        self.black_pieces = ["k", "q", "r", "b", "n", "p"]
        self.squares = [[No(0, 0, 0, 0, 0, 0) for _ in range(8)] for _ in range(8)]
        self.white_castle_short = False
        self.white_castle_long = False
        self.black_castle_short = False
        self.black_castle_long = False
        self.white_castle_short_generally = False
        self.white_castle_long_generally = False
        self.black_castle_short_generally = False
        self.black_castle_long_generally = False
        self.ep = False
        self.played_moves = 0
        self.this_move = 1
        self.turn = True
        self.started_dragging = False
        self.save = None
        self.anchor = False
        self.last_move = None
        self.moves = []
        self.white_storage = [[0 for _ in range(2)] for _ in range(8)]
        self.black_storage = [[0 for _ in range(2)] for _ in range(8)]

    def move_piece(self, piece_square, destination, promotion=False, real=True):
        castled = False
        castled_short = False
        self.get_legal_moves()
        eped = False
        if self.squares[piece_square[0]][piece_square[1]].name.upper() == "K" \
                and piece_square[1] - destination[1] == -2 \
                and self.white_castle_short and \
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)):
            castled = True
            castled_short = True
        elif self.squares[piece_square[0]][piece_square[1]].name.upper() == "K" and \
                piece_square[1] - destination[1] == 2 \
                and self.white_castle_long and \
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)):
            castled = True
        elif self.squares[piece_square[0]][piece_square[1]].name.upper() == "K" \
                and piece_square[1] - destination[1] == -2 \
                and self.black_castle_short and \
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)):
            castled = True
            castled_short = True
        elif self.squares[piece_square[0]][piece_square[1]].name.upper() == "K" and \
                piece_square[1] - destination[1] == 2 \
                and self.black_castle_long and \
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)):
            castled = True
        if (destination in self.squares[piece_square[0]][piece_square[1]].get_possible_moves() or castled) and \
                ((self.turn and self.squares[piece_square[0]][piece_square[1]].direction == -1) or
                 (not self.turn and self.squares[piece_square[0]][piece_square[1]].direction == 1)):
            if self.squares[piece_square[0]][piece_square[1]].name.upper() == "P" and destination == self.ep:
                eped = True
            self.squares[piece_square[0]][piece_square[1]].move_piece_rpos(destination)
            storage = self.squares[piece_square[0]][piece_square[1]]
            if self.squares[destination[0]][destination[1]].name == "!" and not castled and not eped:
                self.squares[piece_square[0]][piece_square[1]] = self.squares[destination[0]][destination[1]]
                self.squares[destination[0]][destination[1]] = storage
                captured_storage = No(0, 0, 0, 0, 0, 0)
            elif not castled and not eped:
                captured_storage = self.squares[destination[0]][destination[1]]
                self.squares[destination[0]][destination[1]].captured = True
                self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
                self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, 0, 0, 0)
            elif castled_short and not eped:
                captured_storage = No(0, 0, 0, 0, 0, 0)
                self.squares[destination[0]][destination[1] + 1].move_piece_rpos([piece_square[0], piece_square[1] + 1])
                self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
                self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, 0, 0, 0)
                self.squares[piece_square[0]][piece_square[1] + 1] = self.squares[destination[0]][destination[1] + 1]
                self.squares[destination[0]][destination[1] + 1] = No(0, 0, 0, 0, 0, 0)
            elif eped:
                self.squares[piece_square[0]][piece_square[1]].move_piece_rpos(destination)
                self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
                self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, 0, 0, 0)
                captured_storage \
                    = self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction] \
                    [destination[1]]
                captured_storage.captured = True
                self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction][destination[1]] \
                    = No(0, 0, 0, 0, 0, 0)
            else:
                captured_storage = No(0, 0, 0, 0, 0, 0)
                self.squares[destination[0]][destination[1] - 2].move_piece_rpos([piece_square[0], piece_square[1] - 1])
                self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
                self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, 0, 0, 0)
                self.squares[piece_square[0]][piece_square[1] - 1] = self.squares[destination[0]][destination[1] - 2]
                self.squares[destination[0]][destination[1] - 2] = No(0, 0, 0, 0, 0, 0)
            illegal_move = self.in_check()
            if illegal_move or self.anchor:
                self.squares[destination[0]][destination[1]].move_piece_rpos(piece_square)
                self.squares[destination[0]][destination[1]] = captured_storage
                self.squares[destination[0]][destination[1]].captured = False
                if eped:
                    captured_storage.captured = False
                    self.squares[destination[0]][destination[1]].move_piece_rpos(piece_square)
                    self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction][
                        destination[1]] = captured_storage
                self.squares[piece_square[0]][piece_square[1]] = storage
                if illegal_move:
                    return "illegal move"
                else:
                    return "legal move"
            if self.squares[destination[0]][destination[1]].name.upper() == "P" and \
                    abs(destination[0] - piece_square[0]) == 2:
                self.ep = [self.squares[destination[0]][destination[1]].pos[0] -
                           self.squares[destination[0]][destination[1]].direction,
                           self.squares[destination[0]][destination[1]].pos[1]]
            else:
                self.ep = [-1, -1]
            if promotion is not False:
                match promotion:
                    case "q":
                        self.squares[destination[0]][destination[1]] = Queen([destination[0], destination[1]],
                                                                             False, self.size, self.window,
                                                                             self.pos, False, self)
                    case "r":
                        self.squares[destination[0]][destination[1]] = Rook([destination[0], destination[1]],
                                                                            False, self.size, self.window,
                                                                            self.pos, False, self)
                    case "b":
                        self.squares[destination[0]][destination[1]] = Bishop([destination[0], destination[1]],
                                                                              False, self.size, self.window,
                                                                              self.pos, False, self)
                    case "n":
                        self.squares[destination[0]][destination[1]] = Knight([destination[0], destination[1]],
                                                                              False, self.size, self.window,
                                                                              self.pos, False, self)
                    case "Q":
                        self.squares[destination[0]][destination[1]] = Queen([destination[0], destination[1]],
                                                                             True, self.size, self.window,
                                                                             self.pos, False, self)
                    case "R":
                        self.squares[destination[0]][destination[1]] = Rook([destination[0], destination[1]],
                                                                            True, self.size, self.window,
                                                                            self.pos, False, self)
                    case "B":
                        self.squares[destination[0]][destination[1]] = Bishop([destination[0], destination[1]],
                                                                              True, self.size, self.window,
                                                                              self.pos, False, self)
                    case "N":
                        self.squares[destination[0]][destination[1]] = Knight([destination[0], destination[1]],
                                                                              True, self.size, self.window,
                                                                              self.pos, False, self)
            promotion = self.check_for_promotion()
            self.squares[destination[0]][destination[1]].moved = True
            if self.real_board and real:
                self.play_move_on_board(piece_square, destination, captured_storage, castled)
            self.turn = not self.turn
            self.played_moves += 1
            self.squares[destination[0]][destination[1]].first_moved = copy.deepcopy(self.played_moves)
            self.last_move = [piece_square, destination, captured_storage, promotion, eped]
            self.moves.append([piece_square, destination, captured_storage, promotion, eped])
            return "legal move"
        else:
            return "illegal move"

    def update_last_move(self):
        if len(self.moves) > 0:
            self.last_move = self.moves[-1]

    def redo_last_move(self, last_move, real=True):
        if len(self.moves) > 0:
            self.moves.pop()
        piece_square = last_move[0]
        destination = last_move[1]
        if self.squares[destination[0]][destination[1]].first_moved == self.played_moves:
            self.squares[destination[0]][destination[1]].moved = False
        captured = last_move[2]
        promotion = last_move[3]
        castled = False
        ep = last_move[4]
        if self.squares[destination[0]][destination[1]].name.lower() == "k" \
                and abs(piece_square[1] - destination[1]) == 2:
            castled = True
            if destination[1] == 6:
                self.squares[destination[0]][destination[1] + 1] = copy.copy(self.squares[destination[0]][destination[1] - 1])
                self.squares[destination[0]][destination[1] - 1] = captured
                self.squares[destination[0]][destination[1] + 1].move_piece_rpos([destination[0], destination[1] + 1])
                self.squares[destination[0]][destination[1] + 1].moved = False
            else:
                self.squares[destination[0]][destination[1] - 2] = copy.copy(self.squares[destination[0]][destination[1] + 1])
                self.squares[destination[0]][destination[1] + 1] = captured
                self.squares[destination[0]][destination[1] - 2].move_piece_rpos([destination[0], destination[1] - 2])
                self.squares[destination[0]][destination[1] - 2].moved = False

        if ep:
            self.ep = destination
            self.squares[piece_square[0]][piece_square[1]] = self.squares[destination[0]][destination[1]]
            self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction][
                destination[1]] = captured
            captured.captured = False
            self.squares[piece_square[0]][piece_square[1]].move_piece_rpos(piece_square)
        else:
            self.ep = [-1, -1]
            self.squares[piece_square[0]][piece_square[1]] = self.squares[destination[0]][destination[1]]
            self.squares[destination[0]][destination[1]] = captured
            captured.captured = False
            self.squares[piece_square[0]][piece_square[1]].move_piece_rpos(piece_square)
        if promotion is not False:
            if self.squares[piece_square[0]][piece_square[1]].direction == -1:
                self.squares[piece_square[0]][piece_square[1]].direction = Pawn([piece_square[0], piece_square[1]],
                                                                                True, self.size,
                                                                                self.window, self.pos, False, self)
            else:
                self.squares[piece_square[0]][piece_square[1]].direction = Pawn([piece_square[0], piece_square[1]],
                                                                                True, self.size,
                                                                                self.window, self.pos, False, self)
        if self.real_board and real:
            self.redo_move_on_board(piece_square=piece_square, target_square=destination, captured=captured, castled=castled)
        if len(self.moves) > 0:
            self.last_move = self.moves[-1]
            self.played_moves -= 1
        else:
            self.last_move = None
        self.turn = not self.turn

    def find_played_move(self, other_board):
        for i in self.squares:
            for j in i:
                if self.turn and j.direction == -1:
                    for k in j.get_possible_moves():
                        if self.move_piece(j.pos, k, real=False) == "legal move":
                            if self.compare_boards(other_board):
                                self.update_storage(self.last_move[2])
                                return True
                            self.redo_last_move(self.last_move, real=False)
                elif not self.turn and j.direction == 1:
                    for k in j.get_possible_moves():
                        if self.move_piece(j.pos, k, real=False) == "legal move":
                            if self.compare_boards(other_board):
                                self.update_storage(self.last_move[2])
                                return True
                            self.redo_last_move(self.last_move, real=False)
        return False

    def compare_boards(self, other_board):
        for x, i in enumerate(self.squares):
            for y, j in enumerate(i):
                if not ((j.name in self.white_pieces and other_board[x][y] == 1) or (j.name in self.black_pieces and
                                                                                    other_board[x][y] == 2) or
                        (j.name == "!" and other_board[x][y] == 0)):
                    return False
        return True

    def highlight_last_move(self):
        pass

    def draw_pieces(self):
        for row in self.squares:
            for i in row:
                if i is not None:
                    i.draw_piece()

    def in_check(self):
        in_check = False
        for i in self.squares:
            for j in i:
                if j.name == "K":
                    for k in self.get_legal_moves()[1]:
                        if j.pos == k[1] and self.turn:
                            in_check = True
                elif j.name == "k":
                    for k in self.get_legal_moves()[0]:
                        if j.pos == k[1] and not self.turn:
                            in_check = True
        return in_check

    def check_for_played_move(self):
        self.find_played_move(self.piece_detector.check_for_pieces())

    def update_storage(self, piece):
        if not piece is False and not piece.name == "!":
            self.find_storage_pos(piece.name)

    def play_move_on_board(self, piece_square, target_square, captured=No(0, 0, 0, 0, 0, 0), castled=False, player_move=False):
        if not captured.name == "!":
            self.move_to_square(captured.pos)
            self.remove_piece([captured.name, target_square])
        self.move_to_square(piece_square)
        self.magnet.on()
        self.stepper_x.move(self.between_squares)
        self.stepper_y.move_to(ptrb.get_pos(target_square[0] + 0.5, False))
        self.stepper_x.run_to()
        self.stepper_y.run_to()
        self.stepper_x.move_to(ptrb.get_pos(target_square[1], True))
        self.stepper_y.move(-self.between_squares)
        self.stepper_x.run_to()
        self.stepper_y.run_to()
        self.magnet.off()
        if castled:
            if target_square[1] == 6:
                self.move_to_square([target_square[0], target_square[1] + 1])
                self.magnet.on()
                self.stepper_y.move(self.between_squares)
                self.stepper_y.run_to()
                self.stepper_x.move_to(ptrb.get_pos(piece_square[1] + 1, True))
                self.stepper_x.run_to()
                self.stepper_y.move(-self.between_squares)
                self.stepper_y.run_to()
                self.magnet.off()
            else:
                self.move_to_square([target_square[0], target_square[1] - 2])
                self.magnet.on()
                self.stepper_y.move(self.between_squares)
                self.stepper_y.run_to()
                self.stepper_x.move_to(ptrb.get_pos(piece_square[1] + 1, True))
                self.stepper_x.run_to()
                self.stepper_y.move(-self.between_squares)
                self.stepper_y.run_to()
                self.magnet.off()
        self.stepper_x.reference()
        self.stepper_y.reference()

    def redo_move_on_board(self, piece_square, target_square, captured=No(0, 0, 0, 0, 0, 0), castled=False):
        if not castled:
            self.play_move_on_board(target_square, piece_square)
            if not captured.name == "!":
                self.extract_piece(captured.name, captured.pos)
        else:
            if target_square[1] == 6:
                self.play_move_on_board([piece_square[0], piece_square[1] + 1], [piece_square[0] + 0.5,
                                                                                 piece_square[1] + 1])
                self.play_move_on_board([piece_square[0] + 0.5, piece_square[1] + 1], [target_square[0] +
                                                                                       0.5, target_square[1] + 1])
                self.play_move_on_board([target_square[0] + 0.5, target_square[1] + 1], [target_square[0],
                                                                                         target_square[1] + 1])
            else:
                self.play_move_on_board([piece_square[0], piece_square[1] + 1], [piece_square[0] + 0.5,
                                                                                 piece_square[1] + 1])
                self.play_move_on_board([piece_square[0] + 0.5, piece_square[1] + 1], [target_square[0] +
                                                                                       0.5, target_square[1] - 1])
                self.play_move_on_board([target_square[0] + 0.5, target_square[1] + 1], [target_square[0],
                                                                                         target_square[1] - 1])
            self.play_move_on_board(target_square, piece_square)

    def remove_piece(self, piece):
        self.play_move_on_board(piece[1], self.find_storage_pos(piece[0]))

    def move_to_square(self, square):
        self.stepper_x.move_to(ptrb.get_pos(square[1], True))
        self.stepper_x.run_to()
        self.stepper_y.move_to(ptrb.get_pos(square[0], False))
        self.stepper_y.run_to()

    def clear_real_board(self):
        for i in self.squares:
            for j in i:
                if not j.name == "!":
                    self.move_to_square(j.pos)
                    self.remove_piece(j.name)

    def setup_real_board(self, old_pos, new_pos):
        leftovers = []
        missing = []
        for x, i in enumerate(old_pos):
            for y, j in enumerate(i):
                if not j.name == new_pos[x][y].name:
                    if new_pos[x][y].name != "!":
                        missing.append([new_pos[x][y].name, [x, y]])
                    if j.name != "!":
                        if new_pos[x][y].name == "!":
                            leftovers.append([j.name, [x, y]])
                        else:
                            self.remove_piece([j.name, [x, y]])

        temp = missing.copy()
        for x, i in enumerate(leftovers):
            if len(temp) > 0:
                for y, j in enumerate(temp):
                    if i[0] == j[0]:
                        if len(temp) > x:
                            temp.pop(x)
                        break
                else:
                    self.remove_piece([i[0], [i[1][0], i[1][1]]])
                    leftovers.pop(x)
            else:
                self.remove_piece([i[0], [i[1][0], i[1][1]]])
                leftovers.pop(x)

        for i in leftovers:
            for x, j in enumerate(missing):
                if i[0] == j[0]:
                    self.play_move_on_board(i[1], j[1])
                    missing.pop(x)
                    break

        for i in missing:
            self.play_move_on_board(self.find_extraction_pos(i[0]), i[1])

    def find_storage_pos(self, piece):
        try:
            storage_pos = piece_to_storage(piece)
            if piece in self.white_pieces:
                while not self.white_storage[storage_pos[0]][storage_pos[1]] == 0:
                    if storage_pos[1] == 1:
                        storage_pos[1] = 0
                    else:
                        storage_pos[1] = 1
                        storage_pos[0] += 1
                    print(storage_pos)
                self.white_storage[storage_pos[0]][storage_pos[1]] = 1
                storage_pos[1] -= 2
                temp = storage_pos.copy()
                storage_pos[0] = temp[1]
                storage_pos[1] = 7 - temp[0]
            else:
                while not self.black_storage[storage_pos[0]][storage_pos[1]] == 0:
                    if storage_pos[1] == 0:
                        storage_pos[1] = 1
                    else:
                        storage_pos[1] = 0
                        storage_pos[0] += 1
                        print(storage_pos)
                self.black_storage[storage_pos[0]][storage_pos[1]] = 1
                storage_pos[1] += 8
            return storage_pos
        except IndexError:
            return [-1, 8]

    def find_extraction_pos(self, piece):
        storage_pos = piece_to_storage(piece)
        print(storage_pos)
        if piece in self.white_pieces:
            while not self.white_storage[storage_pos[0]][storage_pos[1]] == 1:
                if storage_pos[1] == 1:
                    storage_pos[1] = 0
                else:
                    storage_pos[1] = 1
                    storage_pos[0] += 1
            self.white_storage[storage_pos[0]][storage_pos[1]] = 0
            storage_pos[1] -= 2
            temp = storage_pos.copy()
            storage_pos[0] = temp[1]
            storage_pos[1] = 7 - temp[0]
        else:
            while not self.black_storage[storage_pos[0]][storage_pos[1]] == 1:
                if storage_pos[1] == 0:
                    storage_pos[1] = 1
                else:
                    storage_pos[1] = 0
                    storage_pos[0] += 1
            self.black_storage[storage_pos[0]][storage_pos[1]] = 0
            storage_pos[1] += 8
        return storage_pos

    def extract_piece(self, piece, target_square):
        try:
            extraction_pos = self.find_extraction_pos(piece)
            if piece in self.white_pieces:
                piece_pos = [extraction_pos[0], extraction_pos[1] - 2]
            else:
                piece_pos = [extraction_pos[0], 8 + extraction_pos[1]]
            if piece in self.white_pieces:
                self.play_move_on_board(piece_pos, [piece_pos[0] + 0.5, piece_pos[1] + 0.5])
                self.play_move_on_board([piece_pos[0] + 0.5, piece_pos[1] + 0.5], [piece_pos[0] + 0.5, target_square[1] + 0.5])
                self.play_move_on_board([piece_pos[0] + 0.5, target_square[1] + 0.5], [target_square[0] + 0.5,
                                        target_square[1] + 0.5])
                self.play_move_on_board([target_square[0] + 0.5, target_square[1] + 0.5], target_square)
            else:
                self.play_move_on_board(piece_pos, [piece_pos[0] + 0.5, piece_pos[1] + 0.5])
                self.play_move_on_board([piece_pos[0] + 0.5, piece_pos[1] + 0.5], [piece_pos[0] + 0.5, target_square[1] + 0.5])
                self.play_move_on_board([piece_pos[0] + 0.5, target_square[1] + 0.5], [target_square[0] + 0.5,
                                                                                       target_square[1] + 0.5])
                self.play_move_on_board([target_square[0] + 0.5, target_square[1] - 0.5], target_square)
        except IndexError:
            pass

    def square_in_check(self, square, piece_colour):
        in_check = False
        if piece_colour == -1:
            for k in self.get_legal_moves()[1]:
                if square == k[1] and self.turn:
                    in_check = True
        else:
            for k in self.get_legal_moves()[0]:
                if square == k[1] and not self.turn:
                    in_check = True
        return in_check

    def get_legal_moves(self):
        white_moves = []
        black_moves = []
        for i in self.squares:
            for j in i:
                if j.direction == -1:
                    for k in j.get_possible_moves():
                        white_moves.append([j.pos, k])
                else:
                    for k in j.get_possible_moves():
                        black_moves.append([j.pos, k])
        return [white_moves, black_moves]

    def check_for_promotion(self):
        new_piece = False
        for i in self.squares:
            for j in i:
                if j.name == "P" and j.pos[0] == 0:
                    new_piece = input("piece to promote into: ")
                    if new_piece.upper() == "Q":
                        self.squares[j.pos[0]][j.pos[1]] = Queen([j.pos[0], j.pos[1]], True, self.size, self.window,
                                                                 self.pos, False, self)
                    elif new_piece.upper() == "R":
                        self.squares[j.pos[0]][j.pos[1]] = Rook([j.pos[0], j.pos[1]], True, self.size, self.window,
                                                                self.pos, False, self)
                    elif new_piece.upper() == "N":
                        self.squares[j.pos[0]][j.pos[1]] = Knight([j.pos[0], j.pos[1]], True, self.size, self.window,
                                                                  self.pos, False, self)
                    elif new_piece.upper() == "B":
                        self.squares[j.pos[0]][j.pos[1]] = Bishop([j.pos[0], j.pos[1]], True, self.size, self.window,
                                                                  self.pos, False, self)
                elif j.name == "P" and j.pos[0] == 7:
                    new_piece = input("piece to promote into: ")
                    if new_piece.upper() == "Q":
                        self.squares[j.pos[0]][j.pos[1]] = Queen([j.pos[0], j.pos[1]], False, self.size, self.window,
                                                                 self.pos, False, self)
                    elif new_piece.upper() == "R":
                        self.squares[j.pos[0]][j.pos[1]] = Rook([j.pos[0], j.pos[1]], False, self.size, self.window,
                                                                self.pos, False, self)
                    elif new_piece.upper() == "N":
                        self.squares[j.pos[0]][j.pos[1]] = Knight([j.pos[0], j.pos[1]], False, self.size, self.window,
                                                                  self.pos, False, self)
                    elif new_piece.upper() == "B":
                        self.squares[j.pos[0]][j.pos[1]] = Bishop([j.pos[0], j.pos[1]], False, self.size, self.window,
                                                                  self.pos, False, self)
        return new_piece

    def check_for_mate(self):
        mate = True
        if not self.anchor:
            self.anchor = True
            if self.turn:
                for i in self.get_legal_moves()[0]:
                    if self.move_piece(i[0], i[1]) == "legal move":
                        mate = False
                        break
            else:
                for i in self.get_legal_moves()[1]:
                    if self.move_piece(i[0], i[1]) == "legal move":
                        mate = False
                        break
            self.anchor = False
        return mate

    def print_board(self):
        for j in self.squares:
            row = []
            for i in j:
                row.append(i.name)
            print(f"{row}")
        print("printed board")

    def draw_board(self):
        pos_x = self.pos_x
        pos_y = self.pos_y
        alignment = self.alignment
        size = self.size

        squares = [Square(pos_x, pos_y, (192, 192, 192), (204, 0, 0), None, size) for i in range(64)]
        add_line = 0
        add_row = 0
        where_in_line = 1

        for square in squares:
            if where_in_line > 8:
                add_row += size
                add_line = 0
                where_in_line = 1
                alignment = not alignment
            if alignment:
                colour = square.colour_1
            else:
                colour = square.colour_2
            square.pos_x += add_line
            square.pos_y += add_row
            square.draw_square(self.window, colour)

            alignment = not alignment
            add_line += size
            where_in_line += 1

    def draw_outline(self):
        py.draw.rect(self.window, (0, 0, 0), (self.pos_x - 10, self.pos_y - 10, self.size * 8 + 20, self.size * 8 + 20))

    def set_up(self, fen, first_set_up=False):
        if self.real_board and not first_set_up:
            temp = self.squares.copy()
        self.squares = [[No(0, 0, 0, 0, 0, 0) for _ in range(8)] for _ in range(8)]
        row = 0
        column = 0
        blanks = 0
        e_p = ""
        for i in fen:
            if row <= 7:
                if i == '/':
                    row += 1
                    column = 0
                elif i == "r":
                    self.squares[row][column] = Rook([row, column], False, self.size, self.window, self.pos, False,
                                                     self)
                    column += 1
                elif i == "R":
                    self.squares[row][column] = Rook([row, column], True, self.size, self.window, self.pos, False, self)
                    column += 1
                elif i == "n":
                    self.squares[row][column] = Knight([row, column], False, self.size, self.window, self.pos, False,
                                                       self)
                    column += 1
                elif i == "N":
                    self.squares[row][column] = Knight([row, column], True, self.size, self.window, self.pos, False,
                                                       self)
                    column += 1
                elif i == "b":
                    self.squares[row][column] = Bishop([row, column], False, self.size, self.window, self.pos, False,
                                                       self)
                    column += 1
                elif i == "B":
                    self.squares[row][column] = Bishop([row, column], True, self.size, self.window, self.pos, False,
                                                       self)
                    column += 1
                elif i == "q":
                    self.squares[row][column] = Queen([row, column], False, self.size, self.window, self.pos, False,
                                                      self)
                    column += 1
                elif i == "Q":
                    self.squares[row][column] = Queen([row, column], True, self.size, self.window, self.pos, False,
                                                      self)
                    column += 1
                elif i == "k":
                    self.squares[row][column] = King([row, column], False, self.size, self.window, self.pos, False,
                                                     self)
                    column += 1
                elif i == "K":
                    self.squares[row][column] = King([row, column], True, self.size, self.window, self.pos, False, self)
                    column += 1
                elif i == "p":
                    self.squares[row][column] = Pawn([row, column], False, self.size, self.window, self.pos, False,
                                                     self)
                    column += 1
                elif i == "P":
                    self.squares[row][column] = Pawn([row, column], True, self.size, self.window, self.pos, False, self)
                    column += 1
                elif not i == " ":
                    column += int(i)
                if i == " ":
                    row = 8
            if i == " ":
                blanks += 1
            if blanks == 1 and not i == " ":
                if i == "w":
                    self.turn = True
                else:
                    self.turn = False
            if blanks == 2 and not i == " ":
                if i == "K":
                    self.white_castle_short_generally = True
                if i == "Q":
                    self.white_castle_long_generally = True
                if i == "k":
                    self.white_castle_short_generally = True
                if i == "K":
                    self.white_castle_short_generally = True
            if blanks == 3 and not i == " ":
                if i != "-":
                    e_p += i
            if blanks == 4 and not i == " ":
                self.ep = board_to_name.board_to_name(e_p)
                self.played_moves = int(i)
        if self.real_board and not first_set_up:
            self.setup_real_board(temp, self.squares)
            del temp

    def convert_to_fen(self):
        fen = ""
        count = 0
        self.get_legal_moves()
        no_castle = True
        for i in self.squares:
            for j in i:
                if j.name == "!":
                    count += 1
                else:
                    if not count == 0:
                        fen += str(count)
                        count = 0
                    fen += j.name
            if not count == 0:
                fen += str(count)
                count = 0
            fen += "/"
        fen += " "
        if self.turn:
            fen += "w"
        else:
            fen += "b"
        fen += " "
        if self.white_castle_short_generally:
            fen += "K"
            no_castle = False
        if self.white_castle_long_generally:
            fen += "Q"
            no_castle = False
        if self.black_castle_short_generally:
            fen += "k"
            no_castle = False
        if self.white_castle_long_generally:
            fen += "q"
            no_castle = False
        if no_castle:
            fen += "-"
        fen += " "
        if not self.ep == [-1, -1]:
            fen += name_to_board.name_to_board(str(self.ep))
        else:
            fen += "-"
        fen += " "
        fen += "0"
        fen += " "
        fen += "1"
        return fen


class Mouse:
    def __init__(self, board):
        self.mouse = py.mouse
        self.board = board
        self.square_old = [0, 0]
        self.square_new = [0, 0]
        self.pressed = False

    def mouse_pos_to_square(self):
        pos_x = (self.mouse.get_pos()[0] - self.board.pos[0]) / self.board.size
        pos_y = (self.mouse.get_pos()[1] - self.board.pos[1]) / self.board.size
        if 0 < pos_x <= 8 and 0 < pos_y <= 8:
            return [math.ceil(pos_y) - 1, math.ceil(pos_x) - 1]
        else:
            return False

    def drag(self):
        if self.mouse.get_pressed()[0] and not self.pressed:
            self.pressed = True
            self.square_old = self.mouse_pos_to_square()
        elif not self.mouse.get_pressed()[0] and self.pressed:
            self.pressed = False
            self.square_new = self.mouse_pos_to_square()
            return self.square_old, self.square_new
        return False, False


class Square:
    def __init__(self, pos_x, pos_y, colour_1, colour_2, piece, size):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.colour_1 = colour_1
        self.colour_2 = colour_2
        self.piece = piece
        self.size = size

    def draw_square(self, window, colour):
        py.draw.rect(window, colour, (self.pos_x, self.pos_y, self.size, self.size))


class Game:
    def __init__(self, window=pygame.display.set_mode((1536, 810), pygame.RESIZABLE), stepper_x=False, stepper_y=False,
                 magnet=False, real_game=False):
        self.window = window
        self.board = Board(None, True, 250, 75, self.window, 80,stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet,
                           real_board=real_game)
        self.real = real_game
        self.mouse = Mouse(self.board)

    def game_loop(self):
        pygame.display.set_caption("Chess")
        clock = py.time.Clock()
        run = True
        self.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        while run:
            clock.tick(30)
            self.window.fill((176, 196, 222))
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_board()
            self.move_pieces()
            pygame.display.update()

    @staticmethod
    def draw(image, pos_x, pos_y, window):
        window.blit(image, (pos_x, pos_y))

    def setup_board(self, setup, first_setup=False):
        self.board.set_up(setup, first_set_up=first_setup)

    def draw_board(self):
        self.board.draw_outline()
        self.board.draw_board()
        self.board.draw_pieces()

    def get_board(self):
        return self.board

    def is_my_move(self, colour):
        if colour and self.board.turn:
            return True
        if not colour and not self.board.turn:
            return True
        return False

    def play_move(self, old_square, new_square, promotion=False):
        return self.board.move_piece(old_square, new_square, promotion)

    def get_fen(self):
        return self.board.convert_to_fen()

    def update_last_move(self):
        self.board.update_last_move()

    def get_players_move(self):
        return self.board.turn

    def reset_board(self):
        self.board.set_up("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def move_pieces(self):
        print("moving pieces")
        last = self.board.last_move
        if self.board.real_board:
            self.board.check_for_played_move()
        drag_old, drag_new = self.mouse.drag()
        if drag_old is not False and drag_new is not False and not drag_old == drag_new:
            self.board.move_piece(drag_old, drag_new)
            self.mouse.square_old = False
            self.mouse.square_new = False
        if last == self.board.last_move:
            return False
        return True

    def redo_last_move(self):
        if self.board.last_move is not None:
            self.board.redo_last_move(self.board.last_move)

    def is_checkmate(self):
        return self.board.check_for_mate()

    def print_board(self):
        self.board.print_board()

    def get_last_move(self):
        return self.board.last_move


if __name__ == "__main__":
    game = Game(pygame.display.set_mode((1536, 810), pygame.RESIZABLE))
    game.game_loop()
