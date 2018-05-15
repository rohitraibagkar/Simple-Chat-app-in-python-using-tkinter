# Library import area. All the imported libraries mentioned below ######################################################

from builtins import *
import re, time, argparse, select, sys
from  threading import Thread
import  socket


hostName = socket.gethostname() # here, system host name is stored in variable.
hostIP = socket.gethostbyname(socket.getfqdn()) # here ip address of server is stored in variable

# Defining Sockets...
from socket import *


udpPort = 8000
tcpPort = 8001

parser = argparse.ArgumentParser(description='Networking class and app')

#def parameters( parser ):

parser.add_argument('i', type=int, help="Port Number")
parser.add_argument('j', type=int, help="Port number")

inputArgs = parser.parse_args()

if __name__ == '__main__':

    tcpPort = inputArgs.i
    udpPort = inputArgs.j



#parameters(parser)


#udpPort = 8001  # hard coded for now, use argparse later
#tcpPort = 8000  # hard coded for now, use argparse later

imRegServer = socket(AF_INET, SOCK_DGRAM)   # UDP Socket for registration purposes
imChatServer = socket(AF_INET, SOCK_STREAM) # TCP Socket for communiation purposes

imRegServer.bind(('', udpPort))  # here 8001 is input argument for UDP Port...
imChatServer.bind(('', tcpPort)) # here 8000 is input argument for TCP Port...

imChatServer.listen(2)

# Socket defining is done...

# below is the information stored received from the users...

userID = []         # List of user IDs
userAddr = []
clientIP = []       # List of client's Ips
clientTCPPort = []  # List of client's TCP ports
clientUDPPort = []  # List of client's UDP ports
clientHostName = [] # List of client's host names

# Done with storing user's information...

userCount = 0   # the variable to store number of users registered on the server.
finResponseCount = 0

while True:

    print('Server is listening at IP:\t', hostIP, '\tPort number:\t', udpPort)

    userInfo, userAddress = imRegServer.recvfrom(1024)

    print((userInfo.decode()))

    if userInfo.decode() == 'Me too ready':

        finResponseCount += 1

    if finResponseCount == 2: break


    if userInfo is not None:

        if userCount < 2:

            userInfo = re.split(r'\t+', userInfo.decode())
            userID.append(userInfo[0])
            clientIP.append(userInfo[1])
            clientUDPPort.append(int(userInfo[2]))
            clientTCPPort.append(int(userInfo[3]))
            clientHostName.append(userInfo[4])
            userAddr.append(userAddress)
            #print(userID, clientIP, clientUDPPort, clientTCPPort, clientHostName)
            imRegServer.sendto('Registration info. received'.encode(), userAddress)
            userCount += 1
    # Breking the while loop

    if userCount == 2:

        #print('Two users registered.')
        #time.sleep(2)
        imRegServer.sendto('I am ready'.encode(), userAddr[0])
        imRegServer.sendto('I am ready'.encode(), userAddr[1])
        #break

def connectionAcceptor():
    """Acepts incoming chat client connections"""

    while True:
        user, userAddress = imChatServer.accept()
        print("%s:%s joined the chat room..." %userAddress)
        user.send(bytes("Welcome to the chat room. Enter your name.", "utf8"))
        userAddrArray[user] = userAddress
        Thread(target= clientHandler, args=(user,)).start()


def clientHandler (user):
    """This function handles the incoming client connections"""

    userName = user.recv(1024).decode("utf8")
    response = 'Welcome to chat room %s. If you wish to quit, type {exit}' % userName
    user.send(bytes(response, "utf8"))
    message = "%s joined the chat room." % userName
    transmitt(bytes(message, "utf8"))
    arrayOfUsers [user] = userName

    while True:

        try:

            message = user.recv(1024)

            if message != bytes("{exit}", "utf8"):
                transmitt(message, userName + ": ")
                print(userName, message.decode("utf8"))

            else:
                user.send(bytes("{exit}", "utf8"))
                user.close()
                del arrayOfUsers[user]
                transmitt(bytes("%s left the room." % userName, "utf8"))
                break

        except:
            print('Unable to connect. Please check clients and server connections')
            break


def transmitt (message, frame = ""):

    # do nothing
    for numSockets in arrayOfUsers:

        numSockets.send(bytes(frame, "utf8") + message)


arrayOfUsers = {}
userAddrArray = {}

if __name__ == "__main__":

    imChatServer.listen(2)
    print('Server is ready to be connected.')
    trialThread = Thread(target= connectionAcceptor)
    trialThread.start()
    trialThread.join()
    imChatServer.close()
