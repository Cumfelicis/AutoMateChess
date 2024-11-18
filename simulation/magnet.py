import pygame.draw
from tests.config import config
from simulation.piece import SimNo


class SimMagnet:
    def __init__(self, pos, size, window, board):
        self.pos = pos
        self.size = size
        self.window = window
        self.board = board
        self.attached_piece = SimNo(0,0,0,0,0, 0)
        self.board_pos = board.pos
        self.board_size = board.size
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.blit_color = self.blue
        self.last_on = None

    def draw(self):
        pygame.draw.circle(self.window, self.blit_color, (
        config['STEPPER_STARTING_POS'][0] + self.pos[0], config['STEPPER_STARTING_POS'][1] + self.pos[1],), self.size)

    def get_coordinates(self, pos):
        x = round((pos[1] - self.board_pos[1]) / self.board_size - 0.25)
        y = round((pos[0] - self.board_pos[0]) / self.board_size - 0.25)
        return [x, y]

    def on(self):
        coordinates = self.get_coordinates((
        config['STEPPER_STARTING_POS'][0] + self.pos[0], config['STEPPER_STARTING_POS'][1] + self.pos[1]))
        if coordinates[0] < 0:
            self.attached_piece = self.board.white_storage[coordinates[1]][abs(coordinates[0]) - 1]
        elif coordinates [1] > 7:
            self.attached_piece = self.board.black_storage[coordinates[0]][coordinates[1] - 7]
        else:
            self.attached_piece = self.board.squares[coordinates[0]][coordinates[1]]
        self.last_on = coordinates
        self.attached_piece.attach(self)
        self.blit_color = self.red

    def off(self):
        coordinates = self.get_coordinates((
        config['STEPPER_STARTING_POS'][0] + self.pos[0], config['STEPPER_STARTING_POS'][1] + self.pos[1]))
        print(len(self.board.white_storage))
        if coordinates[0] < 0:
            self.board.white_storage[coordinates[1]][abs(coordinates[0]) - 1] = self.attached_piece
        elif coordinates [1] > 7:
            self.board.black_storage[coordinates[0]][coordinates[1] - 7] = self.attached_piece
        else:
            self.board.squares[coordinates[0]][coordinates[1]] = self.attached_piece
        self.attached_piece.detach(self)
        self.attached_piece = SimNo(0, 0, 0,0, 0, 0)
        self.blit_color = self.blue
        if self.last_on[0] < 0:
            self.board.white_storage[self.last_on[1]][abs(self.last_on[0]) - 1] = SimNo(0, 0, 0, 0, 0, 0)
        elif self.last_on[1] > 7:
            self.board.black_storage[self.last_on[0]][self.last_on[1] - 7] = SimNo(0, 0, 0, 0, 0, 0)
        else:
            self.board.squares[self.last_on[0]][self.last_on[1]] = SimNo(0, 0, 0, 0, 0, 0)


