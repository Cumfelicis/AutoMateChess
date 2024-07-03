import piece_detector
import game
import pygame as py
import sys

window = py.display.set_mode((1536, 810), py.RESIZABLE)

detector = piece_detector.PieceDetector()
game = game.Game()

clock = py.time.Clock()
game.setup_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
run = True
while run:
    clock.tick(60)
    window.fill((176, 196, 222))
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
    game.draw_board()
    game.move_pieces()
    game.board.check_for_played_move()
    if game.is_checkmate():
        run = False

    py.display.update()
