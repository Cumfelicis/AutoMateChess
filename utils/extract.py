import pandas as pd
import numpy as np
import pgn_to_board as ptb

while True:
    game = 0
    try:
        with open(f"D:\moves\game{game}", "a") as file:
            moves, time_control = ptb.pgn_to_game(f"D:\games\game{game}")
            try:
                file.write(f"{time_control[0]}, {time_control[1]}")
            except IndexError:
                pass
            for i in moves:
                for j in i:
                    file.write(f"{j[0][0]}{j[1][0]}, {j[1]}")
            game += 1
            continue
    except FileNotFoundError:
        break

