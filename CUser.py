class CUser:
    def __init__(self, clientSocket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def getAddress(self):
        return self.clientAddress
    def getSocket(self):
        return self.clientSocket
    
    def sendToClient(self, message):
        if isinstance(message, str):
            return self.clientSocket.send(message.encode())
        elif isinstance(message, bytes):
            return self.clientSocket.send(message)
        else:
            return False
