import select
import socket
from CUser import CUser
import time

SLEEPTIME = 2 ** -10

class CServer:
    def __init__(self, hostname, port, backlog,
                        messageHandler, buffersize = 4096):
        # The function that will handle incoming messages.
        self.messageHandler = messageHandler

        
        # Creating the greeter socket.
        self.greeterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.greeterSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.greeterSocket.bind((hostname, port))
        self.greeterSocket.listen(backlog)
        self.buffersize = buffersize

        # Used for storing input sockets
        # that are passed to select()
        self.inputs = [self.greeterSocket]
        
        # Used for storing CUser objects.
        self.clients = {}
    
    # Goes through sockets that are reported as being ready to recv from.
    def getReady(self):
        (inReady, outReady, exceptions) = select.select(self.inputs, [], [])
        for inSocket in inReady:
            # If the socket that's ready is the greeter socket it means
            # we've got someone connecting.
            if inSocket == self.greeterSocket:
                (clientSocket, clientAddress) = self.greeterSocket.accept()
                print("+ client:", clientAddress)
                self.clients[clientSocket] = CUser(clientSocket, clientAddress)
                self.inputs.append(clientSocket)
            # The ready socket is a user socket, we should check for data.
            else:
                data = inSocket.recv(self.buffersize).decode()
                # If we find data it means they sent a message
                if data:
                    self.messageHandler(self, self.clients[inSocket], data)
                # If not in means they disconnected.
                else:
                    print("- client:", self.clients[inSocket].getAddress()) 
                    self.inputs.remove(inSocket)
                    self.clients[inSocket] = 0
    
    # Shutdown routine; closes all client sockets first, then the greeter.
    def shutdownServer(self):
        for inputSocket in self.inputs:
            if inputSocket != self.greeterSocket:
                self.clients[inputSocket] = 0
                self.inputs.remove(inputSocket)
        self.greeterSocket.close()
        self.shutdown = True
    
    # Main routine where the server loops for messages/connects/disconnect.
    def run(self):
        self.shutdown = False
        while not self.shutdown:
            self.getReady()
            time.sleep(SLEEPTIME)

