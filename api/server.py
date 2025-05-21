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

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.send(json.dumps({"msg": "Connected to WebSocket server"}))
        async for message in websocket:
            data = json.loads(message)
            event = data.get("event")
            payload = data.get("data")

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

def run_game_against_stockfish(queue, config, command_queue):
    board_1 = pyfirmata.Arduino("COM7")
    board_2 = pyfirmata.ArduinoMega("COM10")
    it = pyfirmata.util.Iterator(board_2)
    it.start()
    time.sleep(1)

    array = Array(board_2, 23)
    stepper_x = Stepper(5, 2, True, board=board_1, board_2=board_2, reference_pin=0, alternative_reference_pin=1)
    stepper_y = Stepper(6, 3, False, board=board_1, board_2=board_2, reference_pin=2)
    magnet = Magnet(board_2, 2, 3, 4)
    magnet.off()

    multistepper = Multistepper()
    game = Stockfish(real=True, fen=config["fen"], time=config["starting_time"], increment=config["increment"],
                     command_queue=command_queue, stepper_x=stepper_x, stepper_y=stepper_y,
                     multistepper=multistepper, magnet=magnet, array=array)

    for move in game.loop():
        queue.put(move)

def run_online_game(queue, config, command_queue):
    game = Lichess(command_queue=command_queue, time=config["time"], increment=config["increment"],
                   challenge_id=config["challenge_id"])
    for move in game.loop():
        queue.put(move)

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(handler, "0.0.0.0", 8080)
    loop.run_until_complete(start_server)
    print("WebSocket server running on ws://0.0.0.0:8080")
    loop.run_forever()

if __name__ == '__main__':
    ws_thread = threading.Thread(target=start_websocket_server)
    ws_thread.start()
