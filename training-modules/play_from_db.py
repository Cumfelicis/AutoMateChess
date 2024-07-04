import game as g
import pgn_to_board
import pygame as py
import pygame.display
import sys
import Button
import time
import arduino_communication
import pyfirmata, pyfirmata.util


board_1 = pyfirmata.Arduino("COM5")
board_2 = pyfirmata.Arduino("COM3")

stepper_x = arduino_communication.Stepper(5, 2, True, second_dir_pin=6, board=board_1, board_2=board_2, reference_pin=1, alternative_reference_pin=2)
stepper_y = arduino_communication.Stepper(7, 4, False, board=board_1, board_2=board_2, reference_pin=0)
it = pyfirmata.util.Iterator(board_2)
it.start()
magnet = arduino_communication.Magnet(12, board_1, board_2)
magnet.off()
time.sleep(1)


pygame.display.init()


class Play:
    def __init__(self, stepper_x=False, stepper_y=False, magnet=False, real_game=False):
        self.window = pygame.display.set_mode((1536, 810), pygame.RESIZABLE)
        self.game = g.Game(self.window, stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet, real_game=real_game)
        self.button = Button.Button(200, 1000, 100, 100, self.window, "exit")
        self.moves = pgn_to_board.pgn_to_game()

        self.loop()

    def loop(self):
        clock = py.time.Clock()
        self.game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", first_setup=True)
        run = True
        i = 0
        while run:
            clock.tick(60)
            self.window.fill((176, 196, 222))
            for event in py.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.draw_board()
            self.button.draw_button()
            keys = py.key.get_pressed()
            if keys[py.K_LEFT]:
                if i > 1:
                    i -= 1
                    self.game.redo_last_move()
                    self.game.draw_board()
                    self.game.move_pieces()
                    self.button.draw_button()
                    time.sleep(0.2)
            elif keys[py.K_RIGHT]:
                if i < len(self.moves[0]) - 1:
                    print(self.moves[0][i])

                    print(self.game.get_players_move())
                    print(self.game.play_move(self.moves[0][i][0][0], self.moves[0][i][0][1], self.moves[0][i][0][2]))
                    self.game.draw_board()
                    self.game.move_pieces()
                    self.button.draw_button()
                    i += 1
                    time.sleep(0.2)
            if self.button.is_pressed():
                run = False
                self.game.reset_board()
            if self.game.is_checkmate():
                run = False
                self.game.reset_board()

            pygame.display.update()


play = Play(stepper_x=stepper_x, stepper_y=stepper_y, magnet=magnet, real_game=True)
