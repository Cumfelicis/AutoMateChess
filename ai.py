import tensorflow
from tensorflow.python import keras
from keras import layers, models
import matplotlib as plt
import numpy as np


BATCH_SIZE = 5
NUM_EPOCHS = 5
FEATURE_SIZE = 50  # Max amount of moves, that can be "thought" about
DECISION_INPUT_SIZE = 3  # rating, time left, inkrement
PIECE_MAPPING = {"!": 0,
                 "p": 1,
                 "n": 2,
                 "b": 3,
                 "r": 4,
                 "q": 5,
                 "k": 6,
                 "P": 7,
                 "N": 8,
                 "B": 9,
                 "R": 10,
                 "Q": 11,
                 "K": 12} # Values of the Pieces


# Board representation CNN
def build_cnn_model():
    model = models.Sequential()
    model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(8, 8, 13)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    return model


# Sequential Information LSTM
def build_rnn_model():
    model = models.Sequential()
    model.add(layers.LSTM(128, input_shape=(None, FEATURE_SIZE)))
    return model


# Time Management Decision Fully Connected Layers
def build_decision_model():
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_dim=DECISION_INPUT_SIZE))
    model.add(layers.Dense(1, activation='linear'))  # Regression task
    return model


# Output Layer
def build_output_layer():
    model = models.Sequential()
    model.add(layers.Dense(1, activation='linear'))  # Classification task
    return model


# create the models
cnn_model = build_cnn_model()
rnn_model = build_rnn_model()
decision_model = build_decision_model()
output_model = build_output_layer()

# Define input layers for each model
cnn_input = layers.Input(shape=(8, 8, 13))  # 13-channel input representing the chessboard
rnn_input = layers.Input(shape=(None, FEATURE_SIZE))  # Variable-length input for sequential information
decision_input = layers.Input(shape=(DECISION_INPUT_SIZE,))  # other factors influencing the decision


# Connect the models
cnn_output = cnn_model(cnn_input)
rnn_output = rnn_model(rnn_input)


# Concatenate the outputs
merged_output = layers.concatenate([cnn_output, rnn_output, decision_input])
final_output = layers.Dense(1, activation='linear')(merged_output)  # Regression task

# Compile the final model
model = models.Model(inputs=[cnn_input, rnn_input, decision_input], outputs=final_output)
model.compile(optimizer='adam', loss='mean_squared_error')


# Example data preparation
def encode_board(board):
    encoded_board = np.zeros((8, 8), dtype=np.int32)
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            encoded_board[x][y] = PIECE_MAPPING[j.name]
    return encoded_board


def encode_moves(moves):
    encoded_moves = np.zeros(FEATURE_SIZE, dtype=np.int32)
    for x, move in enumerate(moves):
        encoded_moves[x] = 1
        if x == FEATURE_SIZE - 1:
            break
    return encoded_moves


def encode_decision_input(info):
    encoded_info = np.zeros(DECISION_INPUT_SIZE, dtype=np.int32)
    for i in range(DECISION_INPUT_SIZE):
        encoded_info[i] = info[i]


# extract Training Data
cnn_input_data = [np.zeros((8, 8), dtype=np.int32)]
rnn_input_data = []
decision_input_data = []
output_data = []

print(model.summary( ))
# Train the model
model.fit([cnn_input_data, rnn_input_data, decision_input_data], output_data, epochs=NUM_EPOCHS,
          batch_size=BATCH_SIZE, use_multiprocessing=True, validation_split=0.01)
