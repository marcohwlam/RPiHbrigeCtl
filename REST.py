from flask import Flask, jsonify, request

import HBrige

app = Flask(__name__)
tank = HBrige.Tank()


@app.route('/control', methods=['POST'])
def control():
    req_data = request.get_json()
    print req_data
    time = req_data['time']
    power = req_data['power']
    if req_data['direction'] == 'forward':
        tank.forward(time, power)
    elif req_data['direction'] == 'backward':
        tank.backward(time, power)
    elif req_data['direction'] == 'right':
        tank.turn_right(time, power)
    elif req_data['direction'] == 'left':
        tank.turn_left(time, power)
    return jsonify({'result': True})


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='3000')
