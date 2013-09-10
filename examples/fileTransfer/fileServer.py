import sys
sys.path.append("../..")
from CServer import CServer

def mHandler(self, user, data):
    if data[-1] == "\n":
        data = data[:-1]

    if data == "shutdown" or data == "exit":
        self.shutdownServer()
    
    if data == "bin":
        self.switchBinary()

    if data.count(" ") >= 1:
        command = data.split(" ")[0]
        argument = data.split(" ")[1]
    else:
        return

    if command == "get":
        filename = argument
        sendFile = self.getFile(filename)
        user.sendToClient(filename + ";" + str(len(sendFile)) + ";")
        user.sendToClient(sendFile)

class CFileServer(CServer):
    def __init__(self, hostname, port, backlog,
                        messageHandler, buffersize = 4096):
        CServer.__init__(self, hostname, port, backlog,
                                messageHandler, buffersize)
        self.binary = True

    def setBinary(self, binaryMode):
        self.binary = binaryMode
    def switchBinary(self):
        self.binary = not self.binary

    def getFile(self, filename):
        if self.binary:
            fileObject = open(filename, "rb")
        else:
            fileObject = open(filename, "r")
        fileString = fileObject.read()
        fileObject.close()

        return fileString

fileServer = CFileServer("", 1337, 1, mHandler, 8192)
fileServer.run()
