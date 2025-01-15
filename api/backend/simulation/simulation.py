import pygame.display

from ..simulation.magnet import SimMagnet
from ..simulation.stepper import SimStepper, SimMultistepper
from ..simulation.piece import SimNo
from ..config import config
import pygame as py
import sys


class Simulation:
    def __init__(self, window, board, mouse, clock):
        self.window = window
        self.board = board
        self.mouse = mouse
        self.magnet = SimMagnet([0, 0], 10, self.window, self.board)
        self.clock = clock
        self.multi_stepper = SimMultistepper(self.clock, self.draw)
        self.stepper_x = SimStepper(True, self.magnet, self.clock, self.draw)
        self.stepper_y = SimStepper(False, self.magnet, self.clock, self.draw)
        self.multi_stepper.add_stepper(self.stepper_x)
        self.multi_stepper.add_stepper(self.stepper_y)
        self.dragging = SimNo(0, 0, 0, 0, 0, 0)
        self.first_drag = True

    def move_pieces(self):
        drag_old, drag_new = self.mouse.drag()
        if self.mouse.pressed:
            if self.first_drag:
                self.dragging = self.board.squares[self.mouse.mouse_pos_to_square()[0]][
                    self.mouse.mouse_pos_to_square()[1]]
                self.first_drag = False
            self.dragging.blit_pos = self.mouse.mouse.get_pos()

        if drag_old is not False and drag_new is not False:
            if self.board.squares[drag_new[0]][drag_new[1]].name != '!' and self.board.squares[drag_new[0]][
                drag_new[1]] != self.board.squares[drag_old[0]][drag_old[1]]:
                captured = self.board.squares[drag_new[0]][drag_new[1]]
                captured.captured = True
            self.board.squares[drag_old[0]][drag_old[1]] = SimNo(0, 0, 0, 0, 0, 0)


            self.board.squares[drag_new[0]][drag_new[1]] = self.dragging

            self.first_drag = True
            self.dragging = SimNo(0, 0, 0, 0, 0, 0)

    def simulation_loop(self):
        py.display.set_caption('simulation')
        run = True
        self.board.set_up("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        while run:
            self.clock.tick(30)
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
            self.draw()
            self.move_pieces()

    def draw(self):
        self.window.fill((0, 0, 0))
        self.board.draw_outline()
        self.board.draw_board()
        self.board.draw_storage(True, (
        config['STEPPER_STARTING_POS'][0] + 8 * config['BOARD_SQUARE_SIZE'], config['STEPPER_STARTING_POS'][1]))
        self.board.draw_storage(False, (
        config['STEPPER_STARTING_POS'][0], config['STEPPER_STARTING_POS'][1] - 2 * config['BOARD_SQUARE_SIZE']))
        self.board.draw_pieces()
        self.magnet.draw()

        py.display.update()
