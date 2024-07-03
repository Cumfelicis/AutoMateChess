import game as g
import board_to_name
from stockfish import Stockfish
import pygame as py
import pygame.display
import sys
import Button
import arduino_communication
import pyfirmata
import time

pygame.display.init()
stockfish = Stockfish(
    path="C:/Users/flixg/PycharmProjects/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
board_1 = pyfirmata.Arduino("COM5")
board_2 = pyfirmata.Arduino("COM3")

stepper_x = arduino_communication.Stepper(5, 2, True, second_dir_pin=6, board=board_1, board_2=board_2, reference_pin=1, alternative_reference_pin=2)
stepper_y = arduino_communication.Stepper(7, 4, False, board=board_1, board_2=board_2, reference_pin=0)
it = pyfirmata.util.Iterator(board_2)
it.start()
magnet = arduino_communication.Magnet(12, board_1, board_2)
magnet.off()
time.sleep(1)



class Play:
    def __init__(self, stepper_x=False, stepper_y=False, magnet=False, real=False):
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.strength = 50  # input("input stockfish strength: ")
        self.colour = "white"  # input("input colour: ")
        stockfish.set_skill_level(int(self.strength))
        if self.colour == "white":
            self.colour = True
        else:
            self.colour = False
        self.game = g.Game(self.window, stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet,  real_game=real)
        print("test")
        self.button = Button.Button(200, 1000, 100, 100, self.window, "exit")

        self.loop()

    def loop(self):
        pygame.display.set_caption(f"playing against stockfish on level {self.strength}")
        clock = py.time.Clock()
        self.game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", first_setup=True)
        run = True
        while run:
            clock.tick(60)
            self.window.fill((176, 196, 222))
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.draw_board()
            self.game.move_pieces()
            self.button.draw_button()
            if self.button.is_pressed():
                run = False
                self.game.reset_board()
            if self.game.is_checkmate():
                run = False
                self.game.reset_board()
            self.stockfish_play_move()

            pygame.display.update()

    def stockfish_play_move(self):
        if not self.game.is_my_move(self.colour):
            stockfish.set_fen_position(self.game.get_fen())
            best_move = stockfish.get_best_move()
            print(best_move)
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
                return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move),
                        move[-1].lower]
            else:
                return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move),
                        move[-1].upper()]

        return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move)]

play = Play(stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet, real=True)