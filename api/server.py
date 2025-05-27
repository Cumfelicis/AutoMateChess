import asyncio
import websockets
import json
import logging
import threading
import time
from multiprocessing import Process, Queue
from flask import Flask, jsonify
from flask_cors import CORS

from .backend.training.play_against_stockfish import Play as Stockfish
from .backend.training.lichess import client
from .backend.training.lichess import Play as Lichess
from .backend.utils.communication_utils import generate_json_from_move
from .backend.arduino_communication.arduino_communication import Stepper, Magnet, Multistepper
from .backend.arduino_communication.hall_array import Array
import pyfirmata, pyfirmata.util

# Flask for API calls (optional)
app = Flask(__name__)
CORS(app)

connected_clients = set()
game_queue = Queue()
command_queue = Queue()

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.send(json.dumps({"event": "connect", "msg": "Connected to WebSocket server"}))
        async for message in websocket:
            print(message)
            data = json.loads(message)
            event = data.get("event")
            payload = data.get("data")
            await websocket.send(json.dumps({"event": "ack", "data": message}))
            print(f'recieved event: {event} with payload: {payload}')

            if event == "ping":
                await websocket.send(json.dumps({"event": "pong", "data": "pong"}))
            elif event == "start_game":
                start_stockfish(payload)
                await websocket.send(json.dumps({"event": "status", "data": "Game Started"}))
            elif event == "start_lichess":
                start_lichess(payload)
                await websocket.send(json.dumps({"event": "status", "data": "Game Started"}))
            elif event == "check":
                command_queue.put("check")
            elif event == "start_stream":
                asyncio.create_task(stream_updates(websocket))
            elif event == "move_stepper_x":
                start_move_stepper_x(int(payload))
            elif event == "run_stepper_x":
                start_run_stepper_x()
            elif event == "move_stepper_y":
                start_move_stepper_y(int(payload))
            elif event == "run_stepper_y":
                start_run_stepper_y()
            elif event == "move_multistepper":
                pos = tuple(payload)
                start_move_multistepper(pos[0], pos[1])
            elif event == "run_multistepper":
                start_run_multistepper()
            elif event == "calibrate_array":
                start_calibrate_array()
            elif event == "challenges":
                challenges = client.challenges.get_mine()["in"]
                await websocket.send(json.dumps({"event": "challenges", "data": challenges}))
    finally:
        connected_clients.remove(websocket)

async def stream_updates(websocket):
    while True:
        try:
            update = game_queue.get(timeout=0.1)
            msg = {"event": "move", "data": generate_json_from_move(update)}
            await websocket.send(json.dumps(msg))
        except Exception:
            await asyncio.sleep(0.1)

def start_stockfish(config):
    p = Process(target=run_game_against_stockfish, args=(game_queue, config, command_queue))
    p.start()

def start_lichess(config):
    p = Process(target=run_online_game, args=(game_queue, config, command_queue))
    p.start()
    
def initialize_components():
    BOARD_1 = pyfirmata.Arduino("/dev/ttyACM1")
    BOARD_2 = pyfirmata.ArduinoMega("/dev/ttyACM0")
    it = pyfirmata.util.Iterator(BOARD_2)
    it.start()
    time.sleep(1)

    ARRAY = Array(BOARD_2, 23)
    STEPPER_X = Stepper(5, 2, True, board=BOARD_1, board_2=BOARD_2, reference_pin=0, alternative_reference_pin=1)
    STEPPER_Y = Stepper(6, 3, False, board=BOARD_1, board_2=BOARD_2, reference_pin=2)
    MAGNET = Magnet(BOARD_2, 2, 3, 4)
    MAGNET.off()

    MULTISTEPPER = Multistepper()
    MULTISTEPPER.add_stepper(STEPPER_X)
    MULTISTEPPER.add_stepper(STEPPER_Y)
    return BOARD_1, BOARD_2, STEPPER_X, STEPPER_Y, MULTISTEPPER, ARRAY, MAGNET

def run_game_against_stockfish(queue, config, command_queue):
    game = Stockfish(real=True, fen=config["fen"], time=config["starting_time"], increment=config["increment"],
                     command_queue=command_queue, stepper_x=STEPPER_X, stepper_y=STEPPER_Y,
                     multistepper=MULTISTEPPER, magnet=MAGNET, array=ARRAY)

    for move in game.loop():
        queue.put(move)

def run_online_game(queue, config, command_queue):
    game = Lichess(command_queue=command_queue, time=config["time"], increment=config["increment"],
                   challenge_id=config["challenge_id"])
    for move in game.loop():
        queue.put(move)
        
def move_stepper_x(pos):
    STEPPER_X.move_to(pos)
    STEPPER_X.run_to()
    
def run_stepper_x():
    STEPPER_X.run_to()   
    
def move_multistepper(pos_x, pos_y):
    STEPPER_X.move_to(pos_x)
    STEPPER_Y.move_to(pos_y)
    MULTISTEPPER.run_to() 
    
def run_multistepper():
    MULTISTEPPER.run_to() 
    
def move_stepper_y(pos):
    STEPPER_Y.move_to(pos)
    STEPPER_Y.run_to()
    
def run_stepper_y():
    STEPPER_Y.run_to()    
    
def start_move_stepper_x(pos):
    p = Process(target=move_stepper_x, args=(pos))
    p.start
    
def start_run_stepper_x():
    p = Process(target=run_stepper_x)
    p.start  
    
def start_move_stepper_y(pos):
    p = Process(target=move_stepper_y, args=(pos))
    p.start
    
def start_run_stepper_y():
    p = Process(target=run_stepper_y)
    p.start
        
def start_move_multistepper(pos_x, pos_y):
    p = Process(target=move_multistepper, args=(pos_x, pos_y))
    p.start()
    
def start_run_multistepper():
    p = Process(target=run_multistepper)
    p.start()
        
  
    
def calibrate_array():
    ARRAY.calibrate()
    
def start_calibrate_array():
    p = Process(target=calibrate_array)
    p.start

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run():
        async with websockets.serve(handler, "0.0.0.0", 8080):
            print("WebSocket server running on ws://0.0.0.0:8080")
            await asyncio.Future()  # run forever

    loop.run_until_complete(run())
    loop.run_forever()

if __name__ == '__main__':
    BOARD_1, BOARD_2, STEPPER_X, STEPPER_Y, MULTISTEPPER, ARRAY, MAGNET = initialize_components()
    ws_thread = threading.Thread(target=start_websocket_server)
    ws_thread.start()
