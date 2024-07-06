import numpy
import numpy as np
import mediapipe as mp
import cv2

mp_hand = mp.solutions.hands


class Camera:
    def __init__(self):
        self.address = "https://172.20.10.2:8080/video"
        self.video = cv2.VideoCapture(0)
        self.video.open(self.address)

    def get_frame(self):
        check, frame = self.video.read()
        cv2.waitKey(1)
        return frame


class PieceDetector:
    def __init__(self):
        self.camera = Camera()
        self.upper_pos = [620, 267]
        self.lower_pos = [1270, 900]
        self.square_size = [(self.lower_pos[0] - self.upper_pos[0]) / 8, (self.lower_pos[1] - self.upper_pos[1]) / 8]
        self.squares = [[[int(self.upper_pos[0] + (self.square_size[0] * (0.5 + j))), int(self.upper_pos[1] +
                                                                                          (self.square_size[1] * (
                                                                                                      0.5 + i)))] for j
                         in range(8)] for i in range(8)]
        print(self.squares)
        self.hand = mp_hand.Hands()

    def check_for_pieces(self):
        print("checking for pieces")
        try:
            frame = self.camera.get_frame()
            hand = self.hand.process(np.flip(np.array(frame), 2))
            board = [[0 for _ in range(8)] for _ in range(8)]
            if hand.multi_hand_landmarks:
                return [[0 for _ in range(8)] for _ in range(8)]
            for x, i in enumerate(self.squares):
                for y, j in enumerate(i):
                    rgb = frame[j[1]][j[0]]
                    if (abs(int(rgb[0]) - int(rgb[1])) + abs(int(rgb[0]) - int(rgb[2])) + abs(
                            int(rgb[1]) - int(rgb[2]))) > 100 and int(rgb[2]) > rgb[1] and int(rgb[2]) > rgb[0]:
                        board[x][y] = 1
                    elif (abs(int(rgb[0]) - int(rgb[1])) + abs(int(rgb[0]) - int(rgb[2])) + abs(
                            int(rgb[1]) - int(rgb[2]))) > 90 and int(rgb[0]) > rgb[1] and int(rgb[0]) > rgb[1]:
                        board[x][y] = 2
                    else:
                        board[x][y] = 0
            print(board)
            return board
        except numpy.AxisError:
            return [[0 for _ in range(8)] for _ in range(8)]




