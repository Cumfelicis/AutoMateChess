import game as g
import board_to_name
import name_to_board
from stockfish import Stockfish
import pygame as py
import pygame.display
import sys
import Button
import pandas as pd
import random
import pyfirmata
import time
import arduino_communication
import pyfirmata.util



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
class Player:
    def __init__(self):
        with open("rating.txt", "r") as file:
            self.rating = int(file.readline())

    def save_rating(self):
        with open("rating.txt", "w") as file:
            file.write(str(self.rating))

class Puzzle:
    def __init__(self, magnet=False, stepper_x=False, stepper_y=False):
        self.player = Player()
        self.df = pd.read_csv("lichess_db_puzzle.csv").sort_values("Rating").reset_index(drop=True)
        self.index = self.find_puzzle(0, len(self.df.index) - 1)
        self.rating = self.df["Rating"][self.index]
        print(self.df["Moves"][self.index])
        self.expectation = self.player.rating / 400 / (self.player.rating / 400 + self.rating / 400)
        self.fen = self.df["FEN"][self.index]
        self.moves = self.df["Moves"][self.index].split()
        self.move_index = 2
        self.solved = 1
        for i, _ in enumerate(self.moves):
            self.moves[i] = [board_to_name.board_to_name(self.moves[i][:2]),
                             board_to_name.board_to_name(self.moves[i][2:4])]

    def find_puzzle(self, lower, upper):
        if upper >= lower:
            index = int((upper + lower) / 2)
            rating = self.df["Rating"][index]
            if abs(self.player.rating - rating) < 100:
                return index
            elif rating > self.player.rating:
                return self.find_puzzle(lower, index - 1)
            else:
                return self.find_puzzle(index + 1, upper)
        return -1

    def new_puzzle(self):
        self.player.rating = int(self.player.rating + 32 * (self.solved - self.expectation))
        self.player.save_rating()
        self.index = self.find_puzzle(0, len(self.df.index) - 1) + random.randint(-10000, 10000)
        self.fen = self.df["FEN"][self.index]
        self.moves = self.df["Moves"][self.index].split()
        self.expectation = self.player.rating / 400 / (self.player.rating / 400 + 10 ** self.rating / 400)
        self.move_index = 2
        self.solved = 1
        for i, _ in enumerate(self.moves):
            self.moves[i] = [board_to_name.board_to_name(self.moves[i][:2]),
                             board_to_name.board_to_name(self.moves[i][2:4])]

    @staticmethod
    def save_rating(self, rating):
        with open("rating.txt", "w") as file:
            file.write(str(rating))


class Play:
    def __init__(self, magnet=False, stepper_x=False, stepper_y=False, real=False, led_red=False, led_green=False):
        self.puzzle = Puzzle()
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.strength = 100
        self.game = g.Game(self.window, real_game=real, magnet=magnet, stepper_x=stepper_x, stepper_y=stepper_y)
        self.game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", first_setup=True)
        self.test = g.Game(self.window)
        self.test.setup_board(self.puzzle.fen)
        stockfish.set_skill_level(int(self.strength))
        print(self.puzzle.fen)
        self.game.setup_board(self.puzzle.fen)
        self.colour = not self.game.get_players_move()
        print(self.colour)
        self.game.play_move(self.puzzle.moves[0][0], self.puzzle.moves[0][1])
        self.test.play_move(self.puzzle.moves[0][0], self.puzzle.moves[0][1])
        self.button = Button.Button(200, 1000, 100, 100, self.window, "exit")
        if real:
            self.green = led_green
            self.red = led_red
        self.loop()

    def loop(self):
        pygame.display.set_caption(f"playing against stockfish on level {self.strength}")
        clock = py.time.Clock()
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
            if self.colour != self.game.get_players_move():
                self.test.play_move(self.puzzle.moves[self.puzzle.move_index - 1][0]
                                    , self.puzzle.moves[self.puzzle.move_index - 1][1])
                if self.game.get_fen() == self.test.get_fen():
                    try:
                        self.game.play_move(self.puzzle.moves[self.puzzle.move_index][0],
                                            self.puzzle.moves[self.puzzle.move_index][1])
                        self.test.play_move(self.puzzle.moves[self.puzzle.move_index][0],
                                            self.puzzle.moves[self.puzzle.move_index][1])
                        self.puzzle.move_index += 2
                    except IndexError:
                        self.puzzle.new_puzzle()
                        self.game = g.Game(self.window)
                        self.test = g.Game(self.window)
                        self.test.setup_board(self.puzzle.fen)
                        self.colour = not self.game.get_players_move()
                        print(self.colour)
                        self.game.setup_board(self.puzzle.fen)
                        self.game.play_move(self.puzzle.moves[0][0], self.puzzle.moves[0][1])
                        self.test.play_move(self.puzzle.moves[0][0], self.puzzle.moves[0][1])
                else:
                    self.red.on()
                    self.game.redo_last_move()
                    self.puzzle.solved = 0
                    self.red.off()
                    self.green.on()

            pygame.display.update()

play = Play(magnet=magnet, stepper_x=stepper_x, stepper_y=stepper_y, real=True, led_green=led_green, led_red=led_red)
