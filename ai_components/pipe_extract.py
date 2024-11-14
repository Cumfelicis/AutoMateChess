import subprocess
import numpy as np
import csv
from backend.utils.pgn_to_board import game_from_lines
from backend.chess.game import Game
import zstandard as zstd

counter = 0
sets = 0
pos_written = 0
header = ['time_control', 'position', 'time_spent', 'elo', 'remaining_times']
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
                encoded_board[row][col][idx] = 1
    return encoded_board


def manage_csv_writing(zst_file_path, max_positions_per_file=100000):
    global counter, sets, pos_written, csv_file
    time_control = []
    positions = []
    times = []
    elo = []
    remaining_times = []

    game_info_found = False

    with zstd.open(zst_file_path, 'r') as file:
        game = []
        for line in file:
            if line == "\n" and not game_info_found:
                game_info_found = True
                continue
            if line == "\n" and game_info_found:
                try:
                    time_control, positions, times, elo, remaining_times = game_from_lines(game, game_object)
                except Exception as e:
                    print('BUG!!!!!!!', e)
                    print(game)
                turn = True
                for position, time, remaining_time in zip(positions, times, remaining_times):
                    if pos_written >= max_positions_per_file or pos_written == 0:
                        print(sets)
                        if csv_file is not None:
                            csv_file.close()

                        # Open a new CSV file
                        csv_file_path = f'D:/csv/{sets}.csv'
                        csv_file = open(csv_file_path, mode='w', newline='')
                        writer = csv.writer(csv_file)

                        # Write the header
                        writer.writerow(header)

                        sets += 1
                        pos_written = 0

                    # Write the row to the CSV file
                    if turn:
                        writer.writerow([time_control, encode_chessboard(position).tolist(), time, elo[0],
                                        remaining_time])
                    else:
                        writer.writerow([time_control, encode_chessboard(position).tolist(), time, elo[1],
                                        remaining_time])
                    turn = not turn
                    pos_written += 1

                # Reset the game list for the next game
                game = []
                game_info_found = False
                continue

            # Append the current line to the game list
            game.append(line)

        # Close the last file if openpipe_extract.py
        if csv_file is not None:
            csv_file.close()


# Path to the .zst file
zst_file_path = 'D:/lichess_db_standard_rated_2023-04.pgn.zst'
if __name__ == '__main__':
    # Process and write the games to CSV
    manage_csv_writing(zst_file_path)
