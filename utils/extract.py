import pandas as pd
import numpy as np
import pgn_to_board as ptb
import csv
from utils.pgn_to_board import game_from_lines
from chess.game import Game


counter = 0
sets = 0
pos_written = 0
header = ['time_control', 'position', 'time_spent']
csv_file = None
game_object = Game(real_game=False)


def encode_chessboard(board):
    piece_to_index = {
        'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
        'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
    }
    encoded_board = np.zeros(shape=(8, 8, 12))
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '!':
                idx = piece_to_index[piece]
                encoded_board[row, col, idx] = 1
    return encoded_board


with open(path, 'r') as file:
    game = []
    for line in file.readlines():
        if line == "\n":
            time_control, positions, times = game_from_lines(game, game_object)
            print(time_control)
            for position, time in positions, times:
                if pos_written >= 100.000 or pos_written == 0:
                    if file is not None:
                        file.close()

                    csv_file_path = f'D:/csv/{sets}.csv'
                    csv_file = open(csv_file_path, mode='a', newline='')
                    writer = csv.writer(file)

                    writer.writerow(header)

                    sets += 1
                    pos_written = 0

                writer.writerow([time_control, encode_chessboard(position), time])
                pos_written += 1
            game = []
            continue
        game.append(line)
