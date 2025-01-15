from ..chess import game as g
from ..utils.board_to_name import board_to_name
from stockfish import Stockfish
import pygame as py
import pygame.display
import sys
from ..utils.Button import Button
from ..arduino_communication import *
import pyfirmata
import time
import numpy as np
from ..ai_components.ai import load_model, predict
from pathlib import Path
from .module import Module

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


class Play(Module):
    def __init__(self, fen, time, increment, stepper_x=False, stepper_y=False, magnet=False, real=False):
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.strength = 50  # input("input stockfish strength: ")
        self.colour = "white"  # input("input colour: ")
        stockfish.set_skill_level(int(self.strength))
        current_dir = Path(__file__).parent
        architecture_path = current_dir / '../ai_components/architecture234.json'
        architecture_path = architecture_path.resolve()
        weight_path = current_dir / '../ai_components/weights234.h5'
        weight_path = weight_path.resolve()
        self.model = load_model(architecture_path, weight_path)
        self.time_remaining = 600
        self.fen = fen
        self.time = time
        self.incerement = increment
        if self.colour == "white":
            self.colour = True
        else:
            self.colour = False
        self.game = g.Game(self.window, stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet, real_game=real)
        print("test")
        self.button = Button(200, 1000, 100, 100, self.window, "exit")

        # self.loop()

    def on_start(self, config):
        self.color = config['color']

    def on_end(self, result):
        return super().on_end(result)

    def loop(self):
        pygame.display.set_caption(f"playing against stockfish on level {self.strength}")
        clock = py.time.Clock()
        self.game.setup_board(self.fen)
        last_move = self.game.get_last_move()
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
            self.game.board.find_played_move(list(map(lambda e: list(map(lambda x: x.name, e)), self.game.simulation.board.squares))) # TODO: remove and move to on_player_move
            self.button.draw_button()
            if self.game.get_last_move() != last_move:
                last_move = self.game.get_last_move()
                yield last_move
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
            delay = predict(self.game.board.board_to_string(),
                            np.array([self.time, self.incerement, 2000, self.time_remaining], dtype=np.float32), self.model)
            delay = int(delay[0][0])
            delay += np.random.normal(delay, self.time_remaining * 0.1)
            print(delay)
            self.time_remaining -= delay
            time.sleep(delay if delay >= 0 else 0)
            self.game.play_move(self.move_to_board(best_move)[0],
                                self.move_to_board(best_move)[1])

    def on_player_move(self, move):
        self.time_remaining = move['time']
        self.game.board.find_played_move()
        
    def on_robot_move(self, move):
        return super().on_robot_move(move)

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
    play.loop()
