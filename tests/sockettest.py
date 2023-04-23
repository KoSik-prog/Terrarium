#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        Socket connection test
#
# Author:      KoSik
#
# Created:     22.04.2023
# Copyright:   (c) kosik 2023
# -------------------------------------------------------------------------------
try:
    import socket
    import datetime
except ImportError:
    print("Import error - communication")

class Socket:
    bufferSize = 1024
    socketLastSendTime = 0

    def __init__(self, address, port):
        self.address = address
        self.serverAddressPort = (address, port)
        self.socketLastSendTime = datetime.datetime.now()
        try:
            self.udpClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            print ("Socket successfully created")
            self.send_test_message()
        except socket.error as err:
            print ("socket creation failed with error %s" %(err))

    def send_test_message(self):
        self.send_message("my test message")
        print("message sended")


    def send_message(self, messageToSend):
        bytesToSend = str.encode(messageToSend)
        self.udpClientSocket.sendto(bytesToSend, self.serverAddressPort)
        self.socketLastSendTime = datetime.datetime.now()

    def send_message_to_server(self):
        log.add_log("test1: " + terrarium.get_socket_message_interval())
        log.add_log("test2: " + (datetime.datetime.now() - self.socketLastSendTime))
        log.add_log("test3: " + ((datetime.datetime.now() - self.socketLastSendTime) > (datetime.timedelta(minutes=terrarium.get_socket_message_interval()))))
        if ((datetime.datetime.now() - self.socketLastSendTime) > (datetime.timedelta(minutes=terrarium.get_socket_message_interval()))):
            self.send_message(terrarium.get_socket_message())

socket = Socket("192.168.0.99", 2222)