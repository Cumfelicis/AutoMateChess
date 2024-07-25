from chess.pieces import Piece
from config import config

from copy import copy

import pygame as py

py.font.init()
my_font = py.font.SysFont('Comic Sans MS', 30)


class SimPiece(Piece):
    def __init__(self, pos, color, size, window, board_pos, name, board, captured):
        super().__init__(pos, color, size, window, board_pos, name, board, captured)
        self.attached = False
        self.blit_pos = self.get_pos()

    def attach(self, magnet):
        self.attached = True
        self.blit_pos = magnet.pos

    def detach(self, magnet):
        self.attached = False
        self.blit_pos = (
            config['STEPPER_STARTING_POS'][0] + self.blit_pos[0] - 0.25 * config['BOARD_SQUARE_SIZE'],
            config['STEPPER_STARTING_POS'][1] + self.blit_pos[1] - 0.25 * config['BOARD_SQUARE_SIZE'])

    def draw_piece(self):
        if not self.captured and self.attached:
            text_surface = my_font.render(self.name, False, self.blit_colour)
            self.window.blit(text_surface, (
                config['STEPPER_STARTING_POS'][0] + self.blit_pos[0] - 0.25 * config['BOARD_SQUARE_SIZE'],
                config['STEPPER_STARTING_POS'][1] + self.blit_pos[1] - 0.25 * config['BOARD_SQUARE_SIZE']))
        elif not self.captured:
            text_surface = my_font.render(self.name, False, self.blit_colour)
            self.window.blit(text_surface, self.blit_pos)

    def get_coordinates(self, pos):
        x = round((pos[1] - self.board_pos[1] + 1) / self.size - 0.25)
        y = round((pos[0] - self.board_pos[0] + 1) / self.size - 0.25)
        return [x, y]


class SimPawn(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(SimPawn, self).__init__(pos, colour, size, window, board_pos, "p", captured, board)

    def get_possible_moves(self):
        if (self.direction == -1 and self.pos[0] == 0) or (self.direction == 1 and self.pos[0] == 7):
            return []

        moves = []
        if self.direction == -1:
            if self.pos[0] == 6:
                if self.board.squares[self.pos[0] + 2 * self.direction][self.pos[1]].name.lower() == "!" and \
                        self.board.squares[self.pos[0] + self.direction][self.pos[1]].name.lower() == "!":
                    moves.append([self.pos[0] + 2 * self.direction, self.pos[1]])  # double step

            if self.board.squares[self.pos[0] + self.direction][self.pos[1]].name.lower() == "!":
                moves.append([self.pos[0] + self.direction, self.pos[1]])  # single step
            if self.pos[1] > 0:
                if self.board.squares[self.pos[0] + self.direction][self.pos[1] + self.direction].name \
                        in self.black_pieces or \
                        [self.pos[0] + self.direction, self.pos[1] + self.direction] == self.board.ep:
                    moves.append(
                        [self.pos[0] + self.direction, self.pos[1] + self.direction])  # capture left
            if 7 > self.pos[1]:
                if self.board.squares[self.pos[0] + self.direction][self.pos[1] - self.direction].name \
                        in self.black_pieces or \
                        [self.pos[0] + self.direction, self.pos[1] - self.direction] == self.board.ep:
                    moves.append(
                        [self.pos[0] + self.direction, self.pos[1] - self.direction])  # capture right
        else:
            if self.pos[0] == 1:
                if self.board.squares[self.pos[0] + 2 * self.direction][self.pos[1]].name.lower() == "!" and \
                        self.board.squares[self.pos[0] + self.direction][self.pos[1]].name.lower() == "!":
                    moves.append([self.pos[0] + 2 * self.direction, self.pos[1]])  # double step
            if self.board.squares[self.pos[0] + self.direction][self.pos[1]].name.lower() == "!":
                moves.append([self.pos[0] + self.direction, self.pos[1]])  # single step
            if self.pos[1] > 0:
                if self.board.squares[self.pos[0] + self.direction][self.pos[1] - self.direction].name \
                        in self.white_pieces or \
                        [self.pos[0] + self.direction, self.pos[1] - self.direction] == self.board.ep:
                    moves.append(
                        [self.pos[0] + self.direction, self.pos[1] - self.direction])  # capture left
            if 7 > self.pos[1]:
                if self.board.squares[self.pos[0] + self.direction][self.pos[1] + self.direction].name \
                        in self.white_pieces or \
                        [self.pos[0] + self.direction, self.pos[1] + self.direction] == self.board.ep:
                    moves.append(
                        [self.pos[0] + self.direction, self.pos[1] + self.direction])  # capture right
        return moves


class SimKing(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(SimKing, self).__init__(pos, colour, size, window, board_pos, "k", captured, board)
        self.moved = False

    def get_possible_moves(self):
        moves = []
        # up left
        if not (self.pos[0] - 1 < 0 or self.pos[1] - 1 < 0):
            if self.board.squares[self.pos[0] - 1][self.pos[1] - 1].name not in self.pieces:
                moves.append([self.pos[0] - 1, self.pos[1] - 1])
        # up right
        if not (self.pos[0] - 1 < 0 or self.pos[1] + 1 > 7):
            if self.board.squares[self.pos[0] - 1][self.pos[1] + 1].name not in self.pieces:
                moves.append([self.pos[0] - 1, self.pos[1] + 1])
        # up
        if not (self.pos[0] - 1 < 0):
            if self.board.squares[self.pos[0] - 1][self.pos[1]].name not in self.pieces:
                moves.append([self.pos[0] - 1, self.pos[1]])
        # down left
        if not (self.pos[0] + 1 > 7 or self.pos[1] - 1 < 0):
            if self.board.squares[self.pos[0] + 1][self.pos[1] - 1].name not in self.pieces:
                moves.append([self.pos[0] + 1, self.pos[1] - 1])
        # down right
        if not (self.pos[0] + 1 > 7 or self.pos[1] + 1 > 7):
            if self.board.squares[self.pos[0] + 1][self.pos[1] + 1].name not in self.pieces:
                moves.append([self.pos[0] + 1, self.pos[1] + 1])
        # down
        if not (self.pos[0] + 1 > 7):
            if self.board.squares[self.pos[0] + 1][self.pos[1]].name not in self.pieces:
                moves.append([self.pos[0] + 1, self.pos[1]])
        # left
        if not (self.pos[1] - 1 < 0):
            if self.board.squares[self.pos[0]][self.pos[1] - 1].name not in self.pieces:
                moves.append([self.pos[0], self.pos[1] - 1])
        # right
        if not (self.pos[1] + 1 > 7):
            if self.board.squares[self.pos[0]][self.pos[1] + 1].name not in self.pieces:
                moves.append([self.pos[0], self.pos[1] + 1])
        if self.direction == -1:
            # short castle white
            if not self.moved and self.pos[1] + 3 < 8:
                if self.moved or self.board.squares[self.pos[0]][self.pos[1] + 3].moved:
                    self.board.white_castle_short_generally = False
                else:
                    self.board.white_castle_short_generally = True
                if not (not self.board.squares[self.pos[0]][self.pos[1] + 3].moved and
                        (self.board.squares[self.pos[0]][self.pos[1] + 2].name == "!" and
                         self.board.squares[self.pos[0]][self.pos[1] + 1].name == "!")):
                    self.board.white_castle_short = False
                else:
                    self.board.white_castle_short = True
                if self.board.white_castle_short:
                    moves.append([self.pos[0], self.pos[1] + 2])
            else:
                self.board.white_castle_long = False
                self.board.white_castle_short_generally = False
            # long castle white
            if not self.moved and self.pos[1] - 4 >= 0:
                if self.moved or self.board.squares[self.pos[0]][self.pos[1] - 4].moved:
                    self.board.white_castle_long_generally = False
                else:
                    self.board.white_castle_long_generally = True
                if not (not self.board.squares[self.pos[0]][self.pos[1] - 4].moved and
                        (self.board.squares[self.pos[0]][self.pos[1] - 2].name == "!" and
                         self.board.squares[self.pos[0]][self.pos[1] - 1].name == "!" and self.board.squares[self.pos[0]][
                             self.pos[1] - 3].name == "!")):
                    self.board.white_castle_long = False
                else:
                    self.board.white_castle_long = True
                if self.board.white_castle_long:
                    moves.append([self.pos[0], self.pos[1] - 2])
            else:
                self.board.white_castle_long = False
                self.board.white_castle_long_generally = False
        if self.direction == 1:
            # short castle black
            if not self.moved and self.pos[1] + 3 < 8:
                if self.moved or self.board.squares[self.pos[0]][self.pos[1] + 3].moved:
                    self.board.black_castle_short_generally = False
                else:
                    self.board.black_castle_short_generally = True
                if not (not self.board.squares[self.pos[0]][self.pos[1] + 3].moved and
                        (self.board.squares[self.pos[0]][self.pos[1] + 2].name == "!" and
                         self.board.squares[self.pos[0]][self.pos[1] + 1].name == "!")):
                    self.board.black_castle_short = False
                else:
                    self.board.black_castle_short = True
                if self.board.black_castle_short:
                    moves.append([self.pos[0], self.pos[1] + 2])
            else:
                self.board.black_castle_long = False
                self.board.black_castle_short_generally = False
            # long castle black
            if not self.moved and self.pos[1] - 4 >= 0:
                if self.moved or self.board.squares[self.pos[0]][self.pos[1] - 4].moved:
                    self.board.black_castle_long_generally = False
                else:
                    self.board.black_castle_long_generally = True
                if not (not self.board.squares[self.pos[0]][self.pos[1] - 4].moved and
                        (self.board.squares[self.pos[0]][self.pos[1] - 2].name == "!" and
                         self.board.squares[self.pos[0]][self.pos[1] - 1].name == "!" and self.board.squares[self.pos[0]][
                             self.pos[1] - 3].name == "!")):
                    self.board.black_castle_long_castle_long = False
                else:
                    self.board.black_castle_long = True
                if self.board.black_castle_long:
                    moves.append([self.pos[0], self.pos[1] - 2])
            else:
                self.board.black_castle_long = False
                self.board.black_castle_long_generally = False
        return moves


class SimQueen(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(SimQueen, self).__init__(pos, colour, size, window, board_pos, "q", captured, board)

    def get_possible_moves(self):
        moves = []
        # all left up diagonal moves
        for i in range(1, self.pos[0] + 1):
            if self.pos[0] - i >= 0 and self.pos[1] - i >= 0:
                if self.board.squares[self.pos[0] - i][self.pos[1] - i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] - i][self.pos[1] - i].name in self.not_pieces:
                    moves.append([self.pos[0] - i, self.pos[1] - i])
                    break
                else:
                    moves.append([self.pos[0] - i, self.pos[1] - i])
        # all right down diagonal moves
        for i in range(1, 8 - self.pos[0]):
            if self.pos[0] + i <= 7 and self.pos[1] + i <= 7:
                if self.board.squares[self.pos[0] + i][self.pos[1] + i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] + i][self.pos[1] + i].name in self.not_pieces:
                    moves.append([self.pos[0] + i, self.pos[1] + i])
                    break
                else:
                    moves.append([self.pos[0] + i, self.pos[1] + i])
        # all right up diagonal moves
        for i in range(1, 8 - self.pos[1]):
            if self.pos[0] - i >= 0 and self.pos[1] + i <= 7:
                if self.board.squares[self.pos[0] - i][self.pos[1] + i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] - i][self.pos[1] + i].name in self.not_pieces:
                    moves.append([self.pos[0] - i, self.pos[1] + i])
                    break
                else:
                    moves.append([self.pos[0] - i, self.pos[1] + i])
        # all left down diagonal moves
        for i in range(1, 8 - self.pos[0]):
            if self.pos[0] + i <= 7 and self.pos[1] - i >= 0:
                if self.board.squares[self.pos[0] + i][self.pos[1] - i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] + i][self.pos[1] - i].name in self.not_pieces:
                    moves.append([self.pos[0] + i, self.pos[1] - i])
                    break
                else:
                    moves.append([self.pos[0] + i, self.pos[1] - i])
            # all moves left
        for i in range(1, self.pos[1] + 1):
            if self.board.squares[self.pos[0]][self.pos[1] - i].name in self.pieces:
                break
            elif self.board.squares[self.pos[0]][self.pos[1] - i].name in self.not_pieces:
                moves.append([self.pos[0], self.pos[1] - i])
                break
            else:
                moves.append([self.pos[0], self.pos[1] - i])
            # all right moves
        for i in range(self.pos[1] + 1, 8):
            if self.board.squares[self.pos[0]][i].name in self.pieces:
                break
            elif self.board.squares[self.pos[0]][i].name in self.not_pieces:
                moves.append([self.pos[0], i])
                break
            else:
                moves.append([self.pos[0], i])
            # all front moves
        for i in range(1, self.pos[0] + 1):
            if self.board.squares[self.pos[0] - i][self.pos[1]].name in self.pieces:
                break
            elif self.board.squares[self.pos[0] - i][self.pos[1]].name in self.not_pieces:
                moves.append([self.pos[0] - i, self.pos[1]])
                break
            else:
                moves.append([self.pos[0] - i, self.pos[1]])
            # all back moves
        for i in range(self.pos[0] + 1, 8):
            if self.board.squares[i][self.pos[1]].name in self.pieces:
                break
            elif self.board.squares[i][self.pos[1]].name in self.not_pieces:
                moves.append([i, self.pos[1]])
                break
            else:
                moves.append([i, self.pos[1]])
        return moves


class SimBishop(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(SimBishop, self).__init__(pos, colour, size, window, board_pos, "b", captured, board)

    def get_possible_moves(self):
        moves = []

        # all left up diagonal moves
        for i in range(1, self.pos[0] + 1):
            if self.pos[0] - i >= 0 and self.pos[1] - i >= 0:
                if self.board.squares[self.pos[0] - i][self.pos[1] - i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] - i][self.pos[1] - i].name in self.not_pieces:
                    moves.append([self.pos[0] - i, self.pos[1] - i])
                    break
                else:
                    moves.append([self.pos[0] - i, self.pos[1] - i])
        # all right down diagonal moves
        for i in range(1, 8 - self.pos[0]):
            if self.pos[0] + i <= 7 and self.pos[1] + i <= 7:
                if self.board.squares[self.pos[0] + i][self.pos[1] + i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] + i][self.pos[1] + i].name in self.not_pieces:
                    moves.append([self.pos[0] + i, self.pos[1] + i])
                    break
                else:
                    moves.append([self.pos[0] + i, self.pos[1] + i])
        # all right up diagonal moves
        for i in range(1, 8 - self.pos[1]):
            if self.pos[0] - i >= 0 and self.pos[1] + i <= 7:
                if self.board.squares[self.pos[0] - i][self.pos[1] + i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] - i][self.pos[1] + i].name in self.not_pieces:
                    moves.append([self.pos[0] - i, self.pos[1] + i])
                    break
                else:
                    moves.append([self.pos[0] - i, self.pos[1] + i])
        # all left down diagonal moves
        for i in range(1, 8 - self.pos[0]):
            if self.pos[0] + i <= 7 and self.pos[1] - i >= 0:
                if self.board.squares[self.pos[0] + i][self.pos[1] - i].name in self.pieces:
                    break
                elif self.board.squares[self.pos[0] + i][self.pos[1] - i].name in self.not_pieces:
                    moves.append([self.pos[0] + i, self.pos[1] - i])
                    break
                else:
                    moves.append([self.pos[0] + i, self.pos[1] - i])

        return moves


class SimKnight(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(SimKnight, self).__init__(pos, colour, size, window, board_pos, "n", captured, board)

    def get_possible_moves(self):
        moves = []
        # up left
        if not (self.pos[0] - 2 < 0 or self.pos[1] - 1 < 0):
            if self.board.squares[self.pos[0] - 2][self.pos[1] - 1].name not in self.pieces:
                moves.append([self.pos[0] - 2, self.pos[1] - 1])
        # up right
        if not (self.pos[0] - 2 < 0 or self.pos[1] + 1 > 7):
            if self.board.squares[self.pos[0] - 2][self.pos[1] + 1].name not in self.pieces:
                moves.append([self.pos[0] - 2, self.pos[1] + 1])
        # left up
        if not (self.pos[0] - 1 < 0 or self.pos[1] - 2 < 0):
            if self.board.squares[self.pos[0] - 1][self.pos[1] - 2].name not in self.pieces:
                moves.append([self.pos[0] - 1, self.pos[1] - 2])
        # left down
        if not (self.pos[0] + 1 > 7 or self.pos[1] - 2 < 0):
            if self.board.squares[self.pos[0] + 1][self.pos[1] - 2].name not in self.pieces:
                moves.append([self.pos[0] + 1, self.pos[1] - 2])
        # right up
        if not (self.pos[0] - 1 < 0 or self.pos[1] + 2 > 7):
            if self.board.squares[self.pos[0] - 1][self.pos[1] + 2].name not in self.pieces:
                moves.append([self.pos[0] - 1, self.pos[1] + 2])
            pass
        # right down
        if not (self.pos[0] + 1 > 7 or self.pos[1] + 2 > 7):
            if self.board.squares[self.pos[0] + 1][self.pos[1] + 2].name not in self.pieces:
                moves.append([self.pos[0] + 1, self.pos[1] + 2])
        # down right
        if not (self.pos[0] + 2 > 7 or self.pos[1] + 1 > 7):
            if self.board.squares[self.pos[0] + 2][self.pos[1] + 1].name not in self.pieces:
                moves.append([self.pos[0] + 2, self.pos[1] + 1])
        # down left
        if not (self.pos[0] + 2 > 7 or self.pos[1] - 1 < 0):
            if self.board.squares[self.pos[0] + 2][self.pos[1] - 1].name not in self.pieces:
                moves.append([self.pos[0] + 2, self.pos[1] - 1])
        return moves


class SimRook(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(SimRook, self).__init__(pos, colour, size, window, board_pos, "r", captured, board)
        self.moved = False

    def get_possible_moves(self):
        moves = []
        # all moves left
        for i in range(1, self.pos[1] + 1):
            if self.board.squares[self.pos[0]][self.pos[1] - i].name in self.pieces:
                break
            elif self.board.squares[self.pos[0]][self.pos[1] - i].name in self.not_pieces:
                moves.append([self.pos[0], self.pos[1] - i])
                break
            else:
                moves.append([self.pos[0], self.pos[1] - i])
        # all right moves
        for i in range(self.pos[1] + 1, 8):
            if self.board.squares[self.pos[0]][i].name in self.pieces:
                break
            elif self.board.squares[self.pos[0]][i].name in self.not_pieces:
                moves.append([self.pos[0], i])
                break
            else:
                moves.append([self.pos[0], i])
        # all front moves
        for i in range(1, self.pos[0] + 1):
            if self.board.squares[self.pos[0] - i][self.pos[1]].name in self.pieces:
                break
            elif self.board.squares[self.pos[0] - i][self.pos[1]].name in self.not_pieces:
                moves.append([self.pos[0] - i, self.pos[1]])
                break
            else:
                moves.append([self.pos[0] - i, self.pos[1]])
        # all back moves
        for i in range(self.pos[0] + 1, 8):
            if self.board.squares[i][self.pos[1]].name in self.pieces:
                break
            elif self.board.squares[i][self.pos[1]].name in self.not_pieces:
                moves.append([i, self.pos[1]])
                break
            else:
                moves.append([i, self.pos[1]])
        return moves


class SimNo(SimPiece):
    def __init__(self, pos, colour, size, window, board_pos, board):
        super(SimNo, self).__init__(pos, colour, size, window, board_pos, "!", True, board)
        self.pos = [0, 0]
        self.moved = False

    def draw_piece(self):
        pass

    def get_pos(self):
        pass
