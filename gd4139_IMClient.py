from builtins import *
import re, time, argparse, select, sys, tkinter
from threading import Thread
from socket import *

class ChatClient (object):

    hostName = ''   # property to store hostname of client
    hostIP = ''     # property to store ip address of host

    clientTCPPort = 7000  # This is TCP port of client 1, to be entered by argparse...
    clientUDPPort = 7001  # This is UDP port of client 1, to be entered by argparse...

    serverIP = '192.168.56.1'  # this is ipaddress of Server, to be entered by argparse...

    servTCPPort = 8000  # This is TCP port of the server, to be entered by argparse...
    servUDPPort = 8001  # This is UDP port of the server, to be entered by argparse...

    userName = ''       # property to store username

    tcpSocket = 0       # tcp socket
    udpSocket = 0       # udp socket

    messageArray = 0    # gui parameters
    messageInput = 0    # gui parameters
    guiWindow = 0       # gui parameters

    def parseArguments (self):

        """The function parses input arguments on command line. The inputs are Client TCP & UDP Port, Server IP Address, Server TCP & UDP port"""

        parser = argparse.ArgumentParser(description='Programming Assignment 2')

        # defining parser properties for storing server parameters.
        parser.add_argument('i', type=int, help="Client TCP Port Number")
        parser.add_argument('j', type=int, help="Client UDP Port number")
        parser.add_argument('k', type=str, help="Server IP Address")
        parser.add_argument('l', type=int, help="Server TCP Port number")
        parser.add_argument('m', type=int, help="Server UDP Port number")

        inputArgs = parser.parse_args()

        #Parsing input arguments serially. First argument is client TCP port itself.
        # Second argument is client UDP Port, Third is server IP Address.
        # Fourth is server TCP port and fifth is server UDP Port.

        self.clientTCPPort = inputArgs.i
        self.clientUDPPort = inputArgs.j
        self.serverIP = inputArgs.k
        self.servTCPPort = inputArgs.l
        self.servUDPPort = inputArgs.m

    def getHostParmeters (self):
        """The function to get host parameters. It collects host ip and host name for sending to server"""

        import socket
        self.hostName = socket.gethostname()
        self.hostIP = socket.gethostbyname(socket.getfqdn())

    def socketBinder (self, udpport, tcpport):
        """The function binds client's udp port to udp socket and tcp port to tcp socket"""

        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.udpSocket.bind(('',udpport))
        self.tcpSocket.bind(('',tcpport))

    def clientRegistration (self, udpsocket, serverip, serverudpport):
        """The function is used for client registration to the server."""
        # the function takes udp socket, server IP address and server UDP port as inputs.
        # once registered, the UDP socket connection is terminated.
        self.userName = input('Please enter user name:')
        clientData = self.userName+'\t'+self.hostIP+'\t'+str(self.clientUDPPort)+'\t'+str(self.clientTCPPort)+'\t'+str(self.hostName)
        readyMsg = 'Me too ready'
        udpsocket.sendto(clientData.encode(), (serverip, serverudpport))

        while True:

            Respone, ServerAddres = udpsocket.recvfrom(1024)
            print(Respone.decode())

            if Respone.decode() == 'I am ready':

                break

        udpsocket.sendto(readyMsg.encode(), (serverip, serverudpport))


    def messageReceiver (self):
        """The function handles message receiving part."""

        while True:

            try:

                inMessage = self.tcpSocket.recv(1024).decode("utf8")
                self.messageArray.insert(tkinter.END, inMessage)

            except OSError:

                break

    def messageTransmitter (self, event = None):
        """The function handles message sending part."""

        outMessage = self.messageInput.get()
        self.messageInput.set("")
        self.tcpSocket.send(bytes(outMessage, "utf8"))

        if outMessage == "exit":

            self.tcpSocket.close()
            self.guiWindow.quit()

    def closeGUIWindow (self, event = None):
        """The function initiates execution of GUI"""

        self.messageInput.set("exit")
        self.messageTransmitter()

    def chatGUI (self):
        """All the GUI parameters, design and behaviour function are defined in this function"""

        self.guiWindow = tkinter.Tk()
        self.guiWindow.title("Programming assignment 2")

        messageFrame = tkinter.Frame(self.guiWindow)
        self.messageInput = tkinter.StringVar()
        self.messageInput.set("iMessage")
        windowSlider = tkinter.Scrollbar(messageFrame)
        self.messageArray = tkinter.Listbox(messageFrame, height = 25, width = 75, yscrollcommand = windowSlider.set)
        windowSlider.pack(side = tkinter.RIGHT, fill = tkinter.Y)
        self.messageArray.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
        self.messageArray.pack()
        messageFrame.pack()

        messageEnter = tkinter.Entry(self.guiWindow, textvariable = self.messageInput)
        messageEnter.bind("<Return>", self.messageTransmitter)
        messageEnter.pack()
        messageTransmit = tkinter.Button(self.guiWindow, text = "Send Message", command = self.messageTransmitter)
        messageTransmit.pack()
        self.guiWindow.protocol("WM_DELETE_WINDOW", self.closeGUIWindow)

        self.tcpSocket.connect((self.serverIP, self.servTCPPort))
        myThread = Thread(target= self.messageReceiver)
        myThread.start()
        tkinter.mainloop()


if __name__ == "__main__":
    

    o = ChatClient()
    o.parseArguments()
    o.getHostParmeters()
    print(o.hostName, '\n', o.hostIP)
    o.socketBinder(o.clientUDPPort, o.clientTCPPort)
    o.clientRegistration(o.udpSocket, o.serverIP, o.servUDPPort)
    o.chatGUI()


