from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return jsonify('test')



if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')