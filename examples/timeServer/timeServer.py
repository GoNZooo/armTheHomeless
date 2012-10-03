import sys
sys.path.append("../..")
from CServer import CServer
import time


def mHandler(self, user, data):
    data = data.strip("\n")
    if data == "exit" or data == "shutdown":
        self.shutdownServer()
    elif data == "msg":
        user.sendToClient(self.message + "\n")
    elif data.split(" ")[0] == "edit":
        self.message = data[5:]
    elif data == "time":
        user.sendToClient(time.asctime() + "\n")

class CTimeServer(CServer):
    def __init__(self, message, hostname, port, backlog,
                        messageHandler, buffersize = 4096):
        CServer.__init__(self, hostname, port, backlog,
                        messageHandler, buffersize)
        self.message = message

server = CTimeServer("HejHej, kanske.", "", 1337, 1, mHandler)
server.run()
