from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from multiprocessing import Process, Queue
from flask_cors import CORS
import logging
from backend.training.play_against_stockfish import Play
from multiprocessing import Process, Queue
from threading import Thread
from backend.utils.communication_utils import generate_json_from_move 

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for testing

logging.basicConfig(level=logging.DEBUG)
game_queue = Queue()

def run_game(queue, config):
    game = Play(real=True, fen=config['fen'], time=config['starting_time'], increment=config['increment'])
    for move in game.loop():
        print(move)
        queue.put(move)

def stream_updates(queue):
    while True:
        socketio.sleep(0)  # neccesary to maintain concurency to the main thread
        try:
            update = queue.get(timeout=0.1)
        except Exception as e:
            print(e)
            continue
        print(f'update: {update}')
        socketio.emit('move', generate_json_from_move(update))
        print('emmited update')

def start_game(config):
    p = Process(target=run_game, args=(game_queue, config))
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
def start(config):
    emit('status', {'msg': start_game(config=config)})
    print(f'started game with Timecontrol: {config}')

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



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
