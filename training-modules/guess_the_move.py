import pygame as py
import pygame.display
import game as g
import board_to_name as btn
import pgn_to_board
import sys
from stockfish import Stockfish
import Button
import pyfirmata.util
import time
import arduino_communication

pygame.display.init()
stockfish = Stockfish(
    path="C:/Users/flixg/PycharmProjects/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")

board_1 = pyfirmata.Arduino("COM5")
board_2 = pyfirmata.Arduino("COM3")

stepper_x = arduino_communication.Stepper(5, 2, True, second_dir_pin=6, board=board_1, board_2=board_2, reference_pin=1, alternative_reference_pin=2)
stepper_y = arduino_communication.Stepper(7, 4, False, board=board_1, board_2=board_2, reference_pin=0)
led_red = arduino_communication.Led(3, board_2)
led_green = arduino_communication.Led(4, board_2)
it = pyfirmata.util.Iterator(board_2)
it.start()
magnet = arduino_communication.Magnet(12, board_1, board_2)
magnet.off()
time.sleep(1)


class Play:
    def __init__(self, colour, real=False, stepper_x=False, stepper_y=False, magnet=False, led_green=False, led_red=False):
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.strength = 100
        self.colour = colour
        stockfish.set_skill_level(int(self.strength))
        self.moves = pgn_to_board.pgn_to_game()
        if self.colour == "white":
            self.colour = True
        else:
            self.colour = False
        self.game = g.Game(self.window, real_game=real, stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet)
        self.verify = g.Game(self.window)
        self.button = Button.Button(200, 1000, 100, 100, self.window, "exit")
        self.button2 = Button.Button(200, 1250, 100, 100, self.window, "back")
        if real:
            self.green = led_green
            self.red = led_red

        self.loop()

    def loop(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        pygame.display.set_caption(f"playing against stockfish on level {self.strength}")
        clock = py.time.Clock()
        self.game.setup_board(fen, first_setup=True)
        self.verify.setup_board(fen)
        in_wrong_line = False
        back_fen = fen
        run = True
        i = 0
        fill_colour = (0, 255, 0)
        if self.colour:
            self.verify.play_move(self.moves[i][0][0][0], self.moves[i][0][0][1], self.moves[i][0][0][2])
            i += 1
        while run:
            clock.tick(60)
            self.window.fill(fill_colour)
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.draw_board()
            self.button2.draw_button()
            self.game.move_pieces()
            self.button.draw_button()
            if self.button.is_pressed():
                run = False
                self.game.reset_board()
            if self.button2.is_pressed():
                self.game.setup_board(back_fen)
                fill_colour = (0, 255, 0)
                in_wrong_line = False
                self.red.off()
                self.green.on()
            if self.game.is_checkmate():
                run = False
                self.game.reset_board()
            if not self.game.is_my_move(self.colour):
                if self.game.get_fen() == self.verify.get_fen():
                    print(self.moves[0][i])
                    self.game.play_move(self.moves[0][i][0][0], self.moves[0][i][0][1], self.moves[0][i][0][2])
                    self.verify.play_move(self.moves[0][i][0][0], self.moves[0][i][0][1], self.moves[0][i][0][2])
                    i += 1
                    self.verify.play_move(self.moves[0][i][0][0], self.moves[0][i][0][1], self.moves[0][i][0][2])
                    i += 1
                else:
                    if not in_wrong_line:
                        self.green.off()
                        self.red.on()
                        fill_colour = (255, 0, 0)
                        storage = self.game.get_last_move()
                        self.game.redo_last_move()
                        back_fen = self.game.get_fen()
                        self.game.play_move(storage[0], storage[1], storage[3])
                        in_wrong_line = True
                    self.stockfish_play_move()

            pygame.display.update()

    def stockfish_play_move(self):
        if not self.game.is_my_move(self.colour):
            stockfish.set_fen_position(self.game.get_fen())
            best_move = stockfish.get_best_move()
            self.game.play_move(self.move_to_board(best_move)[0],
                                self.move_to_board(best_move)[1])

    def move_to_board(self, move):
        first_move = ""
        second_move = ""
        on_first_move = True
        count = 0
        for i in move:
            if on_first_move:
                first_move += i
            else:
                second_move += i
            count += 1
            if count > 1:
                on_first_move = False
        if move[-1].isalpha():
            second_move = second_move[:-1]
            if self.colour:
                return [btn.board_to_name(first_move), btn.board_to_name(second_move),
                        move[-1].lower]
            else:
                return [btn.board_to_name(first_move), btn.board_to_name(second_move),
                        move[-1].upper()]

        return [btn.board_to_name(first_move), btn.board_to_name(second_move)]

play=Play(magnet=magnet, stepper_x=stepper_x, stepper_y=stepper_y, led_green=led_green, led_red=led_red)