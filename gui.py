
import pygame as py
import pygame.display
import sys
import play_against_stockfish
import Button
import puzzles
import guess_the_move
from arduino_communication import Stepper, Magnet
import pyfirmata

pygame.display.init()
font = py.font.SysFont('Comic Sans MS', 30)


class Gui:
    def __init__(self, real=False):
        self.real = real
        if self.real:
            self.board_1 = pyfirmata.Board("COM5")
            self.board_2 = pyfirmata.Board("COM4")
            self.stepper_x = Stepper(5, 2, True, second_dir_pin=6, board=self.board_1, board_2=self.board_2, reference_pin=5)
            self.stepper_y = Stepper(7, 4, True, board=self.board_1, board_2=self.board_2, reference_pin=7)
            self.magnet = Magnet(12 , board=self.board_1)
        else:
            self.magnet = False
            self.stepper_x = False
            self.stepper_y = False
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.buttons = [Button.Button(200, 200, 100, 200, self.window, "play"),
                        Button.Button(200, 600, 100, 200, self.window, "puzzles"),
                        Button.Button(200, 1000, 100, 200, self.window, "Rate-den-Zug")]

        self.loop()

    def loop(self):
        while True:
            self.window.fill((0, 0, 0))
            self.draw_buttons()
            self.check_buttons()
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            py.display.update()

    def draw_buttons(self):
        for i in self.buttons:
            i.draw_button()

    def check_buttons(self):
        if self.buttons[0].is_pressed():
            self.action_button_1(self)
        if self.buttons[1].is_pressed():
            self.action_button_2(self)
        if self.buttons[2].is_pressed():
            self.action_button_3(self)

    @staticmethod
    def action_button_1(self):
        play_against_stockfish.Play(stepper_x=self.stepper_x, stepper_y=self.stepper_y, magnet=self.magnet, real=self.real)

    @staticmethod
    def action_button_2(self):
        puzzles.Play(magnet=self.magnet, stepper_x=self.stepper_x, stepper_y=self.stepper_y, real=self.real, board=self.board_2)

    @staticmethod
    def action_button_3(self):
        guess_the_move.Play("white", magnet=self.magnet, stepper_x=self.stepper_x, stepper_y=self.stepper_y, real=self.real, board=self.board_2)


gui = Gui()
