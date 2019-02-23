import json
import logging

from socketIO_client import SocketIO, LoggingNamespace

import HBrige

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()
my_tank = HBrige.Tank()

ctlMap = {
    "up left": my_tank.forward_left,
    "down left": my_tank.backward_left,
    "up right": my_tank.forward_right,
    "down right": my_tank.backward_right,
    "left end": my_tank.stop_left,
    "right end": my_tank.stop_right
}


def parse_cmd(*args):
    cmdJson = json.loads(json.dumps(args))[0]
    print(cmdJson)
    try:
        if cmdJson['cmd'] == "end":
            ctlMap[cmdJson['side'] + " end"]()
        if cmdJson['cmd'] == "move":
            ctlMap[cmdJson['direction']['y'] + " " + cmdJson['side']](int(float(cmdJson['dutyCycle'])))
    except:
        pass


with SocketIO('localhost', 3000, LoggingNamespace) as socketIO:
    try:
        socketIO.on('cmd', parse_cmd)
    except:
        pass
    while True:
        socketIO.wait(seconds=1)
        socketIO.emit('python-message', "ready")
