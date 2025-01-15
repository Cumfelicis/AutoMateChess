import multiprocessing.process
from flask import Flask, jsonify, request, Response
import time
from backend.training.play_against_stockfish import Play
from multiprocessing import Process, Queue

app = Flask(__name__)
game = Play(real=True)

game_queue = Queue()

def run_game(queue):
    game = Play(real=True)
    for move in game.loop():
        queue.put(move)

def start_game():
    p = Process(target=run_game, args=(game_queue,))
    p.start()
    return jsonify({"status": "Game started!"})

@app.route('/test', methods=['GET'])
def test():
    return jsonify('test')

@app.route('/game/stream')
def play_game():
    def stream():
        while True:
            move = game_queue.get()
            if move == "END":
                break
            yield f"data: {move}\n\n"

    return Response(stream(), content_type='text/event-stream')

@app.route('/game/start', methods=['GET'])
def index():
    p = Process(target=run_game, args=(game_queue,))
    p.start()
    return jsonify({"status": "Game started!"})



if __name__ == '__main__':
    '''
    with app.app_context():
        app.run(port=5000, host='0.0.0.0')
        '''