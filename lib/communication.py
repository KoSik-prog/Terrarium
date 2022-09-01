#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        communication
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import socket, datetime

from lib.log import *
from terrarium import *

class Socket:
    bufferSize = 1024
    socketLastSendTime = 0

    def __init__(self, address, port):
        self.address = address
        self.serverAddressPort = (address, port)
        self.socketLastSendTime = datetime.datetime.now()
        self.UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

    def send_message(self, messageToSend):
        bytesToSend = str.encode(messageToSend)
        self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
        log.add_log("send to {} -> message: {}".format(messageToSend, self.address))
        self.socketLastSendTime = datetime.datetime.now()

    def send_message_to_server(self):
        if((datetime.datetime.now() - self.socketLastSendTime) > (datetime.timedelta(minutes = terrarium.read_socket_message_interval()))):
            self.send_message(terrarium.return_socket_message())
            log.add_log("Temp1: {:.1f} C / Wilg1: {:.0f}%RH  /  Temp2: {:.1f} C / Wilg2: {:.0f}%RH  /  UVA: {:.2f}, UVB: {:.2f}, UVI:{:.4f}".format(terrarium.temperatureTop,terrarium.humidityTop,terrarium.temperatureBottom,terrarium.humidityBottom,terrarium.UVA,terrarium.UVB,terrarium.UVI))
        
socket = Socket("192.168.0.99", 2222)