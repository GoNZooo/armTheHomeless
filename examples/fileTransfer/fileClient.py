import socket
import sys

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = sys.argv[2]
else:
    HOST = input("Host: ")
    PORT = input("Port: ")
PORT = int(PORT)


connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connectionSocket.connect((HOST, PORT))

sendCommand = "get CUser.py".encode()
connectionSocket.send(sendCommand)

recvData = connectionSocket.recv(8192)
data = recvData.decode()
recvFilename = data[: data.find(";")]
data = data[data.find(";") + 1:]
recvSize = data[: data.find(";")]
data = data[data.find(";") + 1:]
recvSize = int(recvSize)

dataOut = open("dataoutput", "wb")
dataOut.write(data.encode())
dataOut.close()

connectionSocket.close()

print("Recv:")
print("Filename:", recvFilename)
print("Size:", recvSize)
print("Data:\n", data)

