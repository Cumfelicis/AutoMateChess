import backend.chess.game as g
from backend.utils.board_to_name import board_to_name
from stockfish import Stockfish
import pygame as py
import pygame.display
import sys
from backend.utils.Button import Button
import backend.arduino_communication
import pyfirmata
import time
import numpy as np
from ai_components.ai import load_model, predict

pygame.display.init()

stockfish = Stockfish(
    path="C:/Users/flixg/PycharmProjects/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")

'''
board_1 = pyfirmata.Arduino("COM5")
board_2 = pyfirmata.Arduino("COM3")

stepper_x = arduino_communication.Stepper(5, 2, True, second_dir_pin=6, board=board_1, board_2=board_2, reference_pin=1, alternative_reference_pin=2)
stepper_y = arduino_communication.Stepper(7, 4, False, board=board_1, board_2=board_2, reference_pin=0)
it = pyfirmata.util.Iterator(board_2)
it.start()
magnet = arduino_communication.Magnet(12, board_1, board_2)
magnet.off()
time.sleep(1)
'''


class Play:
    def __init__(self, stepper_x=False, stepper_y=False, magnet=False, real=False):
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.strength = 50  # input("input stockfish strength: ")
        self.colour = "white"  # input("input colour: ")
        stockfish.set_skill_level(int(self.strength))
        self.model = load_model("D:/models/architecture234.json", "D:/models/weights234.h5")
        self.time_remaining = 600
        if self.colour == "white":
            self.colour = True
        else:
            self.colour = False
        self.game = g.Game(self.window, stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet, real_game=real)
        print("test")
        self.button = Button(200, 1000, 100, 100, self.window, "exit")

        # self.loop()

    def loop(self):
        pygame.display.set_caption(f"playing against stockfish on level {self.strength}")
        clock = py.time.Clock()
        self.game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", first_setup=True)
        run = True
        while run:
            clock.tick(30)
            self.window.fill((176, 196, 222))
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.simulation.draw()
            self.game.simulation.move_pieces()
            self.game.board.find_played_move(self.game.simulation.board.board_to_string())
            self.button.draw_button()
            if self.button.is_pressed():
                run = False
                self.game.reset_board()
            if self.game.is_checkmate():
                run = False
                self.game.reset_board()
            self.stockfish_play_move()
            print

            pygame.display.update()

    def stockfish_play_move(self):
        if not self.game.is_my_move(self.colour):
            stockfish.set_fen_position(self.game.get_fen())
            best_move = stockfish.get_best_move()
            delay = predict(self.game.board.board_to_string(),
                            np.array([600, 0, 2000, self.time_remaining], dtype=np.float32), self.model)
            delay = int(delay[0][0])
            print(delay)
            self.time_remaining -= delay
            time.sleep(delay)
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
                return [board_to_name(first_move), board_to_name(second_move),
                        move[-1].lower]
            else:
                return [board_to_name(first_move), board_to_name(second_move),
                        move[-1].upper()]

        return [board_to_name(first_move), board_to_name(second_move)]

if __name__ == '__main__':
    print('das ist nicht richtig so')
    play = Play(real=True)
