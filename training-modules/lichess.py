import berserk
import game as g
import board_to_name
import pygame as py
import pygame.display
import sys
import Button
import arduino_communication
import name_to_board as ntb
import pyfirmata, pyfirmata.util
import time

pygame.display.init()
with open("C:/Users/flixg/Documents/lichessToken.txt") as token:
    session = berserk.TokenSession(token.readline())
client = berserk.Client(session=session)


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
        self.game = g.Game(self.window, stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet,  real_game=real)
        print("test")
        self.button = Button.Button(200, 1000, 100, 100, self.window, "exit")

        self.loop()

    def loop(self):
        clock = py.time.Clock()
        self.game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", first_setup=True)
        run = True
        while run:
            state = client.games.get_ongoing()[0]
            clock.tick(60)
            self.window.fill((176, 196, 222))
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.draw_board()
            self.button.draw_button()
            if self.button.is_pressed():
                run = False
            if self.game.is_checkmate():
                run = False
            self.lichess_play_move(state)

            pygame.display.update()

    def lichess_play_move(self, state):
        if state["isMyTurn"] is True:
            print(state)
            if len(state["lastMove"]) > 0:
                last_move = self.move_to_board(state["lastMove"])
                print(last_move)
                if len(last_move) > 2:
                    self.game.board.move_piece(last_move[0], last_move[1], promotion=last_move[2])
                else:
                    self.game.board.move_piece(last_move[0], last_move[1])
            if self.game.move_pieces() is True:
                client.board.make_move(state["fullId"], self.board_to_move(self.game.get_last_move()))

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
            if self.game.is_my_move(False):
                return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move),
                        move[-1].lower()]
            else:
                return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move),
                        move[-1].upper()]

        return [board_to_name.board_to_name(first_move), board_to_name.board_to_name(second_move)]

    @staticmethod
    def board_to_move(move):
        uci = ntb.name_to_board(str(move[0])) +  ntb.name_to_board(str(move[1]))
        if move[3] is not False:
            uci += move[3].lower()
        return uci


play = Play(stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet, real=True)
