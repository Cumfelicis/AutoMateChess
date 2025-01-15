import tensorflow
from tensorflow.python import keras
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
from .load_training_data import load_data
from .pipe_extract import encode_chessboard

BATCH_SIZE = 1000
NUM_EPOCHS = 5
DECISION_INPUT_SIZE = 4  # starting time, increment, elo, remaining time
PIECE_MAPPING = {
    "p": 0,
    "n": 1,
    "b": 2,
    "r": 3,
    "q": 4,
    "k": 5,
    "P": 6,
    "N": 7,
    "B": 8,
    "R": 9,
    "Q": 10,
    "K": 11}  # channel of the Pieces


# Board representation CNN
def build_cnn_model():
    model = models.Sequential()
    model.add(layers.Conv2D(128, (3, 3), activation='relu', input_shape=(8, 8, 12), padding='same'))
    model.add(layers.MaxPooling2D((2, 2), 2))
    model.add(build_dense_block(12, 32))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2), 2))
    model.add(build_dense_block(12, 32))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2), 2))
    model.add(build_dense_block(12, 32))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.Flatten())
    # model.add(layers.Dense())
    return model


def build_dense_block(num_layers, growth_rate):
    model = models.Sequential()
    for _ in range(num_layers):
        model.add(build_conv_block(growth_rate))
    return model


def build_conv_block(growth_rate):
    model = models.Sequential()
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.Conv2D(growth_rate, (3, 3), padding='same'))

    return model


def build_transition_block(filters):
    model = models.Sequential()
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.Conv2D(filters, (1, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    return model



'''
# Sequential Information LSTM
def build_rnn_model():
    model = models.Sequential()
    model.add(layers.LSTM(128, input_shape=(None, FEATURE_SIZE)))
    return model
'''


# Time Management Decision Fully Connected Layers
def build_decision_model():
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_dim=DECISION_INPUT_SIZE))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(8, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))  # Regression task
    return model


# Output Layer
def build_output_layer():
    model = models.Sequential()
    model.add(layers.Dense(1, activation='linear'))  # Classification task
    return model

def build_model():
    cnn_model = build_cnn_model()
    #  rnn_model = build_rnn_model()
    decision_model = build_decision_model()
    output_model = build_output_layer()

    # Define input layers for each model
    cnn_input = layers.Input(shape=(8, 8, 12))  # 12-channel input representing the chessboard
    #  rnn_input = layers.Input(shape=(None, FEATURE_SIZE))  # Variable-length input for sequential information
    decision_input = layers.Input(shape=DECISION_INPUT_SIZE)  # other factors influencing the decision

    # Connect the models
    cnn_output = cnn_model(cnn_input)
    #  rnn_output = rnn_model(rnn_input)

    # Concatenate the outputs
    merged_output = layers.concatenate([cnn_output, decision_input])
    final_output = layers.Dense(1, activation='linear')(merged_output)  # Regression task

    # Compile the final model
    model = models.Model(inputs=[cnn_input, decision_input], outputs=final_output)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


if __name__ == '__main__':
    lowest_loss = 100_000
    loss = []
    val_loss = []
    # create the models
    model = build_model()

    # model.load_weights(f'D:/models/weights{73}.h5')


    # Example data preparation
    def encode_board(board):
        encoded_board = np.zeros((8, 8), dtype=np.int32)
        for x, i in enumerate(board):
            for y, j in enumerate(i):
                encoded_board[x][y] = PIECE_MAPPING[j.name]
        return encoded_board


    print(model.summary())
    [print(i.shape, i.dtype) for i in model.inputs]
    [print(o.shape, o.dtype) for o in model.outputs]
    [print(l.name, l.input_shape, l.dtype) for l in model.layers]


    # Train the model
    for i in range(235):
        cnn_input_data, decision_input_data, output_data = load_data(i)

        # Ensure the data is in the correct format
        cnn_input_data = np.array(cnn_input_data)
        decision_input_data = np.array(decision_input_data)
        output_data = np.array(output_data)

        # Expand dims if necessary
        if len(output_data.shape) == 1:
            output_data = np.expand_dims(output_data, -1)

        print(cnn_input_data.shape, decision_input_data.shape, output_data.shape)
        print(type(cnn_input_data), type(decision_input_data), type(output_data))

        history = model.fit(x=[cnn_input_data, decision_input_data], y=output_data, epochs=NUM_EPOCHS,
                            batch_size=BATCH_SIZE, use_multiprocessing=True, validation_split=0.05)
        if history.history['val_loss'][-1] < lowest_loss:
            model.save_weights(f'D:/models/bestweights3.h5', save_format='h5')
            lowest_loss = history.history['val_loss'][-1]
        # summarize history for loss
        _loss = history.history['loss']
        print(loss, type(_loss))
        _val_loss = history.history['val_loss']
        loss.extend(_loss)
        val_loss.extend(_val_loss)
        plt.plot(loss)
        plt.plot(val_loss)
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig(f'D:/models/figure3{i}.png')
        plt.show(block=False)
        model_json = model.to_json()
        with open(f'D:/models/architecture3{i}.json', 'w') as json_file:
            json_file.write(model_json)
        model.save_weights(f'D:/models/weights3{i}.h5', save_format='h5')


def load_model(architecture: str, weights: str):
    with open(architecture, 'r') as json:
        json_model = json.read()
    model = models.model_from_json(json_model)

    model.load_weights(weights)

    return model


def predict(board, info, model):
    board = np.array(encode_chessboard(board))
    board = board.reshape(1, -1).reshape(1, 8, 8, 12)
    print(board.shape)
    info = info.reshape(1, -1)
    return model.predict(x=[board, info], verbose=0)


