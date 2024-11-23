import time
import copy

import pygame as py
import math
import pygame.display
import sys
from utils import board_to_name
from config import config
from utils import name_to_board
from simulation.piece import SimBishop as Bishop, SimPawn as Pawn, SimQueen as Queen, SimKing as King, \
    SimKnight as Knight, SimRook as Rook, SimNo as No, SimPiece as Piece
from backend.simulation.simulation import Simulation
import backend.arduino_communication
from backend.utils import pos_to_real_board as ptrb
from backend.utils.piece_to_storage import piece_to_storage


class Board:
    def __init__(self, setup, alignment, pos_x, pos_y, window, stepper_x=False, stepper_y=False, magnet=False,
                 real_board=False):
        self.setup = setup  # the position the board is set up with
        self.real_board = real_board  # a bool to indicate weather this instance represents the real board
        self.alignment = alignment  # weather this board is seen from the white/black perspective
        self.pos_x = pos_x  # position the board is drawn on the screen
        self.pos_y = pos_y  # "
        self.pos = (pos_x, pos_y)
        self.window = window  # the window instance of pycharm this is rendered in
        self.size = config['BOARD_SQUARE_SIZE']  # the size every square of this instance is rendered in
        self.between_squares = int(config['BOARD_SQUARE_SIZE'] / 2)  # TODO: remove from this class
        if self.real_board:  # TODO: make required, real ones or simulated
            self.stepper_x = stepper_x
            self.stepper_y = stepper_y
            self.magnet = magnet
        self.white_pieces = ["K", "Q", "R", "B", "N", "P"]  # a list of Piece names/Id's to check which color a piece is
        self.black_pieces = ["k", "q", "r", "b", "n", "p"]
        self.squares = [[No(0, 0, 0, self.window, 0, 0) for _ in range(8)] for _ in range(8)]
        # the squares of the board
        self.white_castle_short = False  # variables to decide weather castles is legal
        self.white_castle_long = False
        self.black_castle_short = False
        self.black_castle_long = False
        self.white_castle_short_generally = False
        self.white_castle_long_generally = False
        self.black_castle_short_generally = False
        self.black_castle_long_generally = False
        self.ep = False  # variable that stores weather en passant is legal in the current position
        self.played_moves = 0  # the moves played so far
        self.this_move = 1  # what move this is
        self.turn = True  # which color's turn it is. True: white
        self.started_dragging = False  # TODO: remove from here
        self.save = None  # TODO: no clue
        self.anchor = False  # helper in running simulations
        self.last_move = None  # the last move played TODO: make this not none
        self.moves = []  # the moves played so far
        self.white_storage = [[0 for _ in range(2)] for _ in range(8)]  # storage for the taken pieces
        self.black_storage = [[0 for _ in range(2)] for _ in range(8)]

    def check_for_short_castle(self, piece_square: list[int], destination: list[int]) -> bool:  # checks if the move
        # was a legal short_castling move
        self.get_legal_moves()
        return (self.squares[piece_square[0]][piece_square[1]].name.upper() == "K"
                and piece_square[1] - destination[1] == -2
                and self.white_castle_short and
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)) or
                self.squares[piece_square[0]][piece_square[1]].name.upper() == "K"
                and piece_square[1] - destination[1] == -2
                and self.black_castle_short and
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] + 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)))

    def check_for_long_castle(self, piece_square: list[int], destination: list[int]) -> bool:  # checks if the move
        # was a legal long_castling move
        return (self.squares[piece_square[0]][piece_square[1]].name.upper() == "K" and
                piece_square[1] - destination[1] == 2
                and self.white_castle_long and
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)) or
                self.squares[piece_square[0]][piece_square[1]].name.upper() == "K" and
                piece_square[1] - destination[1] == 2
                and self.black_castle_long and
                (not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 1],
                                          self.squares[piece_square[0]][piece_square[1]].direction) and
                 not self.square_in_check([self.squares[piece_square[0]][piece_square[1]].pos[0],
                                           self.squares[piece_square[0]][piece_square[1]].pos[1] - 2],
                                          self.squares[piece_square[0]][piece_square[1]].direction)))

    def could_be_legal_move(self, piece_square: list[int], destination: list[int], castled: bool) -> bool:  # checks
        # if the move could be legal: move in legal moves and the right player moved
        return (destination in self.squares[piece_square[0]][piece_square[1]].get_possible_moves() or castled) and \
            ((self.turn and self.squares[piece_square[0]][piece_square[1]].direction == -1) or
             (not self.turn and self.squares[piece_square[0]][piece_square[1]].direction == 1))

    def was_ep(self, piece_square: list[int], destination: list[int]) -> bool:  # checks if the move was an en
        # passant move
        return self.squares[piece_square[0]][piece_square[1]].name.upper() == "P" and destination == self.ep

    def move_piece_to_temporary_storage(self, piece_square: list[int], destination: list[int], castled: bool,
                                        castled_short: bool, eped: bool,
                                        storage: Piece) -> Piece:  # returns the piece that was captured, so it can
        # get assigned to a temporary storage
        if self.squares[destination[0]][
            destination[1]].name == "!" and not castled and not eped:  # case: no piece was captured
            self.squares[piece_square[0]][piece_square[1]] = self.squares[destination[0]][destination[1]]
            self.squares[destination[0]][destination[1]] = storage
            return No(0, 0, 0, 0, 0, 0)
        elif not castled and not eped:  # case: pieces was captured
            captured_storage = self.squares[destination[0]][destination[1]]
            self.squares[destination[0]][destination[1]].captured = True
            self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
            self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, self.window, 0, 0)
            return captured_storage
        elif castled_short:  # case: castled short
            self.squares[destination[0]][destination[1] + 1].move_piece_pos([piece_square[0], piece_square[1] + 1])
            self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
            self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, self.window, 0, 0)
            self.squares[piece_square[0]][piece_square[1] + 1] = self.squares[destination[0]][destination[1] + 1]
            self.squares[destination[0]][destination[1] + 1] = No(0, 0, 0, self.window, 0, 0)
            return No(0, 0, 0, self.window, 0, 0)
        elif eped:  # case:ep
            self.squares[piece_square[0]][piece_square[1]].move_piece_pos(destination)
            self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
            self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, self.window, 0, 0)
            captured_storage \
                = self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction] \
                [destination[1]]
            captured_storage.captured = True
            self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction][destination[1]] \
                = No(0, 0, 0, self.window, 0, 0)
            return captured_storage
        else:  # case: castled long
            self.squares[destination[0]][destination[1] - 2].move_piece_pos([piece_square[0], piece_square[1] - 1])
            self.squares[destination[0]][destination[1]] = self.squares[piece_square[0]][piece_square[1]]
            self.squares[piece_square[0]][piece_square[1]] = No(0, 0, 0, self.window, 0, 0)
            self.squares[piece_square[0]][piece_square[1] - 1] = self.squares[destination[0]][destination[1] - 2]
            self.squares[destination[0]][destination[1] - 2] = No(0, 0, 0, self.window, 0, 0)
            return No(0, 0, 0, self.window, 0, 0)

    def redo_move(self, piece_square: list[int], destination: list[int], captured_storage: Piece, storage: Piece,
                  eped: bool) -> None:
        self.squares[destination[0]][destination[1]].move_piece_pos(piece_square)
        self.squares[destination[0]][destination[1]] = captured_storage
        self.squares[destination[0]][destination[1]].captured = False
        if eped:
            captured_storage.captured = False
            self.squares[destination[0]][destination[1]].move_piece_pos(piece_square)
            self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction][
                destination[1]] = captured_storage
        self.squares[piece_square[0]][piece_square[1]] = storage

    def move_piece(self, piece_square, destination, promotion=False,
                   real=True) -> bool:  # method to move a piece on the
        castled = False
        castled_short = False
        self.get_legal_moves()
        eped = False
        if self.check_for_short_castle(piece_square, destination):
            castled = True
            castled_short = True
        elif self.check_for_long_castle(piece_square, destination):
            castled = True
        if not self.could_be_legal_move(piece_square, destination, castled):
            return False
        if self.was_ep(piece_square, destination):
            eped = True
        storage = self.squares[piece_square[0]][piece_square[1]]
        self.squares[piece_square[0]][piece_square[1]].move_piece_pos(destination)
        captured_storage = self.move_piece_to_temporary_storage(piece_square, destination, castled, castled_short,
                                                                eped, storage)
        illegal_move = self.in_check()  # needs to be checked inside here, since this method is also used during
        # the simulation of moves, e.g. to check if a move lands you in check
        if illegal_move or self.anchor:
            self.redo_move(piece_square, destination, captured_storage, storage, eped)
            if illegal_move:
                return False
            else:
                return True
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
                    promotion = Queen([destination[0], destination[1]],
                                      False, self.size, self.window,
                                      self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "r":
                    promotion = Rook([destination[0], destination[1]],
                                     False, self.size, self.window,
                                     self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "b":
                    promotion = Rook([destination[0], destination[1]],
                                     False, self.size, self.window,
                                     self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "n":
                    promotion = Knight([destination[0], destination[1]],
                                       False, self.size, self.window,
                                       self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "Q":
                    promotion = Queen([destination[0], destination[1]],
                                      True, self.size, self.window,
                                      self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "R":
                    promotion = Rook([destination[0], destination[1]],
                                     True, self.size, self.window,
                                     self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "B":
                    promotion = Bishop([destination[0], destination[1]],
                                       True, self.size, self.window,
                                       self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
                case "N":
                    promotion = Knight([destination[0], destination[1]],
                                       True, self.size, self.window,
                                       self.pos, False, self)
                    self.squares[destination[0]][destination[1]] = promotion
        if promotion is True:
            promotion = self.check_for_promotion()
        self.squares[destination[0]][destination[1]].moved = True
        if self.real_board and real:
            self.play_move_on_board(piece_square, destination, captured_storage, castled)
        self.turn = not self.turn
        self.played_moves += 1
        self.squares[destination[0]][destination[1]].first_moved = copy.deepcopy(self.played_moves)
        self.last_move = [piece_square, destination, captured_storage, promotion, eped]
        self.moves.append([piece_square, destination, captured_storage, promotion, eped])
        return True

    def update_last_move(self):  # sets the last move played
        if len(self.moves) > 0:
            self.last_move = self.moves[-1]

    def redo_last_move(self, last_move,
                       real=True):  # redoes the last played move on the digital board and redoes the last move
        # on the real board if real=True
        if len(self.moves) > 0:
            self.moves.pop()
        piece_square = last_move[0]
        destination = last_move[1]
        if self.squares[destination[0]][destination[1]].first_moved == self.played_moves:  # resets the moved value
            # important for castling
            # TODO: check if first_moved hat to be reset
            self.squares[destination[0]][destination[1]].moved = False
        captured = last_move[2]
        promotion = last_move[3]
        castled = False
        ep = last_move[4]
        if self.squares[destination[0]][destination[1]].name.lower() == "k" \
                and abs(piece_square[1] - destination[1]) == 2:
            castled = True
            if destination[1] == 6:
                self.squares[destination[0]][destination[1] + 1] = copy.copy(
                    self.squares[destination[0]][destination[1] - 1])
                self.squares[destination[0]][destination[1] - 1] = captured
                self.squares[destination[0]][destination[1] + 1].move_piece_pos([destination[0], destination[1] + 1])
                self.squares[destination[0]][destination[1] + 1].moved = False
            else:
                self.squares[destination[0]][destination[1] - 2] = copy.copy(
                    self.squares[destination[0]][destination[1] + 1])
                self.squares[destination[0]][destination[1] + 1] = captured
                self.squares[destination[0]][destination[1] - 2].move_piece_pos([destination[0], destination[1] - 2])
                self.squares[destination[0]][destination[1] - 2].moved = False

        if ep:
            self.ep = destination
            self.squares[piece_square[0]][piece_square[1]] = self.squares[destination[0]][destination[1]]
            self.squares[destination[0] - self.squares[destination[0]][destination[1]].direction][
                destination[1]] = captured
            captured.captured = False
            self.squares[piece_square[0]][piece_square[1]].move_piece_pos(piece_square)
        else:
            self.ep = [-1, -1]
            self.squares[piece_square[0]][piece_square[1]] = self.squares[destination[0]][destination[1]]
            self.squares[destination[0]][destination[1]] = captured
            captured.captured = False
            self.squares[piece_square[0]][piece_square[1]].move_piece_pos(piece_square)
        if promotion is not False:
            if self.squares[piece_square[0]][piece_square[1]].direction == -1:
                self.squares[piece_square[0]][piece_square[1]] = Pawn(piece_square,
                                                                      True, self.size,
                                                                      self.window, self.pos, False, self)
            else:
                self.squares[piece_square[0]][piece_square[1]] = Pawn(piece_square,
                                                                      False, self.size,
                                                                      self.window, self.pos, False, self)
        if self.real_board and real:
            self.redo_move_on_board(piece_square=piece_square, target_square=destination, captured=captured,
                                    castled=castled)
        if len(self.moves) > 0:
            self.last_move = self.moves[-1]
            self.played_moves -= 1
        else:
            self.last_move = None
        self.turn = not self.turn

    def find_played_move(self, other_board):  # TODO: rewrite for hall detection
        for i in self.squares:
            for j in i:
                if self.turn and j.direction == -1:
                    for k in j.get_possible_moves():
                        if self.move_piece(j.pos, k, real=False):
                            if self.compare_boards(other_board):
                                self.update_storage(self.last_move[2])
                                return True
                            self.redo_last_move(self.last_move, real=False)
                elif not self.turn and j.direction == 1:
                    for k in j.get_possible_moves():
                        if self.move_piece(j.pos, k, real=False):
                            if self.compare_boards(other_board):
                                self.update_storage(self.last_move[2])
                                return True
                            self.redo_last_move(self.last_move, real=False)
        return False

    def compare_boards(self, other_board):  # TODO: rewrite for detection
        for x, i in enumerate(self.squares):
            for y, j in enumerate(i):
                if not j.name == other_board[x][y]:
                    return False
        return True

    def highlight_last_move(self):  # TODO: ignore and write in App
        pass

    def board_to_string(self):
        board = [['!' for _ in range(8)] for _ in range(8)]
        for x, i in enumerate(self.squares):
            for y, j in enumerate(i):
                board[x][y] = j.name
        return board

    def draw_pieces(self):
        for row in self.squares:
            for i in row:
                i.draw_piece()

    def draw_storage(self, alignment, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        alignment = alignment
        size = self.size

        squares = [Square(pos_x, pos_y, (192, 192, 192), (204, 0, 0), None, size) for _ in range(16)]
        add_line = 0
        add_row = 0
        where_in_line = 1
        if alignment:
            condition = 2
        else:
            condition = 8
            alignment = True

        for square in squares:
            if where_in_line > condition:
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

    def in_check(self):
        def check() -> bool:
            if piece.name == "K":
                for move in self.get_legal_moves()[1]:
                    if piece.pos == move[1] and self.turn:
                        return True
            elif piece.name == "k":
                for move in self.get_legal_moves()[0]:
                    if piece.pos == move[1] and not self.turn:
                        return True

        for i in self.squares:
            for piece in i:
                if check():
                    return True
        return False

    def check_for_played_move(self):  # TODO: rewrite for hall detection
        self.find_played_move(self.piece_detector.check_for_pieces())

    def update_storage(self, piece):
        if piece is not False and not piece.name == "!":
            self.find_storage_pos(piece.name)

    def play_move_on_board(self, piece_square, target_square, captured=No(0, 0, 0, 0, 0, 0), castled=False,
                           player_move=False):
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

    def clear_real_board(self):  # TODO: rewrite
        for i in self.squares:
            for piece in i:
                if not piece.name == "!":
                    self.move_to_square(piece.pos)
                    self.remove_piece(piece.name)

    def setup_real_board(self, old_pos, new_pos):  # this looks like shit
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
        try:  # TODO: rewrite so there is no try/catch
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
                self.play_move_on_board([piece_pos[0] + 0.5, piece_pos[1] + 0.5],
                                        [piece_pos[0] + 0.5, target_square[1] + 0.5])
                self.play_move_on_board([piece_pos[0] + 0.5, target_square[1] + 0.5], [target_square[0] + 0.5,
                                                                                       target_square[1] + 0.5])
                self.play_move_on_board([target_square[0] + 0.5, target_square[1] + 0.5], target_square)
            else:
                self.play_move_on_board(piece_pos, [piece_pos[0] + 0.5, piece_pos[1] + 0.5])
                self.play_move_on_board([piece_pos[0] + 0.5, piece_pos[1] + 0.5],
                                        [piece_pos[0] + 0.5, target_square[1] + 0.5])
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

    def create_piece(self, new_piece: str, piece: Piece) -> Piece:
        if new_piece.upper() == "Q":
            return Queen([piece.pos[0], piece.pos[1]], piece.pos[0] == 0, self.size,
                         self.window,
                         self.pos, False, self)
        elif new_piece.upper() == "R":
            return Rook([piece.pos[0], piece.pos[1]], piece.pos[0] == 0, self.size,
                        self.window,
                        self.pos, False, self)
        elif new_piece.upper() == "N":
            return Knight([piece.pos[0], piece.pos[1]], piece.pos[0] == 0,
                          self.size, self.window,
                          self.pos, False, self)
        elif new_piece.upper() == "B":
            return Bishop([piece.pos[0], piece.pos[1]], piece.pos[0] == 0,
                          self.size, self.window,
                          self.pos, False, self)
        print("Invalid Input")
        new_piece = input("piece to promote into: ")
        return self.create_piece(new_piece, piece)

    def check_for_promotion(self):
        new_piece = No(0, 0, 0, self.window, 0, 0)
        for i in self.squares:
            for piece in i:
                if piece.name.upper() == "P" and (piece.pos[0] == 0 or piece.pos[0] == 7):
                    new_piece = input("piece to promote into: ")
                    new_piece = self.create_piece(new_piece, piece)
                    self.squares[piece.pos[0]][piece.pos[1]] = new_piece

        return new_piece

    def check_for_mate(self):
        if self.anchor:
            return True
        self.anchor = True
        if self.turn:
            for i in self.get_legal_moves()[0]:
                if self.move_piece(i[0], i[1]):
                    self.anchor = False
                    return False

        else:
            for i in self.get_legal_moves()[1]:
                if self.move_piece(i[0], i[1]):
                    self.anchor = False
                    return False
        self.anchor = False
        return True

    def print_board(self):
        for j in self.squares:
            row = []
            for i in j:
                row.append(i.name)
            print(f"{row}")

    def draw_board(self):
        pos_x = self.pos_x
        pos_y = self.pos_y
        alignment = self.alignment
        size = self.size

        squares = [Square(pos_x, pos_y, (192, 192, 192), (204, 0, 0), None, size) for _ in range(64)]
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
        self.squares = [[No(0, 0, 0, self.window, 0, 0) for _ in range(8)] for _ in range(8)]
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
        self.real = real_game
        self.clock = py.time.Clock()
        board_pos = config['STEPPER_STARTING_POS']
        self.sim_board = Board(None, True, board_pos[0], board_pos[1], self.window, real_board=False)
        self.simulation = Simulation(self.window, self.sim_board, Mouse(self.sim_board), self.clock)
        self.board = Board(None, True, board_pos[0], board_pos[1], self.window, stepper_x=self.simulation.stepper_x,
                           stepper_y=self.simulation.stepper_y,
                           magnet=self.simulation.magnet,
                           real_board=real_game)

        self.mouse = Mouse(self.board)

    def game_loop(self):
        pygame.display.set_caption("Chess")
        clock = self.clock
        run = True
        self.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        while run:
            clock.tick(30)
            self.window.fill((176, 196, 222))
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.simulation.draw()
            self.simulation.move_pieces()
            if self.board.check_for_mate():
                print('mate')
            pygame.display.update()

    @staticmethod
    def draw(image, pos_x, pos_y, window):
        window.blit(image, (pos_x, pos_y))

    def setup_board(self, setup, first_setup=False):
        self.board.set_up(setup, first_set_up=first_setup)
        self.sim_board.set_up(setup, False)

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
