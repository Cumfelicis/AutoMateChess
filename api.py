from flask import Flask, jsonify
from backend.training.play_against_stockfish import Play
import multiprocessing


play_against_stockfish = Play(real=True)

def start_game():
    play_against_stockfish.loop()

api = Flask(__name__)

@api.route('/api/test', methods=['GET'])
def test():
    thread = multiprocessing.Process(target=start_game)
    thread.start()
    return jsonify(message='test')

if __name__ == '__main__':
    print('test')
    api.run(debug=True)
