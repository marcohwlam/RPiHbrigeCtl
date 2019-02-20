from flask import Flask, jsonify, request

import HBrige

app = Flask(__name__)
tank = HBrige.Tank()


@app.route('/control', methods=['POST'])
def control():
    req_data = request.get_json()
    print req_data
    if req_data['cmd'] == 'stop':
        tank.stop()
    if req_data['cmd'] == 'move':
        dutyCycle = req_data['dutyCycle']
        if req_data['side'] == 'left':
            if req_data['direction'] == 'up':
                tank.forward_left(dutyCycle)
            elif req_data['direction'] == 'down':
                tank.backward_left(dutyCycle)
        elif req_data['side'] == 'right':
            if req_data['direction'] == 'up':
                tank.backward_left(dutyCycle)
            elif req_data['direction'] == 'down':
                tank.backward_right(dutyCycle)
    return jsonify({'result': True})


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='3001')
