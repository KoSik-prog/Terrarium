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

from libraries.log import *
from terrarium import *

class socket_CL:
    bufferSize = 1024

    def __init__(self, address, port):
        self.address = address
        self.serverAddressPort = (address, port)
        terrarium.socketLastSendTime = datetime.datetime.now()
        self.UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

    def send_message(self, messageToSend):
        bytesToSend = str.encode(messageToSend)
        self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
        log.add_log("send to {} -> message: {}".format(messageToSend, self.address))
        terrarium.socketLastSendTime = datetime.datetime.now()

    def send_message_to_server(self):
        if((datetime.datetime.now() - terrarium.socketLastSendTime) > (datetime.timedelta(minutes = terrarium.interwalWysylania))):
            self.send_message("terrarium.T:{:4.1f}/W:{:3.0f},t:{:4.1f}/w:{:3.0f}/I:{:9.4f}".format(terrarium.tempG,terrarium.wilgG,terrarium.tempD,terrarium.wilgD,terrarium.UVI))
            log.add_log("Temp1: {:.1f} C / Wilg1: {:.0f}%RH  /  Temp2: {:.1f} C / Wilg2: {:.0f}%RH  /  UVA: {:.2f}, UVB: {:.2f}, UVI:{:.4f}".format(terrarium.tempG,terrarium.wilgG,terrarium.tempD,terrarium.wilgD,terrarium.UVA,terrarium.UVB,terrarium.UVI))
        
socket = socket_CL("192.168.0.99", 2222)