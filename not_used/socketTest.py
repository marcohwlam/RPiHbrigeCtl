import logging

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()
from socketIO_client import SocketIO, LoggingNamespace
import json


def printCmd(*args):
    cmdJson = json.loads(json.dumps(args))[0]
    print(cmdJson)


# socketIO = SocketIO('localhost', 3000, LoggingNamespace)
# socketIO.on('cmd', printCmd)
# socketIO.wait(seconds=1)
try:
    with SocketIO('localhost', 3000, LoggingNamespace) as socketIO:
        socketIO.on('cmd', printCmd)
        while True:
            # now = datetime.now()
            # socketIO.emit('python-message', now.strftime("123"))
            socketIO.wait(seconds=1)
        #     print ("hi")
    # while True:
    #     try:
    #         cmd = sys.stdin.readline()
    #         # a = sys.stdin.readline()
    #         print cmd
    #     except:
    #         print "unknow cmd"

finally:
    print("finally")
