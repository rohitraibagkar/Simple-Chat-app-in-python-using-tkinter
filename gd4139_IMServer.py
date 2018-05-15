
# Library import area. All the imported libraries mentioned below ######################################################

from builtins import *
import re, time, argparse, tkinter
import  socket
from  threading import Thread

hostName = socket.gethostname() # this command takes the host name of the Client 1 System.
hostIP = socket.gethostbyname(socket.getfqdn()) # this command takes the IP address of client 1 System...

# defining Sockets...

from socket import *

clientUDPPort = 7000    # This is UDP port of client 1, to be entered by argparse...
clientTCPPort = 7001    # This is TCP port of client 1, to be entered by argparse...

serverIP = ''  # this is ipaddress of Server, to be entered by argparse...

servUDPPort = 8000       # This is UDP port of the server, to be entered by argparse...
servTCPPort = 8001       # This is TCP port of the server, to be entered by argparse...

parser = argparse.ArgumentParser(description='Networking class and app')

#def parameters( parser ):

parser.add_argument('i', type=int, help=" Client TCP Port Number")
parser.add_argument('j', type=int, help=" Client UDP Port number")
parser.add_argument('k', type=str, help="Server IP Address")
parser.add_argument('l', type=int, help=" Server TCP Port number")
parser.add_argument('m', type=int, help=" Server UDP Port number")

inputArgs = parser.parse_args()
if __name__ == '__main__':
    clientUDPPort = inputArgs.j
    clientTCPPort = inputArgs.i
    serverIP = inputArgs.k
    servUDPPort = inputArgs.m
    servTCPPort = inputArgs.l

#parameters(parser)

userName = input('Enter User Name:')

clientData = userName + '\t' + hostIP + '\t' + str(clientUDPPort) + '\t' + str(clientTCPPort) + '\t' + str(hostName)
readyMsg = 'Me too ready'

tcpSocket = socket(AF_INET, SOCK_STREAM)    # socket for tcp communication...
udpSocket = socket(AF_INET, SOCK_DGRAM)     # socket for udp communication...

udpSocket.sendto(clientData.encode(),(serverIP, servUDPPort))

while True:

    #udpSocket.sendto(clientData.encode(),(serverIP, servUDPPort))

    Response, serverAddress = udpSocket.recvfrom(1024)
    print(Response.decode())

    if Response.decode() == 'I am ready':

        break

udpSocket.sendto(readyMsg.encode(), (serverIP, servUDPPort))


def messageReceiver():
    """This function receives the messages from the server and other client..."""

    while True:
        # do nothing
        try:
            message = tcpSocket.recv(1024).decode("utf8")
            messagesArray.insert(tkinter.END, message)

        except OSError:
            break

def msgTransmitter (event = None):

    message = messageInput.get()
    messageInput.set("")
    tcpSocket.send(bytes(message, "utf8"))

    if message == "{exit}":
        tcpSocket.close()
        guiWindow.quit()

def closeGUIWindow ( event = None ):

    messageInput.set("{exit}")
    msgTransmitter()

guiWindow = tkinter.Tk()
guiWindow.title("FaceApp Chwitter")

messageFrame = tkinter.Frame(guiWindow)
messageInput = tkinter.StringVar()
messageInput.set("iMessage Text Message")
windowSlider = tkinter.Scrollbar(messageFrame)
messagesArray = tkinter.Listbox(messageFrame, height = 20, width = 75, yscrollcommand = windowSlider.set)
windowSlider.pack(side = tkinter.RIGHT, fill = tkinter.Y)
messagesArray.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
messagesArray.pack()
messageFrame.pack()

messageEnter = tkinter.Entry(guiWindow, textvariable = messageInput)
messageEnter.bind("<Return>", msgTransmitter)
messageEnter.pack()
messageTransmit = tkinter.Button(guiWindow, text = "Send Message", command = msgTransmitter)
messageTransmit.pack()
guiWindow.protocol("WM_DELETE_WINDOW", closeGUIWindow)


tcpSocket.connect((serverIP, servTCPPort))
trialThread = Thread(target=messageReceiver)
trialThread.start()
tkinter.mainloop()
