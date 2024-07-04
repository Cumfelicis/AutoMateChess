import game as g
import board_to_name
from stockfish import Stockfish
import pygame as py
import pygame.display
import sys
import Button

pygame.display.init()
stockfish = Stockfish(
    path="C:/Users/flixg/PycharmProjects/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")

strength_mapping = {1: ,
                    2: ,
                    3: ,
                    4: ,
                    5: ,
                    6: ,
                    7: ,
                    8: ,
                    9:
}


class Play:
    def __init__(self):
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.strength = input("input stockfish strength: ")
        self.colour = input("input colour: ")
        stockfish.set_skill_level(int(self.strength))
        if self.colour == "white":
            self.colour = True
        else:
            self.colour = False
        self.game = g.Game(self.window)
        self.button = Button.Button(200, 1000, 100, 100, self.window, "exit")

        self.loop()

    def loop(self):
        pygame.display.set_caption(f"playing against stockfish on level {self.strength}")
        clock = py.time.Clock()
        self.game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
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
            if self.game.is_checkmate():
                run = False
            self.stockfish_play_move()

            pygame.display.update()

    def stockfish_play_move(self):
        if not self.game.is_my_move(self.colour):
            stockfish.set_fen_position(self.game.get_fen())
            best_move = stockfish.get_best_move()
            self.game.play_move(self.move_to_board(self, best_move)[0],
                                self.move_to_board(self, best_move)[1])

    @staticmethod
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
        return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move)]