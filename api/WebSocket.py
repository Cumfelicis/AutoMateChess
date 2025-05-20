from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from multiprocessing import Process, Queue, Manager
from flask_cors import CORS
import logging
from .backend.training.play_against_stockfish import Play as Stockfish
from multiprocessing import Process, Queue
from threading import Thread
from .backend.utils.communication_utils import generate_json_from_move 
from .backend.training.lichess import client
from .backend.training.lichess import Play as Lichess
import pyfirmata, pyfirmata.util
from .backend.arduino_communication.arduino_communication import Stepper, Magnet, Multistepper
from .backend.arduino_communication.hall_array import Array
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", path='ws')  # Allow all origins for testing
logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    game_queue = Queue()
    command_queue = Queue()
    
    print(4)
    # magnet = Magnet(12, board_1, board_2)
    # magnet.off()
    print(5)
    time.sleep(1)


@socketio.on('challenges')
def get_challenges():
    challenges = client.challenges.get_mine()['in']
    socketio.emit('challenges', challenges)

def run_game_against_stockfish(queue, config, command_queue):
    print(1)
    board_1 = pyfirmata.Arduino("COM7")
    print('test')
    board_2 = pyfirmata.ArduinoMega("COM10")
    print(2)

    print(3)
    it = pyfirmata.util.Iterator(board_2)
    it.start()
    time.sleep(1)

    array = Array(board_2, 23)
    
    stepper_x = Stepper(5, 2, True, board=board_1, board_2=board_2, reference_pin=0, alternative_reference_pin=1)
    stepper_y = Stepper(6, 3, False, board=board_1, board_2=board_2, reference_pin=2)
    multistepper = Multistepper()
    magnet = Magnet(board_2, 2, 3, 4)
    magnet.off()
    multistepper = Multistepper()
    game = Stockfish(real=True, fen=config['fen'], time=config['starting_time'], increment=config['increment'], command_queue=command_queue, stepper_x=stepper_x, stepper_y=stepper_y, multistepper=multistepper, magnet=magnet, array=array)
    for move in game.loop():
        queue.put(move)
        
def run_online_game(queue, config, command_queue):
    game = Lichess(command_queue=command_queue, time=config['time'], increment=config['increment'], challenge_id=config['challenge_id'])
    for move in game.loop():
        queue.put(move)


def stream_updates(queue):
    while True:
        socketio.sleep(0)  # neccesary to maintain concurency to the main thread
        try:
            update = queue.get(timeout=0.1)
        except Exception as e:
            continue
        print(f'update: {update}')
        socketio.emit('move', generate_json_from_move(update))
        print('emmited update')

def start_stockfish(config):
    p = Process(target=run_game_against_stockfish, args=(game_queue, config, command_queue))
    p.start()
    return 'Game Started'

def start_lichess(config):
    p = Process(target=run_online_game, args=(game_queue, config, command_queue))
    p.start()
    return 'Game Started'

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('status', {'msg': 'Welcome to the WebSocket server!'})

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')
    logging.info('Client disconnected')

@socketio.on('command')
def on_command(data):
    print(f"Received command event with data: {data}")
    emit('status', {'msg': f"Command received: {data}"})
    print('i am not in a loop')

@socketio.on('start_game')
def run_stockfish(config):
    emit('status', {'msg': start_stockfish(config=config)})
    print(f'started game with Timecontrol: {config}')
    
@socketio.on('start_lichess')
def run_lichess(config):
    emit('status', {'msg': start_lichess(config=config)})
    print(f'started game with Timecontrol: {config}')
    
@socketio.on('check')
def check():
    command_queue.put('check')

@socketio.on('start_stream')
def start_stream():
    # Start the background thread to stream updates
    print('starting stream')
    socketio.start_background_task(stream_updates, (game_queue))
    print('me neither')
    emit('status', {'msg': 'Streaming started!'})
    
@socketio.on('ping')    # ping mechanism to keep conection alive
def ping(_):
    logging.info('recieved ping')
    print('recieved ping')
    emit('pong', 'pong')


print(get_challenges())
if __name__ == '__main__':
    print('test')
    socketio.run(app, host='0.0.0.0', port=8000)
    print('running')
