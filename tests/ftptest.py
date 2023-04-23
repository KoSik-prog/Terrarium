#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        FTP post connection test
#
# Author:      KoSik
#
# Created:     22.04.2023
# Copyright:   (c) kosik 2023
# -------------------------------------------------------------------------------
try:
    import requests
    import datetime
except ImportError:
    print("Import error - communication")

class Socket:

    def __init__(self):
        # http://kosik.dynv6.net/webhooks/getdata.php?data=!set^ledDesk.55&port=2223
        data = "!set^ledDesk.100"
        port = 2223
        myurl = "http://kosik.dynv6.net/webhooks/getdata.php?data={}&port={}".format(data, port)
        requests.post(myurl, timeout=2.50)
        print('message sended')

socket = Socket()