import pygame as py

py.font.init()
my_font = py.font.SysFont('Comic Sans MS', 30)


class Piece:
    def __init__(self, pos, colour, size, window, board_pos, name, captured, board):
        self.moved = True
        self.pos = pos
        self.board_pos = board_pos
        self.size = size
        self.name = name.lower()
        self.blit_colour = (0, 0, 0)
        self.board = board
        self.first_moved = False
        self.white_pieces = ["K", "Q", "B", "N", "R", "P"]
        self.black_pieces = ["k", "q", "b", "n", "r", "p"]
        if colour:
            self.colour = (255, 255, 255)
            self.blit_colour = (255, 255, 255)
            self.direction = -1
            self.name = self.name.upper()
            self.pieces = self.white_pieces
            self.not_pieces = self.black_pieces
        else:
            self.colour = (0, 0, 0)
            self.direction = 1
            self.pieces = self.black_pieces
            self.not_pieces = self.white_pieces
        self.captured = captured
        self.window = window

    def move_piece_rpos(self, new_pos):
        self.pos = new_pos

    def get_pos(self):
        x = self.board_pos[0] + self.size * (self.pos[1] + 0.25)
        y = self.board_pos[1] + self.size * (self.pos[0] + 0.25)
        return [x, y]

    def draw_piece(self):
        if not self.captured:
            text_surface = my_font.render(self.name, False, self.blit_colour)
            self.window.blit(text_surface, self.get_pos())

    def get_possible_moves(self):
        return []


class Pawn(Piece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(Pawn, self).__init__(pos, colour, size, window, board_pos, "p", captured, board)

    def get_possible_moves(self):
        moves = []
        if self.direction == -1:
            if self.pos[0] == 6:
                if self.board.squares[self.pos[0] + 2 * self.direction][self.pos[1]].name.lower() == "!":
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
                if self.board.squares[self.pos[0] + 2 * self.direction][self.pos[1]].name.lower() == "!":
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


class King(Piece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(King, self).__init__(pos, colour, size, window, board_pos, "k", captured, board)
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
        # short castle white
        if self.direction == -1 and not self.moved and self.pos[1] + 3 < 8:
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
        # long castle white
        if self.direction == -1 and not self.moved and self.pos[1] - 4 >= 0:
            if self.moved or self.board.squares[self.pos[0]][self.pos[1] - 4].moved:
                self.board.white_castle_long_generally = False
            else:
                self.board.white_castle_long_generally = True
            if not (not self.board.squares[self.pos[0]][self.pos[1] - 4].moved and
                    (self.board.squares[self.pos[0]][self.pos[1] - 2].name == "!" and
                     self.board.squares[self.pos[0]][self.pos[1] - 1].name == "!")):
                self.board.white_castle_long = False
            else:
                self.board.white_castle_long = True
            if self.board.white_castle_long:
                moves.append([self.pos[0], self.pos[1] - 2])
        # short castle black
        if self.direction == 1 and not self.moved and self.pos[1] + 3 < 8:
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
        # long castle black
        if self.direction == 1 and not self.moved and self.pos[1] - 4 >= 0:
            if self.moved or self.board.squares[self.pos[0]][self.pos[1] - 4].moved:
                self.board.black_castle_long_generally = False
            else:
                self.board.black_castle_long_generally = True
            if not (not self.board.squares[self.pos[0]][self.pos[1] - 4].moved and
                    (self.board.squares[self.pos[0]][self.pos[1] - 2].name == "!" and
                     self.board.squares[self.pos[0]][self.pos[1] - 1].name == "!")):
                self.board.black_castle_long_castle_long = False
            else:
                self.board.black_castle_long = True
            if self.board.black_castle_long:
                moves.append([self.pos[0], self.pos[1] - 2])
        return moves


class Queen(Piece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(Queen, self).__init__(pos, colour, size, window, board_pos, "q", captured, board)

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


class Bishop(Piece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(Bishop, self).__init__(pos, colour, size, window, board_pos, "b", captured, board)

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


class Knight(Piece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(Knight, self).__init__(pos, colour, size, window, board_pos, "n", captured, board)

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


class Rook(Piece):
    def __init__(self, pos, colour, size, window, board_pos, captured, board):
        super(Rook, self).__init__(pos, colour, size, window, board_pos, "r", captured, board)
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


class No(Piece):
    def __init__(self, pos, colour, size, window, board_pos, board):
        super(No, self).__init__(pos, colour, size, window, board_pos, "!", True, board)
        self.pos = [0, 0]
