#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        communication
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import socket
    import requests
    import datetime
    from lib.log import *
    from terrarium import *
except ImportError:
    print("Import error - communication")

class Socket:
    socketLastSendTime = 0

    def __init__(self, port):
        self.socketPort = port
        self.socketLastSendTime = datetime.datetime.now()

    def send_message(self, messageToSend): 
        self.socketLastSendTime = datetime.datetime.now()
        #data = str.encode(messageToSend)
        data = messageToSend
        myurl = "http://kosik.dynv6.net/webhooks/getdata.php?data=!{}&port={}".format(data, self.socketPort)
        requests.post(myurl, timeout=2.50)
        log.add_log("send message: {}".format(messageToSend))

    def send_message_to_server(self):
        if ((datetime.datetime.now() - self.socketLastSendTime) > (datetime.timedelta(minutes=terrarium.get_socket_message_interval()))):
            self.send_message(terrarium.get_socket_message())
            log.add_log("Up:{:.1f}°C/{:.0f}% | Dn:{:.1f}°C/{:.0f}% | UVA:{:.2f}, UVB:{:.2f}, UVI:{:.4f}".format(terrarium.temperatureTop,
                        terrarium.humidityTop, terrarium.temperatureBottom, terrarium.humidityBottom, terrarium.uva, terrarium.uvb, terrarium.uvi))


socket = Socket(2223) 