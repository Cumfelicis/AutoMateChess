import cv2
import time

import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageFilter

print("test2")

address = "http://192.168.178.122:8080/video"
video = cv2.VideoCapture(0)
video.open(address)
upper_pos = [40, 60]
lower_pos = [921, 905]
board = [[False for _ in range(8)] for _ in range(8)]
square_size = [(lower_pos[0] - upper_pos[0]) / 8, (lower_pos[1] - upper_pos[1]) / 8]
squares = [[[int(upper_pos[0] + (square_size[0] * (0.5 + j))), int(upper_pos[1] +
                                                                                          (square_size[1] * (
                                                                                                      0.5 + i)))] for j
                         in range(8)] for i in range(8)]
print(f"squares: {squares}")
check, frame = video.read()

start = time.time()
for x, i in enumerate(squares):
    for y, j in enumerate(i):
        rgb = frame[j[1]][j[0]]
        if (abs(int(rgb[0]) - int(rgb[1])) + abs(int(rgb[0]) - int(rgb[2])) + abs(int(rgb[1]) - int(rgb[2]))) > 100:
            board[x][y] = 1
        else:
            board[x][y] = 0


end = time.time()
print(end - start)
print(board)
'''
yellow = (
int((int(frame[squares[0][0][1]][squares[0][0][0]][0]) + int(frame[squares[0][7][1]][squares[0][7][0]][0])) / 2),
int((int(frame[squares[0][0][1]][squares[0][0][0]][1]) + int(frame[squares[0][7][1]][squares[0][7][0]][1])) / 2),
int((int(frame[squares[0][0][1]][squares[0][0][0]][2]) + int(frame[squares[0][7][1]][squares[0][7][0]][2])) / 2))
dark_blue = (
int((int(frame[squares[7][0][1]][squares[7][1][0]][0]) + int(frame[squares[7][7][1]][squares[7][6][0]][0])) / 2),
int((int(frame[squares[7][0][1]][squares[7][1][0]][1]) + int(frame[squares[7][7][1]][squares[7][6][0]][1])) / 2),
int((int(frame[squares[7][0][1]][squares[7][1][0]][2]) + int(frame[squares[7][7][1]][squares[7][6][0]][2])) / 2))
light_brown = (
int((int(frame[squares[0][1][1]][squares[0][1][0]][0]) + int(frame[squares[0][6][1]][squares[0][6][0]][0])) / 2),
int((int(frame[squares[0][1][1]][squares[0][1][0]][1]) + int(frame[squares[0][6][1]][squares[0][6][0]][1])) / 2),
int((int(frame[squares[0][1][1]][squares[0][1][0]][2]) + int(frame[squares[0][6][1]][squares[0][6][0]][2])) / 2))
orange = (
int((int(frame[squares[0][2][1]][squares[0][0][0]][0]) + int(frame[squares[0][5][1]][squares[0][5][0]][0])) / 2),
int((int(frame[squares[0][2][1]][squares[0][0][0]][1]) + int(frame[squares[0][5][1]][squares[0][5][0]][1])) / 2),
int((int(frame[squares[0][2][1]][squares[0][0][0]][2]) + int(frame[squares[0][5][1]][squares[0][5][0]][2])) / 2))
pink = (
int((int(frame[squares[7][0][1]][squares[7][0][0]][0]) + int(frame[squares[7][7][1]][squares[7][7][0]][0])) / 2),
int((int(frame[squares[7][0][1]][squares[7][0][0]][1]) + int(frame[squares[7][7][1]][squares[7][7][0]][1])) / 2),
int((int(frame[squares[7][0][1]][squares[7][0][0]][2]) + int(frame[squares[7][7][1]][squares[7][7][0]][2])) / 2))
dark_brouwn = (
int((int(frame[squares[7][1][1]][squares[7][1][0]][0]) + int(frame[squares[7][6][1]][squares[7][6][0]][0])) / 2),
int((int(frame[squares[7][1][1]][squares[7][1][0]][1]) + int(frame[squares[7][6][1]][squares[7][6][0]][1])) / 2),
int((int(frame[squares[7][1][1]][squares[7][1][0]][2]) + int(frame[squares[7][6][1]][squares[7][6][0]][2])) / 2))
medium_green = (
int((int(frame[squares[7][2][1]][squares[7][0][0]][0]) + int(frame[squares[7][5][1]][squares[7][5][0]][0])) / 2),
int((int(frame[squares[7][2][1]][squares[7][0][0]][1]) + int(frame[squares[7][5][1]][squares[7][5][0]][1])) / 2),
int((int(frame[squares[7][2][1]][squares[7][0][0]][2]) + int(frame[squares[7][5][1]][squares[7][5][0]][2])) / 2))
brown = tuple(frame[squares[7][4][1]][squares[7][4][0]])
light_blue = tuple(frame[squares[7][3][1]][squares[7][3][0]])
light_green = tuple(frame[squares[0][4][1]][squares[0][4][0]])
dark_green = tuple(frame[squares[0][3][1]][squares[0][3][0]])
dark_red = (
int((int(frame[squares[6][0][1]][squares[6][0][0]][0]) + int(frame[squares[6][1][1]][squares[6][1][0]][0]) + int(frame[squares[6][2][1]][squares[6][2][0]][0]) + int(frame[squares[6][3][1]][squares[6][3][0]][0]) + int(frame[squares[6][4][1]][squares[6][4][0]][0]) + int(frame[squares[6][5][1]][squares[6][5][0]][0]) + int(frame[squares[6][6][1]][squares[6][6][0]][0]) + int(frame[squares[6][7][1]][squares[6][7][0]][0])) / 8),
int((int(frame[squares[6][0][1]][squares[6][0][0]][1]) + int(frame[squares[6][1][1]][squares[6][1][0]][1]) + int(frame[squares[6][2][1]][squares[6][2][0]][1]) + int(frame[squares[6][3][1]][squares[6][3][0]][1]) + int(frame[squares[6][4][1]][squares[6][4][0]][1]) + int(frame[squares[6][5][1]][squares[6][5][0]][1]) + int(frame[squares[6][6][1]][squares[6][6][0]][1]) + int(frame[squares[6][7][1]][squares[6][7][0]][1])) / 8),
int((int(frame[squares[6][0][1]][squares[6][0][0]][2]) + int(frame[squares[6][1][1]][squares[6][1][0]][2]) + int(frame[squares[6][2][1]][squares[6][2][0]][2]) + int(frame[squares[6][3][1]][squares[6][3][0]][2]) + int(frame[squares[6][4][1]][squares[6][4][0]][2]) + int(frame[squares[6][5][1]][squares[6][5][0]][2]) + int(frame[squares[6][6][1]][squares[6][6][0]][2]) + int(frame[squares[6][7][1]][squares[6][7][0]][2])) / 8))
bordaux = (
int((int(frame[squares[1][0][1]][squares[1][0][0]][0]) + int(frame[squares[1][1][1]][squares[1][1][0]][0]) + int(frame[squares[1][2][1]][squares[1][2][0]][0]) + int(frame[squares[1][3][1]][squares[1][3][0]][0]) + int(frame[squares[1][4][1]][squares[1][4][0]][0]) + int(frame[squares[1][5][1]][squares[1][5][0]][0]) + int(frame[squares[1][6][1]][squares[1][6][0]][0]) + int(frame[squares[1][7][1]][squares[1][7][0]][0])) / 8),
int((int(frame[squares[1][0][1]][squares[1][0][0]][1]) + int(frame[squares[1][1][1]][squares[1][1][0]][1]) + int(frame[squares[1][2][1]][squares[1][2][0]][1]) + int(frame[squares[1][3][1]][squares[1][3][0]][1]) + int(frame[squares[1][4][1]][squares[1][4][0]][1]) + int(frame[squares[1][5][1]][squares[1][5][0]][1]) + int(frame[squares[1][6][1]][squares[1][6][0]][1]) + int(frame[squares[1][7][1]][squares[1][7][0]][1])) / 8),
int((int(frame[squares[1][0][1]][squares[1][0][0]][2]) + int(frame[squares[1][1][1]][squares[1][1][0]][2]) + int(frame[squares[1][2][1]][squares[1][2][0]][2]) + int(frame[squares[1][3][1]][squares[1][3][0]][2]) + int(frame[squares[1][4][1]][squares[1][4][0]][2]) + int(frame[squares[1][5][1]][squares[1][5][0]][2]) + int(frame[squares[1][6][1]][squares[1][6][0]][2]) + int(frame[squares[1][7][1]][squares[1][7][0]][2])) / 8))
colours = {
    medium_green: "B",  # medium green 0
    brown: "K",  # brown 1
    light_blue: "Q",  # light blue 2
    pink: "R",  # pink 3,
    dark_red: "P",  # dark red 4
    dark_blue: "N",  #  dark blue 5
    orange: "b",  # orange 6
    light_green: "k",  # light green 7
    dark_green: "q",  # dark green 8
    light_brown: "n",  # li ght brown 9
    yellow: "r",  # yellow 10
    bordaux: "p",  # bordaux 11
}
print(colours)

print(bordaux)

print(colours[bordaux])
for i in colours:
    print(i, colours[i])


def piece_to_colour(colour):
    for i in range(colour[0] - 15, colour[0] + 15):
        for j in range(colour[1] - 15, colour[1] + 15):
            for k in range(colour[2] - 15, colour[2] + 15):
                try:
                    return colours[tuple([i, j, k])]
                except KeyError:
                    pass
    return "!"
'''