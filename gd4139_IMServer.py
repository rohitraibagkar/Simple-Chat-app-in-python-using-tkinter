from builtins import *
import re, time, argparse, select, sys
from threading import Thread
from socket import *

class ChatServer (object):

    hostName = ''   # hostname of server
    hostIP = ''     # ip address of the server

    tcpPort = 8000  # tcp socket port
    udpPort = 8001  # udp socket port

    imRegServer = 0     # property for server UDP socket
    imChatServer = 0    # property for server TCP socket

    userID = []  # List of user IDs
    userAddr = []
    clientIP = []  # List of client's Ips
    clientTCPPort = []  # List of client's TCP ports
    clientUDPPort = []  # List of client's UDP ports
    clientHostName = []  # List of client's host name

    userAddrArray = {}
    arrayOfUsers = {}

    chatThread = 0

    def parseArguments (self):
        """The function to parse input arguments for socket connection. The arguments are server tcp and udp socket port numbers."""

        parser = argparse.ArgumentParser(description='Programming Assignment 2')
        parser.add_argument('i', type=int, help="Server TCP Port Number")
        parser.add_argument('j', type=int, help="Server UDP Port number")
        
        inputArgs = parser.parse_args()
        self.tcpPort = inputArgs.i
        self.udpPort = inputArgs.j

    def getHostParameters (self):
        """The function to get host parameters"""

        import socket

        self.hostName = socket.gethostname()
        self.hostIP = socket.gethostbyname(socket.getfqdn())

    def socketBinder (self, udpport, tcpport, numListen):
        """function to bind sockets to respective port numbers."""

        self.imRegServer = socket(AF_INET, SOCK_DGRAM)
        self.imChatServer = socket(AF_INET, SOCK_STREAM)
        self.imRegServer.bind(('', udpport))
        self.imChatServer.bind(('', tcpport))
        self.imChatServer.listen(numListen)

    def userRegistration (self, anyUDPSocket, numUsers):
        """Fucntion to handle registration of users"""

        userCount = 0
        finResponseCount = 0

        while True:

            print('Server is listening at IP:\t', self.hostIP, '\tPort Number:\t', self.udpPort)
            userInfo, userAddress = anyUDPSocket.recvfrom(1024)
            print(userInfo.decode())

            if userInfo.decode() == 'Me too ready':

                finResponseCount += 1

            if finResponseCount == numUsers: break

            if userInfo is not None:

                if userCount < numUsers:

                    userInfo = re.split(r'\t+', userInfo.decode())
                    self.userID.append(userInfo[0])
                    self.clientIP.append(userInfo[1])
                    self.clientUDPPort.append(int(userInfo[2]))
                    self.clientTCPPort.append(int(userInfo[3]))
                    self.clientHostName.append(userInfo[4])
                    self.userAddr.append(userAddress)
                    anyUDPSocket.sendto('Registration info. received'.encode(), userAddress)
                    userCount += 1

            if userCount == numUsers:

                anyUDPSocket.sendto('I am ready'.encode(), self.userAddr[0])
                anyUDPSocket.sendto('I am ready'.encode(), self.userAddr[1])

    def connectionAcceptor (self):
        """This function accepts connections."""

        while True:

            user, userAddress = self.imChatServer.accept()
            print("%s:%s joined the chat room..." % userAddress)
            user.send(bytes("Welcome to the chat room. Enter your name.", "utf8"))
            self.userAddrArray[user] = userAddress
            Thread(target= self.clientHandler, args= (user,)).start()

    def clientHandler (self ,user):
        """The function to handle communication with two clients simultaneously"""

        userName = user.recv(1024).decode("utf8")
        response = 'Welcome to the chat room %s. If you wish to quit type exit' % userName
        user.send(bytes(response, "utf8"))
        message = "%s joined the room." % userName
        self.transmitt(bytes(message, "utf8"))
        self.arrayOfUsers[user] = userName

        while True:

            try:

                message = user.recv(1024)

                if message != bytes("exit", "utf8"):

                    self.transmitt(message, userName + " : ")
                    print(userName, '\t:\t', message.decode("utf8"))

                else:

                    user.send(bytes("exit", "utf8"))
                    user.close()
                    del self.arrayOfUsers[user]
                    self.transmitt(bytes("%s left the room." % userName, "utf8"))
                    break

            except:

                print('Unable to connect. Please check the clients and server connections')
                break

    def transmitt(self, message, frame=""):
        """Function to transmit message."""

        for numSockets in self.arrayOfUsers:

            numSockets.send(bytes(frame, "utf8") + message)

    def startChat (self):
        """Function to start chatserver."""

        self.imChatServer.listen(2)
        print('Server is ready to connect')
        self.chatThread = Thread(target= self.connectionAcceptor)
        self.chatThread.start()
        self.chatThread.join()
        self.imChatServer.close()

if __name__ == "__main__":


    o = ChatServer()
    o.parseArguments()
    o.getHostParameters()
    o.socketBinder(o.udpPort, o.tcpPort, 2)
    print(o.hostName, '\n', o.hostIP, '\n', o.imRegServer, '\n', o.imChatServer)
    o.userRegistration(o.imRegServer, 2)

    o.startChat()
